"""
Check if leads are already in a campaign when created with lead_list_ids
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import json

load_dotenv()


async def test_campaign_leads():
    """Test if creating a campaign with lead_list_ids automatically adds leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    # Use an existing list with leads
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    print(f"🔍 Step 1: Check leads in list {list_id}")
    leads = await instantly_service.get_leads_from_list(list_id, limit=10)
    print(f"✅ Found {len(leads)} leads in list")

    # Create a campaign with this lead_list_id
    print(f"\n📧 Step 2: Create campaign WITH lead_list_ids parameter")
    campaign_data = await instantly_service.create_campaign(
        name="Test - Check if leads auto-add",
        lead_list_id=list_id,  # Pass the list ID during creation
        variants=[
            {
                "subject": "Test",
                "body": "Hi {{firstName}},\n\nTest.\n\nBest"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"✅ Created campaign: {campaign_id}")

    # Now check if this campaign has leads
    print(f"\n🔍 Step 3: Fetch leads that belong to campaign {campaign_id}")

    # Use the leads/list endpoint to filter by campaign_id
    import httpx
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
            print(f"✅ Found {len(campaign_leads)} leads in campaign")

            if len(campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! Leads were automatically added to campaign!")
                print(f"   Sample lead:\n{json.dumps(campaign_leads[0], indent=2)}")
            else:
                print(f"\n❌ No leads in campaign - they were NOT automatically added")
        else:
            print(f"❌ Failed to fetch campaign leads: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_campaign_leads())
