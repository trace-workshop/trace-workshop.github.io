#!/usr/bin/env python3
"""Create next year's TRACE website from this one.

Usage (run from anywhere):
    python3 scripts/new_edition.py 2028
    python3 scripts/new_edition.py 2028 --out ../sigir2028

What it does:
  * copies this site (without .git, build output, caches) to ../sigirYYYY
  * rewrites the EDITION SETTINGS block of _config.yml for the new year
    (edition number + 1, new base URL, all dates reset to "TBD")
  * adds the current edition to _data/past_editions.yml
  * empties speakers, accepted papers, program committee and news
  * keeps organizers, committee, schedule and page text for you to edit

Standard library only; no PyYAML needed.
"""
import argparse
import re
import shutil
import sys
from pathlib import Path

ORDINALS = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
            6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth"}

START = "# >>> EDITION SETTINGS"
END = "# <<< END OF EDITION SETTINGS"

SKIP = {".git", "_site", ".jekyll-cache", ".sass-cache", "vendor", ".bundle",
        "Gemfile.lock", ".jekyll-metadata"}


def ordinal(n: int) -> str:
    if n in ORDINALS:
        return ORDINALS[n]
    suffix = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def field(text: str, key: str) -> str:
    m = re.search(rf'^\s*{re.escape(key)}:\s*"?([^"\n]*)"?\s*$', text, re.M)
    if not m:
        sys.exit(f"Could not find '{key}' in _config.yml")
    return m.group(1).strip()


def edition_block(year: int, number: int, contact_email: str, labels: list[str]) -> str:
    title_long = (f"The {ordinal(number)} Workshop on Trustworthy Retrieval Agents "
                  "under Cost and Evidence Constraints")
    dates = "\n".join(f'    - label: "{l}"\n      date: "TBD"' for l in labels)
    return f'''{START}: everything that changes from one year to the next.
# scripts/new_edition.py rewrites this block when it creates the next edition.
# =============================================================================

# Each edition is its own repository "sigirYYYY" in the trace-workshop
# organization, served at https://trace-workshop.github.io/sigirYYYY
url: "https://trace-workshop.github.io"
baseurl: "/sigir{year}"
url-pretty: "trace-workshop.github.io/sigir{year}"

title: TRACE @ SIGIR {year}
description: "{title_long}"

edition:
  number: {number}
  ordinal: "{ordinal(number)}"
  year: {year}
  conference: "ACM SIGIR {year}"
  conference_url: "https://sigir{year}.org/"   # TODO: check the official URL
  location: "TBD"
  date: "TBD"
  format: "half-day"
  timezone_label: "TBD"
  # proposal | accepted | cfp-open | past  (controls banners on the site)
  status: "proposal"
  proposal_decision: "TBD"
  # Leave empty until they exist; the pages show "to be announced".
  submission_url: ""
  contact_email: "{contact_email}"
  # Above 0 shows "Further organizers will be announced." Set to 0 when the team is complete.
  open_organizer_slots: 0
  # Above 0 shows "Further keynote speakers and panelists will be announced." on the Speakers page.
  open_speaker_slots: 0
  dates:
{dates}

defaults:
  - scope:
      path: "" # all files
    values:
      layout: "page"
      show-avatar: true
  - scope:
      path: "*.md" # top-level workshop pages
    values:
      title: TRACE
      subtitle: "{title_long}"
      use-site-title: true

# =============================================================================
'''


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year", type=int, help="year of the new edition, e.g. 2028")
    ap.add_argument("--out", type=Path, help="output folder (default: ../sigirYYYY next to this site)")
    args = ap.parse_args()

    src = Path(__file__).resolve().parent.parent
    dst = (args.out or src.parent / f"sigir{args.year}").resolve()
    if dst.exists():
        sys.exit(f"{dst} already exists; refusing to overwrite it.")

    cfg = (src / "_config.yml").read_text()
    if START not in cfg or END not in cfg:
        sys.exit("_config.yml is missing the EDITION SETTINGS markers.")

    old_year = int(field(cfg, "year"))
    old_number = int(field(cfg, "number"))
    old_baseurl = field(cfg, "baseurl")
    old_conf = field(cfg, "conference")
    contact = field(cfg, "contact_email")
    labels = re.findall(r'^\s*- label:\s*"([^"]+)"', cfg, re.M)
    if args.year <= old_year:
        sys.exit(f"New year {args.year} must be after the current edition ({old_year}).")

    shutil.copytree(src, dst, ignore=lambda d, names: [n for n in names if n in SKIP])

    # 1) rewrite the edition block
    head, rest = cfg.split(START, 1)
    _, tail = rest.split(END, 1)
    new_cfg = head + edition_block(args.year, old_number + 1, contact, labels) + END + tail
    (dst / "_config.yml").write_text(new_cfg)

    # 2) record the edition we are leaving
    past = dst / "_data" / "past_editions.yml"
    entries = [l for l in past.read_text().splitlines() if l.strip() and l.strip() != "[]"]
    header = [l for l in entries if l.startswith("#")]
    body = [l for l in entries if not l.startswith("#")]
    new_entry = [f'- name: "TRACE @ {old_conf} ({ordinal(old_number)} edition)"',
                 f'  url: "https://trace-workshop.github.io{old_baseurl}"']
    past.write_text("\n".join(header + new_entry + body) + "\n")

    # 3) reset per-edition people and content
    resets = {
        "speakers.yml": "# Keynote speakers and panelists. Only list people who have CONFIRMED.\n"
                        "# Copy the entry format from last year's site.\n[]\n",
        "accepted_papers.yml": "# Fill after notifications. Each entry: title, authors, url (optional), award (optional).\n[]\n",
        "program_committee.yml": "# Program committee (organizers do not serve on the PC).\n"
                                 "# - name: \"Jane Doe\"\n#   affiliation: \"Example University\"\n[]\n",
        "news.yml": "# News items, newest first. See last year's file for the format.\n"
                    f'- text: "TRACE returns for its {ordinal(old_number + 1).lower()} edition at ACM SIGIR {args.year}."\n',
    }
    for name, text in resets.items():
        (dst / "_data" / name).write_text(text)

    print(f"Created {dst}")
    print(f"""
Next steps (see MAINTAINING.md for the full checklist):
  1. Edit {dst.name}/_config.yml: location, date, timezone, dates, conference_url.
  2. Update _data/organizers.yml (and photos in img/), _data/committee.yml, _data/schedule.yml.
  3. Revise the theme text in index.md and cfp.md.
  4. Create the GitHub repository trace-workshop/{dst.name}, push, and enable Pages.
  5. In the OLD site ({src.name}), set edition.status to "past" and push.
  6. Point the org homepage (trace-workshop.github.io) to the new edition.""")


if __name__ == "__main__":
    main()
