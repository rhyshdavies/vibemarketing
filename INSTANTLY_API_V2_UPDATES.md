# ✨ Instantly.ai API v2 Integration - Updated

The backend has been updated to use **Instantly.ai API v2** for improved functionality and better campaign management.

---

## 🔄 What Changed

### API Endpoint Updates

**Old (v1):**
```
https://api.instantly.ai/api/v1/
```

**New (v2):**
```
https://api.instantly.ai/api/v2/
```

---

## 📋 Updated Endpoints

### 1. Create Lead List

**v1:** `POST /api/v1/lead/add`
**v2:** `POST /api/v2/lead-lists`

```python
# v2 format
{
    "api_key": "inst_xxx",
    "name": "Campaign - myapp.com"
}
```

**Returns:**
```json
{
    "id": "lead_list_123",
    "name": "Campaign - myapp.com"
}
```

---

### 2. Upload Leads

**v1:** `POST /api/v1/lead/add` (one at a time)
**v2:** `POST /api/v2/leads/list` (bulk upload)

```python
# v2 format - bulk upload
{
    "api_key": "inst_xxx",
    "lead_list_id": "lead_list_123",
    "leads": [
        {
            "email": "john@company.com",
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Company Inc",
            "phone": "+1234567890",
            "website": "https://company.com",
            "custom_variables": {}
        }
    ],
    "skip_if_in_workspace": false
}
```

---

### 3. Create Campaign

**v1:** `POST /api/v1/campaign/launch`
**v2:** `POST /api/v2/campaigns`

```python
# v2 format - with sequences
{
    "api_key": "inst_xxx",
    "name": "Launch - myapp.com",
    "lead_list_ids": ["lead_list_123"],
    "sequences": [
        {
            "position": 1,
            "subject": "Quick question about {{company}}",
            "body": "Hi {{firstName}},...",
            "wait_days": 0
        },
        {
            "position": 2,
            "subject": "Following up...",
            "body": "Hey {{firstName}},...",
            "wait_days": 3
        }
    ],
    "daily_limit": 50,
    "schedule": {
        "timezone": "America/New_York",
        "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
        "start_hour": 9,
        "end_hour": 17
    }
}
```

**Returns:**
```json
{
    "id": "campaign_123",
    "name": "Launch - myapp.com",
    "status": "created"
}
```

---

### 4. Activate Campaign

**New in v2:** `POST /api/v2/campaigns/{id}/activate`

Campaigns must be explicitly activated after creation.

```python
{
    "api_key": "inst_xxx"
}
```

---

### 5. Get Campaign Analytics

**v1:** `GET /api/v1/analytics/campaign?name=xxx`
**v2:** `GET /api/v2/campaigns/analytics?campaign_id=xxx`

```python
# v2 response
{
    "sent": 150,
    "opened": 68,
    "clicked": 23,
    "replied": 12,
    "bounced": 3
}
```

**New in v2:** Analytics Overview

`GET /api/v2/campaigns/analytics/overview`

Get aggregate analytics across multiple campaigns.

---

### 6. Manage Email Accounts

**v1:** `POST /api/v1/account/add`
**v2:** `POST /api/v2/accounts`

```python
# v2 format
{
    "api_key": "inst_xxx",
    "email": "sales@company.com",
    "smtp_host": "smtp.gmail.com",
    "smtp_port": 587,
    "smtp_username": "sales@company.com",
    "smtp_password": "app_password",
    "warmup_enabled": true
}
```

**Get accounts:** `GET /api/v2/accounts`

---

### 7. Campaign Management

**Pause Campaign:**
```
POST /api/v2/campaigns/{id}/pause
```

**Get Campaign Details:**
```
GET /api/v2/campaigns/{id}
```

**Update Campaign:**
```
PATCH /api/v2/campaigns/{id}
```

**Delete Campaign:**
```
DELETE /api/v2/campaigns/{id}
```

---

## 🆕 New Features in v2

### 1. Sequences Support

Create multi-step email sequences with wait times:

```python
sequences = [
    {
        "position": 1,
        "subject": "First email",
        "body": "...",
        "wait_days": 0  # Send immediately
    },
    {
        "position": 2,
        "subject": "Follow-up",
        "body": "...",
        "wait_days": 3  # Wait 3 days after first email
    },
    {
        "position": 3,
        "subject": "Final follow-up",
        "body": "...",
        "wait_days": 5  # Wait 5 days after second email
    }
]
```

### 2. Campaign Scheduling

Schedule when emails should be sent:

```python
schedule = {
    "timezone": "America/New_York",
    "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
    "start_hour": 9,   # 9 AM
    "end_hour": 17     # 5 PM
}
```

### 3. Daily Sending Limits

Control how many emails to send per day:

```python
"daily_limit": 50  # Send max 50 emails per day
```

### 4. Bulk Lead Upload

