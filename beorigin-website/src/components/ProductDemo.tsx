"use client";

import { useEffect, useRef, useState } from "react";
import { AnimatePresence, m } from "framer-motion";
import { productDemo } from "@/content";
import { Icon } from "./Icons";
import { Orb } from "./Orb";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";
import { SpeakingBars } from "./Hero";

type Mode = "listening" | "thinking" | "speaking";
type Segment = { message: number; kind: "pre" | "show"; mode: Mode; start: number; end: number };
type PlayState = "idle" | "playing" | "paused" | "done";

const TICK_MS = 80;
const script = productDemo.tutor.script;

/** Turns the script into a timeline: a "listening/thinking" gap, then the message being spoken/read. */
function buildTimeline() {
  const segments: Segment[] = [];
  let t = 400;
  script.forEach((line, i) => {
    const isTutor = line.from === "tutor";
    const pre = isTutor ? (script[i - 1]?.from === "tutor" ? 500 : 1100) : 1300;
    segments.push({ message: i, kind: "pre", mode: isTutor ? "thinking" : "listening", start: t, end: t + pre });
    t += pre;
    const show = isTutor ? Math.max(2200, line.text.length * 45) : 1200;
    segments.push({ message: i, kind: "show", mode: isTutor ? "speaking" : "listening", start: t, end: t + show });
    t += show;
  });
  return { segments, total: t + 600 };
}

const { segments, total } = buildTimeline();

function VideoPlayer() {
  const videoRef = useRef<HTMLVideoElement>(null);
  const [started, setStarted] = useState(false);
  const [failed, setFailed] = useState(false);
  const { video } = productDemo;

  const start = () => {
    setStarted(true);
    videoRef.current?.play().catch(() => setFailed(true));
  };

  return (
    <div className="relative overflow-hidden rounded-2xl border border-white/10 bg-ink-900 shadow-[0_30px_80px_-30px_rgba(139,92,246,0.5)]">
      <div className="relative aspect-video">
        <video
          ref={videoRef}
          className="absolute inset-0 h-full w-full object-cover"
          poster={video.poster}
          preload="none"
          playsInline
          controls={started && !failed}
          onError={() => setFailed(true)}
        >
          <source src={video.src} type="video/mp4" onError={() => setFailed(true)} />
        </video>

        {!started || failed ? (
          <button
            type="button"
            onClick={start}
            disabled={failed}
            className="group absolute inset-0 flex flex-col items-center justify-center bg-gradient-to-t from-ink-950/80 via-ink-950/20 to-transparent text-white"
            aria-label={failed ? "Demo video unavailable" : video.label}
          >
            {failed ? (
              <span className="rounded-full bg-ink-900/80 px-4 py-2 text-sm text-slate-300">
                Demo video coming soon
              </span>
            ) : (
              <>
                <span className="relative flex h-16 w-16 items-center justify-center rounded-full bg-accent shadow-[0_0_40px_rgba(139,92,246,0.8)] transition-transform duration-300 group-hover:scale-110">
                  <span className="absolute inset-0 animate-ping rounded-full bg-brand-purple/40" />
                  <Icon name="play" className="relative ml-1 h-6 w-6" />
                </span>
                <span className="absolute bottom-5 text-sm font-medium text-slate-200">{video.label}</span>
              </>
            )}
          </button>
        ) : null}
      </div>
    </div>
  );
}

