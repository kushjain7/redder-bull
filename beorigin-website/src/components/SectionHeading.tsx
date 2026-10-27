import { Reveal } from "./Reveal";

type SectionHeadingProps = {
  eyebrow: string;
  title: string;
  subtitle?: string;
  id?: string;
};

export function SectionHeading({ eyebrow, title, subtitle, id }: SectionHeadingProps) {
  return (
    <Reveal className="mx-auto max-w-2xl text-center">
      <p className="font-mono text-xs font-medium uppercase tracking-[0.25em] text-brand-cyan">
        {eyebrow}
      </p>
      <h2 id={id} className="mt-4 text-3xl font-semibold tracking-tight text-white sm:text-4xl md:text-5xl">
        {title}
      </h2>
      {subtitle ? <p className="mt-5 text-base text-slate-400 sm:text-lg">{subtitle}</p> : null}
    </Reveal>
  );
}
