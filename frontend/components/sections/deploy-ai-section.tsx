import type { FC, ReactNode } from 'react';
import { ArrowRight, FileText, Sparkles, BarChart2, Users, Globe, Building, MapPin, Folder, PiggyBank } from 'lucide-react';
import { Badge } from '@/components/ui/badge';

type AttributeRowProps = {
  icon: ReactNode;
  label: string;
  children: ReactNode;
};

const AttributeRow: FC<AttributeRowProps> = ({ icon, label, children }) => (
  <div className="flex justify-between items-center">
    <div className="flex items-center gap-2 text-text-secondary">
      {icon}
      <span>{label}</span>
    </div>
    {children}
  </div>
);

const DeployAiSection: FC = () => {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 border-b border-border-default">
      <div className="flex flex-col justify-center p-8 lg:p-12 xl:p-24 order-2 md:order-1">
        <h2 className="text-3xl font-semibold text-text-primary leading-tight tracking-tight">Deploy AI</h2>
        <p className="mt-4 max-w-md text-lg text-text-secondary [text-wrap:balance]">
          Put our research agent to work and scale complex tasks that normally require human effort, like prospecting, lead routing and more.
        </p>
        <a href="/platform/ai" className="group mt-6 inline-flex items-center gap-1.5 font-medium text-text-primary">
          Explore AI
          <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
        </a>
      </div>
      <div className="relative border-l-0 md:border-l border-border-default bg-[radial-gradient(theme(colors.border.default)_1px,transparent_1px)] bg-[length:12px_12px] p-8 lg:p-12 xl:p-16 flex items-start justify-center order-1 md:order-2 min-h-[500px]">
        <div className="flex w-full max-w-4xl flex-col items-center justify-center gap-6 lg:flex-row lg:items-start">
          <div className="relative w-full max-w-[340px] shrink-0 pt-0 lg:pt-16">
            <div className="absolute left-[21px] top-12 bottom-6 w-px bg-border-medium hidden sm:block"></div>
            <div className="space-y-4">
              <div className="relative">
                <div className="absolute left-[22px] top-1/2 -translate-y-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-background border-2 border-border-medium hidden sm:block"></div>
                <div className="flex items-center gap-3 rounded-xl border border-border-default bg-background p-3 shadow-sm">
                  <FileText className="h-5 w-5 text-accent-primary" />
                  <span className="font-medium text-sm text-text-primary">New lead found</span>
                </div>
              </div>
              <div className="relative">
                <div className="absolute left-[22px] top-6 -translate-y-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-background border-2 border-border-medium hidden sm:block"></div>
                <div className="rounded-xl border border-border-default bg-background p-3 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Sparkles className="h-5 w-5 text-accent-primary" />
                      <span className="font-medium text-sm text-text-primary">Activate PLG motion</span>
                    </div>
                    <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium">AI</Badge>
                  </div>
                  <div className="mt-3 rounded-lg border border-border-default bg-background-secondary p-3 text-xs">
                    <p className="text-text-secondary">Does the company sell software to other businesses?</p>
                    <p className="mt-1 font-medium text-text-primary">Yes, they are a B2B SaaS business</p>
                  </div>
                </div>
              </div>
              <div className="relative">
                <div className="absolute left-[22px] top-6 -translate-y-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-background border-2 border-border-medium hidden sm:block"></div>
                <div className="rounded-xl border border-border-default bg-background p-3 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <BarChart2 className="h-5 w-5 text-accent-primary" />
                      <span className="font-medium text-sm text-text-primary">Evaluate size of opportunity</span>
                    </div>
                    <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium">AI</Badge>
                  </div>
                  <div className="mt-3 rounded-lg border border-border-default bg-background-secondary p-3 text-xs">
                    <p className="text-text-secondary">Did the company raise any funds recently?</p>
                    <p className="mt-1 font-medium text-text-primary">$25M raised in Series A funding round</p>
                  </div>
                </div>
              </div>
               <div className="relative">
                <div className="absolute left-[22px] top-6 -translate-y-1/2 -translate-x-1/2 w-3 h-3 rounded-full bg-background border-2 border-border-medium hidden sm:block"></div>
                <div className="rounded-xl border border-border-default bg-background p-3 shadow-sm">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-3">
                      <Users className="h-5 w-5 text-accent-primary" />
                      <span className="font-medium text-sm text-text-primary">Identify key stakeholders</span>
                    </div>
                    <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium">AI</Badge>
                  </div>
                  <div className="mt-3 rounded-lg border border-border-default bg-background-secondary p-3 text-xs">
                    <p className="text-text-secondary">Who are the key stakeholders at the company?</p>
                    <p className="mt-1 font-medium text-text-primary">Adam Kingsley, CEO; Anne Zaragoza, CTO; Tom Wagner, VP of Sales</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="w-full max-w-[340px] shrink-0">
            <div className="rounded-xl border border-border-default bg-background p-4 shadow-lg">
              <div className="flex items-center gap-3 border-b border-border-default pb-3">
                <div className="flex h-8 w-8 items-center justify-center rounded-md bg-black text-white font-bold text-lg">B</div>
                <h3 className="font-semibold text-text-primary">Basepoint</h3>
              </div>
              <div className="space-y-3 pt-4 text-sm">
                <AttributeRow icon={<Globe className="h-4 w-4" />} label="Domains">
                  <a href="#" className="font-medium text-accent-primary hover:underline">basepoint.com</a>
                </AttributeRow>
                <AttributeRow icon={<Building className="h-4 w-4" />} label="Name">
                  <span className="font-medium text-text-primary">Basepoint</span>
                </AttributeRow>
                <AttributeRow icon={<BarChart2 className="h-4 w-4" />} label="Estimated ARR">
                  <Badge className="bg-badge-green-bg text-badge-green-text border-none font-medium">$1–10M</Badge>
                </AttributeRow>
                <AttributeRow icon={<MapPin className="h-4 w-4" />} label="Location">
                  <span className="font-medium text-text-primary">California, USA</span>
                </AttributeRow>
                <AttributeRow icon={<Folder className="h-4 w-4" />} label="Categories">
                  <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium h-5">AI</Badge>
                </AttributeRow>
                <AttributeRow icon={<PiggyBank className="h-4 w-4" />} label="Funding raised">
                  <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium h-5">AI</Badge>
                </AttributeRow>
                <AttributeRow icon={<Users className="h-4 w-4" />} label="Stakeholders">
                  <Badge className="bg-badge-blue-bg text-badge-blue-text border-none font-medium h-5">AI</Badge>
                </AttributeRow>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeployAiSection;