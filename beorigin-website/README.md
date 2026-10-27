# BeOrigin website

The marketing site for **BeOrigin**, the AI knowledge-transfer platform. *Believe, Begin, Become.*

Built with Next.js (App Router), TypeScript, Tailwind CSS v4 and Framer Motion. The site is **fully static** (`output: "export"`), so it needs no server or backend and can be hosted on S3, Amplify, or any static host.

---

## Run locally

Requires **Node.js 20.9 or newer** (Node 22 LTS recommended).

```bash
cd beorigin-website
npm install
npm run dev
```

Open <http://localhost:3000>. Edits hot-reload.

| Command             | What it does                                                   |
| ------------------- | -------------------------------------------------------------- |
| `npm run dev`       | Dev server with hot reload                                     |
| `npm run build`     | Production static export to `./out`                            |
| `npm start`         | Serves `./out` locally (with gzip) to preview the real build    |
| `npm run lint`      | ESLint (Next.js + Core Web Vitals rules)                       |
| `npm run typecheck` | TypeScript check                                               |

---

## Edit the copy

**All text lives in [`src/content.ts`](src/content.ts).** Headlines, steps, capability cards, the scripted tutor conversation, stats, team, form labels, footer and the privacy/terms text are all there. Change a string and save.

Before launch, update these two placeholders at the top of `content.ts`:

```ts
contactEmail: "your-email@example.com", // demo form + footer
url: "https://www.example.com",          // canonical URL, Open Graph, sitemap
```

### Media

| File                     | Used for                                      | Notes                                          |
| ------------------------ | --------------------------------------------- | ---------------------------------------------- |
| `public/demo.mp4`        | "Product in action" video                     | Placeholder clip. Replace with your recording (H.264 MP4). |
| `public/demo-poster.jpg` | Poster shown before the video plays           | 1280×720 recommended                           |
| `public/og-image.png`    | Social share image (Open Graph / Twitter)     | Must be 1200×630                               |
| `src/app/icon.svg`       | Favicon                                       |                                                |

The video uses `preload="none"`, so it's only downloaded when someone presses play.

### The demo form

On submit, the form opens the visitor's email app with a pre-filled message to `contactEmail` (a `mailto:` link) and shows a success state.

All sending logic is in **one function**: [`src/lib/submitDemoRequest.ts`](src/lib/submitDemoRequest.ts). To switch to a real form service (Formspree, Web3Forms, HubSpot, or your own API Gateway + Lambda), replace that function's body with a `fetch()` call. The file includes an example. Throw an `Error` to show a message in the form; return normally to show the success state.

---

## Project structure

```
src/
  content.ts               ← all site copy
  lib/submitDemoRequest.ts ← the one form-submit function
  app/
    layout.tsx             ← fonts, SEO + Open Graph metadata, JSON-LD
    page.tsx               ← section order
    privacy/  terms/       ← placeholder legal pages
    robots.ts  sitemap.ts  ← generated at build time
    globals.css            ← Tailwind theme (colours, gradient, utilities)
  components/
    Orb.tsx                ← canvas "speaking" orb (hero + tutor mock)
    Navbar, Hero, HowItWorks, Capabilities, ProductDemo,
    Proof, UseCases, Team, BookDemo, Footer, ...
public/                    ← static files copied as-is
```

To reorder or remove sections, edit `src/app/page.tsx`. Brand colours and the purple→cyan gradient are defined in `src/app/globals.css` (`@theme` and `--accent-gradient`).

---

## Build for production

```bash
npm run build
```

This writes a complete static site to **`./out`**: HTML, CSS, JS, images, `robots.txt`, `sitemap.xml` and `404.html`. Pages are exported as folders (`/privacy/index.html`) because `trailingSlash: true` is set, so clean URLs work on S3.

Preview the exact build locally with `npm start`.

---

## Deploy to AWS

### Option A: AWS Amplify Hosting (easiest)

