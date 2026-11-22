# Home Page Figures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add the approved hero figure (A1) and Failure Clinic figure (C1) to the home page, reorder the home page, and center the reading column on all pages.

**Architecture:** Each figure is a Jekyll include made of plain HTML and CSS, with small inline SVG icons. Figure styles live in `css/figures.css`, loaded only on the home page through the existing `page.css` front-matter hook in `_includes/head.html`. The column fix is one rule in `css/main.css`.

**Tech Stack:** Jekyll (github-pages 231), Bootstrap 3, plain CSS. Local preview: Docker container `trace-site` at `http://localhost:4000/`.

**Spec:** `docs/superpowers/specs/2026-11-21-home-figures-design.md`

## Global Constraints

- Figure copy is verbatim from the spec. No em dash anywhere in copy, CSS comments, or commit messages.
- Colors: blue `#2A6F97`, status red `#D03B3B` (text `#B02F2F`, zone `#FBEAEA`), status green `#0CA30C`, ink `#2B2B2B`, secondary ink `#5C5C5C`, rule `#D9DDE1`.
- Fonts: the site's Lora and Open Sans only. No new font loads.
- No text smaller than 11px at any width.
- Status colors always come with an icon and a text label. Icons are `aria-hidden="true"`.
- Each figure is a `<figure>` with an accessible name (`aria-label`) and a text description.
- Reference markup and CSS: `.superpowers/brainstorm/2762-1795322316/content/hero-final.html` (the `<template id="page">` block, classes `tf-*`) and `clinic-figure.html` (option C1). Port, do not redesign.
- Do not commit. Stage only. The user approves each commit and push.

## Layout Check (used by every task)

Run with the Playwright MCP `browser_run_code_unsafe` against `http://localhost:4000`. For each width in `[320, 375, 430, 641, 700, 768, 1024, 1280, 1440, 1920]` and each page in `['/', '/cfp/', '/speakers/', '/organizers/', '/schedule/', '/papers/']`, assert:

- `document.documentElement.scrollWidth <= document.documentElement.clientWidth` (no sideways scroll).
- No visible text element inside `figure` has a computed `font-size` below `11px`.
- No two of these boxes intersect: each `.tf-chip`, each `.tf-lead`, and the ring dots `.tf-dots i.mark` (a chip may touch only its own leader).
- Every element inside `figure` has `getBoundingClientRect().right <= figure.getBoundingClientRect().right + 1` (nothing clipped or sticking out).

Then take a full-page screenshot of `/` at 375, 768, and 1440 and look at it. Delete the screenshots afterwards.

## Review Focus

- **Widths between the phone and tablet layouts (641 to 767px):** chips are positioned above the dots there, and chip B is wide. Expect no overlap and no clipping. Pinned by the 641 and 700 widths in the Layout Check (Task 2).
- **Browser zoom (200%):** this behaves like a narrower viewport. Expect the phone layout, still readable. Covered by the 320 to 641 widths (Task 2).
- **Screen readers:** expect one spoken description per figure and no icon noise. Task 2 and Task 3 assert `aria-label` on the figure and `aria-hidden` on every icon `svg`.
- **Old links into the home page** (for example from the CFP to `organizers#program-committee`): expect them to still work. Task 4 asserts the anchor still lands below the navbar.
- **Browsers without `text-wrap: balance`:** expect normal wrapping and no layout break. Nothing depends on it, so no test.

---

### Task 1: Centered reading column on all pages

**Files:**
- Modify: `css/main.css` (append one rule near the other `[role=main]` rules at the end of the file)

**Interfaces:**
- Produces: the main content column is at most 835px wide (805px of content) and centered. Tasks 2 and 3 size figures to `max-width: 100%` of this column.

- [ ] **Step 1: Run the check that should fail before the change**

At width 1440 on `/`, evaluate `document.querySelector('[role=main]').getBoundingClientRect().width`.
Expected now: `1170`. Target: `835`.

- [ ] **Step 2: Add `.container[role=main] { max-width: 835px; }` to `css/main.css`**

- [ ] **Step 3: Verify**

At 1440: width is `835` and `left` equals `(clientWidth - 835) / 2` within 1px. At 768: width is unchanged (`750`). Run the Layout Check: all pages pass.

- [ ] **Step 4: Stage**

```bash
git add css/main.css
```

### Task 2: Hero figure (A1)

**Files:**
- Create: `_includes/fig_budget.html` (the `<figure class="tf">` block from `hero-final.html`)
- Create: `css/figures.css` (the `.tf*` rules and the `@media (max-width:640px)` block from `hero-final.html`; change `.tf { max-width:880px }` to `max-width:100%`)
- Modify: `index.md` front matter: add `css: ["/css/figures.css"]`, and add `{% include fig_budget.html %}` as the first line of the content.

