"use client";

import Image from "next/image";
import Link from "next/link";
import {
  Mail,
  Calendar,
  Database,
  Spline,
  Sparkles,
  Wand2,
  Linkedin,
  Briefcase,
  Send,
  History,
  GitCommitHorizontal,
} from "lucide-react";
import { Button } from "@/components/ui/button";

const DataEnrichmentSection = () => {
  const dataSources = [
    {
      name: "Email events",
      icon: <Mail className="size-3.5 text-gray-500" />,
    },
    {
      name: "Calendar events",
      icon: <Calendar className="size-3.5 text-gray-500" />,
    },
    {
      name: "Segment events",
      icon: <Spline className="size-3.5 text-gray-500" />,
    },
    {
      name: "Data sources",
      icon: <Database className="size-3.5 text-gray-500" />,
    },
  ];

  const activityItems = [
    {
      avatarUrl:
        "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-489654-home-enrichment-avatar-1.9c8461f6.jpg?",
      alt: "Michael Chang",
      description: "attended an in-person meeting",
      actor: "Michael Chang",
      time: "6 hours ago",
    },
    {
      avatarUrl:
        "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-583045-home-enrichment-avatar.24fc1e48.png?",
      alt: "Sarah Johnson",
      description: "attended an event",
      actor: "Sarah Johnson",
      time: "2 days ago",
    },
    {
      avatarUrl:
        "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-489654-home-enrichment-avatar-1.9c8461f6.jpg?",
      alt: "Michael Chang",
      description: "made an outbound phone call",
      actor: "Michael Chang",
      time: "4 days ago",
    },
  ];

  return (
    <section className="bg-background-primary py-16 lg:py-24">
      <div className="container mx-auto px-6 lg:px-8 max-w-[1280px]">
        <div className="grid grid-cols-1 items-start gap-x-16 gap-y-16 lg:grid-cols-2">
          {/* Left Column */}
          <div className="lg:mt-12">
            <div className="flex justify-between items-center text-[11px] font-mono uppercase tracking-wider text-text-secondary">
              <span>[03] DATA ENRICHMENT</span>
              <span>/ SPEED 1:1</span>
            </div>
            <h2 className="mt-6 text-[44px] leading-[1.1] tracking-[-0.02em] text-text-primary">
              <span className="font-bold">Build fast.</span>
              <span className="text-text-secondary">
                {" "}
                Forget months of setup. Attio syncs immediately with your email
                and calendar, building a powerful CRM right before your eyes.
              </span>
            </h2>
            <div className="mt-8 flex items-center gap-x-3">
              <Button
                asChild
                className="bg-primary text-primary-foreground hover:bg-primary/90 rounded-lg px-4 py-2 h-auto text-sm font-medium"
              >
                <Link href="https://app.attio.com/welcome/sign-in">
                  Start for free
                </Link>
              </Button>
              <Button
                variant="outline"
                className="border-border-default rounded-lg px-4 py-2 h-auto text-sm font-medium"
              >
                Send me a demo
              </Button>
            </div>
            <div className="mt-12 grid grid-cols-2 sm:grid-cols-4 gap-2.5">
              {dataSources.map((source, index) => (
                <div
                  key={index}
                  className="flex items-center gap-2 rounded-lg border border-border-default bg-background-primary px-3 py-2 text-[13px] font-medium text-text-primary"
                >
                  {source.icon}
                  <span>{source.name}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Right Column */}
          <div className="relative">
            <div className="rounded-2xl border border-border-default bg-background-primary p-6 shadow-2xl shadow-black/5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex items-center gap-4">
                  <Image
                    src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-583045-home-enrichment-avatar.24fc1e48.png?"
                    alt="Sarah Johnson"
                    width={56}
                    height={56}
                    className="rounded-full"
                  />
                  <div>
                    <h3 className="text-lg font-semibold text-text-primary">
                      Sarah Johnson
                    </h3>
                    <p className="text-sm text-text-secondary">
                      Head of IT at GreenLeaf Inc.
                    </p>
                  </div>
                </div>
                <Button
                  variant="outline"
                  size="sm"
                  className="rounded-md h-auto px-3 py-1.5 text-xs font-medium gap-1.5 border-border-medium"
                >
                  <Mail className="size-3.5" />
                  Compose email
                </Button>
              </div>

              <div className="mt-6 border-t border-border-default pt-6">
                <h4 className="flex items-center gap-2 text-sm font-semibold text-text-primary">
                  <Sparkles className="size-4 text-text-secondary" />
                  Highlights
                </h4>
                <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 gap-4">
                  <div className="col-span-1 sm:col-span-2 rounded-xl border border-border-default bg-[#FCFCFD] p-4">
                    <div className="flex justify-between items-center mb-2">
                      <h5 className="text-xs font-medium text-text-secondary">
                        Summary
                      </h5>
                      <Wand2 className="size-4 text-text-tertiary" />
                    </div>
                    <p className="text-sm leading-relaxed text-text-secondary [text-wrap:balance]">
                      Sarah Johnson, the Head of IT, is leading the initiative
                      to modernize their data infrastructure, which aligns with
                      GreenLeaf’s growth and sustainability goals. A successful
                      demo call on August 29 confirmed the need for TechWave’s
                      solutions, and the opportunity is moving forward with a
                      75% confidence level.
                    </p>
                  </div>

                  <div className="rounded-xl border border-border-default p-3">
                    <div className="flex justify-between items-center mb-2">
                      <h5 className="text-xs font-medium text-text-secondary">
                        LinkedIn
                      </h5>
                      <Linkedin className="size-4 text-[#0A66C2]" />
                    </div>
                    <a
                      href="#"
                      className="text-sm font-semibold text-[#0A66C2] hover:underline"
                    >
                      sarahjohnson
                    </a>
                  </div>

                  <div className="rounded-xl border border-border-default p-3">
                    <div className="flex items-start justify-between">
                      <div>
                        <h5 className="text-xs font-medium text-text-secondary">
                          Upcoming
                        </h5>
                        <p className="mt-1 text-sm font-semibold text-text-primary">
                          Demo Call
                        </p>
                        <p className="text-xs text-text-secondary">
                          Nov 29, 10:40 AM
                        </p>
                      </div>
                      <div className="flex flex-col items-center justify-center rounded-md border border-border-medium bg-white shadow-sm w-10">
                        <div className="text-[9px] font-bold uppercase text-text-tertiary bg-background-tertiary w-full text-center py-0.5 rounded-t-[5px]">
                          THU
                        </div>
                        <div className="text-lg font-bold text-text-primary py-0.5">
                          29
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-xl border border-border-default p-3">
                    <div className="flex justify-between items-center mb-2">
                      <h5 className="text-xs font-medium text-text-secondary">
                        Company
                      </h5>
                      <Briefcase className="size-4 text-text-tertiary" />
                    </div>
                    <div className="flex items-center gap-2">
                      <Image
                        src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-755808-home-enrichment-logo.2eaaf090.png?"
                        alt="GreenLeaf Inc. logo"
                        width={28}
                        height={28}
                      />
                      <div>
                        <p className="text-sm font-semibold text-text-primary">
                          GreenLeaf Inc.
                        </p>
                        <p className="text-xs text-text-secondary">
                          San Francisco, CA
                        </p>
                      </div>
                    </div>
                  </div>

                  <div className="rounded-xl border border-border-default p-3">
                    <div className="flex justify-between items-center">
                      <h5 className="text-xs font-medium text-text-secondary">
                        Sales Outreach
                      </h5>
                      <GitCommitHorizontal className="size-4 text-text-tertiary" />
                    </div>
                    <p className="mt-2 text-sm font-semibold text-text-primary">
                      Step 2
                    </p>
                    <p className="text-xs text-text-secondary">
                      Automated email
                    </p>
                    <div className="relative mt-2 h-0.5 w-full rounded-full bg-gray-200">
                      <div
                        className="h-0.5 rounded-full bg-green-500"
                        style={{ width: "66%" }}
                      />
                    </div>
                  </div>
                </div>
              </div>

              <div className="mt-6 border-t border-border-default pt-6">
                <h4 className="flex items-center gap-2 text-sm font-semibold text-text-primary">
                  <History className="size-4 text-text-secondary" />
                  Activity
                </h4>
                <ul className="mt-4 space-y-4">
                  {activityItems.map((item, index) => (
                    <li key={index} className="flex items-start gap-4">
                      <Image
                        src={item.avatarUrl}
                        alt={item.alt}
                        width={32}
                        height={32}
                        className="rounded-full mt-0.5"
                      />
                      <div className="flex-grow">
                        <p className="text-sm text-text-secondary">
                          <span className="font-semibold text-text-primary">
                            {item.actor}
                          </span>{" "}
                          {item.description}
                        </p>
                      </div>
                      <span className="text-xs text-text-tertiary whitespace-nowrap">
                        {item.time}
                      </span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default DataEnrichmentSection;