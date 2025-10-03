# ⚡ Action Items - Get Your App Running

## 🚨 The Error You're Seeing

```
InvalidCharacterError: The string to be decoded is not correctly encoded.
```

**Cause:** Clerk API keys in `frontend/.env.local` are placeholder values (`pk_test_xxxxx`)

**Solution:** Get real Clerk API keys (takes 2 minutes)

---

## 📋 To-Do List (In Order)

### 1️⃣ Get Clerk API Keys (Frontend Authentication)

**Time:** 2 minutes

1. Go to https://clerk.com
2. Sign up for free account
3. Create new application: "Vibe Marketing Autopilot"
4. Copy **Publishable key** (starts with `pk_test_`)
5. Copy **Secret key** (starts with `sk_test_`)

**Update `frontend/.env.local`:**
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_[your_actual_key_here]
CLERK_SECRET_KEY=sk_test_[your_actual_key_here]
```

📄 **Detailed Guide:** See `GET_CLERK_KEYS.md`

---

### 2️⃣ Get Instantly.ai API Key (Email Campaigns)

**Time:** 5 minutes

1. Go to https://instantly.ai
2. Sign up for account (they have a free trial)
3. Navigate to **Settings** → **API**
4. Click **Generate API Key**
5. Copy the key (starts with `inst_`)

**Update `backend/.env`:**
```bash
INSTANTLY_API_KEY=inst_[your_key_here]
```

---

### 3️⃣ Get OpenAI API Key (AI Copy Generation)

**Time:** 3 minutes

1. Go to https://platform.openai.com
2. Sign up or log in
3. Go to **API Keys** in left sidebar
4. Click **+ Create new secret key**
5. Name it "Vibe Marketing"
6. Copy the key (starts with `sk-`)

**Update `backend/.env`:**
```bash
OPENAI_API_KEY=sk-[your_key_here]
```

**Note:** You'll need to add a payment method (costs ~$5/month for testing)

---

### 4️⃣ Setup Supabase Database

**Time:** 5 minutes

1. Go to https://supabase.com
2. Create new project
3. Wait for setup (~2 minutes)
4. Go to **Settings** → **API**
5. Copy **URL** and **anon/public** key

**Update `backend/.env`:**
```bash
SUPABASE_URL=https://[your-project].supabase.co
SUPABASE_KEY=eyJhbGc[your_key_here]
```

6. Go to **SQL Editor**
7. Copy SQL from `SETUP_GUIDE.md` (Step 2.1)
8. Click **Run** to create tables

---

### 5️⃣ Start the Servers

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

Should see:
```
✅ Starting FastAPI server on http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

Should see:
```
✓ Ready in 2.5s
○ Local:        http://localhost:3000
```

---

### 6️⃣ Test the Application

1. **Open browser:** http://localhost:3000
2. **Click "Get Started"**
3. **Sign up with your email**
4. **Create a test campaign:**
   - URL: `https://yourapp.com`
   - Target: `SaaS founders, 1-10 employees`
5. **Wait 10-15 seconds** for AI to generate copy
6. **Review variants** and click "Launch Campaign"
7. **Check Instantly.ai dashboard** to see the campaign

---

## 🎯 Priority Order

### Must Have (App Won't Work Without These):
1. ✅ Clerk keys → Frontend authentication
2. ✅ Instantly keys → Email campaigns
3. ✅ OpenAI keys → AI copy generation
4. ✅ Supabase setup → Database

### Nice to Have (For Full Testing):
- Warmed email account in Instantly.ai
- Test leads (CSV or manual)
- Production deployment

---

## 🚀 Quick Path: Test Backend First

Don't want to get Clerk keys right now? Test the backend API:

```bash
# 1. Get Instantly, OpenAI, and Supabase keys
# 2. Add them to backend/.env
# 3. Start backend
./start-backend.sh

# 4. Test with cURL
curl -X POST http://localhost:8000/api/create-campaign \
  -H "Content-Type: application/json" \
  -d '{"url":"https://test.com","target_audience":"test","user_id":"test"}'
```

See `QUICK_TEST_WITHOUT_CLERK.md` for details.

---

## 📊 Time Estimate

| Task | Time | Difficulty |
|------|------|------------|
| Get Clerk keys | 2 min | Easy |
| Get Instantly keys | 5 min | Easy |
| Get OpenAI keys | 3 min | Easy |
| Setup Supabase | 5 min | Medium |
| Start servers | 1 min | Easy |
| Test app | 5 min | Easy |
| **Total** | **~20 minutes** | |

---

## 💰 Cost Summary

| Service | Free Tier | Paid Tier |
|---------|-----------|-----------|
| Clerk | 10k MAU | $25/mo |
| Instantly.ai | 7-day trial | $37-97/mo |
| OpenAI | $5 credit | Pay as you go (~$5/mo testing) |
| Supabase | 500MB + 2GB storage | Free |
| Vercel (deploy) | Unlimited | Free |
| Railway (deploy) | 500 hours | Free/$5/mo |

**First month cost:** ~$42 (Instantly trial + OpenAI)

---

## ✅ Checklist

Copy this to track your progress:

```
□ Clerk account created
□ Clerk keys added to frontend/.env.local
□ Instantly.ai account created
□ Instantly API key added to backend/.env
□ OpenAI account created
□ OpenAI API key added to backend/.env
□ Supabase project created
□ Supabase URL and key added to backend/.env
□ Supabase tables created (SQL executed)
□ Backend started successfully
□ Frontend started successfully
□ Tested sign-up flow
□ Created test campaign
□ Verified campaign in Instantly.ai
```

---

## 🆘 Still Stuck?

1. **Check the error logs** in terminal
2. **Read relevant guide:**
   - Frontend error → `GET_CLERK_KEYS.md`
   - Backend error → `SETUP_GUIDE.md`
   - API testing → `QUICK_TEST_WITHOUT_CLERK.md`
3. **Verify all environment variables** are set correctly
4. **Restart both servers** after changing `.env` files

---

## 🎉 Once Everything Works

You'll have:
- ✅ Full-stack MVP running locally
- ✅ AI-powered email copy generation
- ✅ Automated campaign creation
- ✅ Real-time analytics dashboard
- ✅ Ready to deploy to production

**Start with Step 1 (Get Clerk Keys) and work your way down! 🚀**
