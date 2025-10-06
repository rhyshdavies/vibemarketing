"use client";

import * as React from "react";
import Image from "next/image";
import {
  Carousel,
  CarouselContent,
  CarouselItem,
  type CarouselApi,
} from "@/components/ui/carousel";

const BravadoLogo = (props: React.SVGProps<SVGSVGElement>) => (
  <svg width="22" height="15" viewBox="0 0 22 15" fill="none" {...props}>
    <path d="M1 14L11 2L21 14" stroke="currentColor" strokeWidth="2" />
  </svg>
);

const FlatfileLogo = (props: React.SVGProps<SVGSVGElement>) => (
  <svg width="22" height="15" viewBox="0 0 22 15" fill="none" {...props}>
    <path d="M1 9.5V1.5H13" stroke="currentColor" strokeWidth="2" />
    <path d="M21 5.5V13.5H9" stroke="currentColor" strokeWidth="2" />
  </svg>
);

const SnackpassLogo = (props: React.SVGProps<SVGSVGElement>) => (
  <svg width="22" height="15" viewBox="0 0 22 15" fill="none" {...props}>
    <path d="M1 1H8.5L14.5 14H21" stroke="currentColor" strokeWidth="2" />
    <path d="M1 14H8.5L14.5 1H21" stroke="currentColor" strokeWidth="2" />
  </svg>
);

const testimonials = [
  {
    company: "Bravado",
    logo: <BravadoLogo className="text-muted-foreground" />,
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-195788-bravado-avatar.88201d51.png?",
    quote:
      "Attio is the first CRM that feels truly modern. It’s powerful, flexible, and fast to build with. There’s nothing like it on the market.",
    author: "Sahil Mansuri",
    title: "CEO & Co-founder",
    features: [
      {
        name: "Workflows",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Workflows.fa1a1249-31.svg?",
      },
      {
        name: "Deals",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Deal.3e9f3d22-32.svg?",
      },
      {
        name: "Reports",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Report.3156be6f-33.svg?",
      },
    ],
  },
  {
    company: "Flatfile",
    logo: <FlatfileLogo className="text-muted-foreground" />,
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-511709-flatfile-avatar.5e2e4656.png?",
    quote: "We're building the first data onboarding platform and we need a CRM that is as flexible and powerful as our own product. Attio is the only CRM that could keep up with us.",
    author: "David Boskovic",
    title: "CEO & Founder",
    features: [
      {
        name: "Custom objects",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Attributes.e6181a5f-34.svg?",
      },
      {
        name: "Hightouch",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Integrations.08d975ad-35.svg?",
      },
      {
        name: "Reports",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Report.3156be6f-33.svg?",
      },
    ],
  },
  {
    company: "Snackpass",
    logo: <SnackpassLogo className="text-muted-foreground" />,
    image: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-561115-snackpass-avatar.2ec8d250.png?",
    quote: "Attio has been a game changer for our sales team. It’s given us a single source of truth for our customer data and has allowed us to scale our sales process.",
    author: "Jamie Marshall",
    title: "COO & Co-founder",
    features: [
      {
        name: "Lists",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/List.cf582b5a-36.svg?",
      },
      {
        name: "Workflows",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Workflows.fa1a1249-31.svg?",
      },
      {
        name: "API",
        icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/PromptCompletion.7ddaa795-37.svg?",
      },
    ],
  },
];

export default function CustomerTestimonialsCarousel() {
  const [api, setApi] = React.useState<CarouselApi>();
  const [current, setCurrent] = React.useState(0);

  React.useEffect(() => {
    if (!api) return;
    setCurrent(api.selectedScrollSnap());
    const handleSelect = () => setCurrent(api.selectedScrollSnap());
    api.on("select", handleSelect);
    return () => {
      api.off("select", handleSelect);
    };
  }, [api]);

  const scrollTo = (index: number) => api?.scrollTo(index);

  return (
    <section className="bg-secondary py-24">
      <div className="container">
        <Carousel setApi={setApi} opts={{ loop: true }}>
          <CarouselContent>
            {testimonials.map((testimonial) => (
              <CarouselItem key={testimonial.company}>
                <div className="grid grid-cols-1 items-center gap-x-16 gap-y-12 lg:grid-cols-[2fr_3fr] xl:gap-x-24">
                  <div className="relative mx-auto max-w-[400px] lg:max-w-none">
                    <Image
                      src={testimonial.image}
                      alt={`Portrait of ${testimonial.author}`}
                      width={640}
                      height={640}
                      className="h-auto w-full object-contain"
                    />
                  </div>
                  <div className="flex flex-col">
                    <div className="flex items-center gap-x-2.5">
                      {testimonial.logo}
                      {testimonial.company === "Bravado" ? (
                        <h4 className="font-medium tracking-[2.1px] text-muted-foreground">
                          {testimonial.company.toUpperCase()}
                        </h4>
                      ) : (
                        <h4 className="text-lg font-medium text-muted-foreground">
                          {testimonial.company}
                        </h4>
                      )}
                    </div>
                    <p className="mt-6 text-2xl/9 font-medium text-foreground lg:text-3xl/9">
                      “{testimonial.quote}”
                    </p>
                    <p className="mt-8 text-foreground lg:text-lg">
                      {testimonial.author},{" "}
                      <span className="text-muted-foreground">{testimonial.title}</span>
                    </p>
                    <div className="mt-10 border-t border-border pt-6">
                      <p className="text-[15px]/[22px] font-medium text-muted-foreground">
                        {testimonial.company}’s favorite features
                      </p>
                      <div className="mt-4 flex flex-wrap items-center gap-x-6 gap-y-2">
                        {testimonial.features.map((feature) => (
                          <div
                            key={feature.name}
                            className="flex items-center gap-x-2"
                          >
                            <Image
                              src={feature.icon}
                              alt={`${feature.name} icon`}
                              width={24}
                              height={24}
                            />
                            <span className="text-foreground">{feature.name}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              </CarouselItem>
            ))}
          </CarouselContent>
        </Carousel>
        <div className="mt-12 flex justify-center gap-x-6">
          {testimonials.map((testimonial, index) => (
            <button
              key={testimonial.company}
              onClick={() => scrollTo(index)}
              className={`flex items-center gap-x-2 rounded-lg py-2.5 px-4 font-medium transition-colors ${
                current === index
                  ? "bg-white text-foreground shadow-sm"
                  : "text-muted-foreground hover:bg-white/50"
              }`}
            >
              {React.cloneElement(testimonial.logo, {
                className: `${current === index ? 'text-foreground' : 'text-muted-foreground'}`,
               })}
              <span>{testimonial.company}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}