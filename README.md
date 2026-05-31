---
exclude: true
---

# Teaching Materials — Workflow Guide

This repo contains lecture materials for courses taught by Prof Aaron Marshall.
The same source files generate both an online textbook and browser-based slide decks.

**Live site:** https://marshall-echem-lab.github.io/teaching

---

## Folder Structure

```
teaching/
├── README.md                        ← this file
├── myst.yml                         ← MyST site config
├── md_to_slides.py                  ← auto-generates .qmd slide files
├── teaching-index.md                ← landing page for the whole site
├── .github/
│   └── workflows/
│       └── deploy.yml               ← GitHub Actions: builds and deploys on every push
└── ENCH-291/                        ← one folder per course
    ├── ench291-index.md             ← course landing page (lecture list + slide links)
    ├── _toc.yml                     ← controls sidebar order
    ├── ench291-L01-topic.md         ← lecture source files
    ├── ench291-L02-topic.md
    └── ...
```

### Naming conventions

| File | Pattern | Example |
|---|---|---|
| Course folder | `CourseName` | `ElectrochemEng` |
| Course index | `CourseName-index.md` | `ElectrochemEng-index.md` |
| Lecture files | `CourseName-LNN-topic.md` | `ElectrochemEng-L01-energy-conservation.md` |
| Site index | `teaching-index.md` | — |

**Never name files `index.md`** — VS Code tabs won't distinguish them.
Files ending in `-index.md` are automatically excluded from slide generation.

---

## Day-to-Day Workflow

### Adding a new lecture

1. Create `CourseName/CourseName-LNN-topic.md` using the four-block pattern below
2. Add the lecture and slide links to `CourseName/CourseName-index.md`
3. Add the file to `CourseName/_toc.yml` in the correct order
4. Commit and push — GitHub Actions handles the rest

### Committing and pushing (VS Code)

1. Click the **Source Control** icon in the left sidebar (branching tree icon)
2. Click **+** next to Changes to stage all files
3. Type a commit message
4. Click **Commit**
5. Click **Sync Changes**

### Local preview

```bash
myst start          # live textbook preview at http://localhost:3000
```

```bash
# Generate and preview slides locally
python md_to_slides.py ENCH-291/ench291-L01-topic.md
quarto render ENCH-291/ench291-L01-topic-slides.qmd
```

---

## Four-Block Authoring Pattern

Every lecture `.md` file uses four types of content blocks:

### 1. Plain content — shown in BOTH book and slides

```markdown
$$
\dot{Q} = \dot{m} \, C_p \, \Delta T
$$

Plain text equations and core content go here with no wrapper.
```

### 2. Book-only plain prose — shown in BOOK only (invisible in slides)

```markdown
<!-- book-only-start -->
A sentence or two of plain prose context. Renders as normal
text in the textbook. Completely invisible in slides.
<!-- book-only-end -->
```

### 3. Slide-only content — shown in SLIDES only

```markdown
:::{note}
:class: slide-only
**Key points for live teaching:**
- Bullet point 1
- Bullet point 2
:::
```

Renders as a styled note box in the textbook. Only the content
inside appears on slides (the box wrapper is stripped).

### 4. Book-only dropdown — shown in BOOK only as collapsed box

```markdown
:::{admonition} Full derivation
:class: dropdown book-only

Detailed explanation, full worked solution, extra context.
Completely stripped from slides. Appears as a collapsed
dropdown in the textbook — students click to expand.
:::
```

### 5. Key term definition — shown in BOTH book and slides

```markdown
:::admonition 📘 Key Terms
:class: keyterm

**Enthalpy** (*H*) — A thermodynamic state function defined as $H = U + PV$

**Internal Energy** (*U*) — The total energy stored within a system
:::
```

Renders as a blue styled callout box in the textbook and as a `callout-note`
box in slides. Multiple terms can appear in one block, or use one block per term.

**Format rules:**
- `:class: keyterm` is required exactly as shown
- Each term must follow the pattern `**Term** (*symbol*) — definition`
- The symbol e.g. `(*H*)` is optional — omit it for terms without one
- The separator must be an em-dash `—` (Mac: `Option+Shift+-`, or copy: —)
- Terms are automatically collected into a `CourseName-definitions.md` glossary on every deploy

---

### Normal slide (new section in book AND new slide)

```markdown
## Slide Title

Content here...
```

### Continuation slide (new slide only, same title, INVISIBLE in book)

```markdown
<!-- new slide -->

More content on the same topic — slide 2 with the same title.
No new section is created in the textbook.
```

Use `<!-- new slide -->` when a topic needs multiple slides but should be a
single section in the textbook.

---

## Course Index File

Each course needs an `ench291-index.md` with this structure:

```markdown
---
title: "Energy Balances"
date: AUTO
---
This page contains the lecture notes, slides and additional resources for "course name". "CourseName" is a course in Chemical and Process Engineering at the University of Canterbury.

## Lecture Notes

- [Lecture 1 — Topic](ench291-L01-topic.md)
- [Lecture 2 — Topic](ench291-L02-topic.md)

## Slides

- [Lecture 1 (Slides)](/slides/ench291-L01-topic-slides.html)
- [Lecture 2 (Slides)](/slides/ench291-L02-topic-slides.html)
```

Slide URLs follow the pattern: `/slides/FILENAME-slides.html`
where `FILENAME` is the lecture `.md` filename without the extension.

---

## Table of Contents File

Each course folder needs a `_toc.yml` to control sidebar order:

```yaml
format: jb-book
root: ench291-index
chapters:
  - file: ench291-L01-topic
  - file: ench291-L02-topic
  - file: ench291-definitions
    title: Key Terms
```

Add new lectures here in the order you want them to appear.
Filenames without the `.md` extension. The `ench291-definitions` file is
auto-generated — just add the entry to `_toc.yml` and it will appear in the nav.

---

## GitHub Actions

Every push to `main` automatically:

1. Runs `collect_definitions.py` — collects keyterms and writes `CourseName-definitions.md` into each course folder
2. Runs `md_to_slides.py` on all lecture `.md` files
3. Renders Quarto Reveal.js slide decks (`.html`)
4. Builds the MyST textbook
5. Copies slide HTML files to `/slides/`
6. Deploys everything to GitHub Pages

**Files excluded from slide generation:**
- `*-index.md` (course index pages)
- `*-definitions.md` (auto-generated glossary pages)
- `index.md` (generic index files)
- Anything in `_build/` or `.github/`

---

## Adding a New Course

1. Create a new folder e.g. `ENCH-302/`
2. Add `ench302-index.md` and `_toc.yml`
3. Add a link to the new course in `teaching-index.md`
4. Start adding lecture files following the naming convention

---

## Key URLs

| Page | URL |
|---|---|
| Teaching home | https://marshall-echem-lab.github.io/teaching |
| ENCH291 | https://marshall-echem-lab.github.io/teaching/ENCH-291/ench291-index |
| Slides folder | https://marshall-echem-lab.github.io/teaching/slides/ |
| GitHub repo | https://github.com/marshall-echem-lab/teaching |
