"""
Test uploading leads using /api/v2/leads (without /list)
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_upload_without_list():
    """Test uploading leads to campaign using /api/v2/leads"""

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

    # Get a lead from the list
    print("📋 Getting a fresh lead from list...")
    leads = await instantly_service.get_leads_from_list(list_id, limit=5)
    print(f"Found {len(leads)} leads\n")

    if not leads:
        print("No leads to test with")
        return

    # Find a lead that's NOT already in our campaign
    test_lead = leads[4] if len(leads) > 4 else leads[0]  # Use 5th lead

    print(f"Test lead: {test_lead.get('email')}")
    print(f"Test lead current campaign: {test_lead.get('campaign')}\n")

    print(f"{'='*80}")
    print("Test: POST /api/v2/leads (singular, not /leads/list)")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads",
            headers=headers,
            json={
                "campaign_id": campaign_id,
                "email": test_lead.get("email"),
                "first_name": test_lead.get("first_name"),
                "last_name": test_lead.get("last_name", ""),
                "company_name": test_lead.get("company_name", ""),
                "skip_if_in_workspace": False,
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")

    # Check if the lead was added
    print(f"\n🔍 Checking if lead was added to campaign...")
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
            print(f"Leads with campaign field = {campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"✅ SUCCESS! Leads were added to campaign:")
                for lead in actual_campaign_leads[:5]:  # Show first 5
                    print(f"  - {lead.get('email')}")
            else:
                print(f"❌ Leads were NOT added to campaign")


if __name__ == "__main__":
    asyncio.run(test_upload_without_list())
