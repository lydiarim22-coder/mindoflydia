/* Local Leaflet + Natural Earth map. No geolocation, tracking, or tile requests. */
(() => {
  'use strict';
  const root = document.querySelector('[data-travel-explorer]');
  if (!root) return;
  const status = root.querySelector('[data-travel-status]');
  const controls = root.querySelector('.travel-controls');
  const search = root.querySelector('#travel-search');
  const countrySelect = root.querySelector('#travel-country');
  const empty = root.querySelector('[data-travel-empty]');
  const count = root.querySelector('[data-travel-count]');
  const detailTitle = root.querySelector('#travel-detail-title');
  const detailType = root.querySelector('[data-detail-type]');
  const detailDescription = root.querySelector('[data-detail-description]');
  const detailRating = root.querySelector('[data-detail-rating]');
  const detailLink = root.querySelector('[data-detail-link]');
  const cards = [...root.querySelectorAll('[data-place-id]')];
  const labels = { past: 'Past trip', wishlist: 'Wish list', rating: 'The Lydia Rating' };
  const symbols = { past: '&#10003;', wishlist: '&#9825;', rating: '&#9733;' };
  const worldBounds = [[-57, -175], [82, 180]];
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  let map, countries, markerGroup, places, visible = [], selected = null;
  let activeFilter = 'all';
  const layers = new Map();
  const markers = new Map();
  const normalize = value => String(value || '').normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
  const elementWithText = text => { const el = document.createElement('span'); el.textContent = text; return el; };

  function validLink(value) {
    if (typeof value !== 'string') return false;
    return (value.startsWith('/') && !value.startsWith('//')) || /^https:\/\//.test(value);
  }
  function countryStyle(feature) {
    const chosen = feature.properties.code === countrySelect.value;
    const populated = visible.some(place => place.country === feature.properties.code);
    return { color: chosen ? '#805978' : '#b7c7bd', weight: chosen ? 1.5 : 0.7,
      fillColor: chosen ? '#d9c4de' : populated ? '#ece3ee' : '#fffdfb', fillOpacity: 1 };
  }
  function clearDetails() {
    selected = null;
    cards.forEach(card => card.classList.remove('is-selected'));
    const feature = layers.get(countrySelect.value)?.feature;
    detailType.textContent = feature ? 'Explore a country' : 'A world of possibilities';
    detailTitle.textContent = feature ? feature.properties.name : 'Start somewhere.';
    detailDescription.textContent = feature
      ? (visible.length ? 'Choose a place below or a pin on the map to discover more.' : 'No places have been shared here for this selection yet. Try another country or reset the map.')
      : 'Select a country to explore, or choose a shared place to see its story.';
    detailRating.hidden = true;
    detailLink.hidden = true;
    detailLink.removeAttribute('href');
  }
  function showPlace(place, focusMap = false) {
    selected = place.id;
    detailType.textContent = labels[place.type];
    detailTitle.textContent = place.name;
    detailDescription.textContent = `${place.location}. ${place.summary}`;
    detailRating.textContent = place.rating ? `Lydia's rating: ${place.rating}` : '';
    detailRating.hidden = !place.rating;
    detailLink.hidden = !validLink(place.url);
    if (validLink(place.url)) {
      detailLink.href = place.url;
      detailLink.textContent = place.type === 'rating' ? 'Read the review →' : 'Read the story →';
    } else { detailLink.removeAttribute('href'); }
    cards.forEach(card => card.classList.toggle('is-selected', card.dataset.placeId === place.id));
    markers.forEach((marker, id) => marker.getElement()?.classList.toggle('is-active', id === place.id));
    map.setView([place.latitude, place.longitude], 4.5, { animate: !reducedMotion });
    status.textContent = `${place.name}, ${place.location}. ${labels[place.type]} selected.`;
    if (focusMap) {
      root.querySelector('.travel-map-frame').scrollIntoView({ behavior: reducedMotion ? 'instant' : 'smooth', block: 'center' });
      const title = root.querySelector('#travel-detail-title');
      title.setAttribute('tabindex', '-1');
      title.focus({ preventScroll: true });
    }
  }
  function fitCountry(layer) {
    // Focus the largest landmass rather than distant overseas territories.
    const geometry = layer.feature.geometry;
    const polygons = geometry.type === 'MultiPolygon' ? geometry.coordinates : [geometry.coordinates];
    const bounds = polygons.map(polygon => L.latLngBounds(polygon[0].map(point => [point[1], point[0]])));
    bounds.sort((a, b) => ((b.getEast()-b.getWest())*(b.getNorth()-b.getSouth())) - ((a.getEast()-a.getWest())*(a.getNorth()-a.getSouth())));
    map.fitBounds(bounds[0], { padding: [25, 25], maxZoom: 4.5, animate: !reducedMotion });
  }
  function render(fit = true) {
    const query = normalize(search.value.trim());
    visible = places.filter(place => (activeFilter === 'all' || place.type === activeFilter)
      && (!countrySelect.value || place.country === countrySelect.value)
      && normalize(`${place.name} ${place.location} ${place.summary} ${layers.get(place.country)?.feature.properties.name || ''}`).includes(query));
    const ids = new Set(visible.map(place => place.id));
    cards.forEach(card => { card.hidden = !ids.has(card.dataset.placeId); });
    markerGroup.clearLayers();
    markers.clear();
    visible.forEach(place => {
      const marker = L.marker([place.latitude, place.longitude], {
        icon: L.divIcon({ className: `travel-pin ${place.type}`, html: `<span aria-hidden="true">${symbols[place.type]}</span>`, iconSize: [30, 30], iconAnchor: [15, 15] }),
        title: `${place.name} — ${labels[place.type]}`, alt: `${place.name}, ${place.location} — ${labels[place.type]}`,
        keyboard: true, riseOnHover: true
      }).bindTooltip(elementWithText(place.name), { direction: 'top', offset: [0, -16] });
      marker.on('click', () => showPlace(place));
      marker.addTo(markerGroup);
      markers.set(place.id, marker);
    });
    clearDetails();
    countries.setStyle(countryStyle);
    count.textContent = `${visible.length} of ${places.length} ${places.length === 1 ? 'place' : 'places'}`;
    empty.hidden = visible.length > 0;
    empty.textContent = places.length === 0
      ? "The travel collection is just beginning. Shared destinations and reviews will appear here as they are added. In the meantime, explore the world map."
      : activeFilter !== 'all' && !places.some(place => place.type === activeFilter)
        ? `No ${activeFilter === 'past' ? 'past trips' : activeFilter === 'wishlist' ? 'wish-list places' : 'Lydia Rating locations'} have been added yet. Choose another filter to explore the collection.`
        : 'No places match this search. Try another name, country, or filter, or reset the map.';
    status.textContent = `${visible.length} ${visible.length === 1 ? 'place' : 'places'} shown. Select a pin or use the location list below.`;
    if (fit) {
      if (countrySelect.value) fitCountry(layers.get(countrySelect.value));
      else if ((query || activeFilter !== 'all') && visible.length) map.fitBounds(markerGroup.getBounds(), { padding: [40, 40], maxZoom: 4, animate: !reducedMotion });
      else map.fitBounds(worldBounds, { padding: [15, 15], animate: !reducedMotion });
    }
  }

  async function init() {
    try {
      if (!window.L) throw new Error('Map library unavailable');
      places = JSON.parse(document.querySelector('#travel-places-data').textContent);
      if (!Array.isArray(places)) throw new Error('Invalid places');
      const response = await fetch(root.dataset.countriesUrl);
      if (!response.ok) throw new Error('Map data unavailable');
      const geo = await response.json();
      if (!Array.isArray(geo.features) || !geo.features.length) throw new Error('Empty map data');
      geo.features.slice().sort((a, b) => a.properties.name.localeCompare(b.properties.name)).forEach(feature => {
        countrySelect.add(new Option(feature.properties.name, feature.properties.code));
      });
      map = L.map('travel-map', { crs: L.CRS.EPSG4326, minZoom: 0, maxZoom: 5,
        zoomSnap: 0.25, zoomDelta: 0.5, scrollWheelZoom: false, maxBounds: [[-90, -210], [90, 210]],
        maxBoundsViscosity: 0.8, zoomAnimation: !reducedMotion, fadeAnimation: !reducedMotion });
      map.attributionControl.addAttribution('Map data: <a href="https://www.naturalearthdata.com/">Natural Earth</a>');
      countries = L.geoJSON(geo, { style: countryStyle, onEachFeature(feature, layer) {
        layers.set(feature.properties.code, layer);
        layer.bindTooltip(elementWithText(feature.properties.name), { sticky: true });
        layer.on('click', () => { countrySelect.value = feature.properties.code; render(); });
        layer.on('mouseover', () => layer.setStyle({ weight: 1.5, color: '#805978' }));
        layer.on('mouseout', () => countries.resetStyle(layer));
      }}).addTo(map);
      markerGroup = L.featureGroup().addTo(map);
      controls.hidden = false;
      root.querySelectorAll('[data-show-place]').forEach(button => {
        button.hidden = false;
        button.addEventListener('click', () => { const place = places.find(item => item.id === button.dataset.showPlace); if (place) showPlace(place, true); });
      });
      root.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
        activeFilter = button.dataset.filter;
        root.querySelectorAll('[data-filter]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        render();
      }));
      search.addEventListener('input', () => render());
      countrySelect.addEventListener('change', () => render());
      root.querySelector('[data-travel-reset]').addEventListener('click', () => {
        search.value = ''; countrySelect.value = ''; activeFilter = 'all';
        root.querySelectorAll('[data-filter]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.filter === 'all')));
        render();
      });
      render();
      root.dataset.mapReady = 'true';
    } catch (error) {
      if (map) map.remove();
      controls.hidden = true;
      cards.forEach(card => { card.hidden = false; });
      root.querySelectorAll('[data-show-place]').forEach(button => { button.hidden = true; });
      status.textContent = 'The map could not load. You can still browse the places and stories below. Please try reloading the page.';
      root.dataset.mapReady = 'failed';
    }
  }
  init();
})();
