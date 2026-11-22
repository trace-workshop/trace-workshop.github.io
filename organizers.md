---
---

# Organizers

{% include profile_list.html people=site.data.organizers %}

{% if site.edition.open_organizer_slots > 0 %}Further organizers will be announced.{% endif %}

{% for c in site.data.committee %}
**{{ c.role }}:** {{ c.name }}{% if c.affiliation %} ({{ c.affiliation }}){% endif %}
{% endfor %}

## Program Committee

{% if site.data.program_committee.size > 0 %}
{% assign pc_keys = "" | split: "" %}
{% for m in site.data.program_committee %}{% assign last = m.name | split: " " | last %}{% assign k = last | append: "|" | append: m.name %}{% assign pc_keys = pc_keys | push: k %}{% endfor %}
{% assign pc_keys = pc_keys | sort_natural %}
<div class="pc-grid">
  {% for k in pc_keys %}{% assign n = k | split: "|" | last %}{% assign m = site.data.program_committee | where: "name", n | first %}<div class="pc-member"><div class="pc-name">{{ m.name }}</div><div class="pc-affiliation">{{ m.affiliation }}</div></div>{% endfor %}
</div>
{% else %}
The program committee will be announced.
{% endif %}
