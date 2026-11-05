import { useCases } from "@/content";
import { Icon } from "./Icons";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export function UseCases() {
  return (
    <section id="use-cases" aria-labelledby="use-cases-title" className="relative py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading id="use-cases-title" eyebrow={useCases.eyebrow} title={useCases.title} />
        <ul className="mt-16 grid gap-6 lg:grid-cols-3">
          {useCases.items.map((item, i) => (
            <Reveal key={item.title} as="li" delay={i * 0.1} className="h-full">
              <article className="group gradient-border flex h-full flex-col rounded-3xl bg-gradient-to-b from-ink-800/90 to-ink-900/60 p-8 transition-transform duration-300 hover:-translate-y-1.5">
                <span className="inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-accent text-white shadow-[0_0_30px_-4px_rgba(139,92,246,0.7)]">
                  <Icon name={item.icon} className="h-6 w-6" />
                </span>
                <h3 className="mt-6 text-2xl font-semibold text-white">{item.title}</h3>
                <p className="mt-3 text-slate-400">{item.body}</p>
                <ul className="mt-6 space-y-2.5 border-t border-white/5 pt-6">
                  {item.points.map((point) => (
                    <li key={point} className="flex items-start gap-2.5 text-sm text-slate-300">
                      <Icon name="check" className="mt-0.5 h-4 w-4 shrink-0 text-brand-cyan" />
                      {point}
                    </li>
                  ))}
                </ul>
              </article>
            </Reveal>
          ))}
        </ul>
      </div>
    </section>
  );
}
