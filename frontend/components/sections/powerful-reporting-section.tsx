"use client";

import React, { useState } from "react";
import { ArrowRight, TrendingUp, History, Filter, Hourglass, GitCommitHorizontal } from "lucide-react";

type ReportSidebarItemProps = {
  icon: React.ElementType;
  label: string;
  isActive?: boolean;
};

const ReportSidebarItem = ({ icon: Icon, label, isActive }: ReportSidebarItemProps) => (
  <button
    className={`flex w-full items-center gap-2.5 rounded-md px-2.5 py-1.5 text-left text-sm transition-colors ${
      isActive
        ? "bg-gray-100 text-text-primary"
        : "text-text-secondary hover:bg-gray-100/50"
    }`}
  >
    <Icon className="h-4 w-4" />
    <span className="font-medium">{label}</span>
  </button>
);

const TimeFilterButton = ({ label, isActive }: { label: string; isActive?: boolean }) => (
  <button
    className={`rounded-[7px] px-3 py-1 text-xs font-medium transition-all ${
      isActive ? "bg-white shadow-sm" : "text-text-secondary"
    }`}
  >
    {label}
  </button>
);

const PowerfulReportingSection = () => {
  const yAxisLabels = ["$ 2.8M", "$ 2.4M", "$ 2.0M", "$ 1.6M", "$ 1.2M", "$ 0.8M", "$ 0.4M"];
  
  return (
    <div className="w-full bg-background-primary py-16 lg:py-0">
      <div className="grid grid-cols-12 items-center border-t border-border-default">
        <div className="col-span-12 flex items-center justify-start lg:col-span-4 lg:pl-16 xl:pl-24">
          <div className="max-w-md px-6 py-12 lg:px-0 lg:py-24">
            <h2 className="text-[32px]/[38px] font-bold tracking-[-0.01em] text-text-primary lg:text-[40px]/[44px]">
              Powerful reporting
            </h2>
            <p className="mt-4 text-lg/[27px] text-text-secondary [text-wrap:pretty] lg:text-xl/[30px]">
              Create real-time, detailed reports that scale with your data. Visualize, customize, and get deep insights in seconds — not hours.
            </p>
            <a href="https://attio.com/platform/reporting" className="group mt-6 inline-flex items-center gap-1.5 text-sm font-medium text-accent-primary transition-colors hover:text-text-primary">
              <span>Explore reporting</span>
              <ArrowRight className="h-4 w-4 transition-transform duration-300 group-hover:translate-x-1" />
            </a>
          </div>
        </div>
        <div className="col-span-12 lg:col-span-8">
          <div className="relative mr-6 flex items-start gap-6 border-l border-border-default p-6 lg:p-10">
            {/* Background Pattern */}
            <div
              className="absolute inset-0 z-0 opacity-50"
              style={{
                backgroundImage: "repeating-linear-gradient(135deg, transparent, transparent 4px, #e5e7eb 4px, #e5e7eb 5px), repeating-linear-gradient(45deg, transparent, transparent 4px, #e5e7eb 4px, #e5e7eb 5px)",
                backgroundSize: '16px 16px',
              }}
            ></div>

            <div className="relative z-10 flex-grow">
              <div className="flex flex-col gap-4">
                <div className="flex flex-wrap items-center justify-between gap-4">
                  <div className="flex items-center gap-1 rounded-lg bg-gray-100 p-1">
                    <TimeFilterButton label="7D" />
                    <TimeFilterButton label="30D" />
                    <TimeFilterButton label="3M" />
                    <TimeFilterButton label="6M" />
                    <TimeFilterButton label="12M" />
                    <TimeFilterButton label="All" isActive />
                  </div>
                  <div className="flex items-center gap-4 text-xs font-medium text-text-secondary">
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-2 rounded-full bg-[#3b82f6]"></div>
                      <span>Plus</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-2 rounded-full bg-[#8b5cf6]"></div>
                      <span>Pro</span>
                    </div>
                    <div className="flex items-center gap-1.5">
                      <div className="h-2 w-2 rounded-full bg-[#10b981]"></div>
                      <span>Enterprise</span>
                    </div>
                  </div>
                </div>
                <div className="text-xs font-medium text-text-secondary">
                  <span>Apr - Jun</span>
                  <span className="mx-2">|</span>
                  <span>Jul - Sep</span>
                </div>
              </div>
              <div className="relative mt-8 flex">
                <div className="flex-shrink-0 pr-4 text-right text-xs text-text-secondary">
                  {yAxisLabels.map((label) => (
                    <div key={label} className="h-10 text-right">
                      {label}
                    </div>
                  ))}
                </div>
                <div className="relative w-full flex-grow">
                  <div className="absolute inset-0 grid grid-rows-7">
                    {yAxisLabels.map((_, index) => (
                      <div key={index} className="border-t border-dashed border-border-default"></div>
                    ))}
                    <div className="border-t border-dashed border-border-default"></div>
                  </div>
                  
                  <div className="relative h-[280px] w-full">
                    <svg
                      viewBox="0 0 500 200"
                      preserveAspectRatio="none"
                      className="absolute inset-0 h-full w-full"
                    >
                      <path d="M0,80 C150,60 350,100 500,70 L500,200 L0,200 Z" fill="#10b981" fillOpacity={0.9} />
                      <path d="M0,120 C150,90 350,140 500,110 L500,200 L0,200 Z" fill="#8b5cf6" fillOpacity={0.9} />
                      <path d="M0,170 C150,140 350,180 500,150 L500,200 L0,200 Z" fill="#3b82f6" fillOpacity={0.9} />
                    </svg>

                     <div className="absolute top-0 bottom-8" style={{ left: '33.33%' }}>
                        <div className="h-full w-px border-l border-dashed border-gray-400"></div>
                        <div className="absolute left-4 top-[20%] w-48 rounded-lg border border-border-default bg-background p-3 shadow-lg">
                           <div className="mb-2 text-sm font-semibold text-text-primary">July</div>
                           <div className="mb-3 flex items-center gap-2 text-xs text-text-secondary">
                               <div className="h-2 w-2 rounded-full bg-[#8b5cf6]"></div> Pro plan
                           </div>
                           <div className="space-y-1 text-xs text-text-secondary">
                               <div className="flex justify-between">
                                   <span>Time</span>
                                   <span className="font-medium text-text-primary">July 2024</span>
                               </div>
                               <div className="flex justify-between">
                                   <span>Amount</span>
                                   <span className="font-medium text-text-primary">$1,920,240.00</span>
                               </div>
                           </div>
                        </div>
                    </div>
                  </div>
                  
                  <div className="mt-2 flex justify-between px-4 text-xs text-text-secondary">
                      <span></span>
                      <span>July</span>
                      <span>August</span>
                      <span>September</span>
                      <span></span>
                  </div>
                </div>
              </div>
            </div>
            <div className="relative z-10 hidden w-48 flex-shrink-0 flex-col gap-1 lg:flex">
                <ReportSidebarItem icon={TrendingUp} label="Insight" isActive />
                <ReportSidebarItem icon={History} label="Historical values" />
                <ReportSidebarItem icon={Filter} label="Funnel" />
                <ReportSidebarItem icon={Hourglass} label="Time in stage" />
                <ReportSidebarItem icon={GitCommitHorizontal} label="Stage changed" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PowerfulReportingSection;