function TutorMock() {
  const { tutor, controls, disclaimer } = productDemo;
  const [elapsed, setElapsed] = useState(0);
  const [state, setState] = useState<PlayState>("idle");
  const elapsedRef = useRef(0);

  // Auto-start once, the first time the mock scrolls into view (skipped for reduced motion).
  const autoStart = () => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    setState((s) => (s === "idle" ? "playing" : s));
  };

  useEffect(() => {
    if (state !== "playing") return;
    const id = window.setInterval(() => {
      const next = Math.min(elapsedRef.current + TICK_MS, total);
      elapsedRef.current = next;
      setElapsed(next);
      if (next >= total) setState("done");
    }, TICK_MS);
    return () => window.clearInterval(id);
  }, [state]);

  const seek = (ms: number) => {
    elapsedRef.current = ms;
    setElapsed(ms);
  };

  const current = segments.find((s) => elapsed >= s.start && elapsed < s.end);
  const visible = segments.filter((s) => s.kind === "show" && elapsed >= s.start).length;
  const pendingFrom = current?.kind === "pre" ? script[current.message].from : null;
  const speaking = state === "playing" && current?.mode === "speaking";

  const status =
    state === "done"
      ? tutor.statusLabels.done
      : state === "paused"
        ? tutor.statusLabels.paused
        : state === "idle" || !current
          ? tutor.statusLabels.idle
          : tutor.statusLabels[current.mode];

  const play = () => {
    if (state === "done") seek(0);
    setState("playing");
  };
  const pause = () => setState("paused");
  const stop = () => {
    setState("idle");
    seek(0);
  };

  return (
    <m.div
      onViewportEnter={autoStart}
      viewport={{ once: true, amount: 0.4 }}
      className="relative flex flex-col overflow-hidden rounded-2xl border border-white/10 bg-gradient-to-b from-ink-800/80 to-ink-950 shadow-[0_30px_80px_-30px_rgba(34,211,238,0.35)]"
    >
      <div className="flex items-center justify-between border-b border-white/5 px-5 py-3.5">
        <div className="min-w-0">
          <p className="truncate text-sm font-medium text-white">{tutor.moduleName}</p>
          <p className="truncate font-mono text-[11px] uppercase tracking-wider text-slate-400">{tutor.expertName}</p>
        </div>
        <span className="flex shrink-0 items-center gap-1.5 rounded-full bg-emerald-400/10 px-2.5 py-1 text-[11px] font-medium text-emerald-300">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Live tutor
        </span>
      </div>

      <div
        role="log"
        aria-live="off"
        aria-label="Tutor conversation"
        className="flex h-[340px] flex-col justify-end gap-3 overflow-hidden px-5 pt-6 pb-2 [mask-image:linear-gradient(to_bottom,transparent,#000_18%)]"
      >
        <AnimatePresence initial={false}>
          {script.slice(0, visible).map((line, i) => (
            <Bubble key={i} from={line.from} text={line.text} />
          ))}
          {pendingFrom && state !== "idle" ? <TypingBubble key={`typing-${visible}`} from={pendingFrom} /> : null}
        </AnimatePresence>
      </div>

      <div className="relative flex flex-col items-center border-t border-white/5 px-5 pt-2 pb-5">
        <div className="relative h-36 w-36">
          <Orb speaking={speaking} className="absolute inset-0 h-full w-full" />
        </div>
        <p className="-mt-2 flex h-5 items-center gap-2 text-sm text-slate-300" aria-live="polite">
          {speaking ? <SpeakingBars /> : null}
          {status}
        </p>

        <div className="mt-4 flex items-center gap-2" role="group" aria-label="Playback controls">
          <ControlButton label={controls.play} icon="play" onClick={play} disabled={state === "playing"} primary />
          <ControlButton label={controls.pause} icon="pause" onClick={pause} disabled={state !== "playing"} />
          <ControlButton label={controls.stop} icon="stop" onClick={stop} disabled={state === "idle"} />
        </div>
        <p className="mt-4 text-center text-[11px] text-slate-400">{disclaimer}</p>
      </div>
    </m.div>
  );
}

function Bubble({ from, text }: { from: string; text: string }) {
  const tutor = from === "tutor";
  return (
    <m.div
      initial={{ opacity: 0, y: 14, scale: 0.97 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.35, ease: [0.22, 1, 0.36, 1] }}
      className={`flex shrink-0 ${tutor ? "justify-start" : "justify-end"}`}
    >
      <p
        className={`max-w-[85%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
          tutor
            ? "rounded-bl-md border border-brand-purple/25 bg-brand-purple/10 text-slate-100"
            : "rounded-br-md bg-white/[0.07] text-slate-200"
        }`}
      >
        <span className="sr-only">{tutor ? "Tutor: " : "Learner: "}</span>
        {text}
      </p>
    </m.div>
  );
}

function TypingBubble({ from }: { from: string }) {
  const tutor = from === "tutor";
  return (
    <m.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, transition: { duration: 0.1 } }}
      className={`flex shrink-0 ${tutor ? "justify-start" : "justify-end"}`}
      aria-hidden="true"
    >
      <span
        className={`flex gap-1 rounded-2xl px-4 py-3 ${
          tutor ? "rounded-bl-md bg-brand-purple/10" : "rounded-br-md bg-white/[0.07]"
        }`}
      >
        {[0, 1, 2].map((d) => (
          <span key={d} className={`typing-dot h-1.5 w-1.5 rounded-full ${tutor ? "bg-brand-violet" : "bg-slate-300"}`} />
        ))}
      </span>
    </m.div>
  );
}

function ControlButton({
  label,
  icon,
  onClick,
  disabled,
  primary,
}: {
  label: string;
  icon: string;
  onClick: () => void;
  disabled?: boolean;
  primary?: boolean;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      title={label}
      className={`inline-flex h-11 w-11 items-center justify-center rounded-full transition disabled:cursor-not-allowed disabled:opacity-35 ${
        primary
          ? "bg-accent text-white shadow-[0_0_24px_-4px_rgba(139,92,246,0.8)] enabled:hover:brightness-110"
          : "border border-white/15 bg-white/[0.04] text-slate-200 enabled:hover:bg-white/10"
      }`}
    >
      <Icon name={icon} className={`h-4 w-4 ${icon === "play" ? "ml-0.5" : ""}`} />
    </button>
  );
}

export function ProductDemo() {
  return (
    <section id="product" aria-labelledby="product-title" className="relative overflow-hidden py-24 sm:py-32">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute top-1/3 left-1/2 h-[500px] w-[800px] -translate-x-1/2 rounded-full bg-brand-cyan/10 blur-[140px]"
      />
      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          id="product-title"
          eyebrow={productDemo.eyebrow}
          title={productDemo.title}
          subtitle={productDemo.subtitle}
        />
        <div className="mt-16 grid items-center gap-8 lg:grid-cols-[1.35fr_1fr]">
          <Reveal>
            <VideoPlayer />
          </Reveal>
          <Reveal delay={0.12}>
            <TutorMock />
          </Reveal>
        </div>
      </div>
    </section>
  );
}
