<dl class="key-dates">
{% for d in site.edition.dates %}<div{% if d.label contains "deadline" %} class="key-deadline"{% endif %}><dt>{{ d.label }}</dt><dd>{{ d.date }}</dd></div>
{% endfor %}<div><dt>Workshop</dt><dd>{{ site.edition.date }} ({{ site.edition.format }}), {{ site.edition.location }}</dd></div>
</dl>
