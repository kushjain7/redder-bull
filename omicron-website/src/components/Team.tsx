import { team } from "@/content";
import { Icon } from "./Icons";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

export function Team() {
  return (
    <section id="team" aria-labelledby="team-title" className="relative py-24 sm:py-32">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading id="team-title" eyebrow={team.eyebrow} title={team.title} />
        <ul className="mx-auto mt-16 grid max-w-3xl gap-6 sm:grid-cols-2">
          {team.members.map((member, i) => (
            <Reveal key={member.name} as="li" delay={i * 0.1}>
              <article className="group flex flex-col items-center rounded-3xl border border-white/8 bg-ink-900/60 p-8 text-center transition-colors hover:border-white/20">
                <span className="relative flex h-24 w-24 items-center justify-center rounded-full bg-accent p-[2px] shadow-[0_0_40px_-6px_rgba(139,92,246,0.7)] transition-transform duration-300 group-hover:scale-105">
                  <span className="flex h-full w-full items-center justify-center rounded-full bg-ink-900 text-2xl font-semibold text-white">
                    {member.initials}
                  </span>
                </span>
                <h3 className="mt-6 text-xl font-semibold text-white">{member.name}</h3>
                <p className="mt-1 text-slate-300">{member.role}</p>
                <p className="mt-3 rounded-full border border-white/10 px-3 py-1 font-mono text-xs uppercase tracking-wider text-slate-400">
                  {member.school}
                </p>
                {member.linkedin ? (
                  <a
                    href={member.linkedin}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="mt-4 text-slate-400 hover:text-white"
                    aria-label={`${member.name} on LinkedIn`}
                  >
                    <Icon name="linkedin" className="h-5 w-5" />
                  </a>
                ) : null}
              </article>
            </Reveal>
          ))}
        </ul>
      </div>
    </section>
  );
}
