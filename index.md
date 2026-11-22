---
---

{% include status_banner.html %}

# News

{% for n in site.data.news %}
* {{ n.text | markdownify | remove: '<p>' | remove: '</p>' | strip }}{% if n.link %} [{{ n.link_text }}]({{ site.baseurl }}/{{ n.link }}){% endif %}
{% endfor %}

# Key Dates

{% include key_dates.md %}

See the [call for papers]({{ site.baseurl }}/cfp) for full submission details.

# Overview

Retrieval systems are becoming agents: they plan queries, call tools, read and discard evidence, and decide when an answer is sufficiently supported to be returned. Each of these decisions consumes budget (tokens, tool calls, latency), and each is a point at which reliability can be lost.

Yet agentic search and retrieval-augmented generation (RAG) systems are still evaluated predominantly by answer quality at a single, generous operating point. Consider a research agent that, with twenty retrieval calls, locates two conflicting sources and correctly reports the disagreement. With three calls it may retrieve only one of them and state that source's claim with full confidence. Its accuracy declines only modestly, while its *calibration* and its willingness to abstain collapse. A benchmark that reports one accuracy figure at the generous budget cannot detect this failure, yet it is the failure a cost-constrained deployment will encounter. We call the missing property **reliability under budget**.

The central question of TRACE is: *how reliable are retrieval agents at the budget at which they are actually deployed, and how should the IR community measure it?* We bring together perspectives from IR, NLP, machine learning, and AI safety, from academia and industry, and from researchers at every career stage, around five questions:

- **Reliability at deployed budgets**: How far are current retrieval agents from being reliable at the budgets used in deployment?
- **Evidence and abstention**: How should agents reason over evidence that is incomplete, conflicting, or adversarial, and when should they abstain?
- **Agent-specific failures**: Which failures (prompt injection through retrieved content, poisoned corpora, reward hacking, overconfident synthesis) are specific to agents that retrieve, and which are inherited from the underlying models?
- **Allocating effort**: How should retrieval and reasoning effort be allocated, and when should an agent stop searching, given a cost–quality–risk trade-off?
- **Measurement**: What test collections, metrics, and judging protocols, including LLM-based judges, can measure calibration and abstention as a function of budget, reproducibly?

TRACE is not a workshop on agent capabilities in general; it concerns the trustworthiness of retrieval agents as a function of evidence quality and cost.

# The Failure Clinic

The half-day program is built around a hands-on **Failure Clinic**. Before the workshop, presenters and registered participants contribute *failure traces*: an input, the agent's retrieval and reasoning trace, and the erroneous outcome. During the session, participants form small groups, each led by an organizer or program committee member, classify the traces against a draft taxonomy, propose revisions, and identify which failures current metrics would not detect. The principal outputs are a **shared taxonomy of agentic retrieval failures** and a public **list of open evaluation problems**, to be summarized in a report to *SIGIR Forum*.

<hr>

# Speakers & Panelists
<div class="profile-section">
{% include profile_grid.html people=site.data.speakers %}
</div>

{% if site.data.speakers.size > 0 %}Further keynote speakers and panelists will be announced.{% else %}Keynote speakers and panelists will be announced.{% endif %}

<hr>

# Organizers

<!-- prettier-ignore -->
<div class="profile-section">
{% include profile_grid.html people=site.data.organizers %}
</div>

{% if site.edition.open_organizer_slots > 0 %}Further organizers will be announced.{% endif %}

<hr>

TRACE is an in-person, {{ site.edition.format }} workshop at [{{ site.edition.conference }}]({{ site.edition.conference_url }}), {{ site.edition.location }}.

{% if site.data.past_editions.size > 0 %}
# Past Editions

{% for p in site.data.past_editions %}
- [{{ p.name }}]({{ p.url }}){% endfor %}
{% endif %}

{% include contact.md %}
