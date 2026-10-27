import type { Metadata } from "next";
import { LegalPage } from "@/components/LegalPage";
import { legal } from "@/content";

export const metadata: Metadata = {
  title: legal.terms.title,
  alternates: { canonical: "/terms/" },
};

export default function TermsPage() {
  return <LegalPage {...legal.terms} />;
}
