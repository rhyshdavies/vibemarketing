"use client";

import React, { useState } from 'react';
import Link from 'next/link';
import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { ArrowUpRight, Sparkles } from 'lucide-react';

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

const TABS = ["ICP Targeting", "AI Personalization", "Multi-Channel", "Analytics"];

const HeroSection = () => {
    const [activeTab, setActiveTab] = useState("AI Personalization");

    return (
        <div className="bg-gradient-to-b from-[#FAFAFB] to-white">
            <div className="container">
                <div className="flex flex-col items-center pt-24 pb-16 text-center lg:pb-20">
                    <div className="group relative inline-flex cursor-pointer items-center justify-center rounded-lg p-px">
                        <div className="absolute inset-0 rounded-lg bg-[conic-gradient(from_180deg_at_50%_50%,rgba(163,236,233,0),#A3ECE9_20deg,#709FF5_100deg,#709FF5_120deg,rgba(0,0,0,0)_149.4deg)] opacity-70 transition-opacity duration-300 group-hover:opacity-100"></div>
                        <div className="relative flex items-center gap-x-1 rounded-[7px] bg-white py-[5px] pl-[11px] pr-[7px] transition-colors duration-300 hover:bg-[#FBFBFC]">
                            <Sparkles className="h-3.5 w-3.5 text-blue-500" />
                            <span className="text-[13px] font-medium leading-[18px] text-secondary-foreground">
                                AI-powered cold outreach automation
                            </span>
                        </div>
                    </div>

                    <h1 className="mt-6 max-w-[14ch] text-5xl font-extrabold tracking-tight text-text-primary md:text-6xl lg:text-[72px] lg:leading-[1.05]">
                        Turn cold emails into warm conversations.
                    </h1>

                    <p className="mt-6 max-w-lg text-lg text-text-secondary md:text-xl">
                        Vibe is the AI-native outreach platform that personalizes at scale.
                    </p>

                    <div className="mt-8 flex w-full max-w-xs flex-col gap-3 sm:max-w-none sm:flex-row sm:justify-center sm:gap-2">
                        <Link
                            href="/dashboard"
                            className="inline-flex h-[46px] items-center justify-center whitespace-nowrap rounded-xl bg-primary px-3.5 text-base font-medium text-primary-foreground shadow-sm transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 lg:h-9 lg:rounded-[10px] lg:px-3 lg:text-sm"
                        >
                            Get Started
                        </Link>
                        <Link
                            href="/sign-in"
                            className="inline-flex h-[46px] items-center justify-center whitespace-nowrap rounded-xl border border-border bg-background px-3.5 text-base font-medium text-primary shadow-sm transition-colors hover:bg-accent hover:text-accent-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 lg:h-9 lg:rounded-[10px] lg:px-3 lg:text-sm"
                        >
                            Sign In
                        </Link>
                    </div>
                </div>
            </div>
            
            <div className="relative border-t border-border bg-gradient-to-b from-[#FDFDFD] to-white">
                <div className="container">
                    <div className="lg:border-x lg:border-border">
                        <div className="grid grid-cols-2 lg:grid-cols-4" style={{ gap: '1px', backgroundColor: 'var(--color-border)' }}>
                            {TABS.map((tab) => (
                                <button
                                    key={tab}
                                    onClick={() => setActiveTab(tab)}
                                    className={cn(
                                        "relative flex h-16 w-full items-center justify-center border-b border-border bg-background px-4 text-[15px] font-medium leading-5 transition-colors duration-150 ease-out focus:z-10 focus:outline-none focus-visible:ring-2 focus-visible:ring-ring",
                                        activeTab === tab 
                                            ? "text-secondary-foreground" 
                                            : "text-muted-foreground hover:text-foreground"
                                    )}
                                    style={{
                                        backgroundColor: activeTab === tab ? 'var(--color-background-secondary)' : 'var(--color-background)'
                                    }}
                                >
                                    {tab}
                                    {activeTab === tab && (
                                        <div className="absolute inset-x-0 bottom-[-1px] h-[3px] bg-primary" />
                                    )}
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default HeroSection;