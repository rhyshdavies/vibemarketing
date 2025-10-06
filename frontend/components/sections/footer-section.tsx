"use client";

import { useState } from 'react';
import Link from 'next/link';
import { ArrowUpRight, ArrowRight, Twitter, Linkedin, Instagram, X } from 'lucide-react';

const AttioLogo = () => (
  <svg width="103" height="26" viewBox="0 0 103 26" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-6 text-white">
    <path d="M5.93333 20.4578V5.33333H9.19999V17.5822L17.7244 5.33333H21.2355L12.7111 17.5822V20.4578H5.93333Z" fill="currentColor"></path>
    <path d="M25.689 20.4578V5.33333H36.3112V8.20889H28.9512V11.5778H35.6179V14.4533H28.9512V17.5822H36.3112V20.4578H25.689Z" fill="currentColor"></path>
    <path d="M47.2657 20.4578V5.33333H50.5323V20.4578H47.2657Z" fill="currentColor"></path>
    <path d="M54.5169 20.4578V5.33333H57.7835V20.4578H54.5169Z" fill="currentColor"></path>
    <path d="M68.8683 20.9422C66.0859 20.9422 63.8569 19.9822 62.1814 18.0622C60.5058 16.1422 59.668 13.7333 59.668 10.8355C59.668 7.93774 60.5058 5.52885 62.1814 3.60885C63.8569 1.68885 66.0859 0.728846 68.8683 0.728846C71.6507 0.728846 73.8797 1.68885 75.5552 3.60885C77.2307 5.52885 78.0685 7.93774 78.0685 10.8355C78.0685 13.7333 77.2307 16.1422 75.5552 18.0622C73.8797 19.9822 71.6507 20.9422 68.8683 20.9422ZM68.8683 18.0622C70.6101 18.0622 71.9572 17.3733 72.9097 16C73.8621 14.6266 74.3383 12.8977 74.3383 10.8133C74.3383 8.72885 73.8621 6.99996 72.9097 5.62662C71.9572 4.25329 70.6101 3.56885 68.8683 3.56885C67.1265 3.56885 65.7794 4.25329 64.827 5.62662C63.8745 6.99996 63.3983 8.72885 63.3983 10.8133C63.3983 12.8977 63.8745 14.6266 64.827 16C65.7794 17.3733 67.1265 18.0622 68.8683 18.0622Z" fill="currentColor"></path>
    <path d="M90.8705 25.0489C86.7016 25.0489 83.2269 23.8311 80.4445 21.4V25H77.1778V5.33333H80.4445V7.61777C83.2269 5.20888 86.7016 4 90.8705 4C94.8882 4 98.1242 5.37333 100.578 8.12C103.031 10.8667 104.258 14.2889 104.258 18.3867C104.258 22.4845 103.031 25.9067 100.578 28.6533C98.1242 31.4 94.8882 32.7733 90.8705 32.7733" transform="translate(0, -9.18667)" fill="currentColor"></path>
    <path d="M90.8705 22.1689C92.6123 22.1689 93.9594 21.48 94.9118 20.1067C95.8643 18.7333 96.3405 16.9822 96.3405 14.8578C96.3405 12.7333 95.8643 10.9599 94.9118 9.54218C93.9594 8.1244 92.6123 7.4133 90.8705 7.4133C89.1287 7.4133 87.7594 8.1244 86.7629 9.54218C85.7665 10.9599 85.2683 12.7333 85.2683 14.8578C85.2683 16.9822 85.7665 18.7333 86.7629 20.1067C87.7594 21.48 89.1287 22.1689 90.8705 22.1689Z" fill="currentColor"></path>
  </svg>
);

const footerColumns = [
  {
    title: 'Platform',
    links: [
      { text: 'Refer a team', href: '/refer', new: true },
      { text: 'Changelog', href: '/changelog' },
      { text: 'Workflows', href: '/platform/automations' },
      { text: 'Data', href: '/platform/data' },
      { text: 'Reporting', href: '/platform/reporting' },
      { text: 'Pipeline', href: '/platform/pipeline' },
      { text: 'Automations', href: '/platform/automations' },
      { text: 'Enrichment', href: '/features/enrichment' },
    ],
  },
  {
    title: 'Import from',
    links: [
      { text: 'Salesforce', href: '/apps/salesforce' },
      { text: 'Hubspot', href: '/apps/hubspot' },
      { text: 'Pipedrive', href: '/apps/pipedrive' },
    ],
  },
  {
    title: 'Apps',
    links: [
      { text: 'Gmail', href: '/apps/gmail' },
      { text: 'Outlook', href: '/apps/outlook' },
      { text: 'Customer.io', href: '/apps/customer-io' },
      { text: 'Segment', href: '/apps/segment' },
      { text: 'Mailchimp', href: '/apps/mailchimp' },
      { text: 'Slack', href: '/apps/slack' },
      { text: 'Outreach', href: '/apps/outreach' },
      { text: 'Mixmax', href: '/apps/mixmax' },
      { text: 'Typeform', href: '/apps/typeform' },
    ],
  },
  {
    title: 'Resources',
    links: [
      { text: 'Startup program', href: '/startups' },
      { text: 'Help center', href: 'https://help.attio.com' },
      { text: 'Automation templates', href: '/templates' },
      { text: 'Developers', href: 'https://developers.attio.com', external: true },
      { text: 'System status', href: 'https://status.attio.com', external: true },
      { text: 'Hire an expert', href: '/experts' },
      { text: 'Downloads', href: '/downloads' },
    ],
  },
  {
    title: 'Company',
    links: [
      { text: 'Customers', href: '/customers' },
      { text: 'About', href: '/about' },
      { text: 'Careers', href: '/careers' },
      { text: 'Blog', href: '/blog' },
      { text: 'Press', href: '/press' },
      { text: 'Contact us', href: '/contact' },
      { text: 'Security', href: '/security' },
      { text: 'Legal', href: '/legal' },
    ],
  },
  {
    title: 'Attio for',
    links: [
      { text: 'Startups', href: '/solutions/startups' },
      { text: 'Scale-ups', href: '/solutions/scale-ups' },
      { text: 'SMBs', href: '/solutions/smbs' },
      { text: 'SaaS', href: '/solutions/saas' },
      { text: 'Venture capital', href: '/solutions/venture-capital' },
      { text: 'Professional services', href: '/solutions/professional-services' },
    ],
  },
];

export default function FooterSection() {
  const [isBannerVisible, setIsBannerVisible] = useState(true);

  return (
    <footer className="bg-[#1a1a1a] text-white">
      <div className="container pt-16 pb-14 lg:pt-20 lg:pb-[4.5rem]">
        <div className="grid w-full grid-cols-12 gap-y-7">
          <div className="col-span-12 flex items-center justify-between lg:col-span-3">
            <Link href="/" className="-mx-1.5 rounded-xl px-1.5">
              <AttioLogo />
            </Link>
          </div>
          <div className="col-span-12">
            <div className="grid grid-cols-[repeat(auto-fill,minmax(140px,1fr))] gap-x-5 gap-y-7 lg:grid-cols-6 lg:gap-x-12">
              {footerColumns.map((column) => (
                <div key={column.title} className="flex flex-col gap-y-3">
                  <span className="text-sm font-medium text-white">{column.title}</span>
                  <ul className="flex flex-col gap-y-2">
                    {column.links.map((link) => (
                      <li key={link.text}>
                        <Link
                          href={link.href}
                          target={link.external ? '_blank' : undefined}
                          rel={link.external ? 'noopener noreferrer' : undefined}
                          className="group flex items-center gap-x-1.5 text-[15px] text-white/70 transition-colors hover:text-white"
                        >
                          {link.text}
                          {link.new && (
                            <span className="ml-1.5 rounded-[4px] bg-[#2E45C3] px-1 py-0.5 text-[10px] font-semibold uppercase leading-3 text-white">
                              New
                            </span>
                          )}
                          {link.external && <ArrowUpRight className="size-3.5 opacity-70 group-hover:opacity-100" />}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      {isBannerVisible && ( <>
        <div className="container relative grid grid-cols-12">
            <span className="col-span-12 -mx-[100vw] h-px bg-white/20"></span>
        </div>
        <div className="isolate flex h-14 w-full items-center justify-center bg-[#1a1a1a]">
            <div className="container flex h-full items-center justify-center">
            <div className="relative flex size-full items-stretch justify-center px-12 max-md:justify-start max-md:pl-0">
                <Link href="/blog/attio-raises-52m-series-b" className="group relative flex size-full items-center justify-center gap-1.5 text-white max-md:justify-start">
                    <span className="relative truncate text-[13px] leading-5 underline-offset-4 group-hover:underline">
                        Announcing our $52M Series B, led by Google Ventures
                    </span>
                    <ArrowRight className="size-3.5 transition-transform duration-300 group-hover:translate-x-0.5" />
                </Link>
                <button
                onClick={() => setIsBannerVisible(false)}
                className="group absolute top-1/2 right-0 -translate-y-1/2 rounded-[10px] p-2 hover:bg-white/10"
                aria-label="Close banner"
                >
                <X className="size-4.5 text-white/70 transition-colors group-hover:text-white" />
                </button>
            </div>
            </div>
        </div>
        </>
      )}

      <div className="container relative grid grid-cols-12">
        <span className="col-span-12 -mx-[100vw] h-px bg-white/20"></span>
      </div>

      <div className="container pt-8 pb-10 lg:py-6">
        <div className="flex flex-col-reverse items-start justify-between gap-y-7 lg:flex-row lg:items-center">
          <div className="text-[13px] text-white/70">© 2024 Attio Ltd.</div>
          <div className="flex items-center gap-x-2">
            <a href="https://twitter.com/attio" target="_blank" rel="noopener noreferrer" aria-label="Attio on Twitter" className="flex size-8 items-center justify-center rounded-[10px] bg-white/10 transition-colors hover:bg-white/20">
              <Twitter className="size-4.5" />
            </a>
            <a href="https://www.linkedin.com/company/attio" target="_blank" rel="noopener noreferrer" aria-label="Attio on LinkedIn" className="flex size-8 items-center justify-center rounded-[10px] bg-white/10 transition-colors hover:bg-white/20">
              <Linkedin className="size-4.5" />
            </a>
            <a href="https://www.instagram.com/attio" target="_blank" rel="noopener noreferrer" aria-label="Attio on Instagram" className="flex size-8 items-center justify-center rounded-[10px] bg-white/10 transition-colors hover:bg-white/20">
              <Instagram className="size-4.5" />
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}