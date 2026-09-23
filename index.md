---
layout: default
title: 'Motherhood, Education & Inspired Living'
description: 'Honest motherhood stories, college-planning resources for parents, and reflections on faith and everyday family life by Lydia Rim.'
---
<section class="hero">
  <div class="shell hero-inner">
    <p class="eyebrow">Welcome to Mind of Lydia</p>
    <h1>Real life.<br><em>Honest motherhood.</em><br>Inspired living.</h1>
    <p class="hero-copy">Honest motherhood stories, college-planning resources for parents, and reflections on faith and everyday family life, by Lydia Rim.</p>
    <a class="button" href="{{ '/motherhood/' | relative_url }}">Explore motherhood stories <span aria-hidden="true">→</span></a>
  </div>
</section>
<section class="shell section" aria-labelledby="latest-title">
  <div class="section-heading"><p class="eyebrow">From the journal</p><h2 id="latest-title">Latest stories</h2></div>
  <div class="post-grid">
    {% for post in site.posts limit: 3 %}
      <article class="post-card">
        <p class="eyebrow">{{ post.category | default: 'Journal' | replace: '-', ' ' }}</p>
        <h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3>
        <p>{{ post.excerpt | strip_html | truncatewords: 24 }}</p>
        <a class="text-link" href="{{ post.url | relative_url }}">Read story →</a>
      </article>
    {% endfor %}
  </div>
  <p><a class="text-link" href="{{ '/journal/' | relative_url }}">Browse all stories &rarr;</a></p>
</section>
<section class="feature-band">
  <div class="shell feature-inner">
    <div><p class="eyebrow">Thoughtful, personal, practical</p><h2>Find your corner.</h2></div>
    <div class="feature-links"><a href="{{ '/motherhood/' | relative_url }}">Motherhood <span aria-hidden="true">→</span></a><a href="{{ '/education/' | relative_url }}">Education <span aria-hidden="true">&rarr;</span></a><a href="{{ '/the-lydia-rating/' | relative_url }}">The Lydia Rating <span aria-hidden="true">→</span></a><a href="{{ '/mental-wellness/' | relative_url }}">Mental Wellness <span aria-hidden="true">&rarr;</span></a><a href="{{ '/maryland-homes/' | relative_url }}">Maryland Homes <span aria-hidden="true">&rarr;</span></a><a href="{{ '/travel/' | relative_url }}">Travel <span aria-hidden="true">&rarr;</span></a><a href="{{ '/faith-and-life/' | relative_url }}">Faith &amp; Life <span aria-hidden="true">&rarr;</span></a><a href="{{ '/shop/' | relative_url }}">Shop <span aria-hidden="true">&rarr;</span></a><a href="{{ '/projects-we-love/' | relative_url }}">Projects We Love <span aria-hidden="true">&rarr;</span></a></div>
  </div>
</section>
