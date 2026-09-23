---
layout: default
title: All Stories
description: "Browse every Mind of Lydia story about motherhood, college planning, faith, family life, and The Lydia Rating."
permalink: /journal/
---
<section class="page-intro shell"><p class="eyebrow">The journal</p><h1>All stories</h1><p>Explore Lydia Rim's latest writing on motherhood, education, faith, and everyday family life.</p></section>
<section class="shell section compact">
  <div class="post-grid">
    {% for post in site.posts %}
    <article class="post-card">
      <p class="eyebrow">{{ post.category | replace: '-', ' ' | escape }}</p>
      <h2><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h2>
      <p>{{ post.description | default: post.excerpt | strip_html | truncatewords: 28 }}</p>
      <p><time datetime="{{ post.date | date_to_xmlschema }}">{{ post.date | date: '%B %-d, %Y' }}</time></p>
    </article>
    {% endfor %}
  </div>
</section>