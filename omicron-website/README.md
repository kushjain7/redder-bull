# Omicron website

The marketing site for **Omicron**, the AI knowledge-transfer platform. *Knowledge, multiplied.*

Built with Next.js (App Router), TypeScript, Tailwind CSS v4 and Framer Motion. The site is **fully static**: `npm run build` produces plain HTML/CSS/JS in `out/`, so there is no server or backend to run.

---

## Deploy on your domain (AWS Amplify, about 10 minutes)

1. **Connect the repo.** In the AWS console open **Amplify → Create new app → GitHub**, authorise GitHub, and pick this repository and the `main` branch.
2. **Build settings.** Amplify picks up `amplify.yml` from this repo automatically (install, build, publish `out/`). Nothing to change.
3. **Environment variables.** Before the first deploy, open *Advanced settings* (or later, **Hosting → Environment variables**) and add:

   | Variable                    | Value                                   | What it does                                       |
   | --------------------------- | --------------------------------------- | -------------------------------------------------- |
   | `NEXT_PUBLIC_SITE_URL`      | `https://www.yourdomain.com`            | Canonical URL, social-share previews, sitemap      |
   | `NEXT_PUBLIC_CONTACT_EMAIL` | the inbox that should get demo requests | Turns on the Book a Demo form and the footer email |

4. **Platform.** If Amplify detects Next.js and offers SSR, make sure the app is set to **static hosting** (platform `WEB`). This site doesn't use SSR.
5. **Deploy**, then open the `*.amplifyapp.com` link to check it.
6. **Domain.** Go to **Hosting → Custom domains → Add domain** and follow the DNS steps. If the domain is on Route 53 this is automatic; at another registrar, add the CNAME records Amplify shows. Amplify issues the HTTPS certificate for you.

After that, every push to `main` redeploys. If you change an environment variable, choose **Redeploy this version**, because the values are baked in at build time.

> **About the demo form:** until `NEXT_PUBLIC_CONTACT_EMAIL` is set, no email appears anywhere on the site, and submitting the form shows "Online demo booking is being set up." Once it's set, submitting opens the visitor's email app with a pre-filled request addressed to that inbox.

Other hosts (Vercel, Netlify, Cloudflare Pages, S3 + CloudFront) also work: build with `npm run build`, publish the `out/` folder, and set the same two environment variables. S3 + CloudFront notes are [further down](#s3--cloudfront).

---

## Run locally

Requires **Node.js 20.9 or newer** (Node 22 LTS recommended).

```bash
npm install
cp .env.example .env.local   # optional: fill in the two values
npm run dev                  # http://localhost:3000
```

| Command             | What it does                                                 |
| ------------------- | ------------------------------------------------------------ |
| `npm run dev`       | Dev server with hot reload                                   |
| `npm run build`     | Production static export to `./out`                          |
| `npm start`         | Serves `./out` locally (with gzip) to preview the real build |
| `npm run lint`      | ESLint (Next.js + Core Web Vitals rules)                     |
| `npm run typecheck` | TypeScript check                                             |

---

## Edit the site

**All text lives in [`src/content.ts`](src/content.ts):** headlines, steps, capability cards, the scripted tutor conversation, stats, team, form labels, footer, and the privacy/terms text. Change a string and push.

| File                     | Used for                                  | Notes                                                  |
| ------------------------ | ----------------------------------------- | ------------------------------------------------------ |
| `public/demo.mp4`        | "Product in action" video                 | Placeholder clip. Replace with a real recording (H.264 MP4, same filename). |
| `public/demo-poster.jpg` | Image shown before the video plays        | 1280×720                                               |
| `public/og-image.png`    | Social-share preview (WhatsApp, LinkedIn, X) | Must be 1200×630                                    |
| `src/app/icon.svg`       | Favicon                                   |                                                        |

The privacy and terms pages are **placeholders**. Replace their text in `content.ts` before relying on them.

### Switching the form to a real form service

All sending logic is in one function: [`src/lib/submitDemoRequest.ts`](src/lib/submitDemoRequest.ts). To use Formspree, Web3Forms, HubSpot or your own API instead of `mailto:`, replace that function's body with a `fetch()` call (there's an example in the file). Throw an `Error` to show a message in the form; return normally to show the success state.

---

## Project structure

```
amplify.yml              ← AWS Amplify build settings
.env.example             ← the two deployment settings
src/
  content.ts             ← all site copy
  lib/submitDemoRequest.ts
  app/
    layout.tsx           ← fonts, SEO + Open Graph metadata, JSON-LD
    page.tsx             ← section order
    privacy/  terms/     ← placeholder legal pages
    robots.ts sitemap.ts ← generated at build time
    globals.css          ← Tailwind theme (colours, purple→cyan gradient)
  components/            ← Navbar, Hero, Orb, HowItWorks, Capabilities,
                           ProductDemo, Proof, UseCases, Team, BookDemo, Footer…
public/                  ← static files copied as-is
```

---

## S3 + CloudFront

1. `npm run build` (with the two environment variables set in your shell).
2. Create a private S3 bucket and upload:

   ```bash
   aws s3 sync out/ s3://YOUR-BUCKET --delete \
     --exclude "*.html" --exclude "*.txt" --exclude "*.xml" \
     --cache-control "public,max-age=31536000,immutable"
   aws s3 sync out/ s3://YOUR-BUCKET --delete \
     --exclude "*" --include "*.html" --include "*.txt" --include "*.xml" \
     --cache-control "public,max-age=0,must-revalidate"
   ```

3. Create a CloudFront distribution with the bucket as origin via **Origin Access Control**, default root object `index.html`, *Redirect HTTP to HTTPS*, *Compress objects automatically* on, and a custom error response mapping 403/404 to `/404.html` (status 404).
4. Add this **CloudFront Function** on viewer request so `/privacy/` serves `/privacy/index.html`:

   ```js
   function handler(event) {
     var request = event.request;
     var uri = request.uri;
     if (uri.endsWith("/")) request.uri += "index.html";
     else if (!uri.includes(".")) request.uri += "/index.html";
     return request;
   }
   ```

5. Point the domain at the distribution (Route 53 alias, ACM certificate in `us-east-1`). After each deploy run `aws cloudfront create-invalidation --distribution-id <ID> --paths "/*"`.

---

## Notes

- **Accessibility:** semantic landmarks, skip link, labelled form controls, keyboard-friendly menu, visible focus states. All animation, including the canvas orb, respects the OS "reduce motion" setting.
- **Performance:** only Framer Motion's DOM feature set is loaded. The orb paints a still frame first, animates once the page is idle, and pauses off-screen. Fonts are self-hosted.
- **SEO:** title, description, canonical URL, Open Graph and Twitter cards, Organization JSON-LD, `robots.txt` and `sitemap.xml`.
- **No tracking:** no cookies, no third-party scripts.
