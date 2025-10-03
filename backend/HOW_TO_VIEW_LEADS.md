# How to View Enriched Leads from SuperSearch

After creating a campaign with SuperSearch, you have **3 options** to view the real enriched leads:

---

## Option 1: Instantly.ai Dashboard (Recommended)

This is the **easiest and most reliable** way to see your enriched leads.

### Steps:

1. Go to **https://app.instantly.ai/**
2. Log in with your Instantly account
3. Navigate to **Campaigns** in the left sidebar
4. Find your campaign (e.g., "Launch - example.com")
5. Click on the campaign to view details
6. Click on **"Leads"** tab to see all enriched leads

### What you'll see:
- ✅ Full name (First & Last)
- ✅ Verified work email
- ✅ Company name
- ✅ Job title
- ✅ LinkedIn profile (if available)
- ✅ Company details (industry, size, revenue)

### Timeline:
- **0-2 minutes**: List created, enrichment in progress
- **2-5 minutes**: Most leads enriched and available
- **5-10 minutes**: All leads fully enriched

---

## Option 2: API Endpoint (For Developers)

Use the new `/api/leads/{list_id}` endpoint to fetch enriched leads programmatically.

### Endpoint:
```
GET http://localhost:8000/api/leads/{list_id}
```

### Example:
```bash
# Replace {list_id} with your SuperSearch list ID
curl http://localhost:8000/api/leads/5c01a50d-5004-4184-a076-39f2c49b6dd5
```

### Response (while enriching):
```json
{
  "success": false,
  "message": "Enrichment still in progress. Please wait 2-5 minutes and try again.",
  "enrichment_status": {
    "resource_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5",
    "in_progress": true,
    "exists": true
  },
  "list_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5"
}
```

### Response (after enrichment):
```json
{
  "success": true,
  "list_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5",
  "lead_count": 10,
  "leads": [
    {
      "email": "john.doe@acmecorp.com",
      "first_name": "John",
      "last_name": "Doe",
      "company_name": "Acme Corp",
      "title": "CTO",
      "linkedin": "https://linkedin.com/in/johndoe"
    },
    // ... more leads
  ]
}
```

### Test Script:
```bash
cd /Users/rhyshamilton-davies/vibemarketing/backend
source venv/bin/activate
python test_fetch_enriched_leads.py
```

---

## Option 3: Instantly.ai Lead Lists

View the lead list directly in Instantly's Lead Lists section.

### Steps:

1. Go to **https://app.instantly.ai/**
2. Navigate to **Lead Lists** in the left sidebar
3. Search for your list by the criteria or date created
4. Click on the list to view all leads

### What you'll find:
- List name: "Search Results - CTO" (or similar)
- Creation date: When you created the campaign
- Lead count: Number of enriched leads
- Full lead details when you click on the list

---

## How to Find Your List ID

When you create a campaign, the backend logs show:

```
✅ SuperSearch sourced 10 REAL leads from Instantly database
   List ID: 5c01a50d-5004-4184-a076-39f2c49b6dd5
   Criteria: Titles: CTO, CEO, VP Engineering | Departments: IT & IS | Levels: C-Level | Location: San Francisco, USA | Keywords: SaaS
```

The **List ID** is what you need for the API endpoint (Option 2).

You can also find it in:
- Campaign response data (in the frontend)
- Instantly dashboard (in the campaign details)
- Backend logs when creating campaigns

---

## Understanding Enrichment Status

### Enrichment Phases:

1. **List Created (0 min)**
   - SuperSearch creates the lead list
   - Filters applied to Instantly's 160M+ database
   - Initial leads matched (but emails not yet found)

2. **Email Enrichment (1-3 min)**
   - Instantly searches for verified work emails
   - Crawls LinkedIn, company websites, email patterns
   - Verifies email deliverability

3. **Profile Enrichment (3-5 min)**
   - Adds LinkedIn profile data
   - Company information (industry, size, revenue)
   - Contact details finalized

4. **Complete (5+ min)**
   - All leads enriched and verified
   - Ready to send emails
   - Available in Instantly dashboard

### Checking Status:

The API endpoint automatically checks status:

```bash
curl http://localhost:8000/api/leads/{list_id}
```

You'll get:
- `"in_progress": true` → Still enriching, wait longer
- `"in_progress": false` + leads → Enrichment complete!

