# ⚡ Quick Start Guide

Get Vibe Marketing Autopilot running in 5 minutes!

## Prerequisites

- Python 3.9+ installed
- Node.js 18+ installed
- API keys ready (see SETUP_GUIDE.md for details)

## 🚀 Fast Setup

### Step 1: Clone & Install

```bash
# Clone the repo (if not already done)
cd vibemarketing

# Install backend dependencies
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
cd frontend
npm install
cd ..
```

### Step 2: Configure Environment Variables

**Backend (.env):**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your keys
```

**Frontend (.env.local):**
```bash
cp frontend/.env.local.example frontend/.env.local
# Edit frontend/.env.local with your keys
```

### Step 3: Setup Database

1. Go to your Supabase project
2. Open SQL Editor
3. Copy and run the SQL from `SETUP_GUIDE.md` Step 2.1

### Step 4: Run the App

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

### Step 5: Test It!

Open [http://localhost:3000](http://localhost:3000)

1. Sign up with your email
2. Click "Create Campaign"
3. Fill in your URL and target audience
4. Watch AI generate your email copy!

---

## 📝 Required API Keys

You need these 4 keys:

1. **Instantly.ai** - Get from instantly.ai → Settings → API
2. **OpenAI** - Get from platform.openai.com → API Keys
3. **Supabase** - Get from supabase.com → Project → Settings → API
4. **Clerk** - Get from clerk.com → Your App → API Keys

---

## 🆘 Troubleshooting

**Backend won't start:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend won't start:**
```bash
cd frontend
rm -rf node_modules .next
npm install
```

**Database errors:**
- Make sure you ran the SQL commands in Supabase
- Check your SUPABASE_URL and SUPABASE_KEY

---

## 📚 Next Steps

- Read `SETUP_GUIDE.md` for detailed setup instructions
- Read `README.md` for full documentation
- Check out the API endpoints
- Deploy to production (Vercel + Railway)

---

**Need help?** Open an issue on GitHub!
