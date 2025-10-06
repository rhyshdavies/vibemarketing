import Image from 'next/image';
import Link from 'next/link';

const avatarImages = [
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-169519-avatar2.a4f6241f.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-163711-avatar3.1cefb7cb.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-408907-avatar4.f2a92621.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-843191-avatar5.514cb6d3.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-599231-avatar6.165300a0.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-654413-avatar7.c8916748.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-536764-avatar8.9e30568f.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-677086-avatar9.e05cdee1.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-639378-avatar10.2590365c.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-108379-avatar11.38d34894.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-093921-avatar12.5dab5434.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-888501-avatar13.f787556b.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-562594-avatar14.4bcebca9.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-654648-avatar15.f47a8fbd.jpeg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-745625-avatar16.a65d5329.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-542387-avatar17.abfc9fe0.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-852796-avatar18.95a64b85.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-766196-avatar19.840cdfa3.png?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-639792-avatar20.a35f4ee2.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-188055-avatar21.950927b0.jpg?",
  "https://slelguoygbfzlpylpxfs.supabase.co/storage/v1/object/public/test-clones/c4074812-55b9-44d9-8884-2b545a988210-attio-com/assets/images/next-505092-avatar22.a2414a5c.jpg?",
];

const gridConfig = [
  { empty: 8, count: 5, opacities: [0.1, 0.2, 0.4, 0.2, 0.1] },
  { empty: 5, count: 11, opacities: [0.1, 0.1, 0.2, 0.2, 0.4, 0.6, 0.4, 0.2, 0.2, 0.1, 0.1] },
  { empty: 2, count: 17, opacities: [0.1, 0.1, 0.2, 0.2, 0.2, 0.4, 0.4, 0.6, 0.8, 0.6, 0.4, 0.4, 0.2, 0.2, 0.2, 0.1, 0.1] },
  { empty: 0, count: 21, opacities: [0.2, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.6, 0.6, 0.8, 1.0, 0.8, 0.6, 0.6, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2] },
  { empty: 0, count: 21, opacities: [0.1, 0.2, 0.2, 0.2, 0.4, 0.4, 0.4, 0.6, 0.6, 0.8, 1.0, 0.8, 0.6, 0.6, 0.4, 0.4, 0.4, 0.2, 0.2, 0.2, 0.1] },
  { empty: 2, count: 17, opacities: [0.1, 0.1, 0.2, 0.2, 0.2, 0.4, 0.4, 0.6, 0.8, 0.6, 0.4, 0.4, 0.2, 0.2, 0.2, 0.1, 0.1] },
  { empty: 5, count: 11, opacities: [0.1, 0.1, 0.2, 0.2, 0.4, 0.6, 0.4, 0.2, 0.2, 0.1, 0.1] },
  { empty: 8, count: 5, opacities: [0.1, 0.2, 0.4, 0.2, 0.1] },
];

let imageCounter = 0;
const gridCells = gridConfig.flatMap((rowConfig, rowIndex) => {
    const row = [];
    for (let i = 0; i < rowConfig.empty; i++) {
        row.push(null);
    }
    for (let i = 0; i < rowConfig.count; i++) {
        row.push({
            src: avatarImages[imageCounter % avatarImages.length],
            opacity: rowConfig.opacities[i],
            key: `avatar-cell-${rowIndex}-${i}`,
        });
        imageCounter++;
    }
    const remaining = 21 - row.length;
    for (let i = 0; i < remaining; i++) {
        row.push(null);
    }
    return row;
});


const FinalCtaSection = () => {
  return (
    <section className="bg-background py-24 sm:py-32">
      <div className="container mx-auto flex flex-col items-center px-4">
        <div className="relative isolate mb-12">
          <div
            className="grid w-full max-w-6xl grid-cols-[repeat(21,minmax(0,1fr))] justify-center gap-x-2 gap-y-3"
            style={{ maskImage: 'linear-gradient(to bottom, transparent, black 20%, black 80%, transparent)' }}
          >
            {gridCells.map((cell, index) => (
              cell ? (
                <div key={cell.key} style={{ opacity: cell.opacity }}>
                  <Image
                    src={cell.src}
                    alt=""
                    width={48}
                    height={48}
                    className="h-12 w-12 rounded-full object-cover"
                    unoptimized
                  />
                </div>
              ) : (
                <div key={`empty-cell-${index}`} />
              )
            ))}
          </div>
        </div>

        <h2 className="text-balance text-center text-5xl font-bold leading-tight tracking-tighter text-text-primary md:text-[56px] lg:text-6xl">
          The CRM behind
          <br />
          thousands of companies.
        </h2>

        <div className="mt-9 flex items-center justify-center gap-x-2">
          <Link
            href="https://app.attio.com/welcome/sign-in"
            className="inline-flex h-11 items-center justify-center rounded-md bg-primary px-6 text-base font-medium text-primary-foreground transition-colors hover:bg-primary/90"
          >
            Start for free
          </Link>
          <Link
            href="#"
            className="inline-flex h-11 items-center justify-center rounded-md border border-border bg-background px-6 text-base font-medium text-primary transition-colors hover:bg-accent hover:text-accent-foreground"
          >
            Talk to sales
          </Link>
        </div>
      </div>
    </section>
  );
};

export default FinalCtaSection;