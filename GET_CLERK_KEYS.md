# 🔑 How to Get Your Clerk API Keys

## Quick Fix for the Error

The error you're seeing means you need to add your actual Clerk API keys to `.env.local`.

---

## Step-by-Step: Get Clerk Keys

### 1. Go to Clerk Dashboard

Visit: https://clerk.com

### 2. Sign Up or Log In

- If you don't have an account, click "Start building for free"
- Sign up with email or GitHub

### 3. Create a New Application

Once logged in:
1. Click **"+ Create application"** button
2. Give it a name: `Vibe Marketing Autopilot`
3. Choose sign-in options:
   - ✅ Email
   - ✅ Google (optional)
4. Click **"Create application"**

### 4. Copy Your API Keys

You'll see a setup screen with your keys:

**Publishable key** (starts with `pk_placeholder_`)
```
pk_placeholder_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**Secret key** (starts with `sk_placeholder_`)
```
sk_placeholder_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### 5. Update .env.local

Edit `frontend/.env.local`:

```bash
# API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Clerk Authentication
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_placeholder_YOUR_ACTUAL_KEY_HERE
CLERK_SECRET_KEY=sk_placeholder_YOUR_ACTUAL_KEY_HERE
```

**Important:** Replace the entire key, including `pk_placeholder_xxxxx` → `pk_placeholder_your_real_key...`

---

## Alternative: Run Without Authentication (For Testing)

If you just want to test the app quickly without Clerk:

### Option 1: Temporarily Disable Clerk

Edit `frontend/app/layout.tsx`:

**Before:**
```typescript
import { ClerkProvider } from '@clerk/nextjs'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <ClerkProvider>
      <html lang="en">
        <body className={inter.className}>
          {children}
          <Toaster position="top-right" />
        </body>
      </html>
    </ClerkProvider>
  )
}
```

**After:**
```typescript
// import { ClerkProvider } from '@clerk/nextjs'  // Comment out

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    // Remove ClerkProvider wrapper
    <html lang="en">
      <body className={inter.className}>
        {children}
        <Toaster position="top-right" />
      </body>
    </html>
  )
}
```

### Option 2: Use Mock Keys (Not Recommended for Production)

Just for local testing, you can temporarily use these test values:

```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_placeholder_Y2xlcmsuaW5zcGlyZWQuZ3Vlc3MtMy5sY2wuZGV2JA
CLERK_SECRET_KEY=sk_placeholder_Y2xlcmsuaW5zcGlyZWQuZ3Vlc3MtMy5sY2wuZGV2JA
```

**Note:** These are example keys and won't actually work for authentication.

---

## Verification

After adding real Clerk keys:

1. **Restart the frontend:**
   ```bash
   # Stop the server (Ctrl+C)
   npm run dev
   ```

2. **Visit http://localhost:3000**
   - The error should be gone
   - You should see the landing page

3. **Test Authentication:**
   - Click "Get Started" or "Sign Up"
   - You should see Clerk's sign-up modal
   - Enter your email to test

---

## Common Issues

### "Invalid publishable key"

**Cause:** Key is malformed or incomplete
**Fix:** Make sure you copied the entire key from Clerk dashboard

### "Clerk API key not found"

**Cause:** Environment variable not loaded
**Fix:**
```bash
# Restart the dev server
cd frontend
npm run dev
```

### "Domain not allowed"

**Cause:** localhost not in Clerk's allowed domains
**Fix:**
1. Go to Clerk dashboard
2. Navigate to **"Configure" → "Domains"**
3. Make sure `localhost:3000` is allowed

---

## For Production

When deploying to production:

1. **Get Production Keys:**
   - In Clerk dashboard, go to your app
   - Switch from "Development" to "Production" environment
   - Copy the **production keys** (start with `pk_live_` and `sk_live_`)

2. **Update Vercel Environment Variables:**
   ```
   NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_live_your_production_key
   CLERK_SECRET_KEY=sk_live_your_production_key
   ```

3. **Add Production Domain:**
   - In Clerk dashboard → Domains
   - Add your production domain (e.g., `vibemarketing.vercel.app`)

---

## Quick Links

- **Clerk Dashboard:** https://dashboard.clerk.com
- **Clerk Docs:** https://clerk.com/docs
- **Next.js + Clerk Guide:** https://clerk.com/docs/quickstarts/nextjs

---

## Summary

1. Go to https://clerk.com
2. Create account + application
3. Copy publishable key (pk_placeholder_...)
4. Copy secret key (sk_placeholder_...)
5. Paste into `frontend/.env.local`
6. Restart dev server
7. ✅ Error should be gone!

**The free tier allows up to 10,000 monthly active users - perfect for testing!**
