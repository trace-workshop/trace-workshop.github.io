---
nav-title: "Papers"
---

# Accepted Papers

{% if site.data.accepted_papers.size > 0 %}
<ol>
  {% for paper in site.data.accepted_papers %}
  <li>{{ paper.title | escape }}{% if paper.authors %} &middot; <em>{{ paper.authors | escape }}</em>{% endif %}{% if paper.award %} <strong>({{ paper.award | escape }})</strong>{% endif %}{% if paper.url %} <a href="{{ paper.url | escape }}">[paper]</a>{% endif %}</li>
  {% endfor %}
</ol>
{% else %}
Accepted papers will be posted here after author notification.
{% endif %}
