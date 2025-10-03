"""
Final test using the EXACT working sequence from the user
"""
import asyncio
import httpx
import os
import uuid
from dotenv import load_dotenv

load_dotenv()


async def test_final_flow():
    api_key = os.getenv('INSTANTLY_API_KEY')
    BASE = "https://api.instantly.ai/api/v2"
    HDRS = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    print("🎯 FINAL WORKING FLOW TEST")
    print("=" * 80)

    # Step 1: Create campaign with proper schedule
    print("\n✅ Step 1: Create campaign")

    async with httpx.AsyncClient(timeout=60.0) as client:
        campaign_res = await client.post(
            f"{BASE}/campaigns",
            headers=HDRS,
            json={
                "name": "API Seed Test - Final",
                "campaign_schedule": {
                    "schedules": [{
                        "name": "Default",
                        "timing": {"from": "09:00", "to": "17:00"},
                        "days": {"1": True, "2": True, "3": True, "4": True, "5": True, "0": False, "6": False},
                        "timezone": "Etc/GMT+12"
                    }]
                }
            }
        )

        print(f"   Status: {campaign_res.status_code}")
        if campaign_res.status_code not in [200, 201]:
            print(f"   ❌ Failed: {campaign_res.text}")
            return

        campaign_data = campaign_res.json()
        campaign_id = campaign_data.get("id")

        if not campaign_id:
            print(f"   ❌ No campaign ID in response: {campaign_data}")
            return

        print(f"   ✅ Campaign created: {campaign_id}")
        print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

        # Step 2: Bulk create fresh leads straight into campaign
        print(f"\n✅ Step 2: Bulk create fresh leads into campaign")

        # Use completely unique emails
        unique_emails = [
            f"fresh-{uuid.uuid4()}@example.com",
            f"fresh-{uuid.uuid4()}@example.com",
            f"fresh-{uuid.uuid4()}@example.com",
        ]

        payload = {
            "campaign_id": campaign_id,
            "skip_if_in_workspace": True,
            "leads": [
                {"email": unique_emails[0], "first_name": "Ada", "company": "Analytical Engines"},
                {"email": unique_emails[1], "first_name": "Alan", "company": "Turing Institute"},
                {"email": unique_emails[2], "first_name": "Grace", "company": "Hopper Systems"},
            ],
        }

        print(f"   Creating 3 fresh leads...")
        bulk_res = await client.post(
            f"{BASE}/leads/list",
            headers=HDRS,
            json=payload
        )

        print(f"   Status: {bulk_res.status_code}")
        if bulk_res.status_code not in [200, 201]:
            print(f"   ❌ Failed: {bulk_res.text}")
            return

        print(f"   ✅ Bulk create successful")

        # Step 3: Verify via analytics
        print(f"\n✅ Step 3: Verify via campaign analytics")

        analytics_res = await client.get(
            f"{BASE}/campaigns/analytics",
            headers=HDRS,
            params={"id": campaign_id}
        )

        if analytics_res.status_code == 200:
            analytics_data = analytics_res.json()

            # Handle array or object response
            if isinstance(analytics_data, list) and len(analytics_data) > 0:
                analytics = analytics_data[0]
            elif isinstance(analytics_data, dict):
                analytics = analytics_data
            else:
                analytics = {}

            leads_count = analytics.get("leads_count", 0)

            print(f"   leads_count: {leads_count}")
            print(f"   status: {analytics.get('status')}")

            if leads_count == 3:
                print(f"\n🎉 SUCCESS! Campaign has {leads_count} leads!")
                print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Dashboard should show leads (no more '👋 Add some leads')!")
            elif leads_count > 0:
                print(f"\n✅ Partial success: {leads_count} leads added")
                print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
            else:
                print(f"\n⚠️ No leads counted yet (might still be processing)")
                print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Analytics failed: {analytics_res.status_code}")

        # Step 4: Double-check with leads/list endpoint
        print(f"\n✅ Step 4: Double-check with leads/list endpoint")

        leads_check = await client.post(
            f"{BASE}/leads/list",
            headers=HDRS,
            json={"campaign_ids": [campaign_id], "limit": 100}
        )

        if leads_check.status_code == 200:
            leads_data = leads_check.json()
            items = leads_data.get("items", [])
            campaign_leads = [l for l in items if l.get("campaign") == campaign_id]

            print(f"   Total items: {len(items)}")
            print(f"   Leads with campaign={campaign_id}: {len(campaign_leads)}")

            if campaign_leads:
                print(f"\n   Sample leads:")
                for lead in campaign_leads[:5]:
                    print(f"     - {lead.get('email')} (campaign: {lead.get('campaign')})")
            else:
                print(f"   ⚠️ No leads found with this campaign ID")

    print(f"\n" + "=" * 80)
    print(f"✅ Test complete!")


if __name__ == "__main__":
    asyncio.run(test_final_flow())
