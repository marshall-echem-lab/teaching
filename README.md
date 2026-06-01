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

## Five-Block Authoring Pattern

Every lecture `.qmd` file uses these five content types:

### 1. Plain content — shown in BOTH book and slides

```markdown
$$
\dot{Q} = \dot{m} \, C_p \, \Delta T
$$

Plain text, equations, and core content go here with no wrapper.
```

### 2. Book-only prose — shown in BOOK only (invisible in slides)

```markdown
::: {.content-visible unless-format="revealjs"}
A sentence or two of plain prose context. Renders as normal
text in the textbook. Completely invisible in slides.
:::
```

> **Important:** Use `unless-format="revealjs"` — NOT `when-format="html"`.
> Quarto treats revealjs as an HTML format, so `when-format="html"` matches
> both the book AND slides. `unless-format="revealjs"` correctly excludes
> only the slides.

### 3. Slide-only content — shown in SLIDES only

```markdown
::: {.content-visible when-format="revealjs"}
**Key points for live teaching:**

- Bullet point 1
- Bullet point 2
:::
```

### 4. Book-only dropdown — shown in BOOK only as collapsed callout

```markdown
::: {.callout-note collapse="true"}
## Full derivation

::: {.content-visible unless-format="revealjs"}
Detailed explanation, full worked solution, extra context.
Completely invisible in slides. Appears as a collapsed
callout in the textbook — students click to expand.
:::
:::
```

### 5. Key term definition — shown in BOTH book and slides

```markdown
::: {.callout-note}
## 📘 Key Terms

**Enthalpy** (*H*) — A thermodynamic state function defined as $H = U + PV$

**Internal Energy** (*U*) — The total energy stored within a system
:::
```

Renders as a styled callout box in both the textbook and slides.
Key terms are also automatically extracted into a course glossary
(`CourseName/definitions.qmd`) by `collect_definitions.py` on each deploy.

**Format rules for key terms:**
- The heading must be exactly `## 📘 Key Terms`
- Each term must follow `**Term** (*symbol*) — definition`
- The symbol e.g. `(*H*)` is optional — omit for terms without one
- The separator must be an em-dash `—` (Mac: `Option+Shift+-`)

---

## Multiple Slides from One Book Section

In the textbook, `##` creates a new section heading. In slides, `##` also
creates a new slide. To continue onto a second slide *without* creating a
new book section, use a horizontal rule `---`:

```markdown
## Energy Conservation

Book prose here — as long as you like.

::: {.content-visible when-format="revealjs"}
Content for slide 1
:::

---

::: {.content-visible when-format="revealjs"}
Content for slide 2 — same book section, new slide
:::
```

The `---` is invisible in the book (Quarto ignores it in HTML output).

---

## Python Code in Lectures

Quarto executes Python code cells and can show or hide the source code
independently of the output. Use the `echo` and `eval` cell options:

```python
#| echo: true     # show the source code in book AND slides
#| eval: true     # execute the code and show the output

import numpy as np
x = np.linspace(0, 10, 100)
```

| Goal | Options |
|---|---|
| Show code + output | `echo: true`, `eval: true` |
| Output only (hide code) | `echo: false`, `eval: true` |
| Code only (don't run) | `echo: true`, `eval: false` |
| Slides only | wrap cell in `{.content-visible when-format="revealjs"}` |

---

## Markdown Quick Reference

### Headings

```markdown
# Heading 1   ← book chapter title / first slide in a deck
## Heading 2  ← book section     / new slide
### Heading 3 ← book subsection  / subheading within a slide
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

Inline: `$\dot{Q} = \dot{m} C_p \Delta T$`

Display block:
```markdown
$$
\dot{Q} = \dot{m} \, C_p \, \Delta T
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
