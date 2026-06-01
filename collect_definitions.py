#!/usr/bin/env python3
"""
collect_definitions.py

Scans all course folders at the repo root for lecture files matching *L??-*.qmd,
extracts key term definitions from :::{.callout-note} blocks whose first line
is a heading containing "Key Term" or "Key Terms", and writes a
definitions.qmd glossary file into each course folder.

Key term block format (in .qmd source files):
    ::: {.callout-note}
    ## Key Term

    **Term** ($U$) — definition text
    :::

    OR for multiple terms in one block:
    ::: {.callout-note}
    ## Key Terms

    **Term 1** ($H$) — first definition
    **Term 2** — second definition (symbol is optional)
    :::

Usage:
    python collect_definitions.py [repo_root]

    repo_root defaults to the current working directory.
"""

import re
import sys
from pathlib import Path


# Folders to skip when scanning for course directories
SKIP_DIRS = {
    "_build", "_site", "_slides", "_freeze", ".github", "_static",
    "node_modules", ".git", "__pycache__", ".venv", "venv",
}

# Only process files matching this pattern (lecture files, not index/glossary)
CHAPTER_PATTERN = re.compile(r'L\d{2}-.+\.qmd$')


def is_course_dir(path: Path) -> bool:
    """Return True if this subdirectory looks like a course folder."""
    return path.is_dir() and path.name not in SKIP_DIRS and not path.name.startswith(".")


def extract_keyterms(qmd_path: Path) -> list[tuple[str, str, str]]:
    """
    Parse a lecture .qmd file and return a list of (term, symbol, definition)
    tuples found in :::{.callout-note} blocks whose heading contains 'Key Term'.

    Expected format:
        ::: {.callout-note}
        ## Key Term

        **Term** ($U$) — definition text
        :::

    The symbol (e.g. $U$) is optional. It must be wrapped in parentheses
    immediately after the bold term: **Term** ($U$) — definition."""
    text = qmd_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    terms = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect opening of a fenced div: :::{...} or ::: {...}
        if re.match(r'^:::\s*\{', line):
            # Only interested in .callout-note blocks
            if ".callout-note" not in line:
                i += 1
                continue

            # Collect inner lines until closing :::
            inner = []
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                s = lines[i].strip()
                if s == ":::":
                    depth -= 1
                elif re.match(r'^:::', s) and len(s) > 3:
                    depth += 1
                    inner.append(lines[i])
                else:
                    inner.append(lines[i])
                i += 1

            # Check if the first non-empty inner line is a "Key Term(s)" heading
            heading_line = next((l for l in inner if l.strip()), "")
            if not re.search(r'Key Terms?', heading_line, re.IGNORECASE):
                continue

            # Extract term/definition pairs from lines like:
            #   **Term** — definition text
            #   **Term** (*H*) — definition text
            for l in inner:
                if not l.strip() or l.strip().startswith("#"):
                    continue
                m = re.match(
                    r'^\s*\*\*(.+?)\*\*'          # **Term**
                    r'(?:\s*(\([^)]*\)))?'         # optional (*symbol*)
                    r'\s*(?:—|--)\s*(.*)',          # — definition
                    l
                )
                if m:
                    term   = m.group(1).strip()
                    symbol = m.group(2).strip() if m.group(2) else ""
                    defn   = m.group(3).strip()
                    terms.append((term, symbol, defn))
        else:
            i += 1

    return terms


def build_glossary(course_dir: Path, all_terms: list[tuple[str, str, str, str]]) -> str:
    """
    Render the definitions.qmd content.

    all_terms: [(term, symbol, definition, source_filename), ...]
    """
    course_name = course_dir.name
    lines = [
        "---",
        f'title: "Key Terms"',
        'subtitle: "Auto-generated glossary — do not edit by hand"',
        "---",
        "",
        f"*This glossary is automatically generated from lecture files.*  ",
        f"*To add or update a term, edit the relevant lecture `.qmd` file.*",
        "",
    ]

    for term, symbol, defn, source in sorted(all_terms, key=lambda x: x[0].lower()):
        # symbol is stored as e.g. "($U$)" — strip outer parens for clean rendering
        symbol_rendered = symbol[1:-1] if symbol.startswith("(") and symbol.endswith(")") else symbol
        term_line = f"**{term}** {symbol_rendered}".rstrip() if symbol_rendered else f"**{term}**"
        lines.append(term_line)
        lines.append(f":   {defn}")
        lines.append("")

    return "\n".join(lines)


def process_course(course_dir: Path) -> int:
    """
    Scan all lecture files in a course directory, extract key terms,
    and write definitions.qmd. Returns count of terms found.
    """
    output_path = course_dir / "definitions.qmd"

    # Find all lecture files matching L??-*.qmd, sorted by filename
    chapter_files = sorted(
        f for f in course_dir.glob("*.qmd")
        if CHAPTER_PATTERN.search(f.name)
    )

    if not chapter_files:
        print(f"  No lecture files found in {course_dir.name}/")
        return 0

    all_terms: list[tuple[str, str, str, str]] = []

    for chapter in chapter_files:
        terms = extract_keyterms(chapter)
        for term, symbol, defn in terms:
            all_terms.append((term, symbol, defn, chapter.name))

    if not all_terms:
        print(f"  {course_dir.name}: no key term definitions found — skipping")
        return 0

    content = build_glossary(course_dir, all_terms)
    output_path.write_text(content, encoding="utf-8")
    print(f"  ✅ {course_dir.name}: {len(all_terms)} term(s) → {output_path.name}")
    return len(all_terms)


def main():
    repo_root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

    if not repo_root.is_dir():
        print(f"Error: {repo_root} is not a directory")
        sys.exit(1)

    print(f"Scanning course folders in: {repo_root}")

    course_dirs = [p for p in sorted(repo_root.iterdir()) if is_course_dir(p)]

    if not course_dirs:
        print("No course folders found.")
        sys.exit(0)

    grand_total = 0
    for course_dir in course_dirs:
        grand_total += process_course(course_dir)

    print(f"\nDone. {grand_total} term(s) collected across {len(course_dirs)} folder(s).")


if __name__ == "__main__":
    main()
