---
---

# Call for Papers

Retrieval systems are becoming agents: they plan queries, call tools, read and discard evidence, and decide when an answer is sufficiently supported to be returned. Each of these decisions consumes budget (tokens, tool calls, latency), and each is a point at which reliability can be lost. TRACE invites work on **how reliable retrieval agents are at the budgets at which they are actually deployed, and how the IR community should measure it**.

{% include status_banner.html %}

## Topics

We welcome contributions on topics including, but not limited to:

- **Reliability at deployed budgets**: calibration, abstention, and answer quality as a function of token, tool-call, and latency budgets.
- **Evidence and abstention**: reasoning over incomplete, conflicting, or adversarial evidence; deciding when to answer and when to abstain.
- **Agent-specific failures**: prompt injection through retrieved content, corpus poisoning, reward hacking, and overconfident synthesis.
- **Allocating effort**: stopping rules, adaptive retrieval, and cost–quality–risk trade-offs for search and reasoning.
- **Measurement**: test collections, metrics, and judging protocols, including LLM-based judges, for measuring calibration and abstention as a function of budget, reproducibly.

Much work on RAG, agents, and LLM evaluation can be connected to this theme. Because the connection is often tenuous, submissions will be evaluated in part on how clearly they articulate it, as well as on technical soundness and potential to generate discussion.

## Important Dates

{% include key_dates.md %}

## Tracks

- **Research papers** (5–8 pages): new work.
- **Short and position papers** (2–4 pages): early results, position statements, or extended abstracts of recently published work.
- **Failure traces**: a short description of an input, the agent's retrieval and reasoning trace, and the erroneous outcome. Traces are accepted on a rolling basis without formal review and are used as material for the Failure Clinic.{% if site.edition.status == "proposal" %} The trace format, a template, and how to send a trace will be posted once the workshop is accepted.{% endif %}

## Submission Requirements

Papers should use the [ACM two-column conference format](https://www.acm.org/publications/proceedings-template) with this document class:

```latex
\documentclass[sigconf,anonymous,review]{acmart}
```

Page limits exclude references. Reviewing is **double-blind** for all reviewed tracks, so every paper, including extended abstracts of published work, must be anonymized. Each paper receives at least two reviews.

The workshop is **non-archival**, so that authors may later publish extended versions at archival venues. Preprints on arXiv and other non-archival venues are welcome. Papers under review at other venues may be submitted concurrently, subject to ACM SIGIR policies.

Every accepted paper will have a poster presentation, and up to six papers will be selected for five-minute lightning talks. Accepted papers, lightning-talk slides, and, optionally, poster thumbnails will be posted on the [Papers]({{ site.baseurl }}/papers) page after author notification.

At least one author of each accepted paper must register for the workshop. Presentations are in person by default. Authors who cannot travel because of visa or funding constraints may have their poster or talk presented by a co-author or an organizer.

Submission site: {% if site.edition.submission_url != "" %}**[{{ site.edition.submission_url }}]({{ site.edition.submission_url }})**{% else %}**to be announced**{% endif %}.

## Program Committee

Reviewing is handled by a [program committee]({{ site.baseurl }}/organizers#program-committee) drawn from academia and industry. Organizers do not serve on the program committee, and organizers will not handle any submission with which they have a conflict.

{% include contact.md %}
