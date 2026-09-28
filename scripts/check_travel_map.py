"""Validate published location data and exercise the built travel page in Chromium."""
import functools
import json
import re
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright, expect

root = Path('_site').resolve()
output = Path('_test-output')
output.mkdir(exist_ok=True)
html = (root / 'travel/index.html').read_text()
pattern = r'(<script type="application/json" id="travel-places-data">)(.*?)(</script>)'
match = re.search(pattern, html, re.S)
assert match, 'Missing travel JSON'
places = json.loads(match.group(2))
geo = json.loads((root / 'assets/data/travel-countries.geojson').read_text())
codes = {feature['properties']['code'] for feature in geo['features']}
ids = set()
for place in places:
    assert re.fullmatch(r'[a-z0-9-]+', place['id']) and place['id'] not in ids
    ids.add(place['id'])
    assert place['type'] in ('past', 'wishlist', 'rating')
    assert place['country'] in codes
    assert -90 <= place['latitude'] <= 90 and -180 <= place['longitude'] <= 180
    for field in ('name', 'location', 'summary'):
        assert isinstance(place[field], str) and place[field].strip()
    if place.get('rating'):
        assert place['type'] == 'rating' and isinstance(place['rating'], str)
    if place.get('url'):
        url = urlsplit(place['url'])
        assert (url.scheme == 'https' and url.netloc) or (place['url'].startswith('/') and not url.netloc)
        if not url.netloc:
            target = root / url.path.lstrip('/')
            assert target.is_file() or (target / 'index.html').is_file(), 'Missing story URL'
    if place.get('image'):
        assert place.get('image_alt') and (root / place['image'].lstrip('/')).is_file()
assert 'niagara-falls-ny' in ids

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_):
        pass
server = ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(QuietHandler, directory=str(root)))
threading.Thread(target=server.serve_forever, daemon=True).start()
base = f'http://127.0.0.1:{server.server_port}'

