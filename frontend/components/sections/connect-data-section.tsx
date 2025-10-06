import Image from "next/image";
import Link from "next/link";
import { ArrowRight } from "lucide-react";

const integrationCategories = [
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/SalesIcon.a56de08f-13.svg?", text: "Sales engagement" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/EmailIcon.e297e71f-14.svg?", text: "Email & calendar" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/DataIcon.8ae70cd0-15.svg?", text: "Data warehouses" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/PointOfContactIcon.6c297a51-16.svg?", text: "Customer support" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/CurrencyIcon.828ed3f2-17.svg?", text: "Billing & invoicing" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/DataBlocksIcon.83b2af9a-18.svg?", text: "Product data" },
];

const dataObjects = [
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/DashboardColourIcon.692a82e7-19.svg?", title: "Workspace", records: "2,857 Records", position: "absolute top-[215px] -right-[100px] max-xl:hidden" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/CompanyColourIcon.1b735a3e-20.svg?", title: "Company", records: "3,096 Records", position: "absolute top-[310px] -right-[50px] max-xl:hidden" },
  { icon: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/DollarDocColourIcon.8b6faf33-21.svg?", title: "Deal", records: "5,490 Records", position: "absolute top-[405px] right-[40px] max-xl:hidden" },
];

const integrationLogos = [
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/attio.aac65cb3-22.svg?", alt: "Attio", position: "absolute top-[115px] left-[170px]", sizeClass: "p-2.5", dimension: 40 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo1.7ab13633-23.svg?", alt: "Zapier logo", position: "absolute top-[55px] left-[230px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo2.101b5a2c-24.svg?", alt: "Slack logo", position: "absolute top-[125px] left-[280px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo3.5d10e012-25.svg?", alt: "Gmail logo", position: "absolute top-[205px] left-[240px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo4.b58c27f7-26.svg?", alt: "Outlook logo", position: "absolute top-[225px] left-[150px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo5.ca4b4565-27.svg?", alt: "Intercom logo", position: "absolute top-[175px] left-[80px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo6.97cf38e6-28.svg?", alt: "Zendesk logo", position: "absolute top-[95px] left-[60px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo7.7caffd4e-29.svg?", alt: "Clearbit logo", position: "absolute top-[45px] left-[120px]", sizeClass: "p-2", dimension: 32 },
  { src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/Logo8.6c074f4f-30.svg?", alt: "Mixpanel logo", position: "absolute top-[285px] left-[60px] max-lg:hidden", sizeClass: "p-2", dimension: 32 },
];


const ConnectDataSection = () => {
  return (
    <div className="grid grid-cols-1 items-start gap-y-6 border-b border-border pb-18 lg:grid-cols-2 lg:gap-x-12 lg:gap-y-0 lg:pb-36">
      <div className="flex flex-col gap-y-6 lg:sticky lg:top-36 self-start">
        <h2 className="text-3xl font-semibold text-text-primary leading-[1.25] tracking-[-0.01em]">
          Connect any type of data
        </h2>
        <p className="max-w-[34ch] text-lg text-text-secondary [text-wrap:balance]">
          Sync product data, billing data, and everything in between, for a real-time single source of truth for your business.
        </p>
        <Link
          href="/platform/data"
          className="group flex items-center gap-1 text-base font-medium text-accent-primary"
        >
          Explore data
          <ArrowRight className="size-4 transition-transform duration-300 group-hover:translate-x-1" />
        </Link>
      </div>

      <div className="relative row-start-1 lg:col-start-2 h-[680px] self-start max-lg:mt-6">
        <div className="absolute top-0 left-0 w-[clamp(310px,100%,340px)] isolate z-10 grid grid-cols-2 gap-4">
          {integrationCategories.map((category, index) => (
            <div key={index} className="flex items-center gap-x-2.5 rounded-lg border border-border bg-card p-2.5">
              <Image
                src={category.icon}
                alt=""
                width={20}
                height={20}
                className="size-5"
              />
              <span className="text-[13px] font-medium leading-[1.4] text-text-primary">
                {category.text}
              </span>
            </div>
          ))}
        </div>

        {integrationLogos.map((logo, index) => (
          <div key={index} className={`isolate z-10 rounded-xl bg-card border border-border shadow-[0_4px_10px_rgba(0,0,0,0.04)] ${logo.position} ${logo.sizeClass}`}>
            <Image src={logo.src} alt={logo.alt} width={logo.dimension} height={logo.dimension} />
          </div>
        ))}
        
        {dataObjects.map((obj, index) => (
          <div
            key={index}
            className={`w-[200px] isolate z-10 flex flex-col gap-2.5 rounded-xl border border-border bg-card p-2.5 shadow-[0px_2px_4px_0px_rgba(28,40,64,0.06),_0px_6px_10px_-3px_rgba(28,40,64,0.1)] ${obj.position}`}
          >
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Image src={obj.icon} alt="" width={24} height={24} className="size-6" />
                <span className="text-[14px] font-medium text-text-primary">{obj.title}</span>
              </div>
              <span className="text-xs font-medium text-muted-foreground bg-muted px-1.5 py-0.5 rounded-md">
                Standard
              </span>
            </div>
            <p className="text-[13px] text-muted-foreground">{obj.records}</p>
          </div>
        ))}

        <Image
          src="https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/DataBlocksIcon.83b2af9a-18.svg?"
          alt="Data blocks illustration"
          width={160}
          height={160}
          className="absolute top-[470px] -right-[150px] text-gray-200 max-xl:hidden"
        />

      </div>
    </div>
  );
};

export default ConnectDataSection;