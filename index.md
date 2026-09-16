---
layout: default
title: Home
---
<section class="hero">
  <div class="shell hero-inner">
    <p class="eyebrow">Welcome to Mind of Lydia</p>
    <h1>Real life.<br><em>Honest motherhood.</em><br>Inspired living.</h1>
    <p class="hero-copy">A place for stories about family, the small moments that matter, and honest reviews that help you choose what is worth your time.</p>
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
</section>
<section class="feature-band">
  <div class="shell feature-inner">
    <div><p class="eyebrow">Thoughtful, personal, practical</p><h2>Find your corner.</h2></div>
    <div class="feature-links"><a href="{{ '/motherhood/' | relative_url }}">Motherhood <span aria-hidden="true">→</span></a><a href="{{ '/the-lydia-rating/' | relative_url }}">The Lydia Rating <span aria-hidden="true">→</span></a></div>
  </div>
</section>
