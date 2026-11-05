import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Fully static site: `npm run build` writes plain HTML/CSS/JS to ./out
  output: "export",
  // Emit /privacy/index.html instead of /privacy.html so S3 static hosting resolves clean URLs
  trailingSlash: true,
  // The Next image optimizer needs a server; static export serves images as-is
  images: { unoptimized: true },
  reactStrictMode: true,
  poweredByHeader: false,
  // Next.js writes an AGENTS.md during `next dev` unless this is off
  agentRules: false,
};

export default nextConfig;
