"use client";

import { m } from "framer-motion";
import { capabilities } from "@/content";
import { Icon } from "./Icons";
import { SectionHeading } from "./SectionHeading";

function trackPointer(e: React.PointerEvent<HTMLElement>) {
  const rect = e.currentTarget.getBoundingClientRect();
  e.currentTarget.style.setProperty("--mx", `${e.clientX - rect.left}px`);
  e.currentTarget.style.setProperty("--my", `${e.clientY - rect.top}px`);
}

export function Capabilities() {
  return (
    <section id="capabilities" aria-labelledby="capabilities-title" className="relative py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          id="capabilities-title"
          eyebrow={capabilities.eyebrow}
          title={capabilities.title}
          subtitle={capabilities.subtitle}
        />

        <ul className="mt-16 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
          {capabilities.items.map((item, i) => (
            <m.li
              key={item.title}
              initial={{ opacity: 0, y: 28 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "0px 0px -10% 0px" }}
              transition={{ duration: 0.55, delay: (i % 3) * 0.08, ease: [0.22, 1, 0.36, 1] }}
              whileHover={{ y: -6 }}
              onPointerMove={trackPointer}
              className="group relative overflow-hidden rounded-2xl border border-white/8 bg-ink-900/60 p-7 transition-colors duration-300 hover:border-brand-purple/40"
            >
              <div aria-hidden="true" className="spotlight pointer-events-none absolute inset-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" />
              <div className="relative">
                <span className="inline-flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-brand-purple/25 to-brand-cyan/15 text-brand-sky ring-1 ring-white/10 transition-all duration-300 group-hover:scale-110 group-hover:rotate-[-4deg] group-hover:text-white group-hover:shadow-[0_0_28px_rgba(139,92,246,0.6)]">
                  <Icon name={item.icon} className="h-6 w-6" />
                </span>
                <h3 className="mt-6 text-lg font-semibold text-white">{item.title}</h3>
                <p className="mt-2.5 text-[15px] leading-relaxed text-slate-400">{item.body}</p>
              </div>
              <div
                aria-hidden="true"
                className="absolute inset-x-6 bottom-0 h-px origin-left scale-x-0 bg-accent transition-transform duration-500 group-hover:scale-x-100"
              />
            </m.li>
          ))}
        </ul>
      </div>
    </section>
  );
}
