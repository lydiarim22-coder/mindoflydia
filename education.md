---
layout: default
title: 'College Planning & Education for Parents'
permalink: /education/
description: 'Explore parent-friendly guides to CLEP exams, AAU universities, and Brown University''s Open Curriculum, with questions to help families consider college fit.'
---
<section class="page-intro shell"><p class="eyebrow">The journal</p><h1>College planning and education for parents</h1><p>College planning comes with unfamiliar terms and plenty of questions. These parent-friendly guides explore college fit, university learning environments, and credit options, with links to official sources and questions to discuss as a family.</p></section>
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
