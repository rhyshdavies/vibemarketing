"use client";

import { useState } from "react";
import {
  UserRound,
  FileText,
  User,
  Plus,
  Diamond,
  Building,
  Handshake,
  FolderKanban,
  FileSignature,
  Landmark,
} from "lucide-react";

// Types
type DataObjectType = {
  id: string;
  icon: React.ElementType;
  iconBg: string;
  iconColor: string;
  title: string;
  type: "Standard" | "Custom";
  attributes: string[];
  moreCount: number;
  connections?: ('top' | 'right' | 'bottom' | 'left')[];
};

type TabDataType = {
  objects: DataObjectType[];
  addObjectPosition: string;
};

// Data for each tab from the content provided
const tabData: Record<string, TabDataType> = {
  "Scale-ups": {
    objects: [
      { id: 'user', icon: UserRound, iconBg: 'bg-green-100', iconColor: 'text-green-700', title: 'User', type: 'Standard', attributes: ['User ID', 'Engagement score', 'User type'], moreCount: 4, connections: ['bottom'] },
      { id: 'deal', icon: FileText, iconBg: 'bg-purple-100', iconColor: 'text-purple-700', title: 'Deal', type: 'Standard', attributes: ['Deal name', 'Workspace', 'Stage'], moreCount: 2, connections: ['bottom'] },
      { id: 'person', icon: User, iconBg: 'bg-blue-100', iconColor: 'text-blue-700', title: 'Person', type: 'Standard', attributes: ['Name', 'Email', 'Company'], moreCount: 12, connections: ['top', 'right'] },
    ],
    addObjectPosition: "xl:absolute xl:top-[225px] xl:left-[calc(50%+40px)]",
  },
  "SaaS startups": {
    objects: [
      { id: 'workspace', icon: Building, iconBg: 'bg-yellow-100', iconColor: 'text-yellow-700', title: 'Workspace', type: 'Standard', attributes: ['Name', 'Company', 'Status'], moreCount: 7 },
      { id: 'deal', icon: FileText, iconBg: 'bg-purple-100', iconColor: 'text-purple-700', title: 'Deal', type: 'Standard', attributes: ['Deal name', 'Stage', 'Deal value'], moreCount: 15 },
      { id: 'company', icon: Building, iconBg: 'bg-red-100', iconColor: 'text-red-700', title: 'Company', type: 'Standard', attributes: ['Domain', 'Industry', 'Location'], moreCount: 8 },
      { id: 'person', icon: User, iconBg: 'bg-blue-100', iconColor: 'text-blue-700', title: 'Person', type: 'Standard', attributes: ['Name', 'Email', 'Company'], moreCount: 6 },
    ],
    addObjectPosition: "",
  },
  SMBs: {
    objects: [
      { id: 'partnership', icon: Handshake, iconBg: 'bg-pink-100', iconColor: 'text-pink-700', title: 'Partnership', type: 'Custom', attributes: ['Partnership name', 'Partnership type', 'Point of contact'], moreCount: 10 },
      { id: 'project', icon: FolderKanban, iconBg: 'bg-indigo-100', iconColor: 'text-indigo-700', title: 'Project', type: 'Custom', attributes: ['Company', 'Point of Contact', 'Status'], moreCount: 5 },
      { id: 'company', icon: Building, iconBg: 'bg-red-100', iconColor: 'text-red-700', title: 'Company', type: 'Standard', attributes: ['Name', 'Industry', 'Domain'], moreCount: 8 },
      { id: 'person', icon: User, iconBg: 'bg-blue-100', iconColor: 'text-blue-700', title: 'Person', type: 'Standard', attributes: ['Email', 'Company', 'LinkedIn'], moreCount: 12 },
    ],
    addObjectPosition: "",
  },
  Investors: {
    objects: [
      { id: 'invoice', icon: FileSignature, iconBg: 'bg-teal-100', iconColor: 'text-teal-700', title: 'Invoice', type: 'Custom', attributes: ['Company', 'Status', 'Amount'], moreCount: 3 },
      { id: 'company', icon: Building, iconBg: 'bg-red-100', iconColor: 'text-red-700', title: 'Company', type: 'Standard', attributes: ['Name', 'Domain', 'Industry'], moreCount: 4 },
      { id: 'person', icon: User, iconBg: 'bg-blue-100', iconColor: 'text-blue-700', title: 'Person', type: 'Standard', attributes: ['Name', 'Email', 'Company'], moreCount: 11 },
      { id: 'deal', icon: FileText, iconBg: 'bg-purple-100', iconColor: 'text-purple-700', title: 'Deal', type: 'Standard', attributes: ['Company', 'Investment amount', 'Deal stage'], moreCount: 10 },
      { id: 'fund', icon: Landmark, iconBg: 'bg-orange-100', iconColor: 'text-orange-700', title: 'Fund', type: 'Custom', attributes: ['Name', 'Domain', 'Employees'], moreCount: 7 },
    ],
    addObjectPosition: "",
  },
};

const TABS = Object.keys(tabData);

