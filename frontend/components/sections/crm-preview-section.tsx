"use client";

import Image from "next/image";
import {
  Bell,
  CheckSquare,
  ChevronDown,
  Mail,
  Zap,
  BarChart2,
  ListOrdered,
  Workflow,
  Star,
  Rocket,
  LayoutDashboard,
  Users,
  Building2,
  Handshake,
  Laptop2,
  Briefcase,
  Settings2,
  Upload,
  Download,
  Filter,
  Users2,
  GitBranch,
  ArrowDownUp,
  MessageSquare,
  Plus,
  Command,
  Rows,
} from "lucide-react";

const sidebarNavItems = [
  { icon: Zap, label: "Quick actions", shortcut: "⌘K", secondaryIcon: Command },
  { icon: Bell, label: "Notifications" },
  { icon: CheckSquare, label: "Tasks" },
  { icon: Mail, label: "Emails" },
  { icon: BarChart2, label: "Reports" },
];

const automationItems = [
  { icon: Workflow, label: "Workflows" },
  { icon: ListOrdered, label: "Sequences" },
];

const favoriteItems = [
  { icon: Star, label: "Onboarding pipeline", emoji: "🌟" },
  { icon: Rocket, label: "Top of funnel", emoji: "🚀" },
  { icon: GitBranch, label: "RevOps workflows" },
];

const recordItems = [
  { icon: Building2, label: "Companies" },
  { icon: Users, label: "People" },
  { icon: Handshake, label: "Deals" },
  { icon: Laptop2, label: "Workspaces" },
  { icon: Briefcase, label: "Partnerships" },
];

const listItems = [
  { icon: Rows, label: "Strategic accounts" },
  { icon: Rows, label: "Top companies" },
];

const tableData = [
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-vercel.dc29fd97.jpeg&w=64&q=75",
    name: "Vercel",
    domain: "vercel.com",
    deals: ["Vercel", "Vercel - Expansion"],
    icpFit: "Excellent",
    arr: "$100M-$250M",
    strength: "Very strong",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-digital-ocean.420a219d.jpeg&w=64&q=75",
    name: "DigitalOcean",
    domain: "digitalocean.com",
    deals: ["DigitalOcean"],
    icpFit: "Medium",
    arr: "$500M-$1B",
    strength: "Strong",
    thinking: true,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-git-hub.3fe5a8f8.png&w=64&q=75",
    name: "GitHub",
    domain: "github.com",
    deals: ["GitHub - x20 Enterprise"],
    icpFit: "Good",
    arr: "$1B-$10B",
    strength: "Very strong",
    thinking: true,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-stripe.24a8a6a7.png&w=64&q=75",
    name: "Stripe",
    domain: "stripe.com",
    deals: ["Stripe"],
    icpFit: "Good",
    arr: "$1B-$10B",
    strength: "Very strong",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-figma.a62a135a.png&w=64&q=75",
    name: "Figma",
    domain: "figma.com",
    deals: ["Figma"],
    icpFit: "Good",
    arr: "$500M-$1B",
    strength: "Very strong",
    thinking: true,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-intercom.70ee1991.jpeg&w=64&q=75",
    name: "Intercom",
    domain: "intercom.com",
    deals: ["Intercom", "Intercom - Automations"],
    icpFit: "Medium",
    arr: "$250M-$500M",
    strength: "Very strong",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-segment.8bc0a9eb.png&w=64&q=75",
    name: "Segment",
    domain: "segment.com",
    deals: ["Segment - x30 Pro"],
    icpFit: "Good",
    arr: "$250M-$500M",
    strength: "Strong",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-notion.5308e8cf.png&w=64&q=75",
    name: "Notion",
    domain: "notion.so",
    deals: ["Notion - Exec", "Notion - GTM"],
    icpFit: "Medium",
    arr: "$100M-$250M",
    strength: "Strong",
    thinking: true,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-slack.2b630b9e.png&w=64&q=75",
    name: "Slack",
    domain: "slack.com",
    deals: ["Slack", "Slack - Expansion"],
    icpFit: "Low",
    arr: "$1B-$10B",
    strength: "Weak",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-loom.6585780e.png&w=64&q=75",
    name: "Loom",
    domain: "loom.com",
    deals: ["Loom"],
    icpFit: "Medium",
    arr: "$50M-$100M",
    strength: "Good",
    thinking: true,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-retool.89bdadd8.jpeg&w=64&q=75",
    name: "Retool",
    domain: "retool.com",
    deals: ["Retool"],
    icpFit: "Excellent",
    arr: "$50M-$100M",
    strength: "Good",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-customer-io.cd633249.png&w=64&q=75",
    name: "Customer.io",
    domain: "customer.io",
    deals: ["Customer.io - x10 Plus"],
    icpFit: "Excellent",
    arr: "$10-$50M",
    strength: "Strong",
    thinking: false,
  },
  {
    logo: "https://attio.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2Fhome-ui-logo-snowflake.0aa4b085.jpeg&w=64&q=75",
    name: "Snowflake",
    domain: "snowflake.com",
    deals: ["Snowflake", "Snowflake - Expansion"],
    icpFit: "Low",
    arr: "$1B-$10B",
    strength: "Strong",
    thinking: true,
  },
];

const IcpFitBadge = ({ fit }: { fit: string }) => {
  const colorClasses: { [key: string]: string } = {
    Excellent: "bg-badge-green-bg text-badge-green-text",
    Good: "bg-badge-blue-bg text-badge-blue-text",
    Medium: "bg-badge-yellow-bg text-badge-yellow-text",
    Low: "bg-badge-orange-bg text-badge-orange-text",
  };
  return (
    <span
      className={`px-2 py-0.5 rounded-full text-xs font-medium ${
        colorClasses[fit] || "bg-gray-200 text-gray-800"
      }`}
    >
      {fit}
    </span>
  );
};

const ConnectionStrength = ({ strength }: { strength: string }) => {
  const colorClasses: { [key: string]: string } = {
    "Very strong": "text-green-600",
    Strong: "text-blue-600",
    Good: "text-green-500",
    Weak: "text-orange-500",
  };
  return (
    <span className={`font-medium ${colorClasses[strength] || "text-text-secondary"}`}>
      {strength}
    </span>
  );
};

export default function CrmPreviewSection() {
  return (
    <div className="relative border-t border-border bg-gradient-to-b from-[#FDFDFD] to-background">
      <div className="relative col-span-12 mx-[calc(50%-50vw)] max-w-screen pl-4 sm:flex sm:justify-center sm:px-6 lg:mx-0 lg:ml-0 lg:w-auto lg:px-20 lg:pb-16 xl:px-28">
        <div className="relative w-full max-w-[570px] p-1 max-sm:pr-0 md:max-w-none [mask-image:linear-gradient(to_bottom,black,black_85%,transparent_100%)]">
          <div className="isolate">
            <div className="w-full overflow-hidden border border-border bg-background shadow-[0px_2px_6px_0px_rgba(28,40,64,0.06),0px_6px_20px_-2px_rgba(28,40,64,0.08)] h-[640px] rounded-lg pointer-events-none select-none">
              <div className="relative grid h-full w-full grid-cols-[237px_1fr]">
                {/* Sidebar */}
                <aside className="bg-background-secondary border-r border-border p-3 flex flex-col gap-4 overflow-y-auto">
                  <div className="flex items-center justify-between px-1">
                    <div className="flex items-center gap-2">
                      <Image
                        src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-683854-home-ui-layout-sidebar-header-avatar.14e2ff59.png?"
                        alt="Basepoint logo"
                        width={24}
                        height={24}
                        className="rounded-md"
                      />
                      <span className="font-semibold text-text-primary text-base">Basepoint</span>
                    </div>
                    <ChevronDown className="h-4 w-4 text-text-secondary" />
                  </div>

                  <div className="flex flex-col gap-1">
                    {sidebarNavItems.map((item, index) => (
                      <a
                        key={index}
                        href="#"
                        className="flex items-center justify-between text-sm text-sidebar-foreground hover:bg-sidebar-accent p-2 rounded-md"
                      >
                        <div className="flex items-center gap-3">
                          <item.icon className="w-4 h-4 text-text-secondary" />
                          <span>{item.label}</span>
                        </div>
                        {item.shortcut && (
                          <div className="flex items-center gap-1 text-text-tertiary text-xs">
                            {item.secondaryIcon && <item.secondaryIcon className="w-3 h-3" />}
                            <span>{item.shortcut}</span>
                          </div>
                        )}
                      </a>
                    ))}
                  </div>

                  <div className="flex flex-col gap-1">
                    <div className="flex items-center justify-between px-2 py-1">
                       <h3 className="text-xs font-medium text-text-secondary">Automations</h3>
                       <ChevronDown className="h-4 w-4 text-text-secondary" />
                    </div>
                    {automationItems.map((item, index) => (
                      <a key={index} href="#" className="flex items-center gap-3 text-sm text-sidebar-foreground hover:bg-sidebar-accent p-2 rounded-md">
                        <item.icon className="w-4 h-4 text-text-secondary" />
                        <span>{item.label}</span>
                      </a>
                    ))}
                  </div>

                  <div className="flex flex-col gap-1">
                    <h3 className="text-xs font-medium text-text-secondary px-2">Favorites</h3>
                    {favoriteItems.map((item, index) => (
                      <a key={index} href="#" className="flex items-center gap-3 text-sm text-sidebar-foreground hover:bg-sidebar-accent p-2 rounded-md">
                        <span className="text-base">{item.emoji}</span>
                        <span>{item.label}</span>
                      </a>
                    ))}
                  </div>

                  <div className="flex flex-col gap-1">
                     <div className="flex items-center justify-between px-2 py-1">
                       <h3 className="text-xs font-medium text-text-secondary">Records</h3>
                       <ChevronDown className="h-4 w-4 text-text-secondary" />
                    </div>
                    {recordItems.map((item, index) => (
                      <a
                        key={index}
                        href="#"
                        className={`flex items-center gap-3 text-sm rounded-md p-2 ${
                          item.label === "Companies"
                            ? "bg-accent text-accent-foreground font-medium"
                            : "text-sidebar-foreground hover:bg-sidebar-accent"
                        }`}
                      >
                        <item.icon className="w-4 h-4" />
                        <span>{item.label}</span>
                      </a>
                    ))}
                  </div>
                   <div className="flex flex-col gap-1">
                    <h3 className="text-xs font-medium text-text-secondary px-2">Lists</h3>
                    {listItems.map((item, index) => (
                      <a key={index} href="#" className="flex items-center gap-3 text-sm text-sidebar-foreground hover:bg-sidebar-accent p-2 rounded-md">
                        <item.icon className="w-4 h-4 text-text-secondary" />
                        <span>{item.label}</span>
                      </a>
                    ))}
                  </div>

                </aside>

                {/* Main Content */}
                <main className="flex flex-col bg-background">
                  <header className="border-b border-border p-3 flex flex-col gap-3">
                    <div className="flex items-center justify-between">
                      <h2 className="text-base font-semibold text-text-primary">Companies</h2>
                      <div className="flex items-center gap-2">
                        <div className="flex -space-x-2">
                          <Image src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-933669-home-ui-layout-header-avatars-1.de28e0a2.jpg?" alt="User 1" width={24} height={24} className="rounded-full border-2 border-background"/>
                          <Image src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-869328-home-ui-layout-header-avatars-2.751288d8.jpg?" alt="User 2" width={24} height={24} className="rounded-full border-2 border-background"/>
                          <div className="w-6 h-6 rounded-full border-2 border-background bg-gray-100 flex items-center justify-center text-xs font-medium text-text-secondary">+1</div>
                        </div>
                        <Plus className="w-4 h-4 text-text-secondary"/>
                      </div>
                    </div>
                    <div className="flex items-center justify-between text-xs text-text-secondary">
                      <div className="flex items-center gap-4">
                        <button className="flex items-center gap-1.5"><Settings2 className="w-3.5 h-3.5"/> View settings</button>
                        <button className="flex items-center gap-1.5"><Upload className="w-3.5 h-3.5"/>/<Download className="w-3.5 h-3.5"/> Import / Export</button>
                      </div>
                       <div className="flex items-center gap-3">
                         <div className="flex items-center gap-1.5">
                           <ArrowDownUp className="w-3.5 h-3.5" />
                           <span>Sorted by Last email interaction</span>
                         </div>
                         <button className="flex items-center gap-1.5 border border-border rounded-md px-2 py-1">
                           <Filter className="w-3.5 h-3.5"/>
                           <span>Advanced filter</span>
                           <span className="bg-primary text-primary-foreground text-[10px] rounded-full px-1.5 py-0.5">3</span>
                         </button>
                       </div>
                    </div>
                  </header>

                  <div className="flex-grow overflow-y-auto">
                    <div className="min-w-[1000px]">
                      {/* Table Header */}
                      <div className="grid grid-cols-[2fr_1.5fr_2fr_1.5fr_1.5fr_1.5fr] gap-x-4 px-4 py-2 border-b border-border text-xs font-medium text-text-secondary">
                        <div className="text-left">Company</div>
                        <div className="text-left">Domains</div>
                        <div className="text-left">Associated deals</div>
                        <div className="text-left flex items-center gap-1">ICP Fit<span className="text-[9px] font-bold text-purple-600 bg-purple-100 px-1 rounded-sm">AI</span></div>
                        <div className="text-left flex items-center gap-1">Estimated ARR<span className="text-[9px] font-bold text-purple-600 bg-purple-100 px-1 rounded-sm">AI</span></div>
                        <div className="text-left">Connection strength</div>
                      </div>

                      {/* Table Body */}
                      <div>
                        {tableData.map((row, index) => (
                          <div key={index} className="grid grid-cols-[2fr_1.5fr_2fr_1.5fr_1.5fr_1.5fr] gap-x-4 items-center px-4 py-3 border-b border-border hover:bg-background-secondary text-sm">
                            <div className="flex items-center gap-3">
                              <Image src={row.logo} alt={`${row.name} logo`} width={24} height={24} className="rounded-md" />
                              <span className="font-medium text-text-primary">{row.name}</span>
                            </div>
                            <div className="text-text-secondary">{row.domain}</div>
                            <div className="flex flex-wrap gap-1">
                              {row.deals.map((deal, i) => (
                                <span key={i} className="bg-blue-100 text-blue-800 text-xs font-medium px-2 py-0.5 rounded-full">{deal}</span>
                              ))}
                            </div>
                            <div>
                              {row.thinking ? ( <span className="text-text-tertiary text-xs animate-pulse">AI is thinking...</span> ) : ( <IcpFitBadge fit={row.icpFit} /> )}
                            </div>
                            <div>
                               {row.thinking ? ( <span className="text-text-tertiary text-xs animate-pulse">AI is thinking...</span> ) : ( <span className="text-text-secondary">{row.arr}</span>)}
                            </div>
                            <div><ConnectionStrength strength={row.strength} /></div>
                          </div>
                        ))}
                      </div>
                      
                      {/* Table Footer */}
                      <div className="grid grid-cols-[2fr_1.5fr_2fr_1.5fr_1.5fr_1.5fr] gap-x-4 px-4 py-2 text-xs text-text-tertiary">
                         <div>
                            <span className="font-medium">1,439</span> count
                         </div>
                         {[...Array(5)].map((_, i) => (
                             <div key={i} className="text-blue-600 hover:underline cursor-pointer">Add calculation</div>
                         ))}
                      </div>

                    </div>
                  </div>
                </main>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}