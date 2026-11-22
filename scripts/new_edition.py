#!/usr/bin/env python3
"""Start next year's TRACE edition.

The root site (https://trace-workshop.github.io/) always shows the latest
edition. Starting a new year does two things:

  1. ARCHIVE: copies this site to ../sigirYYYY (the outgoing year), sets its
     base URL to /sigirYYYY and its status to "past". You push that folder to
     a new repository trace-workshop/sigirYYYY, so the old edition stays
     online at https://trace-workshop.github.io/sigirYYYY.
  2. RESET IN PLACE: rewrites this site for the new year: edition number + 1,
     all dates "TBD", status "proposal", the outgoing year added to Past
     Editions, and speakers, accepted papers, program committee and news
     emptied. Organizers, committee, schedule and page text are kept for you
     to edit.

Usage (run from anywhere):
    python3 scripts/new_edition.py 2028
    python3 scripts/new_edition.py 2028 --archive-out ../sigir2027

Commit or stash your work first: the script refuses to run on a git tree with
uncommitted changes, because step 2 edits files in place.

Standard library only; no PyYAML needed.
"""
import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

ORDINALS = {1: "First", 2: "Second", 3: "Third", 4: "Fourth", 5: "Fifth",
            6: "Sixth", 7: "Seventh", 8: "Eighth", 9: "Ninth", 10: "Tenth"}

START = "# >>> EDITION SETTINGS"
END = "# <<< END OF EDITION SETTINGS"
SITE = "https://trace-workshop.github.io"

SKIP = {".git", "_site", ".jekyll-cache", ".sass-cache", "vendor", ".bundle",
        "Gemfile.lock", ".jekyll-metadata", ".superpowers", ".playwright-mcp"}


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


def set_field(text: str, key: str, value: str) -> str:
    new, n = re.subn(rf'^(\s*{re.escape(key)}:\s*).*$', lambda m: f'{m.group(1)}"{value}"', text, count=1, flags=re.M)
    if n != 1:
        sys.exit(f"Could not set '{key}' in _config.yml")
    return new


def edition_block(year: int, number: int, contact_email: str, labels: list[str]) -> str:
    title_long = (f"The {ordinal(number)} Workshop on Trustworthy Retrieval Agents "
                  "under Cost and Evidence Constraints")
    dates = "\n".join(f'    - label: "{l}"\n      date: "TBD"' for l in labels)
    return f'''{START}: everything that changes from one year to the next.
# scripts/new_edition.py rewrites this block when it creates the next edition.
# =============================================================================

# The root site always shows the latest edition. Past editions are archived
# in their own repositories, served at {SITE}/sigirYYYY
url: "{SITE}"
baseurl: ""
url-pretty: "trace-workshop.github.io"

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
  # One address, or several separated by commas.
  contact_email: "{contact_email}"
  # Above 0 shows "Further organizers will be announced." Set to 0 when the team is complete.
  open_organizer_slots: 0
  # Above 0 shows "Further panelists will be announced." on the home and Speakers pages.
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


def require_clean_git(repo: Path) -> None:
    try:
        out = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"],
                             capture_output=True, text=True, check=True).stdout
    except (FileNotFoundError, subprocess.CalledProcessError):
        return  # not a git checkout; nothing to protect
    if out.strip():
        sys.exit("This repository has uncommitted changes. Commit or stash them first.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("year", type=int, help="year of the new edition, e.g. 2028")
    ap.add_argument("--archive-out", type=Path,
                    help="folder for the outgoing edition's archive (default: ../sigirYYYY next to this site)")
    args = ap.parse_args()

    src = Path(__file__).resolve().parent.parent
    cfg = (src / "_config.yml").read_text()
    if START not in cfg or END not in cfg:
        sys.exit("_config.yml is missing the EDITION SETTINGS markers.")

    old_year = int(field(cfg, "year"))
    old_number = int(field(cfg, "number"))
    old_conf = field(cfg, "conference")
    contact = field(cfg, "contact_email")
    labels = re.findall(r'^\s*- label:\s*"([^"]+)"', cfg, re.M)
    if args.year <= old_year:
        sys.exit(f"New year {args.year} must be after the current edition ({old_year}).")

    archive = (args.archive_out or src.parent / f"sigir{old_year}").resolve()
    if archive.exists():
        sys.exit(f"{archive} already exists; refusing to overwrite it.")
    require_clean_git(src)

    # 1) archive the outgoing edition under /sigirYYYY
    shutil.copytree(src, archive, ignore=lambda d, names: [n for n in names if n in SKIP])
    a_cfg = set_field(cfg, "baseurl", f"/sigir{old_year}")
    a_cfg = set_field(a_cfg, "url-pretty", f"trace-workshop.github.io/sigir{old_year}")
    a_cfg = set_field(a_cfg, "status", "past")
    (archive / "_config.yml").write_text(a_cfg)

    # 2) reset this site for the new year
    head, rest = cfg.split(START, 1)
    _, tail = rest.split(END, 1)
    (src / "_config.yml").write_text(head + edition_block(args.year, old_number + 1, contact, labels) + END + tail)

    past = src / "_data" / "past_editions.yml"
    entries = [l for l in past.read_text().splitlines() if l.strip() and l.strip() != "[]"]
    header = [l for l in entries if l.startswith("#")]
    body = [l for l in entries if not l.startswith("#")]
    new_entry = [f'- name: "TRACE @ {old_conf} ({ordinal(old_number)} edition)"',
                 f'  url: "{SITE}/sigir{old_year}/"']
    past.write_text("\n".join(header + new_entry + body) + "\n")

    resets = {
        "speakers.yml": "# Keynote speakers and panelists. Only list people who have CONFIRMED.\n"
                        "# Copy the entry format from last year's archive.\n[]\n",
        "accepted_papers.yml": "# Fill after notifications. Each entry: title, authors, url (optional), award (optional).\n[]\n",
        "program_committee.yml": "# Program committee (organizers do not serve on the PC).\n"
                                 "# - name: \"Jane Doe\"\n#   affiliation: \"Example University\"\n[]\n",
        "news.yml": "# News items, newest first. See last year's archive for the format.\n"
                    f'- text: "TRACE returns for its {ordinal(old_number + 1).lower()} edition at ACM SIGIR {args.year}."\n',
    }
    for name, text in resets.items():
        (src / "_data" / name).write_text(text)

    print(f"Archived SIGIR {old_year} to {archive}")
    print(f"Reset {src.name} for SIGIR {args.year}")
    print(f"""
Next steps (see MAINTAINING.md for the full checklist):
  1. Create the GitHub repository trace-workshop/sigir{old_year}, push {archive},
     and enable Pages. Check {SITE}/sigir{old_year}/ loads.
  2. In this repository, edit _config.yml: location, date, timezone, dates,
     conference_url, proposal_decision.
  3. Update _data/organizers.yml (and photos in img/), _data/committee.yml, _data/schedule.yml.
  4. Revise the theme text in index.md and cfp.md.
  5. Remake img/share.png (it shows the year, place, date and "Proposed").
  6. Review the diff, commit, and push.""")


if __name__ == "__main__":
    main()
