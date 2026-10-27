import Link from "next/link";
import type { Metadata } from "next";

export const metadata: Metadata = { title: "Page not found" };

export default function NotFound() {
  return (
    <main id="main" className="flex min-h-dvh flex-col items-center justify-center px-5 text-center">
      <p className="font-mono text-sm text-brand-cyan">404</p>
      <h1 className="mt-3 text-4xl font-semibold text-white">This page doesn&apos;t exist</h1>
      <Link href="/" className="mt-8 rounded-full bg-accent px-6 py-3 font-medium text-white">
        Back home
      </Link>
    </main>
  );
}
