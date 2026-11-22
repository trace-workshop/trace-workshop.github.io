---
---

# Organizers

{% include profile_list.html people=site.data.organizers %}

{% if site.edition.open_organizer_slots > 0 %}Further organizers will be announced.{% endif %}

{% for c in site.data.committee %}
**{{ c.role }}:** {{ c.name }}{% if c.affiliation and c.affiliation != "" %} ({{ c.affiliation }}){% endif %}
{% endfor %}

## Program Committee <span class="heading-note">(in alphabetical order)</span> {#program-committee}

{% if site.data.program_committee.size > 0 %}
{% assign pc = site.data.program_committee | sort_natural: "name" %}
<div class="pc-grid">
  {% for m in pc %}<div class="pc-member"><div class="pc-name">{{ m.name }}</div><div class="pc-affiliation">{{ m.affiliation }}</div></div>{% endfor %}
</div>
{% else %}
The program committee will be announced.
{% endif %}
