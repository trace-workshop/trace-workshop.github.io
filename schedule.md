---
---

# Schedule

Below is a **tentative** schedule for the {{ site.edition.format }} workshop on {{ site.edition.date }}. About half of the program is spent in discussion rather than listening.

<table class="table schedule-table">
  <caption>All times are in {{ site.edition.timezone_label }}</caption>
  {% for s in site.data.schedule %}
  <tr><td class="schedule-time">{{ s.time }}</td><td>{{ s.item | markdownify | remove: '<p>' | remove: '</p>' }}</td></tr>
  {% endfor %}
</table>

The panel takes the strongest disagreements surfaced in the Failure Clinic as its opening questions and reserves half of its time for the audience. Keynotes and the panel will be recorded and posted online, subject to available equipment and speaker consent.
