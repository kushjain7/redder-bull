import type { Metadata } from "next";
import { LegalPage } from "@/components/LegalPage";
import { legal } from "@/content";

export const metadata: Metadata = {
  title: legal.privacy.title,
  alternates: { canonical: "/privacy/" },
};

export default function PrivacyPage() {
  return <LegalPage {...legal.privacy} />;
}
