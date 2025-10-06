"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { Menu, X, ChevronDown, LogOut, User } from "lucide-react";
import { cn } from "@/lib/utils";
import { useAuth } from "@/contexts/AuthContext";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

const VibeLogo = () => (
  <span className="text-2xl font-bold tracking-tighter text-foreground">
    Vibe
  </span>
);

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const { user, logout } = useAuth();
  const router = useRouter();

  useEffect(() => {
    const originalStyle = window.getComputedStyle(document.body).overflow;
    if (isMenuOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = originalStyle;
    }
    return () => {
      document.body.style.overflow = originalStyle;
    };
  }, [isMenuOpen]);

  const handleLogout = async () => {
    try {
      await logout();
      toast.success("Logged out successfully");
      router.push("/");
    } catch (error) {
      toast.error("Failed to log out");
    }
  };

  const navItems = [
    { name: "Platform", href: "#", hasDropdown: true },
    { name: "Resources", href: "#", hasDropdown: true },
    { name: "Customers", href: "/customers", hasDropdown: false },
    { name: "Pricing", href: "/pricing", hasDropdown: false },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-border bg-background/95">
      <div className="absolute inset-0 -z-10 backdrop-blur-md" />
      <div className="container">
        <nav className="flex items-center justify-between pt-2 pb-[7px] lg:pt-4 lg:pb-[15px]">
          <div className="flex grow items-center gap-x-9">
            <Link
              href="/"
              className="-mx-1.5 rounded-xl px-1.5"
              onClick={() => setIsMenuOpen(false)}
            >
              <VibeLogo />
            </Link>
            <div className="relative z-10 hidden lg:block">
              <ul className="flex items-center gap-x-1.5">
                {navItems.map((item) => (
                  <li key={item.name}>
                    {item.hasDropdown ? (
                      <button className="group relative inline-flex h-9 cursor-pointer select-none items-center justify-center gap-x-1.5 rounded-[10px] border-transparent bg-transparent px-3 text-[15px] font-medium text-foreground transition-colors hover:bg-accent hover:text-accent-foreground">
                        <span>{item.name}</span>
                        <ChevronDown className="size-[18px] text-foreground/70 transition-transform duration-300 group-hover:text-foreground group-data-[state=open]:rotate-180" />
                      </button>
                    ) : (
                      <Link
                        href={item.href}
                        className="relative inline-flex h-9 cursor-pointer items-center justify-center rounded-[10px] border-transparent bg-transparent px-3 text-[15px] font-medium text-foreground transition-colors hover:bg-accent hover:text-accent-foreground"
                      >
                        {item.name}
                      </Link>
                    )}
                  </li>
                ))}
              </ul>
            </div>
          </div>

          <button
            onClick={() => setIsMenuOpen(!isMenuOpen)}
            className="relative inline-flex size-9 cursor-pointer items-center justify-center rounded-[10px] border-transparent bg-transparent text-foreground transition-colors lg:hidden"
            aria-label="Toggle menu"
          >
            {isMenuOpen ? <X className="size-6" /> : <Menu className="size-6" />}
          </button>

          <div className="hidden items-center gap-x-2.5 lg:flex">
            {user ? (
              <>
                <Link
                  href="/dashboard"
                  className="relative inline-flex h-9 cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-[10px] border border-border bg-transparent px-3 text-sm font-medium text-foreground transition-colors hover:bg-accent"
                >
                  <User className="h-4 w-4" />
                  Dashboard
                </Link>
                <button
                  onClick={handleLogout}
                  className="relative inline-flex h-9 cursor-pointer items-center justify-center gap-2 whitespace-nowrap rounded-[10px] border border-transparent bg-primary px-3 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                >
                  <LogOut className="h-4 w-4" />
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link
                  href="/sign-in"
                  className="relative inline-flex h-9 cursor-pointer items-center justify-center whitespace-nowrap rounded-[10px] border border-border bg-transparent px-3 text-sm font-medium text-foreground transition-colors hover:bg-accent"
                >
                  Sign in
                </Link>
                <Link
                  href="/sign-up"
                  className="relative inline-flex h-9 cursor-pointer items-center justify-center whitespace-nowrap rounded-[10px] border border-transparent bg-primary px-3 text-sm font-medium text-primary-foreground transition-colors hover:bg-primary/90"
                >
                  Get Started
                </Link>
              </>
            )}
          </div>
        </nav>
      </div>

      {isMenuOpen && (
        <div className="fixed inset-x-0 top-[calc(var(--site-header-height,60px))] z-40 h-[calc(100vh-var(--site-header-height,60px))] bg-background lg:hidden">
          <div className="container flex h-full flex-col px-6 pt-6 pb-8">
            <nav className="flex flex-col">
              {navItems.map((item, index) => (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    "flex items-center justify-between border-b border-border py-4 text-base font-medium text-foreground",
                    index === 0 && "border-t"
                  )}
                  onClick={() => setIsMenuOpen(false)}
                >
                  <span>{item.name}</span>
                  {item.hasDropdown && <ChevronDown className="size-5" />}
                </Link>
              ))}
            </nav>
            <div className="mt-auto flex flex-col gap-y-4">
              {user ? (
                <>
                  <Link
                    href="/dashboard"
                    className="flex h-12 w-full items-center justify-center gap-2 rounded-xl border border-border bg-transparent text-base font-medium text-foreground"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    <User className="h-5 w-5" />
                    Dashboard
                  </Link>
                  <button
                    onClick={() => {
                      handleLogout();
                      setIsMenuOpen(false);
                    }}
                    className="flex h-12 w-full items-center justify-center gap-2 rounded-xl bg-primary text-base font-medium text-primary-foreground"
                  >
                    <LogOut className="h-5 w-5" />
                    Logout
                  </button>
                </>
              ) : (
                <>
                  <Link
                    href="/sign-in"
                    className="flex h-12 w-full items-center justify-center rounded-xl border border-border bg-transparent text-base font-medium text-foreground"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Sign in
                  </Link>
                  <Link
                    href="/sign-up"
                    className="flex h-12 w-full items-center justify-center rounded-xl bg-primary text-base font-medium text-primary-foreground"
                    onClick={() => setIsMenuOpen(false)}
                  >
                    Get Started
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </header>
  );
};

export default Header;