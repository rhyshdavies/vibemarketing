"use client";

import {
  ArrowRight,
  ClipboardList,
  Handshake,
  HeartPulse,
  Mail,
  Shuffle,
  TrendingUp,
  UserPlus,
  UserRoundCog,
  Waypoints,
  Zap,
} from "lucide-react";
import Link from 'next/link';
import { FC, ReactNode } from "react";

interface WorkflowCardProps {
  icon: ReactNode;
  iconBgClass: string;
  title: string;
  badge: string;
  badgeClasses: string;
  description: string;
}

const WorkflowCard: FC<WorkflowCardProps> = ({ icon, iconBgClass, title, badge, badgeClasses, description }) => (
  <div className="bg-white p-3 rounded-xl border border-gray-200 shadow-[0px_1px_2px_0px_rgba(0,0,0,0.04),0px_2px_4px_0px_rgba(0,0,0,0.04)] w-[260px]">
    <div className="flex justify-between items-center">
      <div className="flex items-center gap-2">
        <div className={`p-1.5 rounded-md ${iconBgClass}`}>
          {icon}
        </div>
        <span className="text-sm font-medium text-gray-800">{title}</span>
      </div>
      <span className={`px-2 py-0.5 rounded-md text-xs font-medium ${badgeClasses}`}>
        {badge}
      </span>
    </div>
    <hr className="my-2 border-gray-200" />
    <p className="text-xs text-gray-500">{description}</p>
  </div>
);

interface AutomationExampleProps {
  icon: ReactNode;
  text: string;
  isHighlighted?: boolean;
}

const AutomationExample: FC<AutomationExampleProps> = ({ icon, text, isHighlighted }) => (
  <div className={`flex items-center gap-3 p-3 rounded-xl border bg-white cursor-pointer transition-all duration-200 ${isHighlighted 
    ? 'border-gray-800 shadow-[0px_1px_2px_0px_rgba(0,0,0,0.06),0px_4px_8px_0px_rgba(0,0,0,0.06)] scale-[1.02]' 
    : 'border-gray-200 shadow-[0px_1px_2px_0px_rgba(0,0,0,0.04)] hover:shadow-md hover:border-gray-300'}`}>
    <div className="text-gray-500">
      {icon}
    </div>
    <span className="text-sm font-medium text-gray-800">{text}</span>
  </div>
);

