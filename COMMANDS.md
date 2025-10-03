# 🎯 Quick Command Reference

Essential commands for running Vibe Marketing Autopilot.

---

## 🚀 Starting the Application

### Option 1: Using Helper Scripts (Recommended)

**Backend:**
```bash
./start-backend.sh
```

**Frontend:**
```bash
./start-frontend.sh
```

### Option 2: Manual Commands

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend:**
```bash
cd frontend
npm run dev
```

---

## 🛠️ Setup Commands

### Initial Setup

**Install Backend:**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

**Install Frontend:**
```bash
cd frontend
npm install --legacy-peer-deps
```

### Environment Configuration

**Backend:**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env with your API keys
```

**Frontend:**
```bash
cp frontend/.env.local.example frontend/.env.local
# Edit frontend/.env.local with your API keys
```

---

## 🧪 Testing Commands

### Health Check

**Backend:**
```bash
curl http://localhost:8000/health
# Expected: {"status":"healthy"}
```

**Frontend:**
```bash
curl http://localhost:3000
# Should return HTML
```

### API Test

**Create Campaign (test endpoint):**
```bash
curl -X POST http://localhost:8000/api/create-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://test.com",
    "target_audience": "test audience",
    "user_id": "test_user"
  }'
```

---

## 🔄 Maintenance Commands

### Update Dependencies

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

**Frontend:**
```bash
cd frontend
npm update
```

### Clean Install

**Backend:**
```bash
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install --legacy-peer-deps
```

---

## 🗄️ Database Commands

### Create Tables (Supabase SQL Editor)

```sql
-- Run these in Supabase SQL Editor
-- See SETUP_GUIDE.md for complete SQL
```

### Check Database Connection (Python)

```bash
cd backend
source venv/bin/activate
python3 -c "from app.services.supabase_service import SupabaseService; import os; from dotenv import load_dotenv; load_dotenv(); print('Connected!' if SupabaseService(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_KEY')) else 'Failed')"
```

---

## 🚢 Deployment Commands

### Build for Production

**Backend:**
```bash
cd backend
# No build needed - FastAPI runs directly
```

**Frontend:**
```bash
cd frontend
npm run build
npm start
```

### Deploy to Vercel (Frontend)

```bash
cd frontend
vercel
```

### Deploy to Railway (Backend)

```bash
# Push to GitHub, then connect in Railway dashboard
git add .
git commit -m "Deploy to Railway"
git push
```

---

## 🐳 Docker Commands

### Build and Run with Docker

**Using Docker Compose:**
```bash
docker-compose up --build
```

**Backend Only:**
```bash
cd backend
docker build -t vibe-backend .
docker run -p 8000:8000 --env-file .env vibe-backend
```

**Frontend Only:**
```bash
cd frontend
docker build -t vibe-frontend .
docker run -p 3000:3000 --env-file .env.local vibe-frontend
```

---

## 🔍 Debugging Commands

### View Logs

**Backend (if running in background):**
```bash
tail -f backend/logs/app.log
```

**Frontend:**
```bash
# Logs appear in terminal where npm run dev is running
```

### Check Ports

```bash
# Check if ports are in use
lsof -i :8000  # Backend
lsof -i :3000  # Frontend
```

### Kill Processes

```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## 📊 API Testing with cURL

### Health Check
```bash
curl http://localhost:8000/health
```

### Get Campaigns
```bash
curl "http://localhost:8000/api/campaigns?user_id=user_123"
```

### Get Analytics
```bash
curl "http://localhost:8000/api/analytics/campaign_123?user_id=user_123"
```

---

## 🧹 Cleanup Commands

### Remove Everything

**Backend:**
```bash
cd backend
rm -rf venv __pycache__ app/__pycache__ app/services/__pycache__
```

**Frontend:**
```bash
cd frontend
rm -rf node_modules .next
```

### Git Clean (be careful!)

```bash
git clean -fdx  # Removes all untracked files
```

---

## 📱 Mobile Testing

### Expose Local Server

```bash
# Using ngrok (install first: brew install ngrok)
ngrok http 3000  # Frontend
ngrok http 8000  # Backend
```

---

## 🔐 Environment Variable Commands

### Check Variables

**Backend:**
```bash
cd backend
source venv/bin/activate
python3 -c "from dotenv import load_dotenv; import os; load_dotenv(); print('INSTANTLY_API_KEY:', os.getenv('INSTANTLY_API_KEY')[:10] + '...' if os.getenv('INSTANTLY_API_KEY') else 'Not set')"
```

**Frontend:**
```bash
cd frontend
node -e "require('dotenv').config({path: '.env.local'}); console.log('API_URL:', process.env.NEXT_PUBLIC_API_URL)"
```

---

## 🎨 Code Quality Commands

### Linting

**Backend (if you add black/flake8):**
```bash
cd backend
black app/
flake8 app/
```

**Frontend:**
```bash
cd frontend
npm run lint
```

### Type Checking

**Backend:**
```bash
cd backend
mypy app/
```

**Frontend:**
```bash
cd frontend
npm run type-check  # If configured
```

---

## 📦 Package Management

### List Installed Packages

**Backend:**
```bash
cd backend
source venv/bin/activate
pip list
```

**Frontend:**
```bash
cd frontend
npm list --depth=0
```

### Check for Updates

**Backend:**
```bash
cd backend
source venv/bin/activate
pip list --outdated
```

**Frontend:**
```bash
cd frontend
npm outdated
```

---

## 🔄 Git Commands

### Initial Commit

```bash
git add .
git commit -m "Initial commit - Vibe Marketing Autopilot MVP"
git branch -M main
git remote add origin <your-repo-url>
git push -u origin main
```

### Update with New Changes

```bash
git add .
git commit -m "Update: <description>"
git push
```

---

## 💡 Pro Tips

### Run Both Servers in One Command

**Using tmux:**
```bash
tmux new-session -d -s vibe './start-backend.sh'
tmux split-window -h './start-frontend.sh'
tmux attach -t vibe
```

### Auto-restart on File Changes

Both servers support hot reload by default:
- Backend: `uvicorn --reload` flag
- Frontend: Next.js dev mode

### Quick Reset

```bash
# One command to reset everything
./start-backend.sh && ./start-frontend.sh
```

---

**Bookmark this file for quick command reference!** 📌
