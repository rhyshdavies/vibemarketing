import React from 'react';

const HexagonIllustration = () => (
  <svg
    width="401"
    height="152"
    fill="none"
    viewBox="0 0 401 152"
    xmlns="http://www.w3.org/2000/svg"
    className="w-full max-w-[401px] text-primary"
    aria-hidden="true"
  >
    <path
      d="M76 38.33V113.67L38.5 132.5L1 113.67V38.33L38.5 19.5L76 38.33Z"
      stroke="currentColor"
      strokeWidth="1.5"
    />
    <path
      fillRule="evenodd"
      clipRule="evenodd"
      d="M211.5 19.5L249 38.33V113.67L211.5 132.5L174 113.67V38.33L211.5 19.5ZM175.5 39.2135V112.787L211.5 130.792L247.5 112.787V39.2135L211.5 21.2084L175.5 39.2135Z"
      fill="#FEF9F2"
    />
    <path
      d="M249 38.33V113.67L211.5 132.5L174 113.67V38.33L211.5 19.5L249 38.33Z"
      stroke="currentColor"
      strokeWidth="1.5"
    />
    <path
      d="M141.5 130.75L104 112.167V39.8333L141.5 21.25L179 39.8333V58.6667"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeDasharray="3 3"
    />
    <path
      d="M285 58.6667V39.8333L247.5 21.25L210 39.8333V112.167L247.5 130.75L285 112.167V94.7439"
      stroke="currentColor"
      strokeWidth="1.5"
      strokeDasharray="3 3"
    />
    <path
      d="M322 93.3333V112.167L284.5 130.75L247 112.167V41.3852"
      stroke="currentColor"
      strokeWidth="1.5"
    />
    <path
      d="M400 38.33V113.67L362.5 132.5L325 113.67V94.1667"
      stroke="currentColor"
      strokeWidth="1.5"
    />
  </svg>
);

const FreeTrialCtaSection = () => {
  return (
    <section className="border-b border-border bg-background">
      <div className="container py-16 lg:py-24">
        <div className="grid grid-cols-1 items-center gap-10 py-0 lg:grid-cols-2 lg:gap-14 lg:py-0">
          <div className="text-center lg:text-left">
            <h2 className="text-4xl font-bold tracking-tight text-text-primary lg:text-5xl">
              Start with a 14-day
              <br />
              free trial of Pro.
            </h2>
            <div className="mt-8 flex flex-col items-center gap-4 sm:flex-row sm:justify-center lg:justify-start">
              <a
                href="https://app.attio.com/welcome/sign-in"
                className="inline-flex h-11 items-center justify-center whitespace-nowrap rounded-[10px] bg-primary px-6 text-base font-medium text-primary-foreground transition-colors hover:bg-primary/90"
              >
                Start for free
              </a>
              <a
                href="https://attio.com/pricing"
                className="inline-flex h-11 items-center justify-center whitespace-nowrap rounded-[10px] border border-border bg-background px-6 text-base font-medium text-primary transition-colors hover:bg-accent"
              >
                See our plans
              </a>
            </div>
          </div>
          <div className="flex items-center justify-center">
            <HexagonIllustration />
          </div>
        </div>
      </div>
    </section>
  );
};

export default FreeTrialCtaSection;