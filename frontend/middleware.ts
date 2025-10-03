// Temporarily disabled Clerk authentication for testing
// Uncomment below and add your Clerk keys to .env.local to enable

/*
import { authMiddleware } from "@clerk/nextjs"

export default authMiddleware({
  publicRoutes: ["/"],
})

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
}
*/

// Temporary: Allow all routes without authentication
export default function middleware() {
  // No-op middleware
}

export const config = {
  matcher: ["/((?!.+\\.[\\w]+$|_next).*)", "/", "/(api|trpc)(.*)"],
}
