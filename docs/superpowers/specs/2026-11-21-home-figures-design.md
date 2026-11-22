# Home page figures and reorder: design

Date: 2026-11-21. Status: waiting for approval.

## Why

The site has two readers right now:

1. **SIGIR workshop chairs** who judge the proposal.
2. **Senior researchers we cold-email** to ask them to join as co-organizers.

Both open the home page and decide in about a minute. Today the first screen shows a "proposed" banner, News, and Key Dates. The research question comes after the dates, and the Failure Clinic is two screens down. The goal: a reader with no deep IR background understands what TRACE is about from the first screen, and sees that the workshop is well planned.

## Goals

- A hero figure that explains "reliability under budget" in about ten seconds.
- A small figure that shows what the Failure Clinic does and what it produces.
- A home page order that leads with the idea, then the format, then the people, then the logistics.
- Academically polished: it should look like a strong paper figure, not marketing.
- Works at every screen size, from 320px to 1920px.
- One centered reading column on every page, so text lines end where the column ends.

## Non-goals

- No change to site fonts or colors. The only change on other pages is the column width below.
- No rewrite of the Overview or Failure Clinic text.
- No dark mode (the site has none today).

## Anti-goals (a failure even if it works)

- Anything that reads as a product or SaaS landing page: gradients, animation, card grids.
- A figure that looks like real results. Both figures are illustrations, not data.
- Color as the only signal for right and wrong.

## Approaches considered

| Choice | Options | Picked | Why |
|---|---|---|---|
| Hero figure | A1: one search timeline with two stopping points. A2: two side-by-side panels. B: concept curves. | **A1** | It shows that both answers come from the same run, stopped at different points. That is the core idea. It looks like a paper's Figure 1. B looks like a data claim with no data. |
| Clinic figure | C1: four numbered steps (before, during, after). C2: traces in, two outputs out. | **C1** | It shows chairs a concrete plan and tells a possible co-organizer their role ("each group led by an organizer or PC member"). The steps really are a sequence, so the numbers carry meaning. |
| How to build | One fixed SVG. HTML and CSS with small inline SVG icons. | **HTML and CSS** | A fixed SVG shrinks its text to about 5px on phones. HTML reflows and keeps text real and readable. |

## The hero figure (A1), as approved

Content, top to bottom:

- Question, centered, Lora italic: "Is it safe to take drug X together with drug Y?"
- Subtitle, centered: "An AI agent searches for evidence, one dot per search"
- Two budget labels above the track:
  - Left, red bar: **IN REAL LIFE** / stops after 3 searches / (less budget for lower latency)
  - Right, blue bar: **IN BENCHMARKS** / stops after 20 searches / (more budget, no hard limit on latency)
- Track: a dashed blue frame (benchmark), a light red zone over searches 1 to 3 (real life), 20 dots (first 3 solid, rest lighter), rings on dot 2 and dot 12, end labels "1" and "20".
- Source chips with leader lines: dot 2 "**Source A** 'safe together'"; dot 12 "**Source B** 'serious interaction reported'".
- Two answer boxes:
  - Red: "Agent answers after 3 searches" / "Yes, they are safe to combine." / ✗ "Fully confident, and wrong: it never saw Source B"
  - Green: "Agent answers after 20 searches" / "Sources disagree; check the interaction." / ✓ "Appropriately uncertain: it reports the conflict"
- Caption, centered: "Benchmarks let agents search a lot. Real systems can afford only a few searches." then, bold, "TRACE asks: how reliable are agents under real limits?"

Responsive behavior:

- 641px and up: the full layout. The figure fills the reading column (805px at most).
- 640px and below: chips move under the dots as a list, the dots show small "A" and "B" labels, leader lines are hidden, and the answer boxes stack (real life first).
- Text is never smaller than 11px. The question and caption use balanced line wrapping.

Reference mockup: `.superpowers/brainstorm/2762-1795322316/content/hero-final.html` (local only, not committed).

## The Failure Clinic figure (C1), as approved

- Phase labels: BEFORE THE WORKSHOP (step 1), DURING THE WORKSHOP (steps 2 and 3), AFTER (step 4).
- Step 1: "Contribute failure traces". Input, retrieval trace, and the wrong outcome.
- Step 2: "Classify in small groups". Each group led by an organizer or PC member.
- Step 3: "Revise the taxonomy", and find failures that current metrics miss.
- Step 4 (tinted box, the outputs): "Shared failure taxonomy", "Open evaluation problems", summarized in a report to *SIGIR Forum*.
- Each step has a numbered circle and one small line icon.
- 768px and up: four steps in one row with arrows. Below 768px: a vertical list, each step showing its phase label.

## New home page order

1. Header: title, subtitle, venue line (unchanged).
2. **Hero figure (A1).**
3. Proposal status note (unchanged text, moved under the figure).
4. Overview (unchanged text).
5. The Failure Clinic, with the **C1 figure** under its first paragraph.
6. Speakers & Panelists.
7. Organizers.
8. News and Key Dates (moved down from the top).
9. Venue sentence, past editions, contact (unchanged).

## One centered reading column (all pages)

Today the main content area is 1140px wide on large screens, but prose stops at about 805px (the 72-character line limit). Headers, the status note, and the program committee grid use the full width. So the header is centered on the page while the text below starts at the far left and ends in the middle. It looks unbalanced.

Fix: cap the main content area at 835px (805px of content) and center it. Every element then shares one column under the centered header. Line length stays at about 72 characters. The organizer grid (four cards of 190px) still fits. The program committee grid becomes three columns. Screens narrower than 992px are not affected, because their content area is already narrower than this.

## Build notes

- Each figure is a Jekyll include (`_includes/fig_budget.html`, `_includes/fig_clinic.html`), so the home page stays readable.
- Figure styles live in a new `css/figures.css`, loaded only on the home page through the existing `css` front-matter hook in `head.html`.
- Both figures sit in a light gray panel (`#FCFDFD`, 1px border `#EBEEF0`, 10px radius) so they read as exhibits, separate from the header and text.
- Header: the full workshop name is 24px and the venue line is 19px in muted gray (`#5C5C5C`), so the venue line no longer competes with the name.
- Colors: site blue `#2A6F97`, status red `#D03B3B` and green `#0CA30C` from the dataviz palette. Status colors always come with an icon and a text label.
- Fonts: the site's own Lora and Open Sans. No new font loads.
- Accessibility: each figure is a `<figure>` with an accessible name and a text description. Icons are `aria-hidden`.

## Done when

- No horizontal scroll, overlap, or clipped text at 320, 375, 430, 768, 1024, 1280, 1440, and 1920px. Checked with screenshots.
- The figures match the approved mockups.
- On all pages, content sits in one centered column at 992px and wider.
- Apart from the column width, the other pages are unchanged.

## Left to the builder

- Exact spacing between home sections.
- Icon drawings for C1, kept in the mockup's style.

## Open question

The Overview's second paragraph tells the same story as the hero figure in words. We keep the text for now. A later pass could shorten it.
