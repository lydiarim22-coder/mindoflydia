---
layout: default
title: Travel Map & Stories
permalink: /travel/
category: travel
description: "Explore past trips, wish-list destinations, and The Lydia Rating locations on Mind of Lydia's interactive travel map."
travel_map: true
---
<section class="shell travel-intro">
  <p class="eyebrow">The travel journal</p>
  <h1>Places that stay <em>with us.</em></h1>
  <p>Memorable trips, places to dream about, and discoveries worth sharing. Explore the map, then find a little inspiration for your own journey.</p>
</section>
<section class="shell travel-explorer" aria-labelledby="explorer-title" data-travel-explorer data-countries-url="{{ '/assets/data/travel-countries.geojson' | relative_url }}">
  <div class="travel-heading">
    <div><p class="eyebrow">Near, far &amp; someday</p><h2 id="explorer-title">Explore the map</h2></div>
    <a class="travel-stories-link" href="#travel-stories">Go to travel stories &darr;</a>
  </div>
  <div class="travel-controls" hidden>
    <div class="travel-filters" role="group" aria-label="Filter places">
      <button type="button" data-filter="all" aria-pressed="true">All places</button>
      <button type="button" data-filter="past" aria-pressed="false"><span class="travel-dot past" aria-hidden="true"></span>Past trips</button>
      <button type="button" data-filter="wishlist" aria-pressed="false"><span class="travel-dot wishlist" aria-hidden="true"></span>Wish list</button>
      <button type="button" data-filter="rating" aria-pressed="false"><span class="travel-dot rating" aria-hidden="true"></span>The Lydia Rating</button>
    </div>
    <div class="travel-search-row">
      <label for="travel-search">Find a place<input id="travel-search" type="search" placeholder="Search destinations or reviews" autocomplete="off"></label>
      <label for="travel-country">Explore a country<select id="travel-country"><option value="">All countries</option></select></label>
      <button type="button" class="travel-reset" data-travel-reset>Reset map</button>
    </div>
  </div>
  <p class="travel-status" role="status" aria-live="polite" data-travel-status>Loading the world map&hellip;</p>
  <div class="travel-map-frame">
    <div id="travel-map" aria-label="Interactive travel map. Use the country selector or location list to explore with a keyboard."></div>
    <aside class="travel-detail" aria-labelledby="travel-detail-title">
      <p class="eyebrow" data-detail-type>A world of possibilities</p>
      <h3 id="travel-detail-title">Start somewhere.</h3>
      <p data-detail-description>Select a country to explore, or choose a shared place to see its story.</p>
      <p class="travel-detail-rating" data-detail-rating hidden></p>
      <a class="text-link" data-detail-link hidden>Read the story &rarr;</a>
    </aside>
  </div>
  <noscript><p class="travel-notice">Turn on JavaScript to explore the map. Shared places and travel stories are also listed below.</p></noscript>
  <div class="travel-list-heading"><h3>Places to explore</h3><p data-travel-count></p></div>
  <div class="travel-places" data-travel-list>
    {% for place in site.data.travel_places %}
    <article class="travel-place" data-place-id="{{ place.id | escape }}">
      {% if place.image %}<img src="{{ place.image | relative_url }}" alt="{{ place.image_alt | escape }}" width="640" height="400" loading="lazy">{% endif %}
      <div class="travel-place-copy">
        <p class="eyebrow">{% case place.type %}{% when 'past' %}Past trip{% when 'wishlist' %}Wish list{% when 'rating' %}The Lydia Rating{% endcase %}</p>
        <h4>{{ place.name | escape }}</h4>
        <p class="travel-place-location">{{ place.location | escape }}</p>
        <p>{{ place.summary | escape }}</p>
        {% if place.rating %}<p class="travel-place-rating">Lydia's rating: {{ place.rating | escape }}</p>{% endif %}
        <div class="travel-place-actions"><button type="button" data-show-place="{{ place.id | escape }}" hidden>Show on map</button>{% if place.url %}<a href="{{ place.url | relative_url }}">{% if place.type == 'rating' %}Read the review{% else %}Read the story{% endif %} &rarr;</a>{% endif %}</div>
      </div>
    </article>
    {% endfor %}
  </div>
  <p class="travel-empty" data-travel-empty{% if site.data.travel_places.size > 0 %} hidden{% endif %}>The travel collection is just beginning. Past trips, wish-list places, and Lydia's reviews will appear here as they are shared. In the meantime, explore the world map.</p>
  <script type="application/json" id="travel-places-data">{{ site.data.travel_places | jsonify | replace: '<', '\u003c' }}</script>
</section>
<section class="shell section" id="travel-stories" aria-labelledby="travel-stories-title">
  <p class="eyebrow">From the journal</p><h2 id="travel-stories-title">Stories along the way</h2>
  {% assign travel_posts = site.posts | where: 'category', 'travel' %}
  {% if travel_posts.size > 0 %}
  <div class="post-grid">
    {% for post in travel_posts %}
    <article class="post-card"><p class="eyebrow">{{ post.date | date: '%B %-d, %Y' }}</p><h3><a href="{{ post.url | relative_url }}">{{ post.title | escape }}</a></h3><p>{{ post.description | default: post.excerpt | strip_html | truncatewords: 28 }}</p><a class="text-link" href="{{ post.url | relative_url }}">Read story &rarr;</a></article>
    {% endfor %}
  </div>
  {% else %}<p class="travel-story-empty">Travel stories and photographs are coming soon. There is plenty of everyday inspiration in <a href="{{ '/journal/' | relative_url }}">the journal</a> while this collection grows.</p>{% endif %}
</section>
