# Mind of Lydia SEO plan

## Foundation implemented September 23, 2026

- Jekyll SEO Tag supplies canonical URLs, unique titles/descriptions, Open Graph,
  social cards, and WebSite/WebPage/BlogPosting structured data.
- Posts identify Lydia Rim and link to her About page. Publication dates remain
  original. Set `last_modified_at` only when an article is substantively updated;
  the post template displays that update date.
- Category breadcrumbs, related stories, and /journal/ connect every post.
- The education landing page describes the existing college-planning resources.
- The sitemap and robots.txt remain automatic. A custom 404 is excluded from the
  sitemap and marked noindex. Internal planning files are excluded from output.
- Font styles load directly in the document head with preconnects instead of
  a CSS import. No performance-score improvement is claimed without measurement.
- Deployment checks validate rendered metadata, JSON-LD, sitemap coverage,
  headings, and local links before publishing.

## First account task: measure discovery

Search Console ownership and sitemap submission are not verified. The project
notes say an account exists; that alone does not establish successful setup.

1. Open the mindoflydia.com property in Google Search Console.
2. Confirm ownership, then submit https://mindoflydia.com/sitemap.xml if needed.
3. Confirm the sitemap status is Success. Inspect the homepage, /education/,
   and the Brown, AAU, and CLEP article URLs. Request indexing for key URLs when
   appropriate; requests do not guarantee indexing.
4. Record an initial 28-day baseline: clicks, impressions, CTR, average position,
   queries, and landing pages. Review Page indexing for actual exclusion reasons.
5. Verify that GA4 property G-QHQF5V1R4L receives a test visit before relying on it.

## Content priorities for the next month

Priorities below are based on existing content, not keyword-volume or Search
Console data. Refine them once actual queries and impressions are available.

| Focus | Existing starting point | Next useful action |
| --- | --- | --- |
| College planning for parents | CLEP, AAU, Brown curriculum guides | Improve articles around readers' actual questions; keep primary sources current and link related guides contextually. |
| Relatable motherhood | Snacks, kitchen, welcome stories | Publish more original experiences in Lydia's established voice; preserve humor rather than padding short posts. |
| Faith and gratitude | Finding Enough in a Grateful Heart | Expand only with Lydia's own reflections and useful practices; link relevant existing writing. |
| Maryland / Howard County | Maryland Homes introduction and professional link | Develop one locally specific guide using Lydia's expertise and verified sources before expanding this section. |
| Reviews | The Lydia Rating methodology | Publish a firsthand review with original photos, concrete observations, and applicable disclosures. |

Pick a sustainable cadence, such as one useful article per week. Several sections
currently have introductions but no posts. Build depth in the existing strengths
before trying to publish equally across every section. Do not invent experience,
credentials, product ratings, testimonials, or family details.

## Image and editorial checklist

- Add relevant original photos when available, with descriptive filenames, useful
  alt text, dimensions, and efficient compression. Do not expose children's
  identities or location details. Use privacy-checked flattened copies.
- Add `image` front matter only for an actual representative image, for example:

```yaml
image:
  path: /assets/images/your-actual-photo.jpg
  alt: A factual description of the photo
  width: 1200
  height: 630
```

- A relevant image at least 1200 pixels wide can support large previews. The
  shared template allows `max-image-preview:large`; it does not create an image.
- Give each article a distinct, accurate description and one clear main heading.
  Use subheadings when they make longer articles easier to read.
- Keep existing slugs stable. Renaming a URL requires a redirect plan.
- Use official sources for changing education, housing, and health information.
- Earn links by sharing useful work with relevant communities and collaborators.
  No paid link schemes, fabricated reviews, or bulk low-value articles.

## Verify after publishing

Check GitHub Actions, Google Rich Results Test for a representative post, and
Search Console URL Inspection. Run PageSpeed Insights on mobile and desktop to
identify measured performance problems. Review Search Console monthly and improve
pages gaining impressions but failing to answer the searcher's question well.

Technical eligibility and structured data do not guarantee rankings or rich
results. Track outcomes rather than treating a passed checklist as traffic growth.

References:
- https://developers.google.com/search/docs/essentials
- https://developers.google.com/search/docs/appearance/structured-data/article
- https://developers.google.com/search/docs/appearance/structured-data/breadcrumb
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls