/**
 * ─────────────────────────────────────────────────────────────────────────────
 *  BeOrigin website copy — EDIT ALL TEXT HERE.
 *  Every section on the site reads from this file. Change a string, save, and
 *  the dev server hot-reloads. No component code needs to change.
 * ─────────────────────────────────────────────────────────────────────────────
 */

export const site = {
  name: "BeOrigin",
  tagline: "Believe, Begin, Become",
  // TODO: replace with your real address. Used by the demo form (mailto:) and the footer.
  contactEmail: "your-email@example.com",
  // TODO: replace with your production domain once deployed (used for SEO + Open Graph URLs).
  url: "https://www.example.com",
  title: "BeOrigin | AI knowledge transfer in your expert's own voice",
  description:
    "BeOrigin captures a subject matter expert's voice and thinking, turns SOPs and documents into narrated interactive modules, and gives every learner a voice tutor they can cross-question live.",
  keywords: [
    "knowledge transfer",
    "AI training platform",
    "voice cloning",
    "SOP training",
    "expert knowledge capture",
    "AI voice tutor",
    "maritime training",
    "enterprise training",
    "AI for schools",
  ],
};

export const nav = {
  links: [
    { label: "How it works", href: "#how-it-works" },
    { label: "Capabilities", href: "#capabilities" },
    { label: "Product", href: "#product" },
    { label: "Use cases", href: "#use-cases" },
    { label: "Team", href: "#team" },
  ],
  cta: { label: "Book a Demo", href: "#book-demo" },
};

export const hero = {
  eyebrow: "AI knowledge transfer platform",
  tagline: "Believe, Begin, Become",
  valueProp: "Capture expert knowledge once. Transfer it to everyone, in their own voice.",
  supporting:
    "BeOrigin clones your expert's voice and reasoning, turns SOPs into narrated interactive modules, and lets every learner cross-question them live.",
  primaryCta: { label: "Book a Demo", href: "#book-demo" },
  secondaryCta: { label: "See how it works", href: "#how-it-works" },
  orbLabel: "BeOrigin is speaking...",
};

export const howItWorks = {
  eyebrow: "How it works",
  title: "From one expert to every learner",
  subtitle:
    "Four steps turn scattered documents and one expert's experience into knowledge transfer that scales.",
  steps: [
    {
      title: "Upload SOPs & docs",
      body: "Drop in manuals, SOPs, slide decks and recordings. BeOrigin reads and structures everything your expert already knows.",
      tags: ["Document Parsing", "Speech-to-Text"],
    },
    {
      title: "AI captures the expert's voice & thinking",
      body: "A short session with your expert captures how they sound, how they explain, and how they reason through edge cases.",
      tags: ["Voice Cloning", "LLM Reasoning"],
    },
    {
      title: "Generates narrated, interactive modules",
      body: "Documents become bite-sized modules narrated in the expert's voice, with visuals, checkpoints and scenarios.",
      tags: ["LLM Reasoning", "Text-to-Speech", "Video Generation"],
    },
    {
      title: "Voice tutor teaches and cross-questions learners",
      body: "Learners talk to the expert's voice tutor, ask follow-ups live, and get questioned back until the knowledge sticks.",
      tags: ["Speech-to-Text", "LLM Reasoning", "Text-to-Speech"],
    },
  ],
};

/** `icon` must be one of the keys in src/components/Icons.tsx */
export const capabilities = {
  eyebrow: "Capabilities",
  title: "Everything it takes to transfer expertise",
  subtitle: "One platform, from capturing knowledge to proving it landed.",
  items: [
    {
      icon: "voice",
      title: "Expert Voice Cloning",
      body: "A faithful clone of your expert's voice and persona, so every lesson sounds like it came from them.",
    },
    {
      icon: "tutor",
      title: "Live Voice Tutor",
      body: "Learners speak naturally and interrupt with questions. The tutor answers in the expert's style, in real time.",
    },
    {
      icon: "course",
      title: "Doc-to-Course Engine",
      body: "SOPs, manuals and PDFs become structured, narrated modules in minutes, not months.",
    },
    {
      icon: "globe",
      title: "Multilingual Narration",
      body: "Deliver the same expert knowledge in the languages your teams and students actually speak.",
    },
    {
      icon: "assessment",
      title: "Voice Assessments",
      body: "Spoken check-ins that test understanding, not memorisation, and score every answer.",
    },
    {
      icon: "dashboard",
      title: "Analytics Dashboard",
      body: "See who has learned what, where they struggle, and how ready each team is, all in one view.",
    },
  ],
};

