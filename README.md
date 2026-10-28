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
Cloudflare Pages, connected to this repo: build command `python3 build.py`, output directory `_site`. Every push to `main` deploys the live site,
so work on a branch and merge through a PR (branches get their own preview URL).
