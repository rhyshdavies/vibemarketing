# ICP-Driven Campaign Creation Flow API

This document describes the new ICP-driven campaign creation flow that provides a guided, multi-step process for creating highly targeted cold email campaigns.

## Overview

The ICP flow consists of 6 main steps:

1. **Analyze URL** → Get 3 AI-suggested ICPs
2. **Select ICP & Search Leads** → Find leads matching the ICP
3. **Preview Leads** → Review and approve the leads
4. **Generate Emails** → Create email variants with approval/editing
5. **Match DFY Domains** → Get AI-recommended email domains
6. **Create Campaign** → Launch campaign with all components

---

## Step 1: Analyze URL for ICPs

Analyzes a website and suggests 3 Ideal Customer Profiles.

**Endpoint:** `POST /api/icp/analyze`

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "url": "https://example.com",
  "icps": [
    {
      "name": "SaaS Startup Founders",
      "description": "Early-stage founders looking to scale efficiently",
      "target_audience": "Founders and CEOs at seed to Series B startups with 10-100 employees",
      "pain_points": [
        "Limited resources to execute growth strategies",
        "Need to move fast but lack specialized tools",
        "Difficulty scaling operations efficiently"
      ],
      "company_size": "startup"
    },
    // ... 2 more ICPs
  ]
}
```

---

## Step 2: Search for Leads

Search for leads matching the selected ICP using SuperSearch.

**Endpoint:** `POST /api/icp/search-leads`

**Request:**
```json
{
  "url": "https://example.com",
  "target_audience": "Founders and CEOs at seed to Series B startups with 10-100 employees",
  "lead_count": 10
}
```

**Response:**
```json
{
  "success": true,
  "enrichment_id": "7824d4dd-8364-45d1-a9f2-4db213feddc8",
  "search_filters": {
    "title": {"include": ["Founder", "CEO"], "exclude": []},
    "employee_count": ["0 - 25", "25 - 100"],
    "revenue": ["$1 - 10M", "$10 - 50M"]
  },
  "message": "Lead search started. Use enrichment_id to check status."
}
```

---

## Step 3: Preview Leads

Get a preview of found leads. This endpoint waits up to 90 seconds for enrichment to complete.

**Endpoint:** `GET /api/icp/leads/{enrichment_id}?limit=10`

**Response (Success):**
```json
{
  "success": true,
  "enrichment_id": "7824d4dd-8364-45d1-a9f2-4db213feddc8",
  "total_count": 10,
  "leads": [
    {
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "company_name": "Acme Corp",
      "title": "CEO & Founder",
      "website": "https://acme.com",
      "location": "San Francisco, CA"
    },
    // ... more leads
  ]
}
```

**Response (Still in Progress):**
```json
{
  "success": false,
  "message": "Enrichment still in progress. Please try again in a moment.",
  "enrichment_id": "7824d4dd-8364-45d1-a9f2-4db213feddc8",
  "leads": [],
  "total_count": 0
}
```

---

## Step 4: Generate Email Variants

Generate 3 email variants based on the selected ICP and website.

**Endpoint:** `POST /api/icp/generate-emails`

**Request:**
```json
{
  "url": "https://example.com",
  "selected_icp": {
    "name": "SaaS Startup Founders",
    "description": "Early-stage founders looking to scale efficiently",
    "target_audience": "Founders and CEOs at seed to Series B startups",
    "pain_points": [
      "Limited resources to execute growth strategies",
      "Need to move fast but lack specialized tools"
    ],
    "company_size": "startup"
  }
}
```

**Response:**
```json
{
  "success": true,
  "icp_name": "SaaS Startup Founders",
  "variants": [
    {
      "subject": "Quick question about {{company}}",
      "body": "Hi {{firstName}},\n\nI noticed {{company}} is in the SaaS space..."
    },
    {
      "subject": "Solving scaling challenges for {{company}}",
      "body": "Hey {{firstName}},\n\nMost early-stage founders struggle with..."
    },
    {
      "subject": "{{company}} + faster growth?",
      "body": "{{firstName}},\n\nI've been following {{company}}'s work..."
    }
  ]
}
```

### Regenerate Single Variant

**Endpoint:** `POST /api/icp/regenerate-email`

**Request:**
```json
{
  "url": "https://example.com",
  "selected_icp": { /* same as above */ },
  "variant_index": 1  // 0, 1, or 2
}
```

**Response:**
```json
{
  "success": true,
  "variant_index": 1,
  "variant": {
    "subject": "New subject line",
    "body": "New email body..."
  }
}
```

---

## Step 5: Match DFY Email Domains

Get AI-ranked pre-warmed email domains that fit the business.

**Endpoint:** `POST /api/icp/match-domains`

**Request:**
```json
{
  "url": "https://example.com"
}
```

**Response:**
```json
{
  "success": true,
  "total_available": 45,
  "matched_domains": [
    {
      "domain": "growthpartners.co",
      "score": 95,
      "reasoning": "Professional name that aligns with B2B SaaS industry",
      "suggested_use": "Business Development & Partnerships"
    },
    {
      "domain": "scaleventures.com",
      "score": 92,
      "reasoning": "Fits well with startup/growth-focused messaging",
      "suggested_use": "Sales & Growth Consulting"
    },
    // ... up to 5 matched domains
  ]
}
```

---

## Step 6: Create Campaign

Create the final campaign with all approved components. Returns Server-Sent Events (SSE) for real-time progress updates.

**Endpoint:** `POST /api/icp/create-campaign`

**Request:**
```json
{
  "campaign_name": "Q1 SaaS Founders Outreach",
  "url": "https://example.com",
  "user_id": "user_123",
  "selected_icp": { /* ICP object from step 1 */ },
  "enrichment_id": "7824d4dd-8364-45d1-a9f2-4db213feddc8",
  "lead_count": 10,
  "approved_variants": [
    {
      "subject": "Quick question about {{company}}",
      "body": "Hi {{firstName}}..."
    },
    // ... 2 more variants
  ],
  "selected_domains": ["growthpartners.co", "scaleventures.com"],
  "sender_name": "John Smith"
}
```

**Response (SSE Stream):**

The endpoint returns Server-Sent Events with progress updates:

```
data: {"step": 1, "status": "in_progress", "message": "Preparing approved email variants"}