with sync_playwright() as p:
    browser = p.chromium.launch()
    context = browser.new_context(viewport={'width': 1440, 'height': 1100}, reduced_motion='reduce')
    context.route('https://www.googletagmanager.com/**', lambda route: route.fulfill(status=200, body=''))
    page = context.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    try:
        page.goto(base + '/travel/')
        expect(page.locator('[data-travel-explorer]')).to_have_attribute('data-map-ready', 'true')
        expect(page.locator('#travel-map .leaflet-overlay-pane path')).to_have_count(len(geo['features']))
        expect(page.locator('[data-place-id="niagara-falls-ny"]')).to_be_visible()
        expect(page.locator('.travel-pin')).to_have_count(len(places))
        page.locator('.travel-pin.past').first.focus()
        page.keyboard.press('Enter')
        expect(page.locator('#travel-detail-title')).not_to_have_text('Start somewhere.')
        page.locator('[data-travel-reset]').click()
        page.locator('[data-filter="wishlist"]').click()
        expect(page.locator('[data-filter="wishlist"]')).to_have_attribute('aria-pressed', 'true')
        wish_count = sum(place['type'] == 'wishlist' for place in places)
        expect(page.locator('.travel-pin')).to_have_count(wish_count)
        if not wish_count:
            expect(page.locator('[data-travel-empty]')).to_contain_text('wish-list')
        page.locator('[data-filter="rating"]').click()
        rating_count = sum(place['type'] == 'rating' for place in places)
        expect(page.locator('.travel-pin')).to_have_count(rating_count)
        if not rating_count:
            expect(page.locator('[data-travel-empty]')).to_contain_text('Lydia Rating')
        page.locator('[data-filter="past"]').click()
        page.locator('#travel-search').fill('Niagara')
        expect(page.locator('[data-place-id]:visible')).to_have_count(1)
        page.locator('#travel-search').fill('no-such-destination')
        expect(page.locator('[data-travel-empty]')).to_contain_text('No places match')
        page.locator('[data-travel-reset]').click()
        page.locator('#travel-country').select_option('FRA')
        expect(page.locator('#travel-detail-title')).to_have_text('France')
        page.locator('#travel-country').select_option('USA')
        expect(page.locator('[data-place-id="niagara-falls-ny"]')).to_be_visible()
        page.locator('[data-travel-reset]').click()
        page.locator('[data-travel-explorer]').screenshot(path=str(output / 'travel-desktop.png'))
        page.locator('[data-show-place="niagara-falls-ny"]').click()
        expect(page.locator('#travel-detail-title')).to_have_text('Niagara Falls')
        expect(page.locator('[data-detail-link]')).to_be_hidden()
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        page.locator('[data-travel-explorer]').screenshot(path=str(output / 'travel-selected.png'))

        page.set_viewport_size({'width': 390, 'height': 844})
        page.locator('[data-travel-reset]').click()
        expect(page.locator('#travel-map')).to_be_visible()
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), 'Mobile horizontal overflow'
        page.locator('[data-show-place="niagara-falls-ny"]').click()
        expect(page.locator('#travel-detail-title')).to_have_text('Niagara Falls')
        page.locator('[data-travel-explorer]').screenshot(path=str(output / 'travel-mobile.png'))
        page.set_viewport_size({'width': 320, 'height': 740})
        assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth'), '320px horizontal overflow'
        page.locator('[data-filter="wishlist"]').click()
        if not wish_count:
            expect(page.locator('[data-travel-empty]')).to_be_visible()
        assert not errors, errors

        # A failed map request must leave the real destination card readable.
        page.route('**/travel-countries.geojson', lambda route: route.abort())
        page.reload()
        expect(page.locator('[data-travel-explorer]')).to_have_attribute('data-map-ready', 'failed')
        expect(page.locator('[data-place-id="niagara-falls-ny"]')).to_be_visible()
        expect(page.locator('.travel-controls')).to_be_hidden()
        page.unroute('**/travel-countries.geojson')

        # Temporary fixtures exercise wishlist/rating behavior without publishing invented locations.
        fixtures = [
            {'id': 'test-wish', 'name': 'Test wish', 'location': 'Japan', 'country': 'JPN', 'type': 'wishlist', 'latitude': 35.7, 'longitude': 139.7, 'summary': 'Test only'},
            {'id': 'test-review', 'name': 'Test review', 'location': 'France', 'country': 'FRA', 'type': 'rating', 'latitude': 48.9, 'longitude': 2.3, 'summary': 'Test only', 'rating': '4 / 5', 'url': '/the-lydia-rating/'},
        ]
        fixture_html = re.sub(pattern, lambda m: m.group(1) + json.dumps(fixtures) + m.group(3), html, flags=re.S)
        page.route('**/travel/', lambda route: route.fulfill(status=200, content_type='text/html', body=fixture_html))
        page.reload()
        expect(page.locator('[data-travel-explorer]')).to_have_attribute('data-map-ready', 'true')
        page.locator('[data-filter="wishlist"]').click()
        expect(page.locator('.travel-pin')).to_have_count(1)
        page.locator('.travel-pin').click()
        expect(page.locator('#travel-detail-title')).to_have_text('Test wish')
        page.locator('[data-filter="rating"]').click()
        page.locator('.travel-pin').click()
        expect(page.locator('[data-detail-rating]')).to_have_text("Lydia's rating: 4 / 5")
        expect(page.locator('[data-detail-link]')).to_have_attribute('href', '/the-lydia-rating/')
        assert not errors, errors

        no_js = browser.new_context(java_script_enabled=False)
        fallback = no_js.new_page()
        fallback.goto(base + '/travel/')
        expect(fallback.locator('[data-place-id="niagara-falls-ny"]')).to_be_visible()
        expect(fallback.locator('noscript')).to_contain_text('Turn on JavaScript')
        no_js.close()
        print(f'Travel map checks passed: {len(places)} approved places; desktop, mobile, keyboard, filters, search, country selection, rating links, and failure/no-JS fallbacks.')
    except Exception:
        page.screenshot(path=str(output / 'travel-failure.png'), full_page=True)
        print('Map status:', page.locator('[data-travel-status]').inner_text())
        print('Browser errors:', errors)
        print('Map error:', page.locator('[data-travel-explorer]').get_attribute('data-map-error'))
        raise
    finally:
        browser.close()
        server.shutdown()
