# 🏗️ System Architecture

Visual overview of how Vibe Marketing Autopilot works.

---

## 📐 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER BROWSER                             │
│                    (http://localhost:3000)                       │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ HTTPS
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      NEXT.JS FRONTEND                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Landing     │  │  Dashboard   │  │  Campaign    │          │
│  │  Page        │  │  Page        │  │  Form        │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│  Authentication: Clerk                                           │
│  Styling: Tailwind CSS                                           │
│  State: React Hooks                                              │
└──────────────────────────────┬──────────────────────────────────┘
                               │
                               │ REST API (JSON)
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│                      FASTAPI BACKEND                             │
│                   (http://localhost:8000)                        │
│  ┌──────────────────────────────────────────────────┐           │
│  │              API ROUTES                          │           │
│  │  /api/create-campaign                            │           │
│  │  /api/analytics/{id}                             │           │
│  │  /api/campaigns                                  │           │
│  └──────────────────────────────────────────────────┘           │
│                       │                                          │
│  ┌────────────────────┼────────────────────┐                    │
│  │                    │                    │                    │
│  ▼                    ▼                    ▼                    │
│  ┌─────────┐    ┌──────────┐    ┌──────────────┐              │
│  │Instantly│    │  OpenAI  │    │  Supabase    │              │
│  │Service  │    │  Service │    │  Service     │              │
│  └─────────┘    └──────────┘    └──────────────┘              │
└────────┬──────────────┬────────────────┬───────────────────────┘
         │              │                │
         ▼              ▼                ▼
┌────────────┐  ┌──────────────┐  ┌────────────────┐
│ Instantly  │  │   OpenAI     │  │   Supabase     │
│    API     │  │     API      │  │   Database     │
│            │  │              │  │   (Postgres)   │
└────────────┘  └──────────────┘  └────────────────┘
```

---

## 🔄 Data Flow: Creating a Campaign

```
1. USER INPUT
   │
   ├─ URL: "https://myapp.com"
   └─ ICP: "SaaS founders, 1-10 employees"

2. FRONTEND (Next.js)
   │
   ├─ User fills CampaignForm.tsx
   ├─ Validates input
   └─ POST /api/create-campaign

3. BACKEND (FastAPI)
   │
   ├─ Receives request
   ├─ Extracts user_id from Clerk
   └─ Processes in 4 steps:

   STEP 1: Generate AI Copy
   │
   ├─ Call ai_copy.py service
   ├─ Send prompt to OpenAI GPT-4
   ├─ Parse JSON response
   └─ Return 3 variants:
       ├─ Variant 1: Problem-focused
       ├─ Variant 2: Benefit-focused
       └─ Variant 3: Question-based

   STEP 2: Create Lead List
   │
   ├─ Call instantly.py service
   ├─ POST to Instantly API
   └─ Return lead_list_id

   STEP 3: Create Campaign
   │
   ├─ Call instantly.py service
   ├─ POST to Instantly API with variants
   ├─ Set up A/B testing
   └─ Return campaign_id

   STEP 4: Save to Database
   │
   ├─ Call supabase_service.py
   ├─ INSERT into campaigns table
   └─ Return db_record

4. RESPONSE TO FRONTEND
   │
   ├─ campaign_id
   ├─ lead_list_id
   ├─ variants array
   └─ db_record

5. FRONTEND UPDATES
   │
   ├─ Show success message
   ├─ Display variants for review
   └─ Update dashboard
```

---

## 🗂️ Database Schema

```
┌──────────────────────────────────────────────┐
│                 USERS                        │
├──────────────────────────────────────────────┤
│ id (UUID)                    PK              │
│ user_id (TEXT)               UNIQUE          │
│ email (TEXT)                                 │
│ name (TEXT)                                  │
│ plan (TEXT)                  DEFAULT 'free'  │
│ created_at (TIMESTAMP)                       │
└──────────────────────────────────────────────┘
                    │
                    │ 1:N
                    ▼
┌──────────────────────────────────────────────┐
│              CAMPAIGNS                       │
├──────────────────────────────────────────────┤
│ id (UUID)                    PK              │
│ user_id (TEXT)               FK → users      │
│ campaign_id (TEXT)                           │
│ url (TEXT)                                   │
│ target_audience (TEXT)                       │
│ copy_variants (JSONB)                        │
│ status (TEXT)                                │
│ sent (INTEGER)                               │
│ opened (INTEGER)                             │
│ clicked (INTEGER)                            │
│ replied (INTEGER)                            │
│ open_rate (FLOAT)                            │
│ click_rate (FLOAT)                           │
│ reply_rate (FLOAT)                           │
│ created_at (TIMESTAMP)                       │
│ updated_at (TIMESTAMP)                       │
└──────────────────────────────────────────────┘
                    │
                    │ 1:N
                    ▼
┌──────────────────────────────────────────────┐
│             LEAD_LISTS                       │
├──────────────────────────────────────────────┤
│ id (UUID)                    PK              │
│ user_id (TEXT)               FK → users      │
│ campaign_id (TEXT)           FK → campaigns  │
│ leads (JSONB)                                │
│ total_leads (INTEGER)                        │
│ created_at (TIMESTAMP)                       │
└──────────────────────────────────────────────┘

┌──────────────────────────────────────────────┐
│           EMAIL_ACCOUNTS                     │
├──────────────────────────────────────────────┤
│ id (UUID)                    PK              │
│ user_id (TEXT)               FK → users      │
│ email (TEXT)                                 │
│ status (TEXT)                                │
│ warmup_enabled (BOOLEAN)                     │
│ created_at (TIMESTAMP)                       │
└──────────────────────────────────────────────┘
```

---

## 🔌 API Integration Flow

### OpenAI Integration

```
FastAPI Backend
      │
      ├─ ai_copy.py
      │     │
      │     ├─ Build prompt with URL + ICP
      │     │
      │     └─ POST https://api.openai.com/v1/chat/completions
      │           │
      │           ├─ Headers: Authorization: Bearer sk-xxx
      │           │
      │           ├─ Body:
      │           │    {
      │           │      "model": "gpt-4",
      │           │      "messages": [...],
      │           │      "temperature": 0.8
      │           │    }
      │           │
      │           └─ Response:
      │                {
      │                  "choices": [{
      │                    "message": {
      │                      "content": "[{subject, body}, ...]"
      │                    }
      │                  }]
      │                }
      │
      └─ Parse JSON and return variants
```

### Instantly.ai Integration

```
FastAPI Backend
      │
      ├─ instantly.py
      │     │
      │     ├─ CREATE CAMPAIGN
      │     │    └─ POST https://api.instantly.ai/api/v1/campaign/launch
      │     │          {
      │     │            "api_key": "inst_xxx",
      │     │            "name": "Launch - myapp.com",
      │     │            "subject": "...",
      │     │            "body": "..."
      │     │          }
      │     │
      │     ├─ UPLOAD LEADS
      │     │    └─ POST https://api.instantly.ai/api/v1/lead/add
      │     │          {
      │     │            "api_key": "inst_xxx",
      │     │            "campaign_name": "...",
      │     │            "email": "lead@company.com",
      │     │            "first_name": "John"
      │     │          }
      │     │
      │     └─ GET ANALYTICS
      │          └─ GET https://api.instantly.ai/api/v1/analytics/campaign
      │                ?api_key=inst_xxx&name=campaign_name
      │                └─ Returns: sent, opened, clicked, replied
```

---

## 🔐 Authentication Flow (Clerk)

```
1. User clicks "Sign Up"
   │
   ▼
2. Clerk Modal Opens
   │
   ├─ User enters email
   │
   └─ Clerk sends verification code

3. User enters code
   │
   ▼
4. Clerk creates user
   │
   ├─ Returns user object
   │    └─ { id, email, firstName, ... }
   │
   └─ Sets session cookie

5. Next.js middleware checks auth
   │
   ├─ If authenticated → Allow access
   │
   └─ If not → Redirect to /

6. Frontend uses user.id
   │
   └─ Sends as user_id in API requests
```

---

## 📊 Analytics Update Flow

```
User opens Dashboard
   │
   ▼
Frontend: Dashboard.tsx
   │
   ├─ useEffect hook triggers
   │
   └─ GET /api/campaigns?user_id=xxx

Backend: FastAPI
   │
   ├─ Query Supabase for user's campaigns
   │
   ├─ For each campaign:
   │    │
   │    └─ GET analytics from Instantly API
   │         │
   │         ├─ Parse response
   │         │
   │         └─ Update Supabase with latest stats
   │
   └─ Return campaigns array

Frontend receives data
   │
   ├─ Calculate aggregate stats
   │
   ├─ Render StatCards
   │
   ├─ Render BarChart
   │
   └─ Render campaigns table
```

---

## 🚀 Deployment Architecture

```
┌────────────────────────────────────────────────────┐
│                   USERS                            │
│            (browsers worldwide)                    │
└─────────────────────┬──────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│              VERCEL CDN                            │
│           (Next.js Frontend)                       │
│  ┌──────────────────────────────────────────┐     │
│  │  Static pages cached globally            │     │
│  │  Dynamic pages rendered on edge          │     │
│  └──────────────────────────────────────────┘     │
└─────────────────────┬──────────────────────────────┘
                      │
                      ▼
┌────────────────────────────────────────────────────┐
│        RAILWAY / RENDER                            │
│         (FastAPI Backend)                          │
│  ┌──────────────────────────────────────────┐     │
│  │  Docker container                        │     │
│  │  Auto-scaling                            │     │
│  │  Health checks                           │     │
│  └──────────────────────────────────────────┘     │
└─────────────┬───────────┬──────────────┬───────────┘
              │           │              │
              ▼           ▼              ▼
     ┌──────────┐  ┌──────────┐  ┌──────────────┐
     │Instantly │  │  OpenAI  │  │  Supabase    │
     │   API    │  │   API    │  │  (Postgres)  │
     └──────────┘  └──────────┘  └──────────────┘
```

---

## 🔄 State Management

```
FRONTEND STATE (React Hooks)

┌─────────────────────────────────────┐
│         CampaignForm.tsx            │
├─────────────────────────────────────┤
│ useState:                           │
│  - url                              │
│  - targetAudience                   │
│  - loading                          │
│  - generatedCopy                    │
│  - step ('input'|'review'|'success')│
│  - campaignId                       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│          Dashboard.tsx              │
├─────────────────────────────────────┤
│ useState:                           │
│  - campaigns                        │
│  - stats                            │
│  - loading                          │
│                                     │
│ useEffect:                          │
│  - loadDashboardData()              │
│    (runs on mount & user change)   │
└─────────────────────────────────────┘

BACKEND STATE (Stateless)

- No session state stored
- All data in Supabase
- User ID from Clerk on each request
```

---

## 🛡️ Security Layers

```
┌─────────────────────────────────────────┐
│  1. NETWORK LAYER                       │
│     - HTTPS only                        │
│     - CORS configured                   │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  2. AUTHENTICATION LAYER                │
│     - Clerk middleware                  │
│     - Protected routes                  │
│     - Session validation                │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  3. API LAYER                           │
│     - User ID validation                │
│     - Input validation (Pydantic)       │
│     - Error handling                    │
└─────────────────┬───────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────┐
│  4. DATABASE LAYER                      │
│     - Row Level Security (RLS)          │
│     - Query parameterization            │
│     - Access policies                   │
└─────────────────────────────────────────┘
```

---

## 📈 Scaling Considerations

### Current Limits
- **Backend**: ~100 requests/min
- **Database**: 500MB (free tier)
- **OpenAI**: 3,500 requests/min
- **Instantly**: 100 requests/min

### Scale to 1,000 users
```
Users: 1,000
Campaigns per user: 5
Total campaigns: 5,000

Backend:
  - Add caching (Redis)
  - Horizontal scaling
  - Load balancer

Database:
  - Upgrade to Pro ($25/mo)
  - Add indexes
  - Query optimization

APIs:
  - Queue system (Celery/Redis)
  - Rate limit handling
  - Retry logic
```

---

## 🔧 Technology Choices

| Component | Technology | Why? |
|-----------|-----------|------|
| Backend | FastAPI | Fast, modern, async, type hints |
| Frontend | Next.js 14 | SSR, App Router, React 18 |
| Database | Supabase | Postgres + API + Auth + Free tier |
| Auth | Clerk | Easy setup, great UX, free tier |
| Styling | Tailwind | Utility-first, fast development |
| Email API | Instantly.ai | Purpose-built for cold email |
| AI | OpenAI GPT-4 | Best for creative copy |
| Hosting | Vercel + Railway | Easy deployment, free tiers |

---

## 📝 File Structure

```
vibemarketing/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── main.py            # Routes & app init
│   │   ├── services/          # Business logic
│   │   │   ├── instantly.py   # Instantly API
│   │   │   ├── ai_copy.py     # OpenAI API
│   │   │   └── supabase_service.py
│   │   └── models/            # Data models
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/                   # Next.js React
│   ├── app/                   # App Router pages
│   │   ├── page.tsx           # Landing
│   │   ├── layout.tsx         # Root layout
│   │   └── dashboard/         # Dashboard pages
│   ├── components/            # React components
│   │   ├── CampaignForm.tsx
│   │   └── Dashboard.tsx
│   ├── middleware.ts          # Clerk auth
│   ├── package.json
│   ├── Dockerfile
│   └── .env.local.example
│
├── README.md                  # Main docs
├── QUICKSTART.md              # 5-min setup
├── SETUP_GUIDE.md             # Detailed setup
├── API_DOCS.md                # API reference
├── ARCHITECTURE.md            # This file
├── PROJECT_SUMMARY.md         # Overview
├── CHECKLIST.md               # Setup checklist
├── docker-compose.yml         # Docker setup
└── .gitignore
```

---

This architecture is designed to be:
- ✅ **Simple** - Easy to understand and modify
- ✅ **Scalable** - Can grow to 1000s of users
- ✅ **Maintainable** - Clean separation of concerns
- ✅ **Cost-effective** - Leverages free tiers
- ✅ **Modern** - Uses latest best practices

---

**Last Updated**: January 2024
