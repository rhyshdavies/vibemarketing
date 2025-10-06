import React from 'react';

const GdprIcon = () => (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="text-gray-400">
        <path d="M24 6V2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M24 46V42" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M42 24H46" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M2 24H6" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M37.4141 10.5859L40.2425 7.75745" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M7.75732 40.2426L10.5858 37.4142" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M10.5859 10.5859L7.75745 7.75745" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M40.2426 40.2426L37.4142 37.4142" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
        <path d="M19 24.5L23 28.5L31 20.5" stroke="#1A1A1A" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
);

const CcpaIcon = () => (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M24 4L8 9.2V24C8 35 24 44 24 44C24 44 40 35 40 24V9.2L24 4Z" stroke="#B8BCC4" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
        <circle cx="24" cy="23" r="3" stroke="#1A1A1A" strokeWidth="2" />
        <path d="M24 26V31" stroke="#1A1A1A" strokeWidth="2" strokeLinecap="round" />
    </svg>
);

const IsoIcon = () => (
    <svg width="48" height="48" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="1" y="1" width="46" height="46" rx="8" stroke="#B8BCC4" strokeWidth="2" />
        <text x="50%" y="40%" dominantBaseline="middle" textAnchor="middle" fontFamily="Inter, sans-serif" fontSize="14" fontWeight="600" fill="#1A1A1A">ISO</text>
        <text x="50%" y="60%" dominantBaseline="middle" textAnchor="middle" fontFamily="Inter, sans-serif" fontSize="10" fill="#6B7280">27001</text>
    </svg>
);


const stats = [
    { value: "1M+", label: "Customer records" },
    { value: "195+", label: "Countries" },
    { value: "3k+", label: "Customers" },
    { value: "99.9%", label: "Uptime" },
];

const certifications = [
    { name: "GDPR", icon: <GdprIcon /> },
    { name: "CCPA", icon: <CcpaIcon /> },
    { name: "ISO", icon: <IsoIcon /> },
];

const BuiltForScaleSection = () => {
    return (
        <section className="bg-background-primary py-24 lg:py-32">
            <div className="container mx-auto max-w-[1280px] px-4">
                <div className="border-t border-border-default pt-16">
                    <div className="flex justify-between items-center text-text-tertiary text-[13px] font-medium tracking-wide">
                        <span>[04] BUILT FOR SCALE</span>
                        <span>/ GROWTH + SECURITY</span>
                    </div>

                    <div className="mt-20 grid grid-cols-1 lg:grid-cols-12 lg:gap-x-16">
                        <div className="lg:col-span-5">
                            <h3 className="text-[40px] leading-tight font-semibold text-text-primary">
                                The system of action for the next generation.
                            </h3>
                            <p className="mt-6 text-2xl text-text-secondary">
                                Attio is built for scale. Our customers sort through millions of records with sub-50ms latency.
                            </p>
                        </div>
                        <div className="lg:col-span-7 mt-16 lg:mt-0">
                            <div className="grid grid-cols-2 gap-x-8 gap-y-16">
                                {stats.map((stat, index) => (
                                    <div key={index}>
                                        <p className="text-6xl font-medium text-text-primary">{stat.value}</p>
                                        <p className="mt-4 text-base text-text-secondary">{stat.label}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="mt-32 grid grid-cols-1 lg:grid-cols-12 lg:gap-x-16 items-start">
                        <div className="lg:col-span-5">
                            <h4 className="text-3xl font-semibold text-text-primary">Scale with security.</h4>
                            <p className="mt-4 text-lg text-text-secondary">
                                Attio is audited and certified by industry-leading third party standards.
                            </p>
                            <a
                                href="#"
                                className="mt-8 inline-block h-9 cursor-pointer items-center justify-center rounded-[10px] border border-border-default bg-white px-3 text-sm font-medium text-text-primary transition-colors hover:bg-gray-100"
                            >
                                <span className="flex h-full items-center">
                                    Talk to sales
                                </span>
                            </a>
                        </div>
                        <div className="lg:col-span-7 mt-16 lg:mt-0">
                            <div className="flex justify-around items-end h-full">
                                {certifications.map((cert) => (
                                    <div key={cert.name} className="flex flex-col items-center gap-4">
                                        {cert.icon}
                                        <p className="text-sm font-medium text-text-secondary">{cert.name}</p>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    );
};

export default BuiltForScaleSection;