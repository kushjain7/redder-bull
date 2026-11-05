import Link from "next/link";
import { Footer } from "./Footer";
import { Logo } from "./Logo";
import { site } from "@/content";

type LegalPageProps = {
  title: string;
  updated: string;
  sections: { heading: string; body: string }[];
};

export function LegalPage({ title, updated, sections }: LegalPageProps) {
  return (
    <>
      <header className="border-b border-white/5">
        <div className="mx-auto flex h-16 max-w-3xl items-center justify-between px-5 sm:px-8">
          <Link href="/" aria-label={`${site.name} home`}>
            <Logo />
          </Link>
          <Link href="/" className="text-sm text-slate-400 hover:text-white">
            ← Back to site
          </Link>
        </div>
      </header>
      <main id="main" className="mx-auto max-w-3xl px-5 py-16 sm:px-8 sm:py-24">
        <h1 className="text-4xl font-semibold tracking-tight text-white sm:text-5xl">{title}</h1>
        <p className="mt-3 text-sm text-slate-400">{updated}</p>
        <div className="mt-12 space-y-10">
          {sections.map((section) => (
            <section key={section.heading}>
              <h2 className="text-xl font-semibold text-white">{section.heading}</h2>
              <p className="mt-3 leading-relaxed text-slate-300">{section.body}</p>
            </section>
          ))}
        </div>
        {site.contactEmail ? (
          <p className="mt-12 text-slate-300">
            Contact:{" "}
            <a href={`mailto:${site.contactEmail}`} className="text-brand-sky underline-offset-4 hover:underline">
              {site.contactEmail}
            </a>
          </p>
        ) : null}
      </main>
      <Footer />
    </>
  );
}