**From Git (auto-deploys on push):**

1. Push this repo to GitHub, GitLab, Bitbucket or CodeCommit.
2. In the AWS console open **Amplify → Create new app → Host web app** and connect the repo and branch.
3. If the site isn't at the repo root, tick **"My app is a monorepo"** and set the app root to `beorigin-website`.
4. Use this build spec (replace the auto-detected one if needed):

   ```yaml
   version: 1
   applications:
     - appRoot: beorigin-website
       frontend:
         phases:
           preBuild:
             commands:
               - npm ci
           build:
             commands:
               - npm run build
         artifacts:
           baseDirectory: out
           files:
             - "**/*"
         cache:
           paths:
             - node_modules/**/*
   ```

5. Deploy. If Amplify detects Next.js and selects an SSR platform, set the app's platform to **static web hosting** (`WEB`). This site doesn't use SSR.
6. Add your domain under **Hosting → Custom domains**.

**Without Git:** run `npm run build`, zip the *contents* of `out/`, and use **Amplify → Deploy without Git** to upload the zip.

### Option B: S3 + CloudFront (recommended for production)

1. **Build:** `npm run build`
2. **Create a bucket** (for example `beorigin-website`). Keep "Block all public access" **on**; CloudFront will read from it.
3. **Upload:**

   ```bash
   # Hashed assets: cache for a year
   aws s3 sync out/ s3://beorigin-website --delete \
     --exclude "*.html" --exclude "*.txt" --exclude "*.xml" \
     --cache-control "public,max-age=31536000,immutable"

   # HTML and other files: always revalidate so new deploys show immediately
   aws s3 sync out/ s3://beorigin-website --delete \
     --exclude "*" --include "*.html" --include "*.txt" --include "*.xml" \
     --cache-control "public,max-age=0,must-revalidate"
   ```

4. **Create a CloudFront distribution:**
   - Origin: the S3 bucket, with **Origin Access Control (OAC)**. Let CloudFront update the bucket policy.
   - Default root object: `index.html`
   - Viewer protocol policy: Redirect HTTP to HTTPS
   - Compress objects automatically: **Yes** (gzip/brotli matters for Lighthouse)
   - Custom error response: 403 and 404 → `/404.html`, response code 404
5. **Clean URLs:** with OAC, CloudFront doesn't map `/privacy/` to `/privacy/index.html` by itself. Add this **CloudFront Function** (viewer request) to the default behaviour:

   ```js
   function handler(event) {
     var request = event.request;
     var uri = request.uri;
     if (uri.endsWith("/")) {
       request.uri += "index.html";
     } else if (!uri.includes(".")) {
       request.uri += "/index.html";
     }
     return request;
   }
   ```

6. Point your domain at the distribution (Route 53 alias record, with an ACM certificate in `us-east-1`).
7. **After each deploy**, invalidate the HTML:

   ```bash
   aws cloudfront create-invalidation --distribution-id <ID> --paths "/*"
   ```

**Quick test without CloudFront:** turn off "Block public access", add a public-read bucket policy, and enable **Static website hosting** with index document `index.html` and error document `404.html`. This works for previews, but it has no HTTPS and no compression.

---

## Notes

- **Accessibility:** semantic landmarks, a skip link, labelled form controls, keyboard-friendly menu (Esc closes it), and visible focus states. All animation, including the canvas orb, respects the OS "reduce motion" setting.
- **Performance:** only Framer Motion's DOM feature set is loaded (`LazyMotion`). The orb paints a still frame first, starts animating once the page is idle, and pauses when off-screen or in a background tab. Fonts are self-hosted via the `geist` package.
- **SEO:** title and description, canonical URL, Open Graph and Twitter cards, Organization JSON-LD, `robots.txt` and `sitemap.xml`, all driven by `content.ts`.
- **No tracking:** the site sets no cookies and loads no third-party scripts.