**Interfaces:**
- Consumes: Task 1's column.
- Produces: `css/figures.css`, which Task 3 appends to. Class prefix `tf-` belongs to this figure only.

- [ ] **Step 1: Run the check that should fail before the change**

On `/`, `document.querySelector('figure.tf')` is `null`.

- [ ] **Step 2: Create `_includes/fig_budget.html` and `css/figures.css`, and edit `index.md` as listed above**

The figure gets `aria-label="The same AI agent at two search budgets"`. Add a visually hidden `<figcaption class="sr-only">` that holds the spec's text description (Bootstrap 3 already defines `.sr-only`). Every icon `svg` gets `aria-hidden="true"`.

- [ ] **Step 3: Verify**

- `figure.tf` exists. It is the first element after `.venue` in `[role=main]`.
- `figure.tf[aria-label]` is set, and every `figure.tf svg` has `aria-hidden="true"`.
- The texts "IN REAL LIFE", "(less budget for lower latency)", "IN BENCHMARKS", "(more budget, no hard limit on latency)", "An AI agent searches for evidence, one dot per search", and "TRACE asks: how reliable are agents under real limits?" are all present.
- `css/figures.css` loads only on `/`. Check `link[href$="figures.css"]` on `/` and on `/cfp/`.
- Layout Check passes, including the 641 and 700 widths.

- [ ] **Step 4: Stage**

```bash
git add _includes/fig_budget.html css/figures.css index.md
```

### Task 3: Failure Clinic figure (C1)

**Files:**
- Create: `_includes/fig_clinic.html`
- Modify: `css/figures.css` (append `.tc*` rules)
- Modify: `index.md`: insert `{% include fig_clinic.html %}` right after the first paragraph under `# The Failure Clinic`.

**Interfaces:**
- Consumes: `css/figures.css` from Task 2.
- Produces: classes with the prefix `tc-`, used only by this figure.

- [ ] **Step 1: Run the check that should fail before the change**

On `/`, `document.querySelector('figure.tc')` is `null`.

- [ ] **Step 2: Build the figure in HTML and CSS**

Port C1 from `clinic-figure.html`: an ordered list `<ol class="tc-steps">` with four `<li>` steps, plus the phase labels. The copy is verbatim from the spec:
- Step 1: "Contribute failure traces"
- Step 2: "Classify in small groups"
- Step 3: "Revise the taxonomy"
- Step 4: "Shared failure taxonomy" and "Open evaluation problems", with "Summarized in a report to *SIGIR Forum*". Step 4 sits in a tinted box.

Layout by width:
- 768px and up: one row of four, with arrows between the steps.
- Below 768px: a vertical list. Each step shows its own phase label (BEFORE THE WORKSHOP, DURING THE WORKSHOP, AFTER), and the arrows point down.

The figure gets `aria-label="How the Failure Clinic works"`. Icons get `aria-hidden="true"`.

- [ ] **Step 3: Verify**

- `figure.tc` is the next element after the first `<p>` that follows the "The Failure Clinic" heading.
- It contains 4 `li` elements, in the order above.
- At 768px and up, the four steps share one row: their `top` values are equal within 2px.
- Below 768px, the steps are stacked: each step's `top` is greater than the previous step's `bottom`.
- Layout Check passes.

- [ ] **Step 4: Stage**

```bash
git add _includes/fig_clinic.html css/figures.css index.md
```

### Task 4: Home page order

**Files:**
- Modify: `index.md`

**Interfaces:**
- Consumes: the includes from Tasks 2 and 3.

- [ ] **Step 1: Run the check that should fail before the change**

On `/`, list the `[role=main] h1` texts. Expected now: `News, Key Dates, Overview, The Failure Clinic, Speakers & Panelists, Organizers`.

- [ ] **Step 2: Reorder `index.md`**

The target order:
1. hero figure
2. `{% include status_banner.html %}`
3. Overview
4. The Failure Clinic (with the C1 figure)
5. Speakers & Panelists
6. Organizers
7. News, then Key Dates, then the "See the call for papers" line
8. the venue sentence, Past Editions, and the contact line

Move whole blocks only. Do not edit any text.

- [ ] **Step 3: Verify**

- The h1 list is `Overview, The Failure Clinic, Speakers & Panelists, Organizers, News, Key Dates`.
- `.trace-note` comes directly after `figure.tf`.
- `git diff index.md` shows only moved lines, plus the lines added in Tasks 2 and 3.
- `/cfp/` → the "program committee" link → `/organizers/#program-committee`: the heading's `top` is at least `51` (it lands below the navbar).
- Layout Check passes on all pages.

- [ ] **Step 4: Stage, show the user, and ask before committing**

```bash
git add index.md
```

Open `http://localhost:4000/` for the user. Commit and push only after they say so.
