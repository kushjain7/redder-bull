"use client";

import { useEffect, useRef } from "react";

type OrbProps = {
  /** When true the orb pulses with a speech-like rhythm; otherwise it breathes gently. */
  speaking?: boolean;
  className?: string;
};

// Layered blobs: each has its own wobble harmonics so the surface feels organic.
const LAYERS = [
  { scale: 1.0, alpha: 0.55, harmonics: [[3, 0.9, 0.0, 0.5], [5, -1.3, 1.7, 0.3], [7, 1.9, 0.6, 0.2]] },
  { scale: 0.86, alpha: 0.5, harmonics: [[2, -0.7, 2.1, 0.55], [4, 1.5, 0.4, 0.3], [6, -2.2, 3.0, 0.15]] },
  { scale: 0.7, alpha: 0.45, harmonics: [[3, 1.1, 4.2, 0.5], [5, -1.7, 2.6, 0.35], [8, 2.4, 1.1, 0.15]] },
] as const;

const POINTS = 72;
const TAU = Math.PI * 2;

/**
 * Canvas-rendered AI "voice" orb. Pure client-side drawing, no assets.
 * Pauses itself when off-screen or when the tab is hidden, and renders a single
 * still frame for users who prefer reduced motion.
 */
export function Orb({ speaking = true, className }: OrbProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const speakingRef = useRef(speaking);

  useEffect(() => {
    speakingRef.current = speaking;
  }, [speaking]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let width = 0;
    let height = 0;
    let raf = 0;
    let visible = true;
    let ready = false;
    let last = performance.now();
    let time = 0;
    let level = 0.1;
    let target = 0.1;
    let nextChange = 0;

    const resize = () => {
      const rect = canvas.getBoundingClientRect();
      const dpr = Math.min(window.devicePixelRatio || 1, 1.5);
      width = rect.width;
      height = rect.height;
      canvas.width = Math.max(1, Math.round(width * dpr));
      canvas.height = Math.max(1, Math.round(height * dpr));
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      if (reducedMotion || !raf) draw();
    };

    const updateLevel = (dt: number) => {
      if (speakingRef.current) {
        // Syllable-like bursts with occasional short pauses between "words".
        if (time > nextChange) {
          target = Math.random() < 0.14 ? 0.06 : 0.35 + Math.random() * 0.65;
          nextChange = time + 0.07 + Math.random() * 0.18;
        }
      } else {
        target = 0.08 + Math.sin(time * 1.4) * 0.04;
      }
      level += (target - level) * (1 - Math.exp(-dt * 14));
    };

    const draw = () => {
      const cx = width / 2;
      const cy = height / 2;
      const R = Math.min(width, height) * 0.28;
      ctx.clearRect(0, 0, width, height);
      if (R <= 0) return;

      // Ambient glow
      const glow = ctx.createRadialGradient(cx, cy, R * 0.2, cx, cy, R * 1.9);
      glow.addColorStop(0, `rgba(139, 92, 246, ${0.32 + level * 0.25})`);
      glow.addColorStop(0.45, `rgba(34, 211, 238, ${0.1 + level * 0.12})`);
      glow.addColorStop(1, "rgba(5, 6, 13, 0)");
      ctx.fillStyle = glow;
      ctx.fillRect(0, 0, width, height);

      // Ripples that radiate while speaking
      for (let i = 0; i < 3; i++) {
        const p = (time * 0.45 + i / 3) % 1;
        const alpha = (1 - p) * 0.3 * Math.min(1, level * 1.6);
        if (alpha < 0.01) continue;
        ctx.beginPath();
        ctx.arc(cx, cy, R * (1.05 + p * 0.75), 0, TAU);
        ctx.strokeStyle = `rgba(103, 232, 249, ${alpha})`;
        ctx.lineWidth = 1.25;
        ctx.stroke();
      }

      // Blob layers, additively blended
      const angle = time * 0.35;
      const gx = Math.cos(angle) * R;
      const gy = Math.sin(angle) * R;
      const wobble = 0.025 + level * 0.11;
      ctx.globalCompositeOperation = "lighter";
      for (const layer of LAYERS) {
        ctx.beginPath();
        for (let i = 0; i <= POINTS; i++) {
          const a = (i / POINTS) * TAU;
          let n = 0;
          for (const [freq, speed, phase, weight] of layer.harmonics) {
            n += Math.sin(a * freq + time * speed * (1 + level) + phase) * weight;
          }
          const r = R * layer.scale * (1 + wobble * n);
          const x = cx + Math.cos(a) * r;
          const y = cy + Math.sin(a) * r;
          if (i === 0) ctx.moveTo(x, y);
          else ctx.lineTo(x, y);
        }
        ctx.closePath();
        const fill = ctx.createLinearGradient(cx - gx, cy - gy, cx + gx, cy + gy);
        fill.addColorStop(0, `rgba(139, 92, 246, ${layer.alpha})`);
        fill.addColorStop(1, `rgba(34, 211, 238, ${layer.alpha})`);
        ctx.fillStyle = fill;
        ctx.fill();
      }
      ctx.globalCompositeOperation = "source-over";

      // Glassy core highlight
      const core = ctx.createRadialGradient(cx - R * 0.3, cy - R * 0.35, 0, cx, cy, R * 0.95);
      core.addColorStop(0, `rgba(255, 255, 255, ${0.35 + level * 0.2})`);
      core.addColorStop(0.35, "rgba(255, 255, 255, 0.06)");
      core.addColorStop(1, "rgba(255, 255, 255, 0)");
      ctx.fillStyle = core;
      ctx.beginPath();
      ctx.arc(cx, cy, R * 0.95, 0, TAU);
      ctx.fill();
    };

    const frame = (now: number) => {
      const dt = Math.min((now - last) / 1000, 0.05);
      last = now;
      time += dt;
      updateLevel(dt);
      draw();
      raf = requestAnimationFrame(frame);
    };

    const start = () => {
      if (reducedMotion || !ready || raf || !visible || document.hidden) return;
      last = performance.now();
      raf = requestAnimationFrame(frame);
    };
    const stop = () => {
      cancelAnimationFrame(raf);
      raf = 0;
    };

    const resizeObserver = new ResizeObserver(resize);
    resizeObserver.observe(canvas);
    const intersectionObserver = new IntersectionObserver(([entry]) => {
      visible = entry.isIntersecting;
      if (visible) start();
      else stop();
    });
    intersectionObserver.observe(canvas);
    const onVisibility = () => (document.hidden ? stop() : start());
    document.addEventListener("visibilitychange", onVisibility);

    // Paint a still frame now; start animating once the page has finished loading and the
    // main thread is idle, so the orb never competes with the first render.
    level = reducedMotion && speakingRef.current ? 0.5 : 0.1;
    resize();
    let idleId = 0;
    const hasIdle = typeof window.requestIdleCallback === "function";
    const begin = () => {
      const run = () => {
        ready = true;
        start();
      };
      if (hasIdle) idleId = window.requestIdleCallback(run, { timeout: 2000 });
      else idleId = window.setTimeout(run, 300);
    };
    if (!reducedMotion) {
      if (document.readyState === "complete") begin();
      else window.addEventListener("load", begin, { once: true });
    }

    return () => {
      window.removeEventListener("load", begin);
      if (hasIdle) window.cancelIdleCallback(idleId);
      else window.clearTimeout(idleId);
      stop();
      resizeObserver.disconnect();
      intersectionObserver.disconnect();
      document.removeEventListener("visibilitychange", onVisibility);
    };
  }, []);

  return <canvas ref={canvasRef} className={className} aria-hidden="true" />;
}
