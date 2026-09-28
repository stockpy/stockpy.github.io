---
layout: default
permalink: /archive/
title: Archive
---

# Blog Archive

{% assign years = "" | split: "" %}
{% for post in site.posts %}
  {% assign year = post.date | date: "%Y" %}
  {% if years contains year %}
  {% else %}
    {% assign years = years | push: year | sort | reverse %}
  {% endif %}
{% endfor %}

<ul>
  {% for year in years %}
    <li><a href="/archive/{{ year }}/">{{ year }}</a></li>
  {% endfor %}
</ul>