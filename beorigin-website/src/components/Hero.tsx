"use client";

import { m } from "framer-motion";
import { hero } from "@/content";
import { Icon } from "./Icons";
import { Orb } from "./Orb";

const ease = [0.22, 1, 0.36, 1] as const;

export function Hero() {
  return (
    <section id="top" aria-labelledby="hero-title" className="relative overflow-hidden pt-28 pb-20 sm:pt-36 md:pb-28">
      <div aria-hidden="true" className="bg-grid pointer-events-none absolute inset-0" />
      <div
        aria-hidden="true"
        className="pointer-events-none absolute -top-40 left-1/2 h-[520px] w-[900px] -translate-x-1/2 rounded-full bg-brand-purple/20 blur-[120px]"
      />

      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-5 sm:px-8 lg:grid-cols-[1.1fr_1fr]">
        <div className="text-center lg:text-left">
          <m.p
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, ease }}
            className="inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/[0.03] px-3.5 py-1.5 font-mono text-xs uppercase tracking-[0.2em] text-slate-300"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-brand-cyan shadow-[0_0_8px_#22d3ee]" />
            {hero.eyebrow}
          </m.p>

          {/* Headline + value prop are not animated so they paint immediately (best LCP). */}
          <h1
            id="hero-title"
            className="mt-6 text-5xl font-semibold tracking-tight text-white sm:text-6xl lg:text-7xl"
          >
            <span className="text-gradient">{hero.tagline}</span>
          </h1>

          <p className="mx-auto mt-6 max-w-xl text-xl text-slate-200 sm:text-2xl lg:mx-0">{hero.valueProp}</p>
          <m.p
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.16, ease }}
            className="mx-auto mt-4 max-w-xl text-base text-slate-400 lg:mx-0"
          >
            {hero.supporting}
          </m.p>

          <m.div
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.7, delay: 0.24, ease }}
            className="mt-9 flex flex-col items-center gap-3 sm:flex-row sm:justify-center lg:justify-start"
          >
            <a
              href={hero.primaryCta.href}
              className="group inline-flex w-full items-center justify-center gap-2 rounded-full bg-accent px-7 py-3.5 font-medium text-white shadow-[0_0_40px_-8px_rgba(139,92,246,0.9)] transition hover:brightness-110 sm:w-auto"
            >
              {hero.primaryCta.label}
              <Icon name="arrow" className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
            </a>
            <a
              href={hero.secondaryCta.href}
              className="inline-flex w-full items-center justify-center gap-2 rounded-full border border-white/15 bg-white/[0.03] px-7 py-3.5 font-medium text-slate-200 transition hover:border-white/30 hover:bg-white/[0.06] sm:w-auto"
            >
              {hero.secondaryCta.label}
            </a>
          </m.div>
        </div>

        <m.div
          initial={{ opacity: 0, scale: 0.92 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1, delay: 0.1, ease }}
          className="relative mx-auto w-full max-w-[460px]"
        >
          <div className="relative aspect-square w-full">
            <Orb speaking className="absolute inset-0 h-full w-full" />
          </div>
          <div
            role="status"
            className="absolute bottom-6 left-1/2 flex -translate-x-1/2 items-center gap-2.5 whitespace-nowrap rounded-full border border-white/10 bg-ink-900/70 px-4 py-2 text-sm text-slate-300 backdrop-blur-md"
          >
            <SpeakingBars />
            {hero.orbLabel}
          </div>
        </m.div>
      </div>
    </section>
  );
}

export function SpeakingBars({ active = true }: { active?: boolean }) {
  return (
    <span aria-hidden="true" className="flex h-3.5 items-end gap-[3px]">
      {[0, 1, 2, 3].map((i) => (
        <m.span
          key={i}
          className="w-[3px] rounded-full bg-gradient-to-t from-brand-purple to-brand-cyan"
          initial={{ height: "30%" }}
          animate={active ? { height: ["30%", "100%", "45%", "85%", "30%"] } : { height: "30%" }}
          transition={
            active
              ? { duration: 1.1, repeat: Infinity, delay: i * 0.13, ease: "easeInOut" }
              : { duration: 0.3 }
          }
        />
      ))}
    </span>
  );
}
