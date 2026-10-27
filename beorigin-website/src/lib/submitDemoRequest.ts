import { bookDemo, site } from "@/content";

export type DemoRequest = {
  name: string;
  email: string;
  organisation: string;
  useCase: string;
  message: string;
};

/**
 * THE ONLY PLACE THE DEMO FORM SENDS DATA.
 *
 * Right now it opens the visitor's email app with a pre-filled message to
 * `site.contactEmail` (set in src/content.ts). To switch to a real form service
 * (Formspree, Web3Forms, AWS API Gateway + Lambda, HubSpot...), replace the body
 * of this function with a `fetch()` call and keep the same signature, e.g.:
 *
 *   const res = await fetch("https://formspree.io/f/your-id", {
 *     method: "POST",
 *     headers: { "Content-Type": "application/json", Accept: "application/json" },
 *     body: JSON.stringify(data),
 *   });
 *   if (!res.ok) throw new Error("Could not send your request. Please try again.");
 *
 * Throw an Error to show its message in the form; resolve to show the success state.
 */
export async function submitDemoRequest(data: DemoRequest): Promise<void> {
  const body = [
    `Name: ${data.name}`,
    `Work email: ${data.email}`,
    `Organisation: ${data.organisation}`,
    `Use case: ${data.useCase}`,
    "",
    data.message,
  ].join("\n");

  const href =
    `mailto:${site.contactEmail}` +
    `?subject=${encodeURIComponent(`${bookDemo.emailSubject}: ${data.organisation}`)}` +
    `&body=${encodeURIComponent(body)}`;

  window.location.href = href;
}
