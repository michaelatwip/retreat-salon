# The Retreat Salon website

Static site for theretreatsalon.co (The Retreat Salon, San Juan Capistrano). Design: "Linen & Oak" (Comma task a1648).

- `content/*.json`: everything the salon changes (stylists, services and prices, gallery, hours, FAQs, booking link).
- `images/`: photos (web-sized; 1600px wide max for full-width photos).
- `build.py`: builds the site into `_site/` with Python 3, no dependencies. `python3 build.py --serve` previews it on http://localhost:8000.
- `.pages.yml`: the editing form for Pages CMS (pagescms.org), so the salon can change team, prices and photos without code.

## Booking
Booking runs on the salon's Vagaro account (https://www.vagaro.com/theretreatsalonn). Every Book button goes to `bookingUrl` in `content/site.json`.
Paste Vagaro's booking widget code into `vagaroWidget` to embed booking on /book/. A stylist's own Vagaro link goes in their `bookingUrl`.

## Hosting
GitHub Pages, free. `.github/workflows/pages.yml` runs `python3 build.py` and publishes `_site/` on every push to `main`,
so work on a branch and merge through a PR. GitHub Pages needs this repo to be public (free plan); it holds nothing private.
Before launch the site is at https://michaelatwip.github.io/retreat-salon/.

### Pointing the domain (at launch)
1. Repo Settings > Pages > Custom domain: `www.theretreatsalon.co`, then tick Enforce HTTPS once the certificate is issued.
2. In Squarespace > Domains > theretreatsalon.co > DNS, remove the Squarespace defaults and add:
   - A `@` 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153
   - CNAME `www` michaelatwip.github.io
   Keep any MX/TXT email records as they are.
3. Bare `theretreatsalon.co` then redirects to `www`. After it's live, cancel the Squarespace site plan (keep the domain).

Cloudflare Pages works too if preferred: build command `python3 build.py`, output directory `_site`.
