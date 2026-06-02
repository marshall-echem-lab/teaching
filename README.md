---
exclude: true
---

# Teaching Materials — Workflow Guide

This repo contains lecture materials for courses taught by Prof Aaron Marshall.
The same `.qmd` source files generate both an online textbook (Quarto book) and
browser-based Reveal.js slide decks.

**Live site:** https://marshall-echem-lab.github.io/teaching

---

## Folder Structure

```
teaching/
├── README.md                         ← this file (excluded from book/slides)
├── _quarto.yml                       ← Quarto book project config
├── _metadata.yml                     ← shared metadata (MathJax fix for slides)
├── _static/
│   └── custom.css                    ← custom styles for the book
├── collect_definitions.py            ← collects keyterms → CourseName/definitions.qmd
├── py_requirements.txt               ← Python dependencies
├── index.qmd                         ← site landing page
├── .github/
│   └── workflows/
│       └── deploy.yml                ← GitHub Actions: build and deploy on push
└── EnergyBalances/                   ← one folder per course
    ├── index.qmd                     ← course landing page (lecture list + slide links)
    ├── L01-energy-conservation.qmd   ← lecture source files
    ├── L02-state-properties.qmd
    ├── definitions.qmd               ← auto-generated glossary (do not edit by hand)
    └── useful-info.qmd
```

### Naming conventions

| File | Pattern | Example |
|---|---|---|
| Course folder | `CourseName` | `ElectrochemEng` |
| Course index | `CourseName/index.qmd` | `ElectrochemEng/index.qmd` |
| Lecture files | `CourseName/LNN-topic.qmd` | `ElectrochemEng/L01-intro.qmd` |
| Site index | `index.qmd` | — |

Lecture files must start with `L` (e.g. `L01-`, `L02-`) — this is how the
deploy script finds them for slide generation.

---

## Day-to-Day Workflow

### Adding a new lecture

1. Create `CourseName/LNN-topic.qmd` using the authoring pattern below
2. Add the lecture and slide link to `CourseName/index.qmd`
3. Add the file to `_quarto.yml` under the correct course `chapters:` list
4. Commit and push — GitHub Actions handles the rest

### Registering a new lecture in `_quarto.yml`

Open `_quarto.yml` and add the new file to the appropriate `chapters:` block:

```yaml
    - part: "EnergyBalances/index.qmd"
      chapters:
        - EnergyBalances/L01-energy-conservation.qmd
        - EnergyBalances/L02-state-properties.qmd   ← add new lines here
        - EnergyBalances/definitions.qmd
        - EnergyBalances/useful-info.qmd
```

### Adding a slide link in the course index

In `CourseName/index.qmd`, slide URLs follow this pattern:

```markdown
[Slides](/_slides/CourseName/LNN-topic.html){target="_blank"}
```

Example:

```markdown
| 1 — Energy Conservation | [Notes](L01-energy-conservation.qmd) | [Slides](/_slides/EnergyBalances/L01-energy-conservation.html){target="_blank"} |
```

### Committing and pushing (VS Code)

1. Click the **Source Control** icon in the left sidebar
2. Click **+** next to Changes to stage all files
3. Type a commit message
4. Click **Commit**, then **Sync Changes**

### Local preview

```bash
# Preview the textbook (live reload at http://localhost:4200)
quarto preview

# Render a single lecture as slides
quarto render EnergyBalances/L01-energy-conservation.qmd --to revealjs --no-project
```

---

## Standard Section Pattern