const AutomateEverythingSection = () => {

  const automationExamples = [
    { icon: <Zap size={20} className="stroke-width-[1.5]" />, text: 'Re-engage cold leads' },
    { icon: <UserRoundCog size={20} className="stroke-width-[1.5]" />, text: 'MQL lead routing' },
    { icon: <Handshake size={20} className="stroke-width-[1.5]" />, text: 'Onboarding hand-off' },
    { icon: <Mail size={20} className="stroke-width-[1.5]" />, text: 'New Deal email campaign', isHighlighted: true },
    { icon: <ClipboardList size={20} className="stroke-width-[1.5]" />, text: 'Lead form submissions' },
    { icon: <HeartPulse size={20} className="stroke-width-[1.5]" />, text: 'Monitor customer health' },
    { icon: <TrendingUp size={20} className="stroke-width-[1.5]" />, text: 'Identify expansion opportunity' },
  ];
  
  return (
    <div className={`grid grid-cols-1 lg:grid-cols-[minmax(0,_1fr)_minmax(0,_2fr)] gap-x-12 gap-y-10 items-start py-16 px-10 relative bg-background-primary`}>
      <div className="absolute top-0 right-0 h-full w-full lg:w-[calc(2/3*100%)] z-0" style={{
        backgroundImage: 'radial-gradient(circle at 1px 1px, #E5E7EB 1px, transparent 0)',
        backgroundSize: '10px 10px',
      }}></div>
      
      {/* Left Column */}
      <div className="lg:pt-8 relative z-10">
        <h3 className="text-3xl font-medium text-text-primary tracking-tight">Automate everything</h3>
        <p className="mt-4 text-lg text-text-secondary max-w-sm">
          You're in control. Automate even the most complex business processes with our powerful, intelligent automation engine.
        </p>
        <Link href="https://attio.com/platform/automations" className="group inline-flex items-center gap-1.5 mt-6 text-base font-medium text-accent-primary hover:text-blue-700">
          Explore automations
          <ArrowRight className="w-4 h-4 transition-transform duration-200 group-hover:translate-x-1" />
        </Link>
      </div>

      {/* Right Column */}
      <div className="flex flex-col xl:flex-row justify-start items-center xl:items-start gap-8 relative z-10">
        <div className="relative" style={{ width: '580px', height: '530px' }}>
          <svg className="absolute inset-0 pointer-events-none" viewBox="0 0 580 530">
            <circle cx="290" cy="106" r="4" fill="var(--color-background-primary)" stroke="var(--color-border-default)" strokeWidth="1.5" />
            <path d="M 290 110 V 176" stroke="var(--color-border-default)" strokeWidth="1.5" fill="none" />
            <circle cx="290" cy="180" r="4" fill="var(--color-background-primary)" stroke="var(--color-border-default)" strokeWidth="1.5" />
            <path d="M 290 282 V 302" stroke="var(--color-border-default)" strokeWidth="1.5" fill="none" />

            <path d="M 290 302 c 0,20 -65,20 -65,20 h -75 c -30,0 -30,30 -30,40 v 4" stroke="var(--color-border-default)" strokeWidth="1.5" fill="none" />
            <circle cx="120" cy="370" r="4" fill="var(--color-background-primary)" stroke="var(--color-border-default)" strokeWidth="1.5" />
            <text x="125" y="315" fontFamily="var(--font-sans)" fontSize="12" fill="var(--color-text-secondary)">Upsell</text>
           
            <path d="M 290 302 c 0,20 65,20 65,20 h 75 c 30,0 30,30 30,40 v 4" stroke="var(--color-border-default)" strokeWidth="1.5" fill="none" />
            <circle cx="460" cy="370" r="4" fill="var(--color-background-primary)" stroke="var(--color-border-default)" strokeWidth="1.5" />
            <text x="360" y="315" fontFamily="var(--font-sans)" fontSize="12" fill="var(--color-text-secondary)">Nurture</text>
          </svg>

          <div className="absolute top-0 left-1/2 -translate-x-1/2">
            <WorkflowCard
              icon={<Waypoints size={20} className="text-blue-600 stroke-width-[1.5]" />}
              iconBgClass="bg-badge-blue-bg"
              title="Trigger"
              badge="Deals"
              badgeClasses="bg-badge-orange-bg text-badge-orange-text"
              description="When Deal updated"
            />
          </div>

          <div className="absolute top-[180px] left-1/2 -translate-x-1/2">
            <WorkflowCard
              icon={<Shuffle size={20} className="text-purple-600 stroke-width-[1.5]" />}
              iconBgClass="bg-badge-purple-bg"
              title="Switch"
              badge="Condition"
              badgeClasses="bg-gray-100 text-text-secondary"
              description="Route to upsell or nurture"
            />
          </div>
          
          <div className="absolute top-[370px]" style={{ left: '120px', transform: 'translateX(-50%)' }}>
            <WorkflowCard
              icon={<UserPlus size={20} className="text-green-600 stroke-width-[1.5]" />}
              iconBgClass="bg-badge-green-bg"
              title="Enroll in sequence"
              badge="Sequences"
              badgeClasses="bg-badge-green-bg text-badge-green-text"
              description="Enroll person in “Power user upsell”"
            />
          </div>

          <div className="absolute top-[370px]" style={{ left: '460px', transform: 'translateX(-50%)' }}>
            <WorkflowCard
              icon={<UserPlus size={20} className="text-green-600 stroke-width-[1.5]" />}
              iconBgClass="bg-badge-green-bg"
              title="Enroll in sequence"
              badge="Sequences"
              badgeClasses="bg-badge-green-bg text-badge-green-text"
              description="Enroll person in “Nurture”"
            />
          </div>
        </div>

        <div className="w-[280px] flex-shrink-0 pt-1">
          <div className="flex flex-col gap-2">
            {automationExamples.map((item, index) => (
              <AutomationExample key={index} icon={item.icon} text={item.text} isHighlighted={item.isHighlighted} />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AutomateEverythingSection;