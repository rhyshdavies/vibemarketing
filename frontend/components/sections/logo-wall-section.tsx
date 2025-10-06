import Image from "next/image";

const logos = [
  { name: "Granola", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/granola-2-1.svg?", width: 172, height: 60 },
  { name: "Coca-Cola", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/coca-cola-2-2.svg?", width: 172, height: 60 },
  { name: "Flatfile", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/flatfile-2-3.svg?", width: 172, height: 60 },
  { name: "Modal", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/modal-2-4.svg?", width: 172, height: 60 },
  { name: "Union Square Ventures", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/usv-updated-5.svg?", width: 173, height: 60 },
  { name: "Replicate", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/replicate-2-6.svg?", width: 172, height: 60 },
  { name: "Bravado", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/bravado-2-7.svg?", width: 172, height: 60 },
  { name: "Legora", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/legora-logo-wall-8.svg?", width: 173, height: 60 },
  { name: "Railway", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/railway-2-9.svg?", width: 173, height: 60 },
  { name: "Public", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/public-2-10.svg?", width: 173, height: 60 },
  { name: "Plain", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/plain-2-11.svg?", width: 172, height: 60 },
  { name: "Passionfroot", src: "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/svgs/passionfroot-3-12.svg?", width: 173, height: 60 },
];

const LogoWallSection = () => {
  return (
    <div className="bg-background">
      <div className="container mx-auto px-4 py-12 md:py-20">
        <div className="grid grid-cols-2 items-center justify-items-center gap-x-8 gap-y-10 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6">
          {logos.map((logo) => (
            <Image
              key={logo.name}
              src={logo.src}
              alt={`${logo.name} logo`}
              width={logo.width}
              height={logo.height}
              className="col-span-1 h-auto max-w-[173px] opacity-60 transition-opacity duration-300 ease-in-out hover:opacity-100"
            />
          ))}
        </div>
      </div>
    </div>
  );
};

export default LogoWallSection;