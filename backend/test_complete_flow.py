"""
Complete test: Create list, upload leads, create campaign, attach leads to campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_complete_flow():
    """Test the complete flow from creating a list to attaching leads to campaign"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 COMPLETE FLOW TEST")
    print("=" * 80)

    # Step 1: Create a new lead list
    print(f"\n✅ Step 1: Create new lead list")
    list_name = "Test List - Complete Flow"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/lead-lists",
            headers=headers,
            json={"name": list_name},
        )
        if response.status_code in [200, 201]:
            list_data = response.json()
            list_id = list_data.get("id")
            print(f"   ✅ Lead list created: {list_id}")
        else:
            print(f"   ❌ Failed to create list: {response.text}")
            return

    # Step 2: Upload test leads to the list
    print(f"\n✅ Step 2: Upload test leads to list")
    test_leads = [
        {
            "email": f"test1_{list_id[:8]}@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "company_name": "Acme Corp"
        },
        {
            "email": f"test2_{list_id[:8]}@example.com",
            "first_name": "Jane",
            "last_name": "Smith",
            "company_name": "Tech Inc"
        },
        {
            "email": f"test3_{list_id[:8]}@example.com",
            "first_name": "Bob",
            "last_name": "Johnson",
            "company_name": "StartupXYZ"
        }
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "lead_list_id": list_id,
                "leads": test_leads,
                "skip_if_in_workspace": False,
            },
        )
        if response.status_code in [200, 201]:
            print(f"   ✅ Uploaded {len(test_leads)} test leads")
        else:
            print(f"   ❌ Failed to upload leads: {response.text}")
            return

    # Wait a moment for leads to be saved
    await asyncio.sleep(1)

    # Step 3: Verify leads are in the list
    print(f"\n✅ Step 3: Verify leads are in list")
    leads_in_list = await instantly_service.get_leads_from_list(list_id, limit=100)
    print(f"   Found {len(leads_in_list)} leads in list")

    if len(leads_in_list) == 0:
        print("   ⚠️ No leads found, waiting 2 more seconds...")
        await asyncio.sleep(2)
        leads_in_list = await instantly_service.get_leads_from_list(list_id, limit=100)
        print(f"   Found {len(leads_in_list)} leads in list after waiting")

    # Step 4: Create campaign
    print(f"\n✅ Step 4: Create campaign")
    campaign_data = await instantly_service.create_campaign(
        name="TEST - Complete Flow Campaign",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Test complete flow",
                "body": "Hi {{firstName}},\\n\\nThis is a test.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   ✅ Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 5: Add leads to campaign
    print(f"\n✅ Step 5: Add leads from list to campaign")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        lead_list_id=list_id
    )

    if not added:
        print(f"   ❌ Failed to add leads")
        return

    # Step 6: Verify leads are in campaign
    print(f"\n✅ Step 6: Verify leads are in campaign")
    await asyncio.sleep(2)

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
                print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"\n   ✅ The campaign should now show {len(actual_campaign_leads)} leads")
                print(f"   ✅ No more '👋 Add some leads to get started'")

                print(f"\n   Leads in campaign:")
                for lead in actual_campaign_leads:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n❌ Leads were NOT added to campaign")
                print(f"   Campaign still shows: '👋 Add some leads to get started'")
                print(f"\n   Debugging info:")
                print(f"   Total items returned: {len(campaign_leads)}")
                if campaign_leads:
                    print(f"   First lead campaign field: {campaign_leads[0].get('campaign')}")
        else:
            print(f"   ❌ Failed to verify: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_complete_flow())