Upload multiple leads in a single API call instead of one at a time.

### 5. Lead Lists as Separate Entities

Lead lists are now separate from campaigns, allowing you to:
- Reuse lead lists across campaigns
- Manage leads independently
- Better organization

---

## 🔧 Code Changes

### Updated Service Methods

```python
# instantly.py

async def create_lead_list(name: str) -> str:
    # Returns lead_list_id

async def upload_leads(campaign_id: str, lead_list_id: str, leads: List[Dict]) -> str:
    # Bulk upload all leads

async def create_campaign(name: str, lead_list_id: str, variants: List[Dict]) -> Dict:
    # Creates campaign with sequences
    # Returns campaign dict with id

async def activate_campaign(campaign_id: str) -> bool:
    # NEW: Activate campaign to start sending

async def get_campaign_analytics(campaign_id: str) -> Dict:
    # Get analytics by campaign_id (not name)
```

---

## 📊 Updated Campaign Flow

**Old Flow (v1):**
```
1. Create lead → 2. Launch campaign → 3. Get analytics
```

**New Flow (v2):**
```
1. Create lead list
   ↓
2. Upload leads to list
   ↓
3. Create campaign with sequences
   ↓
4. Activate campaign
   ↓
5. Get analytics
```

---

## 🚨 Breaking Changes

### 1. Campaign Identifiers

**v1:** Used campaign `name` as identifier
**v2:** Uses campaign `id` (UUID)

### 2. Lead Upload

**v1:** One lead at a time
**v2:** Bulk upload with `leads` array

### 3. Campaign Status

**v2:** Campaigns are `created` by default, must be `activated` to send

### 4. Analytics Endpoint

**v1:** Query param `name`
**v2:** Query param `campaign_id`

---

## ✅ Migration Checklist

- [x] Updated base URL to v2
- [x] Updated `create_lead_list()` to use `/api/v2/lead-lists`
- [x] Updated `upload_leads()` to use bulk upload
- [x] Updated `create_campaign()` with sequences support
- [x] Added `activate_campaign()` method
- [x] Updated `get_campaign_analytics()` to use campaign_id
- [x] Updated email account creation
- [x] Added campaign management methods (pause, delete, get)
- [x] Updated main.py to activate campaigns after creation

---

## 🔍 Testing the Integration

### 1. Test Lead List Creation

```bash
curl -X POST https://api.instantly.ai/api/v2/lead-lists \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "inst_YOUR_KEY",
    "name": "Test List"
  }'
```

### 2. Test Campaign Creation

```bash
curl -X POST https://api.instantly.ai/api/v2/campaigns \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "inst_YOUR_KEY",
    "name": "Test Campaign",
    "lead_list_ids": ["lead_list_123"],
    "sequences": [{
      "position": 1,
      "subject": "Test",
      "body": "Hi {{firstName}}",
      "wait_days": 0
    }]
  }'
```

### 3. Test Campaign Activation

```bash
curl -X POST https://api.instantly.ai/api/v2/campaigns/campaign_123/activate \
  -H "Content-Type: application/json" \
  -d '{
    "api_key": "inst_YOUR_KEY"
  }'
```

---

## 📚 API v2 Resources

- **Full Documentation:** https://developer.instantly.ai/
- **API Explorer:** Interactive API testing
- **Changelog:** Track API updates
- **Support:** help@instantly.ai

---

## 🐛 Troubleshooting

### Error: "Lead list not found"

**Cause:** Using lead list `name` instead of `id`
**Fix:** Store and use the `id` returned from `create_lead_list()`

### Error: "Campaign not sending"

**Cause:** Campaign not activated
**Fix:** Call `activate_campaign(campaign_id)` after creation

### Error: "Invalid sequences format"

**Cause:** Sequences missing required fields
**Fix:** Ensure each sequence has `position`, `subject`, `body`, `wait_days`

### Error: "Analytics not found"

**Cause:** Using campaign `name` instead of `id`
**Fix:** Use the campaign `id` from the create response

---

## 💡 Best Practices

1. **Store Campaign IDs:** Save the campaign `id` returned from creation
2. **Activate After Creation:** Always activate campaigns to start sending
3. **Use Sequences:** Leverage multi-step sequences for better response rates
4. **Set Limits:** Use `daily_limit` to avoid spam filters
5. **Schedule Wisely:** Send during business hours in recipient's timezone
6. **Monitor Analytics:** Check analytics regularly for performance insights

---

## 🎯 Next Steps

1. **Test the integration** with your Instantly.ai account
2. **Verify campaigns** are created and activated
3. **Check analytics** after 24 hours
4. **Add more features:**
   - CSV lead upload
   - Custom sequences builder
   - Advanced analytics dashboard
   - Webhook integration for replies

---

**Updated:** January 2024
**API Version:** v2.0.0
