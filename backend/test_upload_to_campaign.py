"""
Test uploading leads directly to a campaign (not a list)
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_upload_to_campaign():
    """Test uploading leads with campaign_id"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    campaign_id = "f454e065-4bc3-4ccc-801e-dadb9233fd59"
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Get a few leads from the list
    print("📋 Getting leads from list...")
    leads = await instantly_service.get_leads_from_list(list_id, limit=2)
    print(f"Found {len(leads)} leads\n")

    if not leads:
        print("No leads to test with")
        return

    # Try uploading leads with campaign_id
    print(f"{'='*80}")
    print("Test: POST /api/v2/leads/list with campaign_id (not lead_list_id)")
    print("=" * 80)

    test_leads = [
        {
            "email": leads[0].get("email"),
            "first_name": leads[0].get("first_name"),
            "last_name": leads[0].get("last_name", ""),
            "company_name": leads[0].get("company_name", ""),
        }
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "campaign_id": campaign_id,  # Use campaign_id instead of lead_list_id
                "leads": test_leads,
                "skip_if_in_workspace": False,
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ Response: {response.json()}")
        else:
            print(f"❌ Error: {response.text}")

    # Check if the lead was added
    print(f"\n🔍 Checking if lead was added to campaign...")
    await asyncio.sleep(2)  # Wait a moment for it to process

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
            print(f"Leads with campaign field = {campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"✅ SUCCESS! Leads were added to campaign")
                for lead in actual_campaign_leads:
                    print(f"  - {lead.get('email')}")
            else:
                print(f"❌ Leads were NOT added to campaign")


if __name__ == "__main__":
    asyncio.run(test_upload_to_campaign())