export const productDemo = {
  eyebrow: "Product in action",
  title: "Hear the expert. Question the expert.",
  subtitle:
    "Watch a module come to life, then see how a learner cross-questions the voice tutor mid-lesson.",
  video: {
    // Replace public/demo.mp4 and public/demo-poster.jpg with your own recording.
    src: "/demo.mp4",
    poster: "/demo-poster.jpg",
    label: "Watch the 60-second walkthrough",
  },
  tutor: {
    moduleName: "Enclosed Space Entry · SOP 4.2",
    expertName: "Capt. Mehra's voice",
    statusLabels: {
      idle: "Ready",
      listening: "Listening...",
      thinking: "Thinking...",
      speaking: "Speaking...",
      paused: "Paused",
      done: "Module checkpoint complete",
    },
    // A scripted conversation. `from` is "tutor" or "learner".
    script: [
      {
        from: "tutor",
        text: "Before anyone steps into a ballast tank, what is the very first thing we confirm?",
      },
      { from: "learner", text: "That the oxygen level is safe?" },
      {
        from: "tutor",
        text: "Close. First the entry permit is signed. Then we test the atmosphere for oxygen, flammable and toxic gases.",
      },
      { from: "learner", text: "Why do we take readings at different heights?" },
      {
        from: "tutor",
        text: "Because gases layer. H₂S is heavier than air and pools low. A single reading at the hatch can lie to you.",
      },
      {
        from: "tutor",
        text: "Quick check: who must stay at the entrance the whole time?",
      },
      { from: "learner", text: "The standby person, in contact with the entrant." },
      {
        from: "tutor",
        text: "Exactly right. That answer is logged to your assessment. ✓",
      },
    ],
  },
  controls: { play: "Play", pause: "Pause", stop: "Stop" },
  disclaimer: "Scripted preview. No live AI calls on this page.",
};

export const proof = {
  eyebrow: "Early proof",
  stats: [
    { value: 15, suffix: "+", label: "domain experts onboarded" },
    { value: 80, suffix: "%", label: "of pilot students improved within a month" },
    { value: 3, suffix: "", unit: "sectors", label: "Pilots across Maritime, Enterprise & K-12" },
  ],
  line: "Every learner minute runs speech recognition, reasoning and speech synthesis.",
};

export const useCases = {
  eyebrow: "Use cases",
  title: "Built for knowledge that can't be lost",
  items: [
    {
      icon: "building",
      title: "Enterprise Training",
      body: "Capture what your best people know before they move on. Onboard faster with SOP training that answers back.",
      points: ["SOP & compliance onboarding", "Retiring-expert knowledge capture", "Readiness reporting per team"],
    },
    {
      icon: "ship",
      title: "Maritime",
      body: "Safety-critical procedures taught in a senior officer's voice, available on board, on shore, and between contracts.",
      points: ["Safety & enclosed-space SOPs", "Voice drills before sign-off", "Fleet-wide competency tracking"],
    },
    {
      icon: "school",
      title: "Schools & Education",
      body: "An AI tutor in the teacher's own voice. Multilingual, grounded in the curriculum, available after the bell.",
      points: ["Teacher-voice AI tutor", "Curriculum-grounded answers", "Multilingual for every classroom"],
    },
  ],
};

export const team = {
  eyebrow: "Team",
  title: "The people behind BeOrigin",
  members: [
    { name: "Kush Jain", role: "Co-founder & CEO", school: "IIT Delhi", initials: "KJ", linkedin: "" },
    { name: "Om Patil", role: "Co-founder & CTO", school: "IIT Delhi", initials: "OP", linkedin: "" },
  ],
};

export const bookDemo = {
  eyebrow: "Book a Demo",
  title: "See your expert's knowledge transfer itself",
  subtitle:
    "Tell us a little about your team and the knowledge you want to transfer. We'll set up a live walkthrough with your own SOPs.",
  fields: {
    name: { label: "Name", placeholder: "Your full name" },
    email: { label: "Work Email", placeholder: "you@company.com" },
    organisation: { label: "Organisation", placeholder: "Company, fleet or school" },
    useCase: { label: "Use Case", placeholder: "Select a use case" },
    message: { label: "Message", placeholder: "What knowledge do you want to transfer?" },
  },
  useCaseOptions: ["Enterprise Training", "Maritime", "Schools & Education", "Other"],
  submitLabel: "Book a Demo",
  submittingLabel: "Opening your email app...",
  success: {
    title: "Thanks, you're on the list.",
    body: "Your email app should have opened with your request. Hit send and we'll be in touch within one business day.",
    reset: "Send another request",
  },
  emailSubject: "BeOrigin demo request",
};

export const footer = {
  blurb: "AI knowledge transfer in your expert's own voice.",
  links: [
    { label: "Privacy", href: "/privacy/" },
    { label: "Terms", href: "/terms/" },
  ],
  copyright: "© 2026 BeOrigin. All rights reserved.",
};

export const legal = {
  privacy: {
    title: "Privacy Policy",
    updated: "Last updated: October 2026",
    sections: [
      {
        heading: "Placeholder",
        body: "This is a placeholder privacy policy. Replace it with your final policy before launch.",
      },
      {
        heading: "Information we collect",
        body: "This website does not use cookies or analytics. When you request a demo, the details you enter are sent through your own email app to our team.",
      },
      {
        heading: "How we use it",
        body: "We use demo request details only to respond to you and schedule a walkthrough.",
      },
      {
        heading: "Contact",
        body: "Questions about privacy? Email us at the address in the footer.",
      },
    ],
  },
  terms: {
    title: "Terms of Use",
    updated: "Last updated: October 2026",
    sections: [
      {
        heading: "Placeholder",
        body: "These are placeholder terms. Replace them with your final terms of use before launch.",
      },
      {
        heading: "Use of this site",
        body: "Content on this website is provided for general information about BeOrigin and its products.",
      },
      {
        heading: "Intellectual property",
        body: "The BeOrigin name, logo and site content belong to BeOrigin unless stated otherwise.",
      },
      {
        heading: "Contact",
        body: "Questions about these terms? Email us at the address in the footer.",
      },
    ],
  },
};
