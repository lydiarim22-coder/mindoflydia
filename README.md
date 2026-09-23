# Mind of Lydia

The blog is a GitHub Pages site with all sections listed below. Posts are Markdown files in
`_posts/`; the site is styled in `assets/css/style.css`.

## Publishing a post

Add a file named `YYYY-MM-DD-post-title.md` in `_posts/`. Start it with:

```yaml
---
layout: post
title: Your post title
category: motherhood
description: A short description for search results.
---
```

Write the post below that header. Use `category: the-lydia-rating` for a review or `category: education` for an education post.
Commit to `main` to publish. The workflow in `.github/workflows/pages.yml`
builds and deploys the site. In the repository's **Settings → Pages**, select
**GitHub Actions** as the build and deployment source before the first deploy.

The site uses the custom domain `mindoflydia.com`. Its GitHub Pages custom-domain
file is `CNAME`, and `_config.yml` generates links from the domain root.

**Real life. Honest motherhood. Inspired living.**

Mind of Lydia is Lydia Rim's personal editorial platform for honest motherhood,
mental wellness, Maryland real estate, food and product reviews, faith, travel,
photography, original designs, and family projects.

## Mission

Mind of Lydia helps mothers feel seen, encouraged, and inspired through honest
stories about family life, mental wellness, faith, work, and creativity. It also
connects readers with Maryland real-estate guidance, memorable food and travel,
and Lydia's original products.

Mental-health writing reflects personal experience and general encouragement;
it is not medical advice or a substitute for care from a qualified professional.

## Content pillars

- Motherhood and family life
- Mental wellness
- Maryland homes, with an emphasis on Howard County
- The Lydia Rating for restaurants, snacks, and products
- Faith and everyday life
- Travel and photography
- Purple Cloth Shop apparel
- Purple Print Shop journals, sketchbooks, and print products
- Projects We Love

## Site sections

- Home
- Motherhood
- Education
- Mental Wellness
- Maryland Homes
- The Lydia Rating
- Travel
- Faith & Life
- Shop
- Projects We Love
- About
- Contact

## The Lydia Rating

Restaurant reviews consider taste, service, atmosphere, value, and
family-friendliness. Product reviews consider quality, ease of use, value,
design, and usefulness. Snack reviews can also distinguish between a parent's
perspective and the children's anonymous responses. Reviews conclude with an
overall rating and a clear answer to either “Would I return?” or “Would I buy it
again?”

Reviews will identify whether an item was purchased, gifted, sponsored, linked
through an affiliate program, or created and sold by Lydia.

## Privacy principles

- Protect the children's names, schools, schedules, and regular locations.
- Avoid real-time travel updates and identifying family photographs.
- Publish only flattened, privacy-checked copies of edited photos.
- Moderate every comment before it becomes public.
- Ask permission before featuring family stories or projects.

## Initial editorial plan

1. Why I Created Mind of Lydia After Burnout
2. What Raising Four Children Has Taught Me About Giving Myself Grace
3. The Lydia Rating: My First Maryland Restaurant Review
4. How I Balance Motherhood, Real Estate, and Creative Work
5. What Maryland Homebuyers Should Prepare Before Starting Their Search

## Business links

- [Lydia Rim — Coldwell Banker Realty](https://lydiarim.sites.cbmoxi.com/)
- [Purple Print Shop on Amazon](https://www.amazon.com/stores/Purple-Print-Shop/author)

Purple Cloth Shop products will be featured through their individual Amazon
product links.

## Visual direction

The brand uses a soft, elegant editorial style with lavender, blush, cream,
sage, deep plum, and charcoal. Original food, home, garden, product, nature, and
travel photography will be combined with occasional portraits and branded quote
graphics for the website, Facebook, and Instagram.

## Section categories

New section pages automatically list posts with these categories:
mental-wellness, maryland-homes, travel, faith-and-life, shop, and projects-we-love.
Use the existing motherhood, education, and the-lydia-rating categories for those sections.

## Search optimization

See [SEO-PLAN.md](SEO-PLAN.md) for account setup, content priorities, and image
guidelines. Every deployment checks the built site's metadata, structured data,
sitemap, and internal links with scripts/check_seo.py before publishing.
