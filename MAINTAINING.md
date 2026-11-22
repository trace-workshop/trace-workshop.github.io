# Maintaining the TRACE website

## How the sites are organized

| Repository (GitHub org `trace-workshop`) | URL | Purpose |
|---|---|---|
| `trace-workshop.github.io` | https://trace-workshop.github.io/ | Landing page listing every edition |
| `sigir2027` | https://trace-workshop.github.io/sigir2027 | 2027 edition |
| `sigir2028`, `sigir2029`, ... | https://trace-workshop.github.io/sigirYYYY | one repository per later edition |

Each edition keeps its own repository so that a past year's page, papers, and
speakers stay online unchanged as an archive. A new edition starts as a copy of
the previous one.

## Where to edit what

| To change | Edit |
|---|---|
| Year, venue, date, key dates, submission link, contact email, status banner | `_config.yml`, EDITION SETTINGS block |
| Organizers (and their photos) | `_data/organizers.yml`, `img/` |
| "Further organizers will be announced" / "Panelists will be announced" lines (shown when the value is above 0) | `edition.open_organizer_slots` / `edition.open_speaker_slots` in `_config.yml` (restart `jekyll serve` after changing it) |
| Keynotes and panelists | `_data/speakers.yml` (confirmed people only) |
| Publicity chair and other roles | `_data/committee.yml` |
| Program committee | `_data/program_committee.yml` |
| News on the home page | `_data/news.yml` |
| Program table | `_data/schedule.yml` |
| Accepted papers | `_data/accepted_papers.yml` |
| Theme, topics, tracks text | `index.md`, `cfp.md` |

Photos: square, about 600×600 px, saved as `img/<id>.jpg`, where `<id>` is the
person's key in the data file (e.g. `ehossain.jpg`).

`edition.status` in `_config.yml` controls the banner at the top of the home page
and call for papers:

- `proposal`: proposal under review; shows the decision date
- `accepted`, `cfp-open`: no banner
- `past`: marks the page as an archive and points to the landing page

## Starting a new edition (each year)

1. From this repository run:
   ```bash
   python3 scripts/new_edition.py 2028
   ```
   This creates `../sigir2028` with:
   - the edition number and base URL updated
   - every date reset to `TBD`
   - this edition added to the Past Editions list
   - speakers, PC, accepted papers and news emptied
2. In the new folder, fill in the EDITION SETTINGS block of `_config.yml`:
   location, date, timezone, key dates, conference URL, decision date.
3. Update `_data/organizers.yml` and photos, `_data/committee.yml`, `_data/schedule.yml`.
4. Revise the theme text in `index.md` and `cfp.md`.
5. Create the repository `trace-workshop/sigir2028`, push, and enable Pages
   (see README.md).
6. In the previous year's repository, set `edition.status: "past"` and push.
7. In `trace-workshop.github.io`, update the "Latest edition" box and add the
   new edition to the list.

## Timeline within one edition

| When | What to update |
|---|---|
| Proposal submitted | status `proposal`, organizers, tentative dates |
| Proposal accepted | status `accepted`; add the news item |
| Call for papers opens | status `cfp-open`; `submission_url`; news item |
| Speakers confirm | add them to `_data/speakers.yml` with photo and bio |
| PC formed | `_data/program_committee.yml` (people who agreed to be listed) |
| After notification | `_data/accepted_papers.yml`; final `_data/schedule.yml` |
| After the workshop | slides or recordings links; then status `past` once the next edition exists |

## Rules of thumb

- List speakers and PC members only after they have confirmed.
- Never hard-code a date or the venue in a page; use the settings and data files.
- Internal links must start with `{{ site.baseurl }}/`.
- Check the site locally (README.md, "Local preview") before pushing larger changes.
