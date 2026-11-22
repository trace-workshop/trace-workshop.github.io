# Maintaining the TRACE website

## How the sites are organized

| Repository (GitHub org `trace-workshop`) | URL | Purpose |
|---|---|---|
| `trace-workshop.github.io` (this one) | https://trace-workshop.github.io/ | The latest edition, always at the root |
| `sigir2027`, `sigir2028`, ... | https://trace-workshop.github.io/sigirYYYY | Archive of each past edition |

The root always shows the current year, so links you share keep working. When a new year starts, the outgoing edition is copied to its own archive repository, so its pages, papers, and speakers stay online unchanged.

Until an archive repository exists, `404.html` sends old `/sigir2027/...` links to the same page at the root.

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
- `past`: marks the page as an archive and points to the root (the latest edition). `scripts/new_edition.py` sets this in the archive copy.

## Starting a new edition (each year)

1. Commit or stash your work. The script refuses to run on uncommitted changes, because it edits this repository in place.
2. From this repository run:
   ```bash
   python3 scripts/new_edition.py 2028
   ```
   This does two things:
   - **Archive:** copies the current site to `../sigir2027`, with base URL `/sigir2027` and status `past`.
   - **Reset in place:** rewrites this repository for 2028. The edition number goes up by one, every date becomes `TBD`, the status becomes `proposal`, 2027 is added to Past Editions, and speakers, PC, accepted papers, and news are emptied.
3. Create the repository `trace-workshop/sigir2027`, push `../sigir2027` to it, and enable Pages (see README.md). Check that https://trace-workshop.github.io/sigir2027/ loads.
4. In this repository, fill in the EDITION SETTINGS block of `_config.yml`: location, date, timezone, key dates, conference URL, decision date.
5. Update `_data/organizers.yml` and photos, `_data/committee.yml`, `_data/schedule.yml`.
6. Revise the theme text in `index.md` and `cfp.md`.
7. Remake `img/share.png`, the link-preview image. It shows the year, place, date, and "Proposed".
8. Review the diff, commit, and push.

## Timeline within one edition

| When | What to update |
|---|---|
| Proposal submitted | status `proposal`, organizers, tentative dates |
| Proposal accepted | status `accepted`; add the news item; remake `img/share.png` without "Proposed" |
| Call for papers opens | status `cfp-open`; `submission_url`; news item |
| Speakers confirm | add them to `_data/speakers.yml` with photo and bio |
| PC formed | `_data/program_committee.yml` (people who agreed to be listed) |
| After notification | `_data/accepted_papers.yml`; final `_data/schedule.yml` |
| After the workshop | slides or recordings links; the archive copy gets status `past` when the next edition starts |

## Rules of thumb

- List speakers and PC members only after they have confirmed.
- Never hard-code a date or the venue in a page; use the settings and data files.
- Internal links must start with `{{ site.baseurl }}/`.
- Check the site locally (README.md, "Local preview") before pushing larger changes.
