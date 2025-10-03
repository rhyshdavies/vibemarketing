# Firebase Setup Guide

This guide will help you set up Firebase/Firestore for the Vibe Marketing Autopilot backend.

---

## Prerequisites

- A Google account
- Firebase free credits (as mentioned)

---

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click **"Add project"** or **"Create a project"**
3. Enter a project name (e.g., `vibe-marketing-autopilot`)
4. Choose whether to enable Google Analytics (optional)
5. Click **"Create project"**

---

## Step 2: Enable Firestore Database

1. In your Firebase project dashboard, click **"Firestore Database"** in the left sidebar
2. Click **"Create database"**
3. Choose **"Start in production mode"** (we'll add security rules later)
4. Select a location (choose closest to your users, e.g., `us-central1`)
5. Click **"Enable"**

---

## Step 3: Generate Service Account Credentials

1. Click the **gear icon** ⚙️ next to "Project Overview" in the left sidebar
2. Select **"Project settings"**
3. Go to the **"Service accounts"** tab
4. Click **"Generate new private key"**
5. A JSON file will be downloaded - **keep this secure!**
6. Rename the file to something simple like `firebase-credentials.json`

---

## Step 4: Add Credentials to Backend

### Option A: Using Environment Variable (Recommended for Production)

1. Move the `firebase-credentials.json` file to your backend directory:
   ```bash
   mv ~/Downloads/firebase-credentials.json /Users/rhyshamilton-davies/vibemarketing/backend/
   ```

2. Update `backend/.env`:
   ```bash
   # Add this line to backend/.env
   GOOGLE_APPLICATION_CREDENTIALS=/Users/rhyshamilton-davies/vibemarketing/backend/firebase-credentials.json
   ```

### Option B: Direct Path (Quick Testing)

The backend will automatically use the credentials if `GOOGLE_APPLICATION_CREDENTIALS` is set.

---

## Step 5: Install Firebase Dependencies

```bash
cd backend
pip install -r requirements.txt
```

This will install `firebase-admin==6.5.0`.

---

## Step 6: Test Firebase Connection

Create a test script to verify the connection:

```bash
cd backend
python -c "
from app.services.firebase_service import FirebaseService
import asyncio

async def test():
    db = FirebaseService()
    print('✅ Firebase connected successfully!')

    # Test saving a campaign
    result = await db.save_campaign(
        user_id='test_user',
        campaign_id='test_campaign_123',
        url='https://example.com',
        target_audience='Test audience',
        copy_variants=[{'subject': 'Test', 'body': 'Test body'}]
    )
    print(f'✅ Test campaign saved: {result}')

    # Test retrieving campaigns
    campaigns = await db.get_user_campaigns('test_user')
    print(f'✅ Found {len(campaigns)} campaigns')

asyncio.run(test())
"
```

---

## Step 7: Firestore Collections Structure

The backend automatically creates these collections:

### `campaigns` Collection
```
campaigns/
  {campaign_id}/
    - user_id: string
    - campaign_id: string
    - url: string
    - target_audience: string
    - copy_variants: array
    - status: string (active/paused/completed)
    - sent: number
    - opened: number
    - clicked: number
    - replied: number
    - bounced: number
    - open_rate: number
    - click_rate: number
    - reply_rate: number
    - created_at: timestamp
    - updated_at: timestamp
```

### `users` Collection
```
users/
  {user_id}/
    - user_id: string
    - email: string
    - name: string
    - created_at: timestamp
    - plan: string (free/pro/enterprise)
```

### `email_accounts` Collection
```
email_accounts/
  {account_id}/
    - user_id: string
    - email: string
    - status: string
    - warmup_enabled: boolean
    - created_at: timestamp
```

### `lead_lists` Collection
```
lead_lists/
  {list_id}/
    - user_id: string
    - campaign_id: string
    - leads: array
    - total_leads: number
    - created_at: timestamp
```

---

## Step 8: Set Up Firestore Security Rules (Optional)

For production, add security rules in Firebase Console → Firestore Database → Rules:

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // Users can read/write their own campaigns
    match /campaigns/{campaignId} {
      allow read, write: if request.auth != null &&
                           request.auth.uid == resource.data.user_id;
    }

    // Users can read/write their own profile
    match /users/{userId} {
      allow read, write: if request.auth != null &&
                           request.auth.uid == userId;
    }

    // Users can read/write their own email accounts
    match /email_accounts/{accountId} {
      allow read, write: if request.auth != null &&
                           request.auth.uid == resource.data.user_id;
    }

    // Users can read/write their own lead lists
    match /lead_lists/{listId} {
      allow read, write: if request.auth != null &&
                           request.auth.uid == resource.data.user_id;
    }
  }
}
```

**Note**: For demo mode (no authentication), you can use:
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /{document=**} {
      allow read, write: if true;  // WARNING: Only for development!
    }
  }
}
```

