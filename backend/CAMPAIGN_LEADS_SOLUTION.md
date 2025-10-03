# Campaign with Leads Solution

## Problem
Campaigns created via API showed "👋 Add some leads to get started" even though SuperSearch enrichment was running. The `resource_type=1` parameter (supposed to enrich directly into campaign) doesn't actually work - SuperSearch always creates a list.

## Root Causes
1. **SuperSearch always creates a list** - Even with `campaign_id` and `resource_type=1`, SuperSearch creates a lead list, not enriching directly into the campaign
2. **Workspace-level deduplication** - Existing leads cannot be reassigned to different campaigns via API
3. **Async enrichment** - SuperSearch takes 2-5 minutes to find and enrich leads
4. **No direct move endpoint** - There's no API endpoint to move leads from a list to a campaign

## Solution: Poll + Auto-Move Flow

The updated flow automatically handles the entire process:

### Step-by-Step Process:

1. **Create Campaign First**
   ```python
   campaign = await service.create_campaign(
       name="My Campaign",
       variants=[...]
   )
   campaign_id = campaign.get("id")
   ```

2. **Run SuperSearch to Create Lead List**
   ```python
   search_result = await service.search_leads_supersearch(
       search_filters=filters,
       limit=10,
       work_email_enrichment=True,
       list_name="Leads for My Campaign"  # Creates a list
   )
   enrichment_id = search_result.get("resource_id")
   ```

3. **Poll Until Enrichment Completes**
   ```python
   # Poll every 10 seconds, max 5 minutes
   while poll_count < 30:
       await asyncio.sleep(10)
       enriched_leads = await service.get_leads_from_list(enrichment_id, limit=1)
       if enriched_leads:
           break  # Enrichment complete!
   ```

4. **Automatically Move Leads to Campaign**
   ```python
   success = await service.move_leads_to_campaign(campaign_id, enrichment_id)
   # This fetches all leads from the list and bulk creates them with campaign_id
   ```

### What `move_leads_to_campaign` Does:

1. Fetches all enriched leads from the SuperSearch list
2. Prepares bulk payload with `campaign_id` in BOTH wrapper AND each lead
3. Uses `skip_if_in_workspace: true` to handle deduplication
4. Creates leads via `POST /api/v2/leads/list`
5. Only **NEW** leads (not in workspace) will be added to the campaign

### Key Implementation Details:

**Bulk Create Format:**
```json
{
  "campaign_id": "<uuid>",
  "skip_if_in_workspace": true,
  "leads": [
    {
      "email": "john@example.com",
      "campaign_id": "<uuid>",  // Also in each lead for compatibility
      "first_name": "John",
      "company": "Example Corp"
    }
  ]
}
```

**Campaign Creation Requires Schedule:**
```json
{
  "name": "Campaign Name",
  "campaign_schedule": {
    "schedules": [{
      "name": "Default",
      "timing": {"from": "09:00", "to": "17:00"},
      "days": {"1": true, "2": true, "3": true, "4": true, "5": true, "0": false, "6": false},
      "timezone": "Etc/GMT+12"  // Must be valid timezone
    }]
  }
}
```

## Updated Files

### `/Users/rhyshamilton-davies/vibemarketing/backend/app/main.py`

**Changes:**
- Line 138-143: Changed to use `list_name` instead of `campaign_id` parameter
- Line 277-361: Added polling logic and automatic lead movement
  - Polls every 10 seconds for up to 5 minutes
  - Checks if leads are available in the list
  - Automatically calls `move_leads_to_campaign` when ready
  - Provides detailed progress updates via SSE

**New Flow:**
1. Create campaign
2. Run SuperSearch (creates list)
3. Poll until enrichment complete
4. Auto-move leads to campaign
5. Activate campaign

### `/Users/rhyshamilton-davies/vibemarketing/backend/app/services/instantly.py`

**Key Function: `move_leads_to_campaign` (lines 83-240)**

Already implemented correctly:
- Fetches leads from SuperSearch list
- Prepares bulk payload with proper format
- Uses `skip_if_in_workspace: true`
- Handles background jobs if returned
- Verifies assignment

## Testing

### Test Script: `test_updated_flow.py`

Demonstrates the complete flow:
1. Creates campaign
2. Runs SuperSearch with small lead count
3. Polls for enrichment completion
4. Moves leads to campaign
5. Verifies in dashboard

**Run:**
```bash
source venv/bin/activate && python test_updated_flow.py
```

## Limitations

### Workspace Deduplication
- Leads that already exist in the workspace (even in other campaigns) **cannot** be reassigned via API
- Only **brand new** leads (not in workspace) will be added to the campaign
- This is an Instantly.ai platform limitation, not a bug in our code

### Workaround for Testing
Since your workspace has many existing leads, SuperSearch may keep returning leads that already exist. To test with guaranteed new leads:

1. **Use very specific filters** - Narrow down to find leads you definitely don't have
2. **Wait longer** - SuperSearch takes time to find truly new leads
3. **Check workspace first** - Use the UI to see what leads already exist

## Production Usage

The main API endpoint `/api/launch` now automatically:
1. Creates the campaign
2. Runs SuperSearch
3. Waits for enrichment (up to 5 minutes)
4. Moves new leads to campaign
5. Activates campaign

**User sees progress via SSE:**
- "Finding and enriching new leads..."
- "Enriching leads... (30s)"
- "Enrichment complete! Adding leads to campaign..."
- "Leads added to campaign!"

**If enrichment takes longer than 5 minutes:**
- Campaign is still created and activated
- Leads will appear later once enrichment completes
- User gets clear instructions to check back

## Why This Works

1. **SuperSearch finds NEW leads** - When you specify search criteria, it searches the Instantly.ai database for leads matching those criteria (not just your workspace)
2. **Only new leads are created** - The `skip_if_in_workspace: true` flag ensures we only add leads that don't already exist
3. **Automatic polling** - Backend waits for enrichment and automatically moves leads without user intervention
4. **Graceful degradation** - If enrichment takes too long, campaign is still created and user can check back later

## Future Improvements

1. **Background task** - Move polling to a background job so API can return immediately
2. **Webhook support** - If Instantly.ai adds webhooks, we can be notified when enrichment completes
3. **Better deduplication** - Check workspace leads before SuperSearch to estimate how many new leads we'll get
4. **Lead preview** - Show sample enriched leads to user before adding to campaign
