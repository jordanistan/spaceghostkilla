# Backlog

Milestone: **a stranger visits, finds something useful, leaves an email, buys, receives the product, and is measured as a conversion.**

## P0 — first revenue

| # | Item | Owner | Status |
|---|---|---|---|
| 1 | Store section, checkout config, thanks page, positioning | Claude | ✅ on `feat/monetization-foundation` |
| 2 | SEO fundamentals (canonical, OG, sitemap) | Claude | ✅ |
| 3 | Keep internal docs off the live site | Claude | ✅ |
| 4 | Quick Audit v1 content (25 checks) | Claude | ✅ drafted, kept outside the repo (see DECISIONS D5). Needs owner review, then export to PDF. |
| 5 | Cloudflare Email Routing: `support@` + `security@` → owner inbox (adds MX/SPF) | **Owner** | ⬜ |
| 6 | Lemon Squeezy store: $0 Quick Audit + $29 Field Manual, redirect → `https://spaceghostkilla.com/thanks.html`, support email set | **Owner** | ⬜ |
| 7 | Paste the two checkout URLs into `CHECKOUT` in `script.js` | Claude | ⬜ blocked on 6 |
| 8 | `/legal.html`: Terms, Privacy, Refund | Claude drafts | ⬜ blocked on refund-policy decision |
| 9 | Analytics: pageviews + `/thanks.html` + outbound checkout clicks | Claude | ⬜ blocked on provider decision |
| 10 | Field Manual v1 content | Claude drafts + owner | ⬜ can start now |
| 11 | Merge to `main`, then an end-to-end test purchase (free + paid, then refund) on mobile and desktop | Owner approves | ⬜ |

## P1 — right after launch

- Enforce HTTPS in Pages settings, add DMARC `p=quarantine`, protect `main` (PR required).
- Mobile nav (the nav is hidden under 720px today).
- Email nurture sequence (Day 0/2/4/6) via ESP. Sync buyers/leads from the Lemon Squeezy webhook through a Cloudflare Worker with HMAC verification.
- Real `/research` article pages, turning the Field Notes into indexed content. Add `Product` + `Organization` JSON-LD.
- Image optimization (WebP wallpaper, small nav emblem).
- `/services` page with a light "request an assessment" lead form.
- CSP `<meta>` tag.
- First open-source repo (e.g. the Quick Audit as a runnable read-only script).

## P2 — platform

- SpaceGhostKilla Pro ($29/mo) using Lemon Squeezy subscriptions. **Don't charge until the content justifies it.**
- SGK CloudScan (open-source core + licensed Pro via LS license-key API).
- Further ladder products: Cloudflare Hardening Blueprint → AWS Workbook → DevSecOps Kit → …
- Team/corporate licenses, training platform, community.

## IDEAS (not committed)

- Terminal easter-egg commands that surface products (`sgk scan --demo`).
- Lemon Squeezy affiliate program.
- Sponsorship slot in newsletter.
