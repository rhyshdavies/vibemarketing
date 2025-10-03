"""
Test the new flow: Create campaign FIRST, then enrich leads with campaign_id
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_new_flow():
    """Test creating campaign first, then enriching leads into it"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 NEW FLOW TEST - Campaign First, Then Enrich")
    print("=" * 80)

    # Step 1: Create campaign FIRST
    print(f"\n✅ Step 1: Create campaign")

    # Create temporary lead list for campaign
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp list for new flow test"
    )
    print(f"   Created temp list: {temp_list_id}")

    campaign_data = await instantly_service.create_campaign(
        name="NEW FLOW TEST - Campaign First",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test new flow",
                "body": "Hi {{firstName}},\\n\\nThis is a test of the new flow.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   ✅ Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Enrich leads WITH campaign_id
    print(f"\n✅ Step 2: Enrich leads directly into campaign {campaign_id}")

    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    try:
        search_result = await instantly_service.search_leads_supersearch(
            search_filters=search_filters,
            limit=3,
            work_email_enrichment=True,
            list_name=f"Enriched for campaign {campaign_id}",
            campaign_id=campaign_id  # THIS IS THE KEY!
        )

        lead_list_id = search_result.get("resource_id") or search_result.get("id")
        print(f"   ✅ SuperSearch started: {lead_list_id}")
        print(f"   Enrichment in progress with campaign_id={campaign_id}")

    except Exception as e:
        print(f"   ❌ SuperSearch failed: {str(e)}")
        return

    # Step 3: Wait for enrichment to complete
    print(f"\n✅ Step 3: Wait for enrichment (30 seconds)")
    await asyncio.sleep(30)

    # Step 4: Verify leads are in the campaign
    print(f"\n✅ Step 4: Verify leads are in campaign")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "campaign_ids": [campaign_id],
                "limit": 100
            },
        )

        if response.status_code == 200:
            data = response.json()
            campaign_leads = data.get("items", [])
            # Filter to leads that actually have our campaign_id
            actual_campaign_leads = [l for l in campaign_leads if l.get("campaign") == campaign_id]
            print(f"   Leads with campaign field = {campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads were enriched directly into campaign!")
                print(f"\n   Campaign: {campaign_id}")
                print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"\n   ✅ The campaign shows {len(actual_campaign_leads)} leads")
                print(f"   ✅ No more '👋 Add some leads to get started'")

                print(f"\n   Leads in campaign:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n⏳ Enrichment still in progress (may take 2-5 minutes)")
                print(f"   Check campaign in a few minutes: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Failed to verify: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_new_flow())
