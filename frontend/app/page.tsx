import HeroSection from "@/components/sections/hero-section";
import CrmPreviewSection from "@/components/sections/crm-preview-section";
import LogoWallSection from "@/components/sections/logo-wall-section";
import TestimonialSection from "@/components/sections/testimonial-section";
import PowerfulPlatformSection from "@/components/sections/powerful-platform-section";
import AutomateEverythingSection from "@/components/sections/automate-everything-section";
import DeployAiSection from "@/components/sections/deploy-ai-section";
import ConnectDataSection from "@/components/sections/connect-data-section";
import PowerfulReportingSection from "@/components/sections/powerful-reporting-section";
import FreeTrialCtaSection from "@/components/sections/free-trial-cta-section";
import AdaptiveModelSection from "@/components/sections/adaptive-model-section";
import CustomerTestimonialsCarousel from "@/components/sections/customer-testimonials-carousel";
import DataEnrichmentSection from "@/components/sections/data-enrichment-section";
import BuiltForScaleSection from "@/components/sections/built-for-scale-section";
import FinalCtaSection from "@/components/sections/final-cta-section";
import FooterSection from "@/components/sections/footer-section";
import CookieBanner from "@/components/sections/cookie-banner";
import Header from "@/components/navigation/header";

export default function Page() {
  return (
    <>
      <Header />
      <main>
        <HeroSection />
        <CrmPreviewSection />
        <LogoWallSection />
        <TestimonialSection />
        <PowerfulPlatformSection />
        <div className="border-y border-border">
          <AutomateEverythingSection />
        </div>
        <DeployAiSection />
        <div className="container max-w-[1280px] px-6 lg:px-8">
          <ConnectDataSection />
        </div>
        <PowerfulReportingSection />
        <FreeTrialCtaSection />
        <AdaptiveModelSection />
        <CustomerTestimonialsCarousel />
        <DataEnrichmentSection />
        <BuiltForScaleSection />
        <FinalCtaSection />
      </main>
      <FooterSection />
      <CookieBanner />
    </>
  );
}
