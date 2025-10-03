# 📡 API Documentation

Complete API reference for Vibe Marketing Autopilot backend.

**Base URL**: `http://localhost:8000` (development)

---

## Authentication

All endpoints require a valid Clerk user ID passed in the request.

---

## Endpoints

### 1. Health Check

Check if the API is running.

**GET** `/health`

**Response:**
```json
{
  "status": "healthy"
}
```

---

### 2. Create Campaign

Create a new campaign with AI-generated copy.

**POST** `/api/create-campaign`

**Headers:**
```
Content-Type: application/json
```

**Request Body:**
```json
{
  "url": "https://yourapp.com",
  "target_audience": "SaaS founders in US, 1-10 employees, CTOs at B2B companies",
  "user_id": "user_2abc123xyz",
  "leads_csv": null  // Optional: CSV data as string
}
```

**Response (Success):**
```json
{
  "success": true,
  "campaign_id": "Launch - https://yourapp.com",
  "lead_list_id": "Campaign - https://yourapp.com",
  "variants": [
    {
      "subject": "Quick question about {{company}}",
      "body": "Hi {{firstName}},\n\nI noticed {{company}} is working on..."
    },
    {
      "subject": "Solving a problem for {{company}}",
      "body": "Hey {{firstName}},\n\nMost SaaS teams struggle with..."
    },
    {
      "subject": "{{company}} + YourApp?",
      "body": "{{firstName}},\n\nI've been following {{company}}'s work..."
    }
  ],
  "db_record": {
    "id": "abc-123-def",
    "user_id": "user_2abc123xyz",
    "campaign_id": "Launch - https://yourapp.com",
    "url": "https://yourapp.com",
    "target_audience": "SaaS founders...",
    "status": "active",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

**Response (Error):**
```json
{
  "detail": "Failed to create campaign: API key invalid"
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error (check API keys, Instantly.ai connection)

---

### 3. Get Campaign Analytics

Fetch real-time analytics for a campaign.

**GET** `/api/analytics/{campaign_id}`

**Parameters:**
- `campaign_id` (path) - The campaign ID
- `user_id` (query) - User ID for authentication

**Example:**
```
GET /api/analytics/Launch%20-%20https://yourapp.com?user_id=user_2abc123xyz
```

**Response:**
```json
{
  "success": true,
  "campaign_id": "Launch - https://yourapp.com",
  "analytics": {
    "sent": 150,
    "opened": 68,
    "clicked": 23,
    "replied": 12,
    "bounced": 3,
    "open_rate": 45.33,
    "click_rate": 33.82,
    "reply_rate": 8.0
  }
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 4. Get User Campaigns

Get all campaigns for a user.

**GET** `/api/campaigns`

**Parameters:**
- `user_id` (query) - User ID

**Example:**
```
GET /api/campaigns?user_id=user_2abc123xyz
```

**Response:**
```json
{
  "success": true,
  "campaigns": [
    {
      "id": "abc-123",
      "user_id": "user_2abc123xyz",
      "campaign_id": "Launch - https://yourapp.com",
      "url": "https://yourapp.com",
      "target_audience": "SaaS founders...",
      "status": "active",
      "sent": 150,
      "opened": 68,
      "clicked": 23,
      "replied": 12,
      "open_rate": 45.33,
      "click_rate": 33.82,
      "reply_rate": 8.0,
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T15:45:00Z",
      "copy_variants": [...]
    }
  ]
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 5. Create Email Account

Add a warmed email account to Instantly.ai.

**POST** `/api/create-email-account`

**Request Body:**
```json
{
  "user_id": "user_2abc123xyz",
  "email": "sales@yourcompany.com",
  "smtp_config": {
    "host": "smtp.gmail.com",
    "port": 587,
    "username": "sales@yourcompany.com",
    "password": "your_app_password"
  }
}
```

**Response:**
```json
{
  "success": true,
  "account": {
    "email": "sales@yourcompany.com",
    "status": "active",
    "warmup_enabled": true
  }
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

### 6. Upload Leads

Upload leads to a campaign.

**POST** `/api/upload-leads`

**Request Body:**
```json
{
  "campaign_name": "Launch - https://yourapp.com",
  "leads": [
    {
      "email": "john@company.com",
      "first_name": "John",
      "last_name": "Doe",
      "company": "Company Inc",
      "phone": "+1234567890",
      "website": "https://company.com"
    },
    {
      "email": "jane@startup.io",
      "first_name": "Jane",
      "last_name": "Smith",
      "company": "Startup.io"
    }
  ]
}
```

**Response:**
```json
{
  "success": true,
  "lead_list_id": "Launch - https://yourapp.com"
}
```

**Status Codes:**
- `200` - Success
- `500` - Server error

---

## Error Handling

All errors return this format:

```json
{
  "detail": "Error message here"
}
```

### Common Errors

**Invalid API Key:**
```json
{
  "detail": "Failed to create campaign: Invalid API key"
}
```

**Missing Parameters:**
```json
{
  "detail": "url field required"
}
```

**Database Connection Failed:**
```json
{
  "detail": "Database connection failed"
}
```

---

## Rate Limits

- **OpenAI API**: 3,500 requests/minute (GPT-4)
- **Instantly.ai**: 100 requests/minute
- **Supabase**: Unlimited (free tier)

---

## Data Models

### Campaign
```typescript
{
  id: string              // UUID
  user_id: string         // Clerk user ID
  campaign_id: string     // Campaign name in Instantly
  url: string             // Product/service URL
  target_audience: string // ICP description
  copy_variants: Array<{
    subject: string
    body: string
  }>
  status: 'active' | 'paused' | 'completed'
  sent: number
  opened: number
  clicked: number
  replied: number
  bounced: number
  open_rate: number
  click_rate: number
  reply_rate: number
  created_at: string      // ISO timestamp
  updated_at: string      // ISO timestamp
}
```

### Lead
```typescript
{
  email: string           // Required
  first_name?: string
  last_name?: string
  company?: string
  phone?: string
  website?: string
  personalization?: string
}
```

---

## Testing the API

### Using cURL

**Create Campaign:**
```bash
curl -X POST http://localhost:8000/api/create-campaign \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://yourapp.com",
    "target_audience": "SaaS founders",
    "user_id": "user_123"
  }'
```

**Get Analytics:**
```bash
curl "http://localhost:8000/api/analytics/campaign_123?user_id=user_123"
```

### Using Postman

1. Import the API endpoints
2. Set `Content-Type: application/json` header
3. Use the request examples above

---

## Integration Examples

### JavaScript/React

```javascript
const createCampaign = async (url, audience, userId) => {
  const response = await fetch('http://localhost:8000/api/create-campaign', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      url,
      target_audience: audience,
      user_id: userId,
    }),
  })

  const data = await response.json()
  return data
}
```

### Python

```python
import requests

def create_campaign(url, audience, user_id):
    response = requests.post(
        'http://localhost:8000/api/create-campaign',
        json={
            'url': url,
            'target_audience': audience,
            'user_id': user_id
        }
    )
    return response.json()
```

---

## Webhooks (Future)

Coming soon: Instantly.ai webhook integration for real-time reply notifications.

---

## API Versioning

Current version: `v1`

All endpoints are prefixed with `/api/`. Future versions will use `/api/v2/`, etc.

---

## Support

For API issues:
1. Check error messages
2. Verify API keys are correct
3. Check backend logs
4. Open a GitHub issue

---

**Last Updated**: January 2024
