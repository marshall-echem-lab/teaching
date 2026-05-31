#!/usr/bin/env python3
"""
collect_definitions.py

Scans all course folders at the repo root for chapter files matching *-L??-*.md,
extracts :::admonition / :class: keyterm blocks, and writes a
CourseName-definitions.md glossary file into each course folder.

Folder detection: any subdirectory of the repo root that is not a known
system/tool folder (_build, .github, _static, node_modules, .git, __pycache__).

Chapter files: only files matching the pattern *-L??-*.md (e.g. ench291-L01-energy-conservation.md).
Index, info, and other supporting files are ignored.

Usage:
  python collect_definitions.py [repo_root]

  repo_root defaults to the current working directory.
"""

import re
import sys
from pathlib import Path


# Folders to skip when scanning for course directories
SKIP_DIRS = {
    "_build", ".github", "_static", "node_modules",
    ".git", "__pycache__", ".venv", "venv",
}

# Only process files matching this pattern
CHAPTER_PATTERN = re.compile(r'.+-L\d{2}-.+\.md$')


def is_course_dir(path: Path) -> bool:
    """Return True if this subdirectory looks like a course folder."""
    return path.is_dir() and path.name not in SKIP_DIRS and not path.name.startswith(".")


def extract_keyterms(md_path: Path) -> list[tuple[str, str, str]]:
    """
    Parse a chapter .md file and return a list of (term, definition) pairs
    found in :::admonition / :class: keyterm blocks.

    Expected format:
        :::admonition 📘 Key Term
        :class: keyterm

        **Term** — definition text

        **Another Term** — another definition
        :::
    """
    text = md_path.read_text(encoding="utf-8")
    lines = text.splitlines()
    terms = []
    i = 0

    while i < len(lines):
        line = lines[i].strip()

        # Detect opening of an admonition block
        if line.startswith(":::") and len(line) > 3 and not line.startswith("::::"):
            # Collect inner lines until closing :::
            inner = []
            i += 1
            depth = 1
            while i < len(lines) and depth > 0:
                s = lines[i].strip()
                if s == ":::":
                    depth -= 1
                elif s.startswith(":::") and len(s) > 3:
                    depth += 1
                    inner.append(lines[i])
                else:
                    inner.append(lines[i])
                i += 1

            # Check if this block has :class: keyterm
            classes = []
            for l in inner:
                m = re.match(r'^\s*:class:\s*(.*)', l)
                if m:
                    classes.extend(m.group(1).split())
            if "keyterm" not in classes:
                continue

            # Extract term/definition pairs from lines like:
            #   **Term** — definition text
            #   **Term** (*H*) — definition text
            for l in inner:
                # Skip option lines and blank lines
                if re.match(r'^\s*:(class|name):', l) or not l.strip():
                    continue
                # Capture: **Term** [optional (*symbol*)] — definition
                m = re.match(r'^\s*\*\*(.+?)\*\*(?:\s*(\([^)]*\)))?\s*(?:—|-{1,2})\s*(.*)', l)
                if m:
                    term = m.group(1).strip()
                    symbol = m.group(2).strip() if m.group(2) else ""
                    defn = m.group(3).strip()
                    terms.append((term, symbol, defn))
        else:
            i += 1

    return terms


def build_glossary(
    course_dir: Path,
    all_terms: list[tuple[str, str, str, str]]
) -> str:
    """
    Render the definitions file content.

    all_terms: [(term, symbol, definition, source_filename), ...]
    """
    course_name = course_dir.name
    lines = [
        "---",
        f"title: \"Key Terms\"",
        "subtitle: \"Auto-generated glossary\"",
        "---",
        "",
        f"# {course_name} Key Terms",
        "",
        "*This glossary is automatically generated from lecture chapter files.*",
        "*To add or update a term, edit the relevant lecture file.*",
        "",
    ]

    for term, symbol, defn, source in sorted(all_terms, key=lambda x: x[0].lower()):
        term_line = f"**{term}** {symbol}".rstrip() if symbol else f"**{term}**"
        lines.append(term_line)
        lines.append(f":   {defn}")
        lines.append("")

    return "\n".join(lines)


def process_course(course_dir: Path) -> int:
    """
    Scan all chapter files in a course directory, extract keyterms,
    and write the definitions file. Returns count of terms found.
    """
    course_name = course_dir.name
    output_path = course_dir / f"{course_name}-definitions.md"

    # Find all chapter files matching *-L??-*.md, sorted by filename
    chapter_files = sorted(
        f for f in course_dir.glob("*.md")
        if CHAPTER_PATTERN.match(f.name)
    )

    if not chapter_files:
        print(f"  No chapter files found in {course_dir.name}/")
        return 0

    # Collect all terms as a flat list
    all_terms: list[tuple[str, str, str]] = []
    total = 0

    for chapter in chapter_files:
        terms = extract_keyterms(chapter)
        for term, symbol, defn in terms:
            all_terms.append((term, symbol, defn, chapter.name))
            total += 1

    if total == 0:
        print(f"  {course_name}: no keyterm definitions found — skipping")
        return 0

    content = build_glossary(course_dir, all_terms)
    output_path.write_text(content, encoding="utf-8")
    print(f"  ✅ {course_name}: {total} term(s) → {output_path.name}")
    return total


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
