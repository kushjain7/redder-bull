import { site } from "@/content";

export function Logo() {
  return (
    <span className="flex items-center gap-2.5">
      <span
        aria-hidden="true"
        className="relative h-7 w-7 rounded-full bg-accent shadow-[0_0_18px_rgba(139,92,246,0.7)]"
      >
        <span className="absolute inset-[5px] rounded-full bg-ink-950/80" />
        <span className="absolute inset-[9px] rounded-full bg-accent" />
      </span>
      <span className="text-lg font-semibold tracking-tight text-white">{site.name}</span>
    </span>
  );
}
