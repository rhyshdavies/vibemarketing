"""
Final comprehensive test: Create SuperSearch list → Create campaign → Verify leads auto-add
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import json
import httpx

load_dotenv()


async def test_complete_flow():
    """Test the complete flow with a list that has enriched leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 FINAL FLOW TEST")
    print("=" * 80)

    # Use an existing list ID that we know has enriched leads
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    print(f"\n✅ Step 1: Verify list {list_id} has enriched leads")
    list_leads = await instantly_service.get_leads_from_list(list_id, limit=5)
    print(f"   Found {len(list_leads)} leads in list")

    if not list_leads or len(list_leads) == 0:
        print("   ❌ List is empty - skipping test")
        return

    print(f"   Sample lead email: {list_leads[0].get('email')}")

    print(f"\n✅ Step 2: Create campaign WITH lead_list_id={list_id}")
    campaign_data = await instantly_service.create_campaign(
        name="FINAL TEST - Auto Lead Addition",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Final Test",
                "body": "Hi {{firstName}},\n\nFinal test.\n\nBest"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")

    print(f"\n✅ Step 3: Verify leads were AUTO-ADDED to campaign {campaign_id}")

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
            print(f"   ✅ Campaign has {len(campaign_leads)} leads!")

            if len(campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! Campaign was created with leads automatically!")
                print(f"\n   Summary:")
                print(f"   - List {list_id} has leads: ✅")
                print(f"   - Campaign {campaign_id} created: ✅")
                print(f"   - Leads auto-added to campaign: ✅ ({len(campaign_leads)} leads)")
                print(f"\n   This confirms that:")
                print(f"   1. get_leads_from_list() now works correctly with POST /api/v2/leads/list")
                print(f"   2. Creating a campaign with lead_list_id automatically adds all leads")
                print(f"   3. No manual 'moveleads' or 'add leads' step is needed!")
                print(f"\n   The user should now see {len(campaign_leads)} leads in the Instantly.ai dashboard")
                print(f"   for campaign '{campaign_data.get('name')}' instead of '👋 Add some leads'")
            else:
                print(f"   ❌ Campaign has 0 leads - something went wrong")
        else:
            print(f"   ❌ Failed to fetch campaign leads: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_complete_flow())
