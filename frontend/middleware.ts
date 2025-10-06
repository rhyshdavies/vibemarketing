// import { authMiddleware } from "@clerk/nextjs"

// Temporarily disabled - add your Clerk API keys to .env.local to enable authentication
// export default authMiddleware({
//   publicRoutes: ["/", "/sign-in(.*)", "/sign-up(.*)"],
// })

export default function middleware() {
  // No-op middleware
}

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
}
