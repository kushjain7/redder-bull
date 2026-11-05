import Link from "next/link";
import { footer, nav, site } from "@/content";
import { Icon } from "./Icons";
import { Logo } from "./Logo";

export function Footer() {
  return (
    <footer className="relative border-t border-white/5 bg-ink-950">
      <div className="mx-auto grid max-w-6xl gap-10 px-5 py-14 sm:px-8 md:grid-cols-[1.4fr_1fr_1fr]">
        <div>
          <Link href="/" aria-label={`${site.name} home`} className="inline-block">
            <Logo />
          </Link>
          <p className="mt-4 max-w-xs text-sm text-slate-400">{footer.blurb}</p>
          <p className="mt-2 text-sm font-medium text-gradient">{site.tagline}</p>
        </div>

        <nav aria-label="Footer">
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-slate-400">Explore</p>
          <ul className="mt-4 space-y-2.5">
            {nav.links.map((link) => (
              <li key={link.href}>
                <a href={`/${link.href}`} className="text-sm text-slate-400 hover:text-white">
                  {link.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>

        <div>
          <p className="font-mono text-xs uppercase tracking-[0.2em] text-slate-400">{site.contactEmail ? "Contact" : "Legal"}</p>
          {site.contactEmail ? (
            <a
              href={`mailto:${site.contactEmail}`}
              className="mt-4 inline-flex items-center gap-2 text-sm text-slate-300 hover:text-white"
            >
              <Icon name="mail" className="h-4 w-4" />
              {site.contactEmail}
            </a>
          ) : null}
          <ul className={`flex gap-5 ${site.contactEmail ? "mt-6" : "mt-4"}`}>
            {footer.links.map((link) => (
              <li key={link.href}>
                <Link href={link.href} className="text-sm text-slate-400 hover:text-white">
                  {link.label}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </div>
      <div className="border-t border-white/5">
        <p className="mx-auto max-w-6xl px-5 py-6 text-xs text-slate-400 sm:px-8">{footer.copyright}</p>
      </div>
    </footer>
  );
}
