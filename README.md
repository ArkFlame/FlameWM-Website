# FlameWM website

Static GitHub Pages website for **FlameWM — IceWM made friendly by ArkFlame Studios**.

Production domain: **https://wm.arkflame.com**

## Deploy

1. Create or use the GitHub repository that will host the website.
2. Push this directory to the repository's `main` branch.
3. In **Settings → Pages**, set **Source** to **GitHub Actions** if it is not already selected.
4. The included `.github/workflows/pages.yml` publishes the static site automatically.
5. Keep the repository-root `CNAME` file. It contains `wm.arkflame.com`.

## DNS for wm.arkflame.com

Because `wm.arkflame.com` is a custom subdomain, configure a DNS `CNAME` record at the domain provider:

```text
Type:  CNAME
Name:  wm
Value: <YOUR-GITHUB-USER-OR-ORG>.github.io
```

Replace the value with the GitHub Pages host for the account/organization that owns the website repository. Do not point the DNS record at `wm.arkflame.com` itself.

After DNS resolves, GitHub Pages can provision HTTPS. GitHub recommends verifying the custom domain in the account/organization settings as an additional takeover-protection measure.

## Local preview

No build tool or package manager is required.

```bash
python3 -m http.server 8080
```

Then open `http://127.0.0.1:8080/`.

## Structure

```text
.
├── .github/workflows/pages.yml
├── assets/
│   ├── css/site.css
│   ├── images/
│   └── js/site.js
├── .gitignore
├── .nojekyll
├── 404.html
├── CNAME
├── android-chrome-192x192.png
├── android-chrome-512x512.png
├── apple-touch-icon.png
├── favicon-16x16.png
├── favicon-32x32.png
├── favicon.ico
├── index.html
├── README.md
├── robots.txt
├── site.webmanifest
└── sitemap.xml
```

## Project links used by the site

- Source: https://github.com/arkflame/flamewm
- Donate: https://paypal.me/LinsaFTW
- Website: https://wm.arkflame.com
