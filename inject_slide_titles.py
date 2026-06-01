"""
inject_slide_titles.py

Run after copying course folders into slides/ but BEFORE quarto render slides/.

Replaces every  <!-- repeat slide title -->  comment in L*.qmd files with:

    ---

    ## {most recent ## heading}

This creates a new Reveal.js slide that repeats the current section title,
without adding any extra headings in the book/HTML render (where the comment
is simply ignored by Quarto).

Usage:
    python inject_slide_titles.py          # processes slides/ by default
    python inject_slide_titles.py slides/  # explicit path
"""

import re
import sys
from pathlib import Path

MARKER = "<!-- repeat slide title -->"
HEADING_RE = re.compile(r"^## .+")


def inject(qmd_path: Path) -> None:
    lines = qmd_path.read_text(encoding="utf-8").split("\n")
    current_h2: str | None = None
    output: list[str] = []

    for line in lines:
        if HEADING_RE.match(line):
            current_h2 = line
            output.append(line)
        elif line.strip() == MARKER:
            if current_h2:
                output.append("")
                output.append("---")
                output.append("")
                output.append(current_h2)
            # If no heading seen yet, drop the marker silently
        else:
            output.append(line)

    qmd_path.write_text("\n".join(output), encoding="utf-8")


def main() -> None:
    slides_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("slides")

    if not slides_dir.is_dir():
        print(f"ERROR: {slides_dir} is not a directory", file=sys.stderr)
        sys.exit(1)

    qmd_files = list(slides_dir.rglob("L*.qmd"))

    if not qmd_files:
        print(f"No L*.qmd files found under {slides_dir}/")
        return

    for qmd in sorted(qmd_files):
        inject(qmd)
        print(f"  injected: {qmd}")

    print(f"Done — processed {len(qmd_files)} file(s)")


if __name__ == "__main__":
    main()
