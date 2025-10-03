# 🚀 Quick Test Without Clerk (Backend Only)

While you're getting your Clerk keys, you can test the backend API directly!

---

## Test Backend API Without Frontend

### 1. Make Sure Backend is Running

```bash
./start-backend.sh
```

You should see:
```
✅ Starting FastAPI server on http://localhost:8000
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 2. Test Endpoints with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy"}
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

Expected response:
```json
{"message":"Vibe Marketing Autopilot API","status":"active"}
```

---

## 3. Test Campaign Creation (with Mock Data)

**Important:** You need to add your API keys to `backend/.env` first:

```bash
# Edit backend/.env
INSTANTLY_API_KEY=inst_your_key
OPENAI_API_KEY=sk-your_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

Then test:

```bash
curl -X POST http://localhost:8000/api/create-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://myapp.com",
    "target_audience": "SaaS founders, 1-10 employees, US-based",
    "user_id": "test_user_123"
  }'
```

This will:
1. ✅ Call OpenAI to generate 3 email variants
2. ✅ Create a lead list in Instantly
3. ✅ Create and activate a campaign
4. ✅ Save to Supabase database

Expected response (takes 10-15 seconds):
```json
{
  "success": true,
  "campaign_id": "campaign_xyz",
  "lead_list_id": "list_xyz",
  "variants": [
    {
      "subject": "Quick question about {{company}}",
      "body": "Hi {{firstName}},..."
    },
    {
      "subject": "Solving a problem for {{company}}",
      "body": "Hey {{firstName}},..."
    },
    {
      "subject": "{{company}} + MyApp?",
      "body": "{{firstName}},..."
    }
  ]
}
```

---

## 4. Test Other Endpoints

### Get Campaigns (after creating one)
```bash
curl "http://localhost:8000/api/campaigns?user_id=test_user_123"
```

### Get Campaign Analytics
```bash
curl "http://localhost:8000/api/analytics/campaign_xyz?user_id=test_user_123"
```

---

## 5. Use Postman or Insomnia

If you prefer a GUI:

### Postman
1. Download from https://postman.com
2. Import this collection:

```json
{
  "info": {
    "name": "Vibe Marketing API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Health Check",
      "request": {
        "method": "GET",
        "header": [],
        "url": {
          "raw": "http://localhost:8000/health",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["health"]
        }
      }
    },
    {
      "name": "Create Campaign",
      "request": {
        "method": "POST",
        "header": [
          {
            "key": "Content-Type",
            "value": "application/json"
          }
        ],
        "body": {
          "mode": "raw",
          "raw": "{\n  \"url\": \"https://myapp.com\",\n  \"target_audience\": \"SaaS founders\",\n  \"user_id\": \"test_user\"\n}"
        },
        "url": {
          "raw": "http://localhost:8000/api/create-campaign",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "create-campaign"]
        }
      }
    }
  ]
}
```

---

## 6. Test with Python

Create `test_api.py`:

```python
import requests

BASE_URL = "http://localhost:8000"

# Test health
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Test campaign creation
response = requests.post(
    f"{BASE_URL}/api/create-campaign",
    json={
        "url": "https://myapp.com",
        "target_audience": "SaaS founders",
        "user_id": "test_user_123"
    }
)
print("Campaign:", response.json())
```

Run it:
```bash
python test_api.py
```

---

## 7. Check Instantly.ai Dashboard

After creating a campaign:

1. Log into your Instantly.ai account
2. Go to **Campaigns**
3. You should see: `Launch - https://myapp.com`
4. Click on it to see the AI-generated email variants
5. Check if it's activated and sending

---

## What This Tests

✅ Backend API is running
✅ OpenAI integration works (AI copy generation)
✅ Instantly.ai integration works (campaign creation)
✅ Supabase integration works (data storage)
✅ All endpoints respond correctly

---

## Frontend Will Work Once You:

1. Get Clerk API keys from https://clerk.com
2. Add them to `frontend/.env.local`
3. Restart frontend with `npm run dev`
4. Visit http://localhost:3000

---

## Quick Summary

**Backend Testing (No Clerk Needed):**
```bash
# 1. Start backend
./start-backend.sh

# 2. Test health
curl http://localhost:8000/health

# 3. Test campaign creation
curl -X POST http://localhost:8000/api/create-campaign \
  -H "Content-Type: application/json" \
  -d '{"url":"https://test.com","target_audience":"test","user_id":"test"}'
```

**Frontend (Needs Clerk Keys):**
1. Get keys from https://clerk.com
2. Add to `frontend/.env.local`
3. Run `npm run dev`

---

**The backend is fully functional and you can test all API endpoints right now!** 🎯
