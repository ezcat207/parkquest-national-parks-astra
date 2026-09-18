# ParkQuest Astra

A photography-led national parks checklist, map and personal travel collection for young explorers and families.

Production: https://parkquest-national-parks-astra.pages.dev

## Build & check

Requires Node 22+; production has no third-party JavaScript dependencies.

```sh
npm run build
npm test
python3 -m http.server 8947 --directory site
```

Browser regression suite: install Playwright in your test environment, install its Chromium browser, start the local server on port 8947, then run `node scripts/browser-test.cjs`. An optional `PLAYWRIGHT_MODULE` environment variable can point to a shared Playwright installation.

## Product

63 park guides, search and region filtering, want-to-go lists, date/note visit records, travel journal, real map, collection milestones, regional counter, printable family activities and JSON backup import/export. Progress is local to the browser. There is no login or cloud sync.

## Sources & design

- `design.md`: research, design rationale, SEO architecture and acceptance criteria.
- `data/photos.json`: per-image credit, source, descriptive alternative text and park data.
- `data/nps-units.json`: NPS description cache inherited from the original project; dynamic conditions must be checked on official park pages.
- `/credits/`: public photography and privacy information.
- `site/usmap.js`: original project's d3-geo / US Atlas geometry, with Alaska and Hawaii insets and labeled territory markers.

`build.mjs` generates static HTML with unique metadata and canonical URLs. Publish `site/`. Local image originals were converted to optimized WebP; the published assets are checked in, so rebuilding needs no network or image tools. `scripts/photos.py` is an acquisition helper, not part of the build; manually curated image selections are recorded in `data/photos.json`.

## Deployment

```sh
wrangler pages deploy site --project-name=parkquest-national-parks-astra --branch=main
```

This is an independent repository and Cloudflare Pages project. The original ParkQuest deployment is preserved. Deployments are made explicitly with Wrangler; no automatic GitHub deployment is claimed.
