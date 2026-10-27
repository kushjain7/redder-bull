"use client";

import { useEffect, useRef } from "react";
import { animate, m, useInView, useReducedMotion } from "framer-motion";
import { proof } from "@/content";
import { Reveal } from "./Reveal";

function Counter({ value, suffix }: { value: number; suffix: string }) {
  const ref = useRef<HTMLSpanElement>(null);
  // Same trigger as <Reveal>, so the reset to 0 happens while the stat is still faded out.
  const inView = useInView(ref, { once: true, margin: "0px 0px -10% 0px" });
  const reduce = useReducedMotion();

  useEffect(() => {
    const node = ref.current;
    if (!node || !inView) return;
    if (reduce) {
      node.textContent = `${value}${suffix}`;
      return;
    }
    // Writes straight to the DOM node so the count-up doesn't re-render React every frame.
    const controls = animate(0, value, {
      duration: 1.6,
      ease: [0.16, 1, 0.3, 1],
      onUpdate: (v) => {
        node.textContent = `${Math.round(v)}${suffix}`;
      },
    });
    return () => controls.stop();
  }, [inView, reduce, value, suffix]);

  // Server-rendered with the final value so crawlers and no-JS visitors see real numbers.
  return (
    <span ref={ref} className="tabular-nums">
      {value}
      {suffix}
    </span>
  );
}

export function Proof() {
  return (
    <section aria-label="Results" className="relative py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <div className="relative overflow-hidden rounded-3xl border border-white/10 bg-ink-900/70 px-6 py-12 sm:px-12">
          <div aria-hidden="true" className="absolute inset-x-0 top-0 h-px bg-accent opacity-70" />
          <div
            aria-hidden="true"
            className="pointer-events-none absolute -top-24 right-0 h-64 w-64 rounded-full bg-brand-purple/20 blur-[90px]"
          />
          <p className="text-center font-mono text-xs uppercase tracking-[0.25em] text-brand-cyan">{proof.eyebrow}</p>
          <dl className="mt-10 grid gap-10 text-center sm:grid-cols-3 sm:gap-6">
            {proof.stats.map((stat, i) => (
              <Reveal key={stat.label} delay={i * 0.1} className="flex flex-col-reverse items-center">
                <dt className="mt-3 max-w-[16rem] text-sm text-slate-400 sm:text-base">{stat.label}</dt>
                <dd className="text-5xl font-semibold tracking-tight text-white sm:text-6xl">
                  <span className="text-gradient">
                    <Counter value={stat.value} suffix={stat.suffix} />
                  </span>
                  {"unit" in stat && stat.unit ? (
                    <span className="ml-2 text-2xl font-medium text-slate-300 sm:text-3xl">{stat.unit}</span>
                  ) : null}
                </dd>
              </Reveal>
            ))}
          </dl>
          <m.p
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8, delay: 0.3 }}
            className="mx-auto mt-12 max-w-2xl border-t border-white/5 pt-8 text-center text-base text-slate-300 sm:text-lg"
          >
            {proof.line}
          </m.p>
        </div>
      </div>
    </section>
  );
}
