# Decisions

## D1 — Keep the static site on GitHub Pages (2026-09-25)
Zero dependencies, no build step, 30s deploys, and a minimal attack surface. Nothing in the P0 funnel needs a server. **Revisit** when webhooks or gated member content need compute. Add a Cloudflare Worker alongside the site rather than migrating it.

## D2 — Commerce: Lemon Squeezy hosted checkout (2026-09-25)
Owner preference. As merchant of record it handles sales tax/VAT, receipts, and signed, expiring download links. That means paid files never touch this public repo, and it covers future subscriptions and license keys. The site links to hosted checkout URLs, which are public values, not secrets. We skip the `lemon.js` overlay for now: no third-party script, simpler CSP.

## D3 — Lead magnet delivered as a $0 Lemon Squeezy product (proposed, 2026-09-25)
One provider captures the email and delivers the file on day one, so the ESP choice no longer blocks launch. The trade-off is that the nurture sequence needs an ESP later (P1), fed by the LS webhook. **Owner to confirm.**

## D4 — Checkout buttons are config-driven and disabled until configured (2026-09-25)
The `CHECKOUT` map in `script.js` holds the URLs, and an empty URL renders a disabled "RELEASING SOON" button. This lets the storefront merge safely before the products exist.

## D5 — Product source files live outside this repo (2026-09-25)
This repo is public, so anything committed is free to everyone. Drafts are currently in `~/Work/spaceghostkilla/products/`. **Recommended:** a private repo `jordanistan/spaceghostkilla-products`.

## D6 — docs/ and README excluded from deployment (2026-09-25)
The Pages workflow publishes every file. Internal planning should stay on GitHub, not on spaceghostkilla.com.

## D7 — Store is an in-page section for now, not a `/store` route (2026-09-25)
Consistent with the current single-page architecture. Split into routes once there are 3+ products or article pages.
