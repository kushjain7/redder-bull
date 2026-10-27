"use client";

import { useRef } from "react";
import { m, useScroll, useSpring } from "framer-motion";
import { howItWorks } from "@/content";
import { SectionHeading } from "./SectionHeading";

export function HowItWorks() {
  const listRef = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: listRef, offset: ["start 80%", "end 55%"] });
  const progress = useSpring(scrollYProgress, { stiffness: 120, damping: 30, restDelta: 0.001 });

  return (
    <section id="how-it-works" aria-labelledby="how-title" className="relative overflow-x-clip py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          id="how-title"
          eyebrow={howItWorks.eyebrow}
          title={howItWorks.title}
          subtitle={howItWorks.subtitle}
        />

        <div ref={listRef} className="relative mt-16 md:mt-20">
          {/* Rail + scroll-driven progress fill */}
          <div aria-hidden="true" className="absolute top-2 bottom-2 left-5 w-px bg-white/10 md:left-1/2 md:-translate-x-1/2" />
          <m.div
            aria-hidden="true"
            style={{ scaleY: progress }}
            className="absolute top-2 bottom-2 left-5 w-px origin-top bg-gradient-to-b from-brand-purple to-brand-cyan shadow-[0_0_12px_rgba(34,211,238,0.6)] md:left-1/2 md:-translate-x-1/2"
          />

          <ol className="relative space-y-10 md:space-y-16">
          {howItWorks.steps.map((step, i) => {
            const right = i % 2 === 1;
            return (
              <li key={step.title} className="relative grid pl-16 md:grid-cols-2 md:gap-16 md:pl-0">
                <m.span
                  aria-hidden="true"
                  initial={{ scale: 0.4, opacity: 0 }}
                  whileInView={{ scale: 1, opacity: 1 }}
                  viewport={{ once: true, margin: "0px 0px -20% 0px" }}
                  transition={{ type: "spring", stiffness: 260, damping: 20 }}
                  className="absolute top-1 left-0 flex h-10 w-10 items-center justify-center rounded-full bg-ink-900 font-mono text-sm font-semibold text-white ring-1 ring-white/15 shadow-[0_0_24px_rgba(139,92,246,0.55)] md:left-1/2 md:-translate-x-1/2"
                >
                  <span className="absolute inset-0 rounded-full bg-accent opacity-25" />
                  <span className="relative">{String(i + 1).padStart(2, "0")}</span>
                </m.span>

                <m.div
                  initial={{ opacity: 0, x: right ? 32 : -32 }}
                  whileInView={{ opacity: 1, x: 0 }}
                  viewport={{ once: true, margin: "0px 0px -15% 0px" }}
                  transition={{ duration: 0.7, ease: [0.22, 1, 0.36, 1] }}
                  className={`rounded-2xl border border-white/8 bg-white/[0.025] p-6 backdrop-blur-sm sm:p-7 ${
                    right ? "md:col-start-2" : "md:col-start-1 md:text-right"
                  }`}
                >
                  <p className="font-mono text-xs uppercase tracking-[0.2em] text-brand-violet">Step {i + 1}</p>
                  <h3 className="mt-2 text-xl font-semibold text-white sm:text-2xl">{step.title}</h3>
                  <p className="mt-3 text-slate-400">{step.body}</p>
                  <ul
                    aria-label="AI behind this step"
                    className={`mt-5 flex flex-wrap gap-2 ${right ? "" : "md:justify-end"}`}
                  >
                    {step.tags.map((tag, t) => (
                      <m.li
                        key={tag}
                        initial={{ opacity: 0, y: 8 }}
                        whileInView={{ opacity: 1, y: 0 }}
                        viewport={{ once: true }}
                        transition={{ duration: 0.4, delay: 0.3 + t * 0.08 }}
                        className="rounded-full border border-brand-cyan/25 bg-brand-cyan/[0.07] px-3 py-1 font-mono text-[11px] tracking-wide text-brand-sky"
                      >
                        {tag}
                      </m.li>
                    ))}
                  </ul>
                </m.div>
              </li>
            );
          })}
          </ol>
        </div>
      </div>
    </section>
  );
}
