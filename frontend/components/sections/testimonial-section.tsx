import React from 'react';

const TestimonialSection = (): JSX.Element => {
  return (
    <section className="relative flex w-full max-w-screen flex-col items-center justify-center overflow-x-clip bg-gradient-to-b from-[#FAFAFB] to-[#FFFFFF]">
      <div className="container">
        <div className="relative mx-auto w-full max-w-[1392px] border-border lg:border-x">
          <div className="sticky top-[var(--site-header-height)] grid h-[calc(100vh-var(--site-header-height))] w-full justify-center gap-[36px] lg:grid-rows-2 lg:gap-[52px] lg:px-6 lg:pt-[72px]">
            <div className="absolute inset-0 -z-10 overflow-hidden">
              <div className="absolute inset-0 h-[120%]">
                <svg
                  width="100%"
                  height="100%"
                  className="h-full w-full text-border"
                >
                  <defs>
                    <pattern
                      id="testimonial-pattern"
                      width="10"
                      height="10"
                      patternUnits="userSpaceOnUse"
                    >
                      <rect width="1" height="1" fill="currentColor" />
                    </pattern>
                  </defs>
                  <rect
                    width="100%"
                    height="100%"
                    fill="url(#testimonial-pattern)"
                    className="opacity-70"
                  />
                </svg>
              </div>
            </div>
            <p className="max-w-[18em] self-end px-6 text-center font-display text-[35px] leading-tight tracking-[-0.01em] text-text-primary lg:text-[48px]/[1.1]">
              “When I first opened Attio,
              <br className="hidden md:block" /> I instantly got the feeling this
              was
              <br className="hidden md:block" /> the next generation of CRM.”
            </p>
            <p className="flex flex-col items-center px-6 text-center">
              <span className="font-bold text-text-primary">
                Margaret Shen
              </span>
              <span className="text-sm text-text-secondary">
                Head of Business Operations · Modal
              </span>
            </p>
          </div>
        </div>
        <svg
          width="100%"
          height="1"
          className="absolute inset-x-0 bottom-0 text-border lg:hidden"
        >
          <line x1="0" y1="0.5" x2="100%" y2="0.5" stroke="currentColor" />
        </svg>
      </div>
    </section>
  );
};

export default TestimonialSection;