data: {"step": 1, "status": "completed", "message": "Email variants ready", "log": "Using 3 approved email variants"}

data: {"step": 2, "status": "in_progress", "message": "Creating campaign in Instantly.ai"}

data: {"step": 2, "status": "completed", "message": "Campaign created", "log": "Campaign created with ID: abc-123"}

data: {"step": 3, "status": "in_progress", "message": "Adding 10 leads to campaign"}

data: {"step": 3, "status": "completed", "message": "Leads added to campaign", "log": "Successfully added 10 leads to campaign"}

data: {"step": 4, "status": "in_progress", "message": "Saving campaign to database"}

data: {"step": 4, "status": "completed", "message": "Campaign saved to database", "log": "Campaign saved to database"}

data: {"step": "done", "status": "success", "data": {
  "campaign_id": "abc-123",
  "lead_list_id": "7824d4dd-8364-45d1-a9f2-4db213feddc8",
  "variants": [ /* 3 variants */ ],
  "icp": { /* selected ICP object */ }
}}
```

---

## Complete Flow Example

Here's how to integrate all steps in the frontend:

```javascript
// Step 1: Analyze URL
const icpResponse = await fetch('/api/icp/analyze', {
  method: 'POST',
  body: JSON.stringify({ url: websiteUrl })
});
const { icps } = await icpResponse.json();

// User selects an ICP from the 3 suggestions
const selectedICP = icps[0];

// Step 2: Search for leads
const searchResponse = await fetch('/api/icp/search-leads', {
  method: 'POST',
  body: JSON.stringify({
    url: websiteUrl,
    target_audience: selectedICP.target_audience,
    lead_count: 50
  })
});
const { enrichment_id } = await searchResponse.json();

// Step 3: Poll for leads
let leadsReady = false;
let leads = [];
while (!leadsReady) {
  await new Promise(resolve => setTimeout(resolve, 5000));
  const leadsResponse = await fetch(`/api/icp/leads/${enrichment_id}?limit=50`);
  const leadsData = await leadsResponse.json();

  if (leadsData.success && leadsData.leads.length > 0) {
    leads = leadsData.leads;
    leadsReady = true;
  }
}

// User reviews and approves leads
// Step 4: Generate email variants
const emailResponse = await fetch('/api/icp/generate-emails', {
  method: 'POST',
  body: JSON.stringify({
    url: websiteUrl,
    selected_icp: selectedICP
  })
});
const { variants } = await emailResponse.json();

// User can approve, edit, or regenerate each variant
// If regenerating:
const regenResponse = await fetch('/api/icp/regenerate-email', {
  method: 'POST',
  body: JSON.stringify({
    url: websiteUrl,
    selected_icp: selectedICP,
    variant_index: 1  // Regenerate variant 2
  })
});
const { variant } = await regenResponse.json();
variants[1] = variant;  // Replace with new variant

// Step 5: Get DFY domains
const domainsResponse = await fetch('/api/icp/match-domains', {
  method: 'POST',
  body: JSON.stringify({ url: websiteUrl })
});
const { matched_domains } = await domainsResponse.json();

// User selects domains
const selectedDomains = matched_domains.slice(0, 2).map(d => d.domain);

// Step 6: Create campaign with SSE
const eventSource = new EventSource('/api/icp/create-campaign');
eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);

  if (data.step === 'done' && data.status === 'success') {
    console.log('Campaign created!', data.data.campaign_id);
    eventSource.close();
  } else if (data.status === 'error') {
    console.error('Error:', data.message);
    eventSource.close();
  } else {
    console.log(`Step ${data.step}: ${data.message}`);
  }
};
```

---

## Error Handling

All endpoints return standard error responses:

```json
{
  "detail": "Error message here"
}
```

HTTP Status Codes:
- `200` - Success
- `500` - Server error (API failures, database errors, etc.)

---

## Notes

- **Lead enrichment** typically takes 10-30 seconds but can take up to 2 minutes
- **Email generation** takes 5-15 seconds with OpenAI web search
- **Domain matching** requires available pre-warmed domains from Instantly.ai
- **Campaign creation** adds leads in bulk using the `/api/v2/leads/add` endpoint
- All email variants support `{{firstName}}`, `{{company}}`, and other Instantly.ai variables
