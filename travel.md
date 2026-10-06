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
  <p><a href="{{ '/photo-gallery/' | relative_url }}">Browse the Photo Gallery &rarr;</a></p>
  <p class="travel-status" role="status" aria-live="polite" data-travel-status>Turn on JavaScript to explore the map. Shared places and travel stories are also listed below.</p>
  <div class="travel-map-frame" hidden>
    <div id="travel-map" aria-label="Interactive travel map. Use the country selector or location list to explore with a keyboard."></div>
    <aside class="travel-detail" aria-labelledby="travel-detail-title">
      <p class="eyebrow" data-detail-type>A world of possibilities</p>
      <h3 id="travel-detail-title">Start somewhere.</h3>
      <p data-detail-description>Select a country to explore, or choose a shared place to see its story.</p>
      <p class="travel-detail-rating" data-detail-rating hidden></p>
      <a class="text-link" data-detail-link hidden>Read the story &rarr;</a>
      <p><a class="text-link" data-detail-gallery hidden>View trip photos &rarr;</a></p>
    </aside>
  </div>
  <div class="travel-list-heading"><h3>Places to explore</h3><p data-travel-count></p></div>
  <div class="travel-groups" data-travel-list>
    {% assign place_groups = site.data.travel_places | group_by: 'type' %}
    {% assign group_types = 'past,wishlist,rating' | split: ',' %}
    {% for group_type in group_types %}
    {% for group in place_groups %}{% if group.name == group_type %}
    <section class="travel-group" data-travel-group="{{ group_type }}" aria-labelledby="group-{{ group_type }}">
      <h4 id="group-{{ group_type }}">{% case group_type %}{% when 'past' %}Past trips{% when 'wishlist' %}Wish list{% when 'rating' %}The Lydia Rating{% endcase %}</h4>
      {% if group_type == 'past' %}
      {% assign regions = group.items | group_by: 'region' %}
      {% for region in regions %}
      <details class="travel-region" data-travel-region open>
        <summary>{{ region.name | default: 'Other destinations' | escape }} <span data-region-count>{{ region.items.size }} places</span></summary>
        <div class="travel-places">
          {% for place in region.items %}{% include travel-place.html %}{% endfor %}
        </div>
      </details>
      {% endfor %}
      {% else %}
      <div class="travel-places">
        {% for place in group.items %}{% include travel-place.html %}{% endfor %}
      </div>
      {% endif %}

    </section>
    {% endif %}{% endfor %}
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