---

## Example: Full Workflow

### 1. Create Campaign
```bash
# User creates campaign with ICP: "CTOs at Series A SaaS companies in San Francisco"
# Frontend sends request to backend
# Backend creates SuperSearch list
```

### 2. Get List ID from Logs
```
✅ SuperSearch sourced 10 REAL leads from Instantly database
   List ID: 5c01a50d-5004-4184-a076-39f2c49b6dd5
```

### 3. Wait 2-5 Minutes
Let Instantly enrich the leads with verified emails and profile data.

### 4. View Leads (Choose One)

**Option A: Instantly Dashboard**
- Go to https://app.instantly.ai/
- Navigate to Campaigns → "Launch - example.com"
- Click "Leads" tab
- See all 10 enriched leads with full details

**Option B: API Endpoint**
```bash
curl http://localhost:8000/api/leads/5c01a50d-5004-4184-a076-39f2c49b6dd5
```

**Option C: Lead Lists**
- Go to https://app.instantly.ai/
- Navigate to Lead Lists
- Find "Search Results - CTO" list
- View all leads

---

## Troubleshooting

### "Enrichment still in progress" for 10+ minutes

**Cause**: Large lead lists or high API load

**Solution**:
1. Check Instantly dashboard directly (it may show enriched leads even if API says in progress)
2. Wait up to 15 minutes for large lists (50+ leads)
3. Contact Instantly support if enrichment is stuck

### "List not found" error

**Cause**: Invalid list ID or list deleted

**Solution**:
1. Double-check the list ID from campaign creation logs
2. Verify the list exists in Instantly dashboard
3. Ensure you're using the correct Instantly API key

### Empty leads array after enrichment

**Cause**:
- No matching leads found for the search criteria
- Too restrictive filters
- Niche ICP with limited database coverage

**Solution**:
1. Broaden your ICP (e.g., remove location or expand job titles)
2. Check Instantly dashboard to see if any leads were found
3. Try a different ICP or upload a CSV with known leads

---

## API Reference

### GET /api/leads/{list_id}

Fetch enriched leads from a SuperSearch list.

**Parameters:**
- `list_id` (path, required): The SuperSearch list ID

**Response (Enriching):**
```json
{
  "success": false,
  "message": "Enrichment still in progress. Please wait 2-5 minutes and try again.",
  "enrichment_status": {
    "resource_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5",
    "enrichment_payload": {
      "work_email_enrichment": true,
      "fully_enriched_profile": false,
      "email_verification": true
    },
    "in_progress": true,
    "exists": true
  },
  "list_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5"
}
```

**Response (Complete):**
```json
{
  "success": true,
  "list_id": "5c01a50d-5004-4184-a076-39f2c49b6dd5",
  "lead_count": 10,
  "leads": [
    {
      "email": "john.doe@acmecorp.com",
      "first_name": "John",
      "last_name": "Doe",
      "company_name": "Acme Corp",
      "title": "CTO",
      "linkedin": "https://linkedin.com/in/johndoe",
      "location": "San Francisco, CA",
      "company_size": "100 - 250",
      "industry": "Software"
    }
  ]
}
```

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

---

## Quick Reference

| Method | Where | When | Best For |
|--------|-------|------|----------|
| **Instantly Dashboard** | https://app.instantly.ai/ | After 2-5 min | Viewing all lead details, managing campaigns |
| **API Endpoint** | `GET /api/leads/{list_id}` | After 2-5 min | Programmatic access, building UI features |
| **Lead Lists** | https://app.instantly.ai/lead-lists | After 2-5 min | Managing multiple lists, bulk operations |

---

## Next Steps

Now that you can view enriched leads, you might want to:

1. **Monitor Campaign Performance**
   - Check open rates in Instantly dashboard
   - Track replies and engagement
   - A/B test different email variants

2. **Refine Your ICP**
   - Analyze which leads respond best
   - Adjust filters to target similar prospects
   - Create new campaigns with refined criteria

3. **Scale Your Outreach**
   - Create multiple campaigns with different ICPs
   - Test different messaging approaches
   - Expand to new markets or verticals

---

## Support

- **Instantly API Docs**: https://developer.instantly.ai/
- **Vibe Marketing Support**: Check your application logs and error messages
- **Test Scripts**: Run `test_fetch_enriched_leads.py` to debug API issues
