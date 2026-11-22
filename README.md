# TRACE @ SIGIR 2027

Website for **TRACE: The First Workshop on Trustworthy Retrieval Agents under Cost and Evidence Constraints**, ACM SIGIR 2027, San Jose, CA.

Live at: https://trace-workshop.github.io/ (repository `trace-workshop/trace-workshop.github.io`). Old links under `/sigir2027/` redirect to the same page at the root (see `404.html`).

Built with Jekyll on the [beautiful-jekyll](https://deanattali.com/beautiful-jekyll/) theme (MIT, see `LICENSE`), adapted from the MATH-AI 2026 workshop site layout. Yearly upkeep is described in **[MAINTAINING.md](MAINTAINING.md)**.

## Repository layout

```
_config.yml              EDITION SETTINGS block (year, dates, venue, links) + fixed site settings
_data/
  organizers.yml         organizers (photo, bio, role)
  speakers.yml           confirmed keynotes and panelists only
  committee.yml          supporting roles (publicity chair, ...)
  program_committee.yml  PC list (shown once non-empty)
  schedule.yml           program table
  news.yml               News items on the home page
  accepted_papers.yml    accepted papers (after notification)
  past_editions.yml      links to earlier editions
  SocialNetworks.yml     footer icon definitions (theme)
index.md cfp.md speakers.md organizers.md schedule.md papers.md   pages
_includes/  _layouts/  css/  js/   theme (rarely touched)
img/                     photos (any person without img: gets placeholder.png)
scripts/new_edition.py   creates next year's site from this one
```

Pages never hard-code dates or the venue; they read them from `_config.yml` and `_data/`.
Internal links must start with `{{ site.baseurl }}`. It is empty today because the site lives at the root, but the prefix lets the site move to a sub-path without broken links.

## Publishing on GitHub Pages

1. Create (once) a GitHub organization named `trace-workshop`.
2. Create a public repository **`trace-workshop.github.io`** in it and push this folder to `main`.
3. *Settings → Pages → Build and deployment → Source: Deploy from a branch*, branch `main`, folder `/ (root)`.
4. The site is live at `https://trace-workshop.github.io/` within a few minutes.

## Local preview

```bash
bundle install
bundle exec jekyll serve
# open http://localhost:4000/
```

The `github-pages` gem needs Ruby below 4.0. If your Ruby is newer, run the site in Docker instead:

```bash
docker run --rm -p 4000:4000 -v "$PWD":/site -v trace-gems:/usr/local/bundle -w /site ruby:3.3 \
  sh -c "bundle install && bundle exec jekyll serve --host 0.0.0.0 --force_polling"
```
