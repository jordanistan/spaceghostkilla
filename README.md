# SpaceGhostikilla // Phantom Protocol

A dependency-free static security research website built around the SpaceGhostikilla visual identity.

## Run locally

You can open `index.html` directly, or serve the folder locally:

```bash
python -m http.server 8080
```

Then visit `http://localhost:8080`.

## Deploy

This site can be deployed as-is to GitHub Pages, Cloudflare Pages, Netlify, Vercel static hosting, or any ordinary web server.

## Structure

- `index.html` — page content
- `styles.css` — theme, responsive layout, effects
- `script.js` — starfield, filters, terminal UI
- `assets/` — SpaceGhostikilla logo, wallpaper, favicon
- `.well-known/security.txt` — responsible disclosure contact placeholder

## Customize

Search for `YOUR-SECURITY-EMAIL@example.com` in `.well-known/security.txt` and replace it with your real disclosure address before publishing.

The vulnerability cards are intentionally defensive and educational: they explain root cause and remediation without shipping weaponized exploit instructions.
