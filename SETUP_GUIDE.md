# 🚀 Setup Guide - Vibe Marketing Autopilot

Complete step-by-step guide to get your Vibe Marketing Autopilot MVP up and running.

## 📋 Prerequisites Checklist

Before you begin, make sure you have:

- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] A code editor (VS Code recommended)

## 🔑 Step 1: Get Your API Keys

You'll need API keys from these services. Set them up in this order:

### 1.1 Instantly.ai

1. Go to [instantly.ai](https://instantly.ai)
2. Sign up for an account (they have a free trial)
3. Navigate to **Settings** → **API**
4. Click **Generate API Key**
5. Copy the key (starts with `inst_`)

💡 **Tip**: Instantly.ai is the core service that sends emails. Without it, campaigns won't work.

### 1.2 OpenAI

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up/login
3. Click on **API Keys** in the left sidebar
4. Click **+ Create new secret key**
5. Name it "Vibe Marketing" and copy the key (starts with `sk-`)

💡 **Tip**: You'll need to add billing info, but GPT-4 usage for email generation costs pennies.

### 1.3 Supabase

1. Go to [supabase.com](https://supabase.com)
2. Sign up and create a new project
3. Wait for project setup (2-3 minutes)
4. Go to **Settings** → **API**
5. Copy these values:
   - Project URL (looks like `https://xxxxx.supabase.co`)
   - `anon/public` key (starts with `eyJ`)

💡 **Tip**: Supabase is free for the MVP. Don't use the `service_role` key - only use `anon`.

### 1.4 Clerk (Authentication)

1. Go to [clerk.com](https://clerk.com)
2. Sign up and create a new application
3. Choose **Email** and **Google** as sign-in options
4. Go to **API Keys** in the dashboard
5. Copy:
   - Publishable Key (starts with `pk_test_` or `pk_live_`)
   - Secret Key (starts with `sk_test_` or `sk_live_`)

💡 **Tip**: Clerk handles all authentication. Use test keys for development.

---

## 🗄️ Step 2: Setup Database (Supabase)

### 2.1 Create Tables

In your Supabase project:

1. Go to **SQL Editor**
2. Click **+ New query**
3. Run this SQL:

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  name TEXT,
  plan TEXT DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW()
);

-- Campaigns table
CREATE TABLE campaigns (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  url TEXT NOT NULL,
  target_audience TEXT NOT NULL,
  copy_variants JSONB,
  status TEXT DEFAULT 'active',
  sent INTEGER DEFAULT 0,
  opened INTEGER DEFAULT 0,
  clicked INTEGER DEFAULT 0,
  replied INTEGER DEFAULT 0,
  bounced INTEGER DEFAULT 0,
  open_rate FLOAT DEFAULT 0,
  click_rate FLOAT DEFAULT 0,
  reply_rate FLOAT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Email accounts table
CREATE TABLE email_accounts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  email TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  warmup_enabled BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Lead lists table
CREATE TABLE lead_lists (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  leads JSONB,
  total_leads INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

4. Click **Run** to execute

### 2.2 Setup Row Level Security (RLS)

For security, enable RLS:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaigns ENABLE ROW LEVEL SECURITY;
ALTER TABLE email_accounts ENABLE ROW LEVEL SECURITY;
ALTER TABLE lead_lists ENABLE ROW LEVEL SECURITY;

-- Create policies to allow authenticated access
CREATE POLICY "Users can read own data" ON users
  FOR SELECT USING (true);

CREATE POLICY "Users can insert own data" ON users
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can read own campaigns" ON campaigns
  FOR SELECT USING (true);

CREATE POLICY "Users can create campaigns" ON campaigns
  FOR INSERT WITH CHECK (true);

CREATE POLICY "Users can update own campaigns" ON campaigns
  FOR UPDATE USING (true);

-- Similar policies for other tables
CREATE POLICY "Users can manage email accounts" ON email_accounts
  FOR ALL USING (true);

CREATE POLICY "Users can manage lead lists" ON lead_lists
  FOR ALL USING (true);
```

---

## 💻 Step 3: Install & Run Backend

### 3.1 Navigate to Backend

```bash
cd backend
```

### 3.2 Create Virtual Environment

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal.

### 3.3 Install Dependencies

```bash
pip install -r requirements.txt
```

### 3.4 Setup Environment Variables

```bash
cp .env.example .env
```

Now edit `.env` file with your API keys:

```bash
INSTANTLY_API_KEY=inst_your_key_here
OPENAI_API_KEY=sk-your_key_here
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGc...your_key_here
```

### 3.5 Run Backend

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

✅ **Success**: You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

Test it: Open [http://localhost:8000](http://localhost:8000) - you should see:
```json
{"message": "Vibe Marketing Autopilot API", "status": "active"}
```

---

## 🎨 Step 4: Install & Run Frontend

### 4.1 Open New Terminal

Keep backend running. Open a new terminal window.

### 4.2 Navigate to Frontend

```bash
cd frontend
```

### 4.3 Install Dependencies

```bash
npm install
```

This takes 1-2 minutes.

### 4.4 Setup Environment Variables

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_your_key_here
CLERK_SECRET_KEY=sk_test_your_key_here
```

### 4.5 Run Frontend

```bash
npm run dev
```

✅ **Success**: You should see:
```
- ready started server on 0.0.0.0:3000, url: http://localhost:3000
```

Open [http://localhost:3000](http://localhost:3000)

---

## 🎉 Step 5: Test the Application

### 5.1 Sign Up

1. Click **Get Started** button
2. Enter your email
3. Check email for verification code
4. Complete signup

### 5.2 Create Your First Campaign

1. Click **Create Campaign**
2. Enter:
   - **URL**: `https://yourapp.com`
   - **Target Audience**: `SaaS founders, 1-10 employees, US-based`
3. Click **Generate Campaign**
4. Wait 10-15 seconds for AI to generate copy
5. Review the 3 email variants
6. Click **Launch Campaign**

### 5.3 Check Instantly.ai

1. Log into your Instantly.ai account
2. Go to **Campaigns**
3. You should see your new campaign!

---

## 🐛 Troubleshooting

### Backend won't start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Fix**: Make sure you activated the virtual environment:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

---

**Error**: `Port 8000 already in use`

**Fix**: Kill the process using port 8000:
```bash
# Mac/Linux
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Frontend won't start

**Error**: `Module not found` errors

**Fix**:
```bash
rm -rf node_modules package-lock.json
npm install
```

---

**Error**: Clerk authentication not working

**Fix**:
1. Check `.env.local` has correct Clerk keys
2. Make sure keys start with `pk_test_` and `sk_test_`
3. Restart the dev server: `Ctrl+C` then `npm run dev`

---

### Database Issues

**Error**: `relation "campaigns" does not exist`

**Fix**: Run the SQL commands from Step 2.1 in Supabase SQL Editor

---

**Error**: `permission denied for table campaigns`

**Fix**: Run the RLS policies from Step 2.2

---

### API Integration Issues

**Error**: Campaign created but no emails sent

**Check**:
1. Instantly.ai API key is correct
2. You have a warmed email account in Instantly
3. Check Instantly dashboard for errors

---

## 📚 Next Steps

Once everything is working:

1. **Add leads**: Upload a CSV of leads in Instantly.ai
2. **Monitor analytics**: Check the dashboard daily
3. **Customize**: Edit email templates in the code
4. **Deploy**: Follow deployment guide in README.md

---

## 🆘 Still Having Issues?

1. Check all API keys are correct
2. Make sure both backend and frontend are running
3. Check browser console for errors (F12)
4. Check backend logs in terminal
5. Open a GitHub issue with error details

---

## 🎓 Understanding the Flow

1. **User creates campaign** → Frontend sends to `/api/create-campaign`
2. **Backend generates AI copy** → Calls OpenAI API
3. **Backend creates campaign** → Calls Instantly.ai API
4. **Backend saves to DB** → Stores in Supabase
5. **User views dashboard** → Backend fetches from Instantly + Supabase
6. **Emails send** → Instantly.ai handles sending automatically

---

**That's it! You're ready to automate your cold outreach! 🚀**
