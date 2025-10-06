import React from 'react';

const PowerfulPlatformSection = (): JSX.Element => {
  return (
    <section className="relative z-10 max-w-screen overflow-x-clip bg-background pt-[94px] lg:pt-[126px]">
      <div className="relative">
        <div className="container relative">
          <div className="grid grid-cols-12">
            <div className="col-span-12 border-y border-border bg-background lg:col-span-10 lg:col-start-2">
              <div className="grid grid-cols-1 divide-y divide-border">
                <div id="powerful-platform" className="px-5 pt-8 pb-10 lg:px-12 lg:pb-20 lg:pt-14">
                  <div className="flex items-center justify-between">
                    <h2 className="text-xs font-medium uppercase tracking-[0.05em] text-muted-foreground lg:text-sm">
                      [01]
                      <span className="max-md:hidden">&nbsp;Powerful platform</span>
                    </h2>
                    <p className="text-[13px] font-normal leading-snug text-gray-400">
                      / item 1 ⋮ 4
                    </p>
                  </div>
                  <div className="mt-8 grid grid-cols-1 gap-x-12 gap-y-12 lg:mt-14 lg:grid-cols-2">
                    <div>
                      <h3 className="text-3xl font-medium leading-tight text-foreground lg:text-4xl">
                        GTM
                        <span className="text-muted-foreground">&nbsp;at&nbsp;full&nbsp;throttle.</span>
                      </h3>
                      <p className="mt-4 text-xl leading-relaxed text-muted-foreground [text-wrap:pretty] lg:mt-6">
                        Execute your revenue strategy with precision. Design powerful workflows, deploy AI, integrate your data and build detailed reports — all in one platform.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PowerfulPlatformSection;