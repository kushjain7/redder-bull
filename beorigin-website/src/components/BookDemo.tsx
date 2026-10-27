"use client";

import { useState } from "react";
import { AnimatePresence, m } from "framer-motion";
import { bookDemo, site } from "@/content";
import { submitDemoRequest, type DemoRequest } from "@/lib/submitDemoRequest";
import { Icon } from "./Icons";
import { Reveal } from "./Reveal";
import { SectionHeading } from "./SectionHeading";

type Status = "idle" | "submitting" | "success" | "error";

const inputClass =
  "mt-2 block w-full rounded-xl border border-white/10 bg-ink-950/60 px-4 py-3 text-[15px] text-white placeholder:text-slate-500 transition focus:border-brand-purple/70 focus:ring-2 focus:ring-brand-purple/30 focus:outline-none";
const labelClass = "block text-sm font-medium text-slate-200";

export function BookDemo() {
  const [status, setStatus] = useState<Status>("idle");
  const [error, setError] = useState("");
  const { fields } = bookDemo;

  const onSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const form = e.currentTarget;
    if (!form.reportValidity()) return;
    const data = Object.fromEntries(new FormData(form)) as unknown as DemoRequest;
    setStatus("submitting");
    setError("");
    try {
      await submitDemoRequest(data);
      form.reset();
      setStatus("success");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong. Please try again.");
      setStatus("error");
    }
  };

  return (
    <section id="book-demo" aria-labelledby="book-demo-title" className="relative overflow-hidden py-24 sm:py-32">
      <div
        aria-hidden="true"
        className="pointer-events-none absolute bottom-0 left-1/2 h-[420px] w-[760px] -translate-x-1/2 rounded-full bg-brand-purple/15 blur-[130px]"
      />
      <div className="relative mx-auto max-w-6xl px-5 sm:px-8">
        <SectionHeading
          id="book-demo-title"
          eyebrow={bookDemo.eyebrow}
          title={bookDemo.title}
          subtitle={bookDemo.subtitle}
        />

        <Reveal className="mx-auto mt-14 max-w-2xl">
          <div className="gradient-border rounded-3xl bg-ink-900/80 p-6 backdrop-blur-md sm:p-10">
            <AnimatePresence mode="wait" initial={false}>
              {status === "success" ? (
                <m.div
                  key="success"
                  initial={{ opacity: 0, scale: 0.96 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0 }}
                  className="flex min-h-[440px] flex-col items-center justify-center py-10 text-center"
                  role="status"
                >
                  <span className="flex h-16 w-16 items-center justify-center rounded-full bg-accent text-white shadow-[0_0_40px_rgba(139,92,246,0.7)]">
                    <Icon name="check" className="h-8 w-8" />
                  </span>
                  <h3 className="mt-6 text-2xl font-semibold text-white">{bookDemo.success.title}</h3>
                  <p className="mt-3 max-w-md text-slate-400">{bookDemo.success.body}</p>
                  <p className="mt-4 text-sm text-slate-400">
                    Email didn&apos;t open? Write to{" "}
                    <a className="text-brand-sky underline-offset-4 hover:underline" href={`mailto:${site.contactEmail}`}>
                      {site.contactEmail}
                    </a>
                  </p>
                  <button
                    type="button"
                    onClick={() => setStatus("idle")}
                    className="mt-8 rounded-full border border-white/15 px-5 py-2.5 text-sm text-slate-200 hover:bg-white/5"
                  >
                    {bookDemo.success.reset}
                  </button>
                </m.div>
              ) : (
                <m.form
                  key="form"
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  exit={{ opacity: 0 }}
                  onSubmit={onSubmit}
                  className="grid gap-5 sm:grid-cols-2"
                  aria-describedby={error ? "form-error" : undefined}
                >
                  <div>
                    <label htmlFor="name" className={labelClass}>
                      {fields.name.label}
                    </label>
                    <input
                      id="name"
                      name="name"
                      type="text"
                      required
                      autoComplete="name"
                      placeholder={fields.name.placeholder}
                      className={inputClass}
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className={labelClass}>
                      {fields.email.label}
                    </label>
                    <input
                      id="email"
                      name="email"
                      type="email"
                      required
                      autoComplete="email"
                      placeholder={fields.email.placeholder}
                      className={inputClass}
                    />
                  </div>
                  <div>
                    <label htmlFor="organisation" className={labelClass}>
                      {fields.organisation.label}
                    </label>
                    <input
                      id="organisation"
                      name="organisation"
                      type="text"
                      required
                      autoComplete="organization"
                      placeholder={fields.organisation.placeholder}
                      className={inputClass}
                    />
                  </div>
                  <div>
                    <label htmlFor="useCase" className={labelClass}>
                      {fields.useCase.label}
                    </label>
                    <div className="relative">
                      <select
                        id="useCase"
                        name="useCase"
                        required
                        defaultValue=""
                        className={`${inputClass} appearance-none pr-10`}
                      >
                        <option value="" disabled>
                          {fields.useCase.placeholder}
                        </option>
                        {bookDemo.useCaseOptions.map((option) => (
                          <option key={option} value={option} className="bg-ink-900">
                            {option}
                          </option>
                        ))}
                      </select>
                      <Icon
                        name="chevron"
                        className="pointer-events-none absolute top-1/2 right-4 mt-1 h-4 w-4 -translate-y-1/2 text-slate-400"
                      />
                    </div>
                  </div>
                  <div className="sm:col-span-2">
                    <label htmlFor="message" className={labelClass}>
                      {fields.message.label}
                    </label>
                    <textarea
                      id="message"
                      name="message"
                      rows={4}
                      placeholder={fields.message.placeholder}
                      className={`${inputClass} resize-y`}
                    />
                  </div>

                  {error ? (
                    <p id="form-error" role="alert" className="text-sm text-rose-300 sm:col-span-2">
                      {error}
                    </p>
                  ) : null}

                  <div className="sm:col-span-2">
                    <button
                      type="submit"
                      disabled={status === "submitting"}
                      className="group inline-flex w-full items-center justify-center gap-2 rounded-full bg-accent px-7 py-3.5 font-medium text-white shadow-[0_0_40px_-8px_rgba(139,92,246,0.9)] transition hover:brightness-110 disabled:opacity-60"
                    >
                      {status === "submitting" ? bookDemo.submittingLabel : bookDemo.submitLabel}
                      <Icon name="arrow" className="h-4 w-4 transition-transform group-hover:translate-x-0.5" />
                    </button>
                  </div>
                </m.form>
              )}
            </AnimatePresence>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