---

## Step 9: Start the Backend

```bash
cd /Users/rhyshamilton-davies/vibemarketing
./start-backend.sh
```

You should see:
```
✅ Firebase connected successfully!
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## Step 10: Test Full Flow

1. **Start backend**:
   ```bash
   ./start-backend.sh
   ```

2. **Start frontend** (in a new terminal):
   ```bash
   ./start-frontend.sh
   ```

3. **Visit**: http://localhost:4000

4. **Create a campaign**:
   - Click "Get Started"
   - Enter URL: `https://yourapp.com`
   - Enter target: `SaaS founders, 1-10 employees`
   - Click "Generate Campaign"

5. **Check Firestore**:
   - Go to Firebase Console → Firestore Database
   - You should see a new document in the `campaigns` collection

---

## Troubleshooting

### Error: "Could not automatically determine credentials"

**Solution**: Make sure `GOOGLE_APPLICATION_CREDENTIALS` is set in `backend/.env`:
```bash
GOOGLE_APPLICATION_CREDENTIALS=/Users/rhyshamilton-davies/vibemarketing/backend/firebase-credentials.json
```

### Error: "Permission denied"

**Solution**:
1. Check Firestore security rules (see Step 8)
2. For demo mode, temporarily allow all reads/writes
3. For production, implement proper authentication with Clerk

### Error: "Module 'firebase_admin' not found"

**Solution**:
```bash
cd backend
pip install firebase-admin==6.5.0
```

---

## Firebase vs Supabase

**Why Firebase/Firestore?**
- ✅ You have free credits
- ✅ No PostgreSQL schema setup needed
- ✅ Real-time updates out of the box
- ✅ Automatic scaling
- ✅ Google Cloud integration
- ✅ Easy authentication integration (if switching from Clerk later)

**Firestore Benefits**:
- NoSQL document database (flexible schema)
- Built-in caching
- Offline support
- Real-time listeners
- Better for demo/MVP phase

---

## Next Steps

1. ✅ Firebase project created
2. ✅ Firestore enabled
3. ✅ Service account credentials downloaded
4. ✅ Credentials added to backend
5. ✅ Dependencies installed
6. ✅ Backend started
7. 🎯 **Test creating a campaign!**

---

## Quick Commands Reference

```bash
# Install dependencies
cd backend && pip install -r requirements.txt

# Start backend
./start-backend.sh

# Start frontend
./start-frontend.sh

# Test Firebase connection
cd backend && python -c "from app.services.firebase_service import FirebaseService; print('✅ Firebase works!')"
```

---

## Production Deployment Notes

### Environment Variables for Production

When deploying to Railway/Render/Vercel:

1. **Upload credentials file** to your server OR
2. **Use environment variable** with the full JSON content:
   ```bash
   FIREBASE_CREDENTIALS='{"type":"service_account","project_id":"your-project",...}'
   ```

3. Update `firebase_service.py` to handle JSON string:
   ```python
   import json

   creds_json = os.getenv("FIREBASE_CREDENTIALS")
   if creds_json:
       cred = credentials.Certificate(json.loads(creds_json))
   ```

---

**You're all set! Firebase is now configured and ready to use.** 🚀

Your backend will now store all campaign data in Firestore instead of Supabase.
