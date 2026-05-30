#!/usr/bin/env python3
"""
md_to_slides.py

Converts a MyST Markdown lecture file (.md) to a Quarto Reveal.js slide deck (.qmd).

Content rules:
  - Plain text and equations        → book AND slides
  - :::note / :class: slide-only    → slides only (extra teaching prompts)
  - :::{only} book                  → book only, plain prose (stripped from slides)
  - :::admonition / :class: book-only → book only, dropdown (stripped from slides)

Usage:
  python md_to_slides.py <input.md> [output.qmd]
"""

import re
import sys
from pathlib import Path


QUARTO_FRONTMATTER = """\
---
format:
  revealjs:
    theme: simple
    slide-number: true
    controls: true
    progress: true
    smaller: false
    scrollable: false
    html-math-method: mathjax
title: "{title}"
---
"""


def extract_myst_title(frontmatter: str) -> str:
    match = re.search(r'^title:\s*["\']?(.*?)["\']?\s*$', frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else "Lecture"


def strip_frontmatter(text: str) -> tuple[str, str]:
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[3:end].strip(), text[end + 3:].strip()
    return "", text


def collect_block(lines: list[str], start: int) -> tuple[list[str], int]:
    """
    Collect all lines belonging to a ::: block starting AFTER the opening :::.
    Handles nested ::: blocks. Returns (inner_lines, next_index).
    """
    depth = 1
    i = start
    inner = []
    while i < len(lines) and depth > 0:
        l = lines[i]
        s = l.strip()
        if s == ":::":
            depth -= 1
            if depth == 0:
                i += 1
                break
        elif s.startswith(":::") and len(s) > 3:
            # opening of a nested block
            depth += 1
            inner.append(l)
        else:
            inner.append(l)
        i += 1
    return inner, i


def classify_block(opening_line: str, inner_lines: list[str]) -> str:
    """
    Given the opening ::: line and inner content, return block type:
      slide_only | book_prose | book_only | other
    """
    # Check opening line for {only} book
    if re.search(r'\{only\}\s*book', opening_line):
        return "book_prose"

    # Check inner lines for :class: directives
    classes = []
    for l in inner_lines:
        m = re.match(r'^\s*:class:\s*(.*)', l)
        if m:
            classes.extend(m.group(1).split())

    if "slide-only" in classes:
        return "slide_only"
    if "book-only" in classes:
        return "book_only"

    return "other"


def clean_slide_only(inner_lines: list[str]) -> list[str]:
    """Strip :class: lines from slide_only content."""
    return [l for l in inner_lines if not re.match(r'^\s*:class:', l)]


def parse_blocks(body: str) -> list[dict]:
    lines = body.splitlines()
    blocks = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            blocks.append({"type": "heading", "level": len(m.group(1)), "text": m.group(2).strip()})
            i += 1
            continue

        # ::: directive
        if line.strip().startswith(":::") and len(line.strip()) > 3:
            opening = line.strip()
            inner, i = collect_block(lines, i + 1)
            btype = classify_block(opening, inner)

            if btype == "slide_only":
                blocks.append({"type": "slide_only", "lines": clean_slide_only(inner)})
            elif btype == "book_prose":
                blocks.append({"type": "book_prose"})
            elif btype == "book_only":
                blocks.append({"type": "book_only"})
            else:
                # unknown directive — pass through as body
                blocks.append({"type": "body", "lines": inner})
            continue

        # plain body lines
        body_lines = []
        while i < len(lines):
            l = lines[i]
            if (l.strip().startswith(":::") and len(l.strip()) > 3) or re.match(r'^#{1,6}\s', l):
                break
            body_lines.append(l)
            i += 1
        if body_lines:
            blocks.append({"type": "body", "lines": body_lines})

    return blocks


def blocks_to_slides(blocks: list[dict]) -> list[dict]:
    slides = []
    current = None

    for block in blocks:
        if block["type"] == "heading" and block["level"] == 2:
            if current is not None:
                slides.append(current)
            current = {"title": block["text"], "lines": []}

        elif block["type"] in ("body", "slide_only"):
            if current is not None:
                if current["lines"]:
                    current["lines"].append("")
                current["lines"].extend(block["lines"])

        # book_prose and book_only are silently dropped

    if current is not None:
        slides.append(current)

    return slides


def render_qmd(title: str, slides: list[dict]) -> str:
    parts = [QUARTO_FRONTMATTER.format(title=title)]
    for slide in slides:
        parts.append(f"## {slide['title']}")
        parts.append("")
        content = slide["lines"][:]
        while content and not content[0].strip():
            content.pop(0)
        while content and not content[-1].strip():
            content.pop()
        if content:
            parts.extend(content)
        parts.append("")
        parts.append("---")
        parts.append("")
    return "\n".join(parts)


def convert(input_path: Path, output_path: Path) -> None:
    text = input_path.read_text(encoding="utf-8")
    frontmatter, body = strip_frontmatter(text)
    title = extract_myst_title(frontmatter)
    blocks = parse_blocks(body)
    slides = blocks_to_slides(blocks)
    if not slides:
        print(f"Warning: no slides found in {input_path}")
    qmd = render_qmd(title, slides)
    output_path.write_text(qmd, encoding="utf-8")
    print(f"✅ Generated {output_path}  ({len(slides)} slides)")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    input_path = Path(sys.argv[1])
    if not input_path.exists():
        print(f"Error: file not found: {input_path}")
        sys.exit(1)
    output_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else \
        input_path.with_name(input_path.stem + "-slides.qmd")
    convert(input_path, output_path)


if __name__ == "__main__":
    main()
