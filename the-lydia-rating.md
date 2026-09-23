---
layout: default
title: 'The Lydia Rating: Food & Product Reviews'
description: 'Learn how Lydia Rim approaches restaurant, snack, and product reviews, including value, family-friendliness, and purchase and sponsorship disclosures.'
permalink: /the-lydia-rating/
---
<section class="page-intro shell"><p class="eyebrow">Reviews with a point of view</p><h1>The Lydia Rating</h1><p>Food, snacks, and products considered with care—and a clear answer to whether I would return or buy again.</p></section>
<section class="shell section compact"><div class="prose narrow"><h2>How reviews work</h2><p>Restaurant reviews consider taste, service, atmosphere, value, and family-friendliness. Product reviews consider quality, ease of use, value, design, and usefulness. Snack reviews may include an adult perspective and anonymous responses from children.</p><p>Every review will say whether the item was purchased, gifted, sponsored, linked through an affiliate program, or made and sold by Lydia.</p></div><div class="post-grid">
{% assign rating_posts = site.posts | where: 'category', 'the-lydia-rating' %}
{% for post in rating_posts %}
<article class="post-card"><p class="eyebrow">{{ post.date | date: '%B %-d, %Y' }}</p><h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2><p>{{ post.excerpt | strip_html | truncatewords: 28 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read story →</a></article>
{% endfor %}
</div></section>
