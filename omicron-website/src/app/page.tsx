import { BookDemo } from "@/components/BookDemo";
import { Capabilities } from "@/components/Capabilities";
import { Footer } from "@/components/Footer";
import { Hero } from "@/components/Hero";
import { HowItWorks } from "@/components/HowItWorks";
import { Navbar } from "@/components/Navbar";
import { ProductDemo } from "@/components/ProductDemo";
import { Proof } from "@/components/Proof";
import { Team } from "@/components/Team";
import { UseCases } from "@/components/UseCases";

export default function HomePage() {
  return (
    <>
      <Navbar />
      <main id="main">
        <Hero />
        <HowItWorks />
        <Capabilities />
        <ProductDemo />
        <Proof />
        <UseCases />
        <Team />
        <BookDemo />
      </main>
      <Footer />
    </>
  );
}
