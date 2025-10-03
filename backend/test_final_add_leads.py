"""
Final test: Add leads from list to campaign using new approach
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_final_add_leads():
    """Test adding leads from a list to a campaign"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    print("🎯 FINAL TEST - Add Leads to Campaign")
    print("=" * 80)

    print(f"\n✅ Step 1: Get leads from list {list_id}")
    leads = await instantly_service.get_leads_from_list(list_id, limit=5)
    print(f"   Found {len(leads)} leads")

    if not leads:
        print("   No leads to test with")
        return

    print(f"\n✅ Step 2: Create new campaign")
    campaign_data = await instantly_service.create_campaign(
        name="FINAL TEST - Lead Addition v2",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Final test v2",
                "body": "Hi {{firstName}},\n\nFinal test.\n\nBest"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")

    print(f"\n✅ Step 3: Add {len(leads)} leads to campaign using new method")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        leads=leads
    )

    if added:
        print(f"   ✅ Leads addition process completed")
    else:
        print(f"   ❌ Failed to add leads")

    # Check if the leads were added
    print(f"\n✅ Step 4: Verify leads were added to campaign")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    await asyncio.sleep(2)  # Wait for API to process

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
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads were added to campaign!")
                print(f"\n   Campaign: {campaign_id}")
                print(f"   Name: FINAL TEST - Lead Addition v2")
                print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"\n   The campaign should now show {len(actual_campaign_leads)} leads")
                print(f"   instead of '👋 Add some leads to get started'")
            else:
                print(f"\n❌ Leads were NOT added to campaign")
                print(f"   The 'campaign' field is still pointing to old campaigns")
        else:
            print(f"   ❌ Failed to verify: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_final_add_leads())
