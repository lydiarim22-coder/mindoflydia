---
layout: default
title: Education
permalink: /education/
description: Reflections, practical ideas, and resources to support our children's education and nurture a lifelong love of learning.
---
<section class="page-intro shell"><p class="eyebrow">The journal</p><h1>Education</h1><p>Learning is part of everyday life, from questions around the kitchen table to new discoveries in the classroom. Here, I'll share reflections, practical ideas, and resources to support our children's education and nurture a lifelong love of learning.</p></section>
<section class="shell section compact">
{% assign education_posts = site.posts | where: 'category', 'education' %}
{% if education_posts.size > 0 %}
<div class="post-grid">
{% for post in education_posts %}
<article class="post-card"><p class="eyebrow">{{ post.date | date: '%B %-d, %Y' }}</p><h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2><p>{{ post.excerpt | strip_html | truncatewords: 28 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read story &rarr;</a></article>
{% endfor %}
</div>
{% else %}
<p>Education stories are coming soon. Check back for new posts.</p>
{% endif %}
</section>