Every `##` heading creates a new book section **and** a new slide. Within each
section the content is layered in three parts: a shared anchor sentence, then
slide-only bullet points, then book-only prose. This is the pattern produced by
the `newsection` VS Code snippet (see [VS Code Snippets](#vs-code-snippets) below).

```markdown
## Section Title

One sentence that appears in BOTH the book and the slides — the core idea.

<!-- Slide only bullet points -->
::: {.content-visible when-format="revealjs"}
Optional intro phrase if needed.

- Bullet point for slides
- Another bullet point
:::

<!-- Book only content -->
::: {.content-visible unless-format="revealjs"}
Full prose paragraphs for the textbook. As long as needed. Invisible in slides.

:::
```

> **Important:** Always use `unless-format="revealjs"` for book-only blocks —
> NOT `when-format="html"`. Quarto treats revealjs as an HTML format, so
> `when-format="html"` matches both the book AND slides.

---

## Content Block Reference

### 1. Shared content — shown in BOTH book and slides

Plain text, equations, and the anchor sentence go here with no wrapper.
Each section should have at least one shared sentence at the top.

```markdown
## Section Title

One sentence that appears in both book and slides.

$$
E_p = mgz
$$
```

### 2. Slide-only bullets — shown in SLIDES only

Used for the bullet-point summary of the section shown during live teaching.

```markdown
<!-- Slide only bullet points -->
::: {.content-visible when-format="revealjs"}
Optional intro phrase.

- Bullet point
- Another bullet point
:::
```

#### Incremental (animated) bullets

Add `::: {.incremental}` inside the slide block to reveal bullets one at a time:

```markdown
::: {.content-visible when-format="revealjs"}
::: {.incremental}
- First point — appears on click
- Second point — appears on next click
- Third point — appears on next click
:::
:::
```

#### Pause within a slide

Use `. . .` (space-dot-space-dot-space-dot) to create a reveal break mid-slide,
e.g. to show an equation before its explanation:

```markdown
::: {.content-visible when-format="revealjs"}
$$E_p = mgz$$

. . .

- $m$ = mass, $g$ = gravity, $z$ = height
:::
```

### 3. Book-only prose — shown in BOOK only

Full explanatory paragraphs, subsection headings, and detailed working.
Completely invisible in slides.

```markdown
<!-- Book only content -->
::: {.content-visible unless-format="revealjs"}
Full prose for the textbook. Can include `###` subheadings, equations,
and as much detail as needed.

### Subsection heading (book only)

More detail here.

:::
```

### 4. Book-only collapsed callout — shown in BOOK only, collapsed by default

Used for optional depth: full derivations, tangential context, worked solutions.
Students click to expand. Nest the `unless-format` block inside the callout so
it is also invisible in slides.

```markdown
::: {.callout-note collapse="true"}
### What about nuclear?

::: {.content-visible unless-format="revealjs"}
Detailed explanation here. Completely invisible in slides.
Appears as a collapsed callout in the textbook.
:::

:::
```

### 5. Key term definition — shown in BOTH book and slides

Renders as a styled callout box in both formats. Key terms are also
automatically extracted into the course glossary by `collect_definitions.py`
on each deploy.

```markdown
::: {.callout-note}
### Key Term

**Internal Energy** ($U$) — a thermodynamic state function; how energy is stored within matter.
:::
```

**Format rules for key terms:**
- The heading must be exactly `### Key Term` (singular)
- Each term follows `**Term** ($symbol$) — definition`
- The `($symbol$)` uses inline math and is optional — omit for terms without a symbol
- The separator must be an em-dash `—` (Mac: `Option+Shift+-`)

---

## Multiple Slides from One Book Section

To continue onto a second slide *within the same book section* (no new `##`
heading), use a horizontal rule `---`. This is the pattern produced by the
`newslide` VS Code snippet.

The `---` is invisible in the book (Quarto ignores it in HTML output).

```markdown
## Energy Conservation

One sentence for both book and slides.

<!-- Slide only bullet points -->
::: {.content-visible when-format="revealjs"}
- Point for slide 1
:::

<!-- Book only content -->
::: {.content-visible unless-format="revealjs"}
Book prose for this part of the section.
:::

---

<!-- repeat slide title -->
One sentence that continues the section in book and slides.

::: {.content-visible when-format="revealjs"}
- Point for slide 2 — same book section, new slide
:::

::: {.content-visible unless-format="revealjs"}
Book prose that continues the section.
:::
```

Note the `<!-- repeat slide title -->` comment on the continuation slide — this
is a reminder that the slide has no heading, so the shared sentence acts as the
visual anchor.

---

## VS Code Snippets

Snippets are stored at:
```
/Users/atm45/Library/Application Support/Code/User/snippets/
```

Two snippets are available. Trigger them by typing the prefix and pressing `Tab`.

### `newsection` — new `##` section (new book section + new slide)

Inserts the full three-part pattern: shared sentence, slide bullets, book prose.

| Tab stop | Field |
|---|---|
| `$1` | Section heading (replaces `## Section (and Slide) title`) |
| `$2` | Shared anchor sentence (book + slides) |
| `$3` | Optional intro phrase for slide bullets |
| `$4` | Slide bullet point |
| `$5` | Book-only prose |

### `newslide` — continuation slide (same book section, new slide)

Inserts a `---` break followed by the shared/slide/book pattern, without a new
`##` heading. Use this when a section needs more than one slide.

| Tab stop | Field |
|---|---|
| `$1` | Shared anchor sentence (book + slides) |
| `$2` | Slide bullet point |
| `$3` | Book-only prose |

---

## Python Code in Lectures

Quarto executes Python code cells and can show or hide the source code
independently of the output. Use the `echo` and `output` cell options:

```python
#| echo: false    # hide the source code
#| output: true   # show the output (result, plot, printed text)

m = 1000
g = 9.81
z = 50
E_p = m * g * z
print(f"E_p = {E_p:,.0f} J")
```

| Goal | Options |
|---|---|
| Show code + output | `echo: true`, `output: true` |
| Output only (hide code) | `echo: false`, `output: true` |
| Code only (don't run) | `echo: true`, `eval: false` |
| Slides only | wrap cell in `{.content-visible when-format="revealjs"}` |

---

## Markdown Quick Reference

### Headings

```markdown
# Heading 1   ← book chapter title / first slide in a deck
## Heading 2  ← book section     / new slide
### Heading 3 ← book subsection  / subheading within a slide (book only)
```

### Text Formatting

```markdown
**bold**    *italic*    `inline code`
```

### Lists

```markdown
- Bullet item
  - Indented sub-item

1. Numbered item
2. Another item
```

### Mathematics

Inline: `$E_p = mgz$`

Display block:
```markdown
$$
E_p = mgz
$$
```

### Links

```markdown
[Link text](https://example.com)               ← external
[Another lecture](L02-state-properties.qmd)    ← relative within site
```

---

## GitHub Actions

Every push to `main` automatically:

1. Runs `collect_definitions.py` — collects key terms, writes `CourseName/definitions.qmd`
2. Renders all `L*.qmd` files as standalone Reveal.js slide decks into `_slides/`
3. Renders the Quarto book into `_site/`
4. Copies `_slides/` into `_site/_slides/` so slide links resolve on GitHub Pages
5. Deploys `_site/` to GitHub Pages

Slides are rendered by copying each `.qmd` to a temp directory outside the
repo before rendering, so Quarto doesn't see the book `_quarto.yml` and
applies no project restrictions.

---

## Adding a New Course

1. Create a new folder, e.g. `ElectrochemEng/`
2. Add `ElectrochemEng/index.qmd` (course landing page)
3. Add a `part:` block for the new course in `_quarto.yml`
4. Add a link to the new course in `index.qmd`
5. Start adding lecture files following the naming convention

---

## Key URLs

| Page | URL |
|---|---|
| Teaching home | https://marshall-echem-lab.github.io/teaching |
| EnergyBalances | https://marshall-echem-lab.github.io/teaching/EnergyBalances/index.html |
| ElectrochemEng | https://marshall-echem-lab.github.io/teaching/ElectrochemEng/index.html |
| Slides folder | https://marshall-echem-lab.github.io/teaching/_slides/ |
| GitHub repo | https://github.com/marshall-echem-lab/teaching |
