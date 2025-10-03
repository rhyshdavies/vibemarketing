# 🚀 Vibe Marketing Autopilot

**AI-powered cold outreach automation for indie founders**

Paste your URL, define your audience, and watch AI build + launch your cold email campaign in minutes.

## 🎯 What This Does

1. **Input**: User provides a website/app URL + target audience description (ICP)
2. **AI Generation**: Generates 3 A/B tested email variants using GPT-4
3. **Campaign Setup**: Creates campaign in Instantly.ai with leads
4. **Analytics**: Real-time dashboard showing opens, clicks, replies, booked calls

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Python web framework
- **Instantly.ai API v2** - Email campaign management (updated to v2)
- **OpenAI API** - AI copy generation (GPT-4)
- **Supabase** - Database (Postgres)

### Frontend
- **Next.js 14** - React framework with App Router
- **Clerk** - Authentication
- **Tailwind CSS** - Styling
- **Recharts** - Analytics visualization

## 📦 Project Structure

```
vibe-marketing-autopilot/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── main.py         # Main API routes
│   │   ├── services/
│   │   │   ├── instantly.py    # Instantly.ai integration
│   │   │   ├── ai_copy.py      # OpenAI integration
│   │   │   └── supabase_service.py  # Database service
│   │   └── models/         # Data models
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/               # Next.js frontend
│   ├── app/
│   │   ├── page.tsx       # Landing page
│   │   ├── dashboard/     # Dashboard pages
│   │   └── layout.tsx     # Root layout
│   ├── components/
│   │   ├── CampaignForm.tsx   # Campaign creation
│   │   └── Dashboard.tsx      # Analytics dashboard
│   ├── package.json
│   └── .env.local.example
│
└── README.md
```

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- Node.js 18+
- Instantly.ai account + API key
- OpenAI API key
- Supabase account
- Clerk account (for auth)

### 1. Clone & Setup

```bash
git clone <your-repo>
cd vibe-marketing-autopilot
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env with your API keys
```

**Required Environment Variables:**

```bash
INSTANTLY_API_KEY=your_instantly_api_key
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

**Run the backend:**

```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: `http://localhost:8000`

### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Setup environment variables
cp .env.local.example .env.local
# Edit .env.local with your keys
```

**Required Environment Variables:**

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
CLERK_SECRET_KEY=sk_test_xxxxx
```

**Run the frontend:**

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

### 4. Database Setup (Supabase)

Create these tables in your Supabase project:

**campaigns table:**
```sql
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
```

**email_accounts table:**
```sql
CREATE TABLE email_accounts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  email TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  warmup_enabled BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT NOW()
);
```

**users table:**
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT UNIQUE NOT NULL,
  email TEXT NOT NULL,
  name TEXT,
  plan TEXT DEFAULT 'free',
  created_at TIMESTAMP DEFAULT NOW()
);
```

**lead_lists table:**
```sql
CREATE TABLE lead_lists (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id TEXT NOT NULL,
  campaign_id TEXT NOT NULL,
  leads JSONB,
  total_leads INTEGER DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW()
);
```

## 📝 API Endpoints

### POST `/api/create-campaign`
Create a new campaign with AI-generated copy

**Request:**
```json
{
  "url": "https://yourapp.com",
  "target_audience": "SaaS founders, 1-10 employees, US",
  "user_id": "user_123",
  "leads_csv": "optional_csv_data"
}
```

**Response:**
```json
{
  "success": true,
  "campaign_id": "campaign_123",
  "lead_list_id": "list_123",
  "variants": [
    {"subject": "...", "body": "..."},
    {"subject": "...", "body": "..."},
    {"subject": "...", "body": "..."}
  ]
}
```

### GET `/api/analytics/{campaign_id}`
Get campaign analytics

**Response:**
```json
{
  "success": true,
  "analytics": {
    "sent": 100,
    "opened": 45,
    "clicked": 12,
    "replied": 8,
    "open_rate": 45.0,
    "click_rate": 26.7,
    "reply_rate": 8.0
  }
}
```

### GET `/api/campaigns?user_id={user_id}`
Get all campaigns for a user

## 🚢 Deployment

### Backend Deployment (Railway / Render)

**Railway:**
1. Connect your GitHub repo
2. Add environment variables
3. Deploy automatically

**Render:**
1. Create new Web Service
2. Connect repo, select `backend` directory
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Frontend Deployment (Vercel)

```bash
cd frontend
vercel
```

Or connect your GitHub repo to Vercel for automatic deployments.

**Don't forget to add environment variables in Vercel dashboard!**

## 🎨 Features

### MVP Features (Included)
✅ User authentication (Clerk)
✅ Campaign creation form
✅ AI copy generation (3 variants)
✅ Instantly.ai integration
✅ Analytics dashboard
✅ Campaign management

### Future Enhancements
- [ ] CSV lead upload
- [ ] Clay/Apollo API integration for lead sourcing
- [ ] LinkedIn outreach (Expandi.io)
- [ ] Reddit automation
- [ ] Email scheduling
- [ ] Advanced A/B testing
- [ ] Stripe billing
- [ ] Team collaboration

## 🔑 Getting API Keys

### Instantly.ai
1. Sign up at [instantly.ai](https://instantly.ai)
2. Go to Settings → API
3. Generate API key

### OpenAI
1. Sign up at [platform.openai.com](https://platform.openai.com)
2. Go to API Keys
3. Create new secret key

### Supabase
1. Create project at [supabase.com](https://supabase.com)
2. Go to Settings → API
3. Copy URL and anon/public key

### Clerk
1. Create application at [clerk.com](https://clerk.com)
2. Copy publishable key and secret key

## 🐛 Troubleshooting

**Backend won't start:**
- Check Python version (3.9+)
- Verify all environment variables are set
- Check if port 8000 is available

**Frontend won't start:**
- Run `npm install` again
- Check Node version (18+)
- Clear `.next` folder: `rm -rf .next`

**Database errors:**
- Verify Supabase tables are created
- Check Supabase connection URL
- Ensure RLS policies allow operations

## 📄 License

MIT License - Feel free to use for your own projects!

## 🤝 Contributing

PRs welcome! This is an MVP so there's lots of room for improvement.

## 💬 Support

For issues or questions, open a GitHub issue or contact the maintainers.

---

Built with ⚡ by indie founders, for indie founders.
