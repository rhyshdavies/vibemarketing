"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";

export default function CookieBanner() {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    // In a real-world application, you would check for a 'cookie_consent' cookie.
    // For this example, we'll simulate this by showing the banner after a delay
    // if no such cookie is found. This also ensures it only renders client-side.
    if (typeof window !== "undefined" && !document.cookie.includes("cookie_consent")) {
      const timer = setTimeout(() => {
        setIsVisible(true);
      }, 1500); // Delay appearance for a less intrusive user experience
      return () => clearTimeout(timer);
    }
  }, []);

  const handleConsent = (consent: boolean) => {
    // Set a cookie to remember the user's choice for one year.
    const expiryDate = new Date();
    expiryDate.setFullYear(expiryDate.getFullYear() + 1);
    document.cookie = `cookie_consent=${consent}; path=/; expires=${expiryDate.toUTCString()}; SameSite=Lax; Secure`;
    setIsVisible(false);
  };

  if (!isVisible) {
    return null;
  }

  return (
    <div className="fixed inset-x-4 bottom-4 z-50 animate-in fade-in slide-in-from-bottom-5 duration-500 md:inset-x-6 md:bottom-6">
      <div className="mx-auto flex w-full max-w-6xl flex-col items-center justify-between gap-4 rounded-lg border border-border bg-background/95 p-4 shadow-2xl backdrop-blur-md md:flex-row md:gap-6">
        <p className="flex-grow text-center text-sm leading-relaxed text-text-secondary md:text-left">
          We use cookies to improve your experience. You can opt out of certain
          cookies. Find out more in our{" "}
          <a
            href="https://attio.com/legal/privacy"
            target="_blank"
            rel="noopener noreferrer"
            className="font-medium text-text-primary underline hover:no-underline"
          >
            privacy policy
          </a>
          .
        </p>
        <div className="flex flex-shrink-0 items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => handleConsent(false)}
          >
            Reject
          </Button>
          <Button
            variant="default"
            size="sm"
            onClick={() => handleConsent(true)}
          >
            Continue
          </Button>
        </div>
      </div>
    </div>
  );
}