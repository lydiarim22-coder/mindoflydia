---
layout: default
title: Motherhood
permalink: /motherhood/
---
<section class="page-intro shell"><p class="eyebrow">The journal</p><h1>Motherhood</h1><p>Stories about family life, learning as we go, and making room for grace.</p></section>
<section class="shell section compact"><div class="post-grid">
{% assign motherhood_posts = site.posts | where: 'category', 'motherhood' %}
{% for post in motherhood_posts %}
<article class="post-card"><p class="eyebrow">{{ post.date | date: '%B %-d, %Y' }}</p><h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2><p>{{ post.excerpt | strip_html | truncatewords: 28 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read story →</a></article>
{% endfor %}
</div></section>
