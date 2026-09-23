"""Check rendered Jekyll output before it can be deployed; stdlib only."""
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import xml.etree.ElementTree as ET

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else "_site").resolve()
BASE = "https://mindoflydia.com"
errors = []

def require(condition, message):
    if not condition:
        errors.append(message)

class Page(HTMLParser):
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.meta, self.canonicals, self.links, self.schemas = [], [], [], []
        self.title, self.h1, self.titles = "", 0, 0
        self.in_title = self.in_schema = False
        self.schema = ""
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "title":
            self.titles += 1
            self.in_title = True
        if tag == "h1":
            self.h1 += 1
        if tag == "meta":
            self.meta.append(attrs)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href"))
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])
        if tag == "script" and attrs.get("type") == "application/ld+json":
            self.in_schema, self.schema = True, ""
        if tag == "img":
            require("alt" in attrs, "Image missing alt text")

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_schema:
            self.schema += data

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "script" and self.in_schema:
            self.schemas.append(json.loads(self.schema))
            self.in_schema = False

    def values(self, name):
        return [m.get("content", "") for m in self.meta
                if m.get("name", m.get("property")) == name]

pages = {}
for file in sorted(ROOT.rglob("*.html")):
    relative = file.relative_to(ROOT).as_posix()
    path = "/" + relative
    if path.endswith("index.html"):
        path = path[:-len("index.html")]
    try:
        pages[path] = Page(file.read_text(encoding="utf-8"))
    except (ValueError, OSError) as exc:
        errors.append(f"{path}: cannot parse page or JSON-LD: {exc}")

require(bool(pages), "No HTML pages found")
titles, descriptions = [], []
for path, page in pages.items():
    require(page.titles == 1 and bool(page.title.strip()), f"{path}: need one nonempty title")
    require(page.h1 == 1, f"{path}: need exactly one H1")
    description = page.values("description")
    require(len(description) == 1 and bool(description[0].strip()), f"{path}: need one description")
    require(page.canonicals == [BASE + path], f"{path}: incorrect or duplicate canonical")
    require(page.values("og:url") == [BASE + path], f"{path}: incorrect Open Graph URL")
    require(bool(page.values("og:title")), f"{path}: missing Open Graph title")
    require(bool(page.values("twitter:card")), f"{path}: missing social card")
    require(bool(page.schemas), f"{path}: missing structured data")
    if path != "/404.html":
        require(not any("noindex" in r for r in page.values("robots")), f"{path}: unexpectedly noindex")
        titles.append(page.title)
        descriptions.extend(description)
    for href in page.links:
        url = urlsplit(urljoin(BASE + path, href))
        if url.netloc != "mindoflydia.com" or url.scheme not in ("http", "https"):
            continue
        target = unquote(url.path)
        require(target in pages or (ROOT / target.lstrip("/")).is_file(), f"{path}: broken link {href}")
    articles = [s for s in page.schemas if s.get("@type") == "BlogPosting"]
    for article in articles:
        require(article.get("author", {}).get("name") == "Lydia Rim", f"{path}: missing author")
        require(article.get("author", {}).get("url") == BASE + "/about/", f"{path}: missing author URL")
        require(bool(article.get("datePublished")), f"{path}: missing publication date")
        require(bool(article.get("headline")), f"{path}: missing article headline")
        breadcrumbs = [s for s in page.schemas if s.get("@type") == "BreadcrumbList"]
        require(len(breadcrumbs) == 1, f"{path}: missing breadcrumbs")
        for breadcrumb in breadcrumbs:
            items = breadcrumb["itemListElement"]
            require([i["position"] for i in items] == [1, 2, 3], f"{path}: invalid breadcrumb order")
            require(items[-1]["item"] == BASE + path, f"{path}: wrong breadcrumb URL")
            for item in items:
                require(urlsplit(item["item"]).path in pages, f"{path}: broken breadcrumb")

for label, values in [("title", titles), ("description", descriptions)]:
    for value, count in Counter(values).items():
        require(count == 1, f"Duplicate {label}: {value}")

sitemap = ET.parse(ROOT / "sitemap.xml")
locations = [node.text for node in sitemap.findall(".//{*}loc")]
expected = {BASE + path for path in pages if path != "/404.html"}
require(set(locations) == expected, "Sitemap must contain exactly the indexable pages")
require(len(locations) == len(set(locations)), "Duplicate sitemap URLs")
require("Sitemap: " + BASE + "/sitemap.xml" in (ROOT / "robots.txt").read_text(), "robots.txt missing sitemap")
require(any("noindex" in r for r in pages["/404.html"].values("robots")), "404 page must be noindex")
require(not (ROOT / "SEO-PLAN.md").exists() and not (ROOT / "scripts").exists(), "Internal files leaked into site")
require(sum(s.get("@type") == "BlogPosting" for p in pages.values() for s in p.schemas) > 0, "No article schema found")
if errors:
    print("SEO checks failed:\n" + "\n".join(errors))
    sys.exit(1)
print(f"SEO checks passed: {len(pages)} HTML pages, {len(locations)} sitemap URLs; metadata, JSON-LD, and internal links valid.")