const ObjectModelCard = ({ data }: { data: DataObjectType }) => (
  <div className="relative w-full max-w-[280px] bg-white border border-gray-200 rounded-xl shadow-[0_4px_12px_rgba(0,0,0,0.05)] p-4 h-fit">
    <div className="flex justify-between items-start">
      <div className="flex items-center gap-2">
        <div className={`p-1.5 rounded-md ${data.iconBg}`}>
          <data.icon className={`w-5 h-5 ${data.iconColor}`} />
        </div>
        <h4 className="font-semibold text-base text-gray-900">{data.title}</h4>
      </div>
      <span className="text-xs font-medium text-gray-500 bg-gray-100 rounded-full px-2 py-0.5">
        {data.type}
      </span>
    </div>
    <div className="mt-4 space-y-2 border-t border-gray-200 pt-3">
      {data.attributes.map(attr => (
        <div key={attr} className="flex items-center gap-2 text-sm text-gray-600">
          <Diamond className="w-3 h-3 text-gray-400" />
          <span>{attr}</span>
        </div>
      ))}
    </div>
    {data.moreCount > 0 && (
      <div className="mt-3 text-sm text-gray-500">
        + {data.moreCount} More Attributes
      </div>
    )}
    {data.connections?.map(side => {
        let positionClasses = '';
        if (side === 'top') positionClasses = 'top-0 left-1/2 -translate-x-1/2 -translate-y-1/2';
        if (side === 'bottom') positionClasses = 'bottom-0 left-1/2 -translate-x-1/2 translate-y-1/2';
        if (side === 'left') positionClasses = 'left-0 top-1/2 -translate-x-1/2 -translate-y-1/2';
        if (side === 'right') positionClasses = 'right-0 top-1/2 translate-x-1/2 -translate-y-1/2';
        return <div key={side} className={`absolute w-2.5 h-2.5 bg-gray-300 rounded-full ${positionClasses}`} />;
    })}
  </div>
);

const AddObjectCard = ({ className = '' }: { className?: string }) => (
  <div className={`flex items-center justify-center w-full max-w-[280px] h-[190px] bg-white/50 border-2 border-dashed border-gray-300 rounded-xl ${className}`}>
    <div className="flex items-center gap-2 text-gray-500">
      <Plus className="w-4 h-4" />
      <span className="font-medium text-sm">Add object</span>
    </div>
  </div>
);

const ScaleUpsLayout = ({ data, addObjectPosition }: { data: TabDataType, addObjectPosition: string }) => (
    <>
        {/* Mobile/Tablet fallback grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-8 justify-items-center xl:hidden">
            {data.objects.map(obj => (
                <ObjectModelCard key={obj.id} data={obj} />
            ))}
            <AddObjectCard />
        </div>
        {/* Desktop absolute layout */}
        <div className="relative w-full max-w-4xl mx-auto h-[450px] hidden xl:block">
            <svg className="absolute inset-0 w-full h-full" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M 140 190 C 140 230, 240 210, 310 215" stroke="#D1D5DB" strokeWidth="1.5" />
              <path d="M 740 190 C 740 230, 640 210, 570 215" stroke="#D1D5DB" strokeWidth="1.5"/>
              <path d="M 440 332 C 500 332, 510 332, 570 320" stroke="#D1D5DB" strokeWidth="1.5" />
            </svg>
            <div className="absolute top-0 left-0"><ObjectModelCard data={data.objects[0]} /></div>
            <div className="absolute top-0 right-0"><ObjectModelCard data={data.objects[1]} /></div>
            <div className="absolute top-[220px] left-1/2 -translate-x-1/2"><ObjectModelCard data={data.objects[2]} /></div>
            <AddObjectCard className={addObjectPosition} />
        </div>
    </>
);

export default function AdaptiveModelSection() {
  const [activeTab, setActiveTab] = useState(TABS[0]);
  const currentTabData = tabData[activeTab];

  return (
    <section className="bg-white py-24 sm:py-32">
      <div className="container mx-auto px-4">
        <div className="max-w-3xl mx-auto text-center">
          <div className="flex justify-between items-center text-xs font-mono uppercase text-gray-500 mb-4 px-2 tracking-wider">
            <span>[02] ADAPTIVE MODEL</span>
            <span>/ data ↔ business</span>
          </div>
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 tracking-tight leading-tight [text-wrap:balance]">
            A seismic shift in CRM flexibility.
          </h2>
          <p className="mt-6 text-lg text-gray-600 [text-wrap:balance]">
            Attio’s powerful data model adapts to how your business works, not the other way around. Your business model — perfectly reflected in your CRM.
          </p>
          <a
            href="/platform/data"
            className="mt-8 inline-flex items-center justify-center px-5 py-2.5 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 transition-colors"
          >
            Explore our data model
          </a>
        </div>

        <div className="mt-16">
          <div className="flex justify-center gap-1 bg-gray-100 p-1 rounded-lg max-w-md mx-auto">
            {TABS.map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`w-full py-1.5 px-3 text-sm font-medium rounded-md transition-all duration-200 ${
                  activeTab === tab
                    ? 'bg-white text-gray-800 shadow-sm'
                    : 'bg-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>

        <div 
          className="mt-12 relative py-12 bg-no-repeat bg-center" 
          style={{ backgroundImage: `url("data:image/svg+xml,%3csvg width='10' height='10' viewBox='0 0 10 10' fill='none' xmlns='http://www.w3.org/2000/svg'%3e%3crect width='1' height='1' fill='%23E5E7EB'/%3e%3c/svg%3e")` }}>
          {activeTab === 'Scale-ups' ? (
              <ScaleUpsLayout data={currentTabData} addObjectPosition={currentTabData.addObjectPosition} />
          ) : (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 justify-items-center max-w-7xl mx-auto px-4">
              {currentTabData.objects.map(obj => (
                <ObjectModelCard key={obj.id} data={obj} />
              ))}
              <AddObjectCard/>
            </div>
          )}
        </div>
      </div>
    </section>
  );
}