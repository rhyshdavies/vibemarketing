"""
Debug: Check if leads are actually in the campaign or just in the list
"""
import asyncio
import os
from dotenv import load_dotenv
import httpx
import json

load_dotenv()


async def debug_campaign_leads():
    """Debug campaign leads issue"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    campaign_id = "f454e065-4bc3-4ccc-801e-dadb9233fd59"
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("🔍 DEBUGGING CAMPAIGN LEADS ISSUE")
    print("=" * 80)

    # Test 1: Get leads filtered by campaign_id
    print(f"\n1️⃣  Fetch leads with campaign_ids filter")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "campaign_ids": [campaign_id],
                "limit": 10
            },
        )

        if response.status_code == 200:
            data = response.json()
            campaign_leads = data.get("items", [])
            print(f"   ✅ Found {len(campaign_leads)} leads with campaign_ids=[{campaign_id}]")

            if len(campaign_leads) > 0:
                # Check if these leads actually belong to OUR campaign
                first_lead = campaign_leads[0]
                assigned_campaign = first_lead.get("campaign")
                print(f"   First lead's campaign field: {assigned_campaign}")
                print(f"   Does it match our campaign? {assigned_campaign == campaign_id}")
            else:
                print(f"   ❌ No leads found with this campaign_id filter!")
        else:
            print(f"   ❌ Error: {response.text}")

    # Test 2: Get leads filtered by list_id
    print(f"\n2️⃣  Fetch leads with list_ids filter")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "list_ids": [list_id],
                "limit": 10
            },
        )

        if response.status_code == 200:
            data = response.json()
            list_leads = data.get("items", [])
            print(f"   ✅ Found {len(list_leads)} leads with list_ids=[{list_id}]")

            if len(list_leads) > 0:
                first_lead = list_leads[0]
                assigned_campaign = first_lead.get("campaign")
                print(f"   First lead's campaign field: {assigned_campaign}")
                print(f"   Does it match our campaign? {assigned_campaign == campaign_id}")
        else:
            print(f"   ❌ Error: {response.text}")

    # Test 3: Check campaign details
    print(f"\n3️⃣  Get campaign details")
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"https://api.instantly.ai/api/v2/campaigns/{campaign_id}",
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            print(f"   Campaign response keys: {data.keys()}")
            print(f"   Campaign name: {data.get('name')}")
            print(f"   Campaign status: {data.get('status')}")
            print(f"   Lead list IDs: {data.get('lead_list_ids')}")
            print(f"\n   Full campaign data:")
            print(json.dumps(data, indent=2))
        else:
            print(f"   ❌ Error: {response.text}")

    print(f"\n" + "=" * 80)
    print("ANALYSIS:")
    print("If leads with list_ids filter have campaign field != our campaign_id,")
    print("it means Instantly did NOT automatically assign them to our campaign.")
    print("We may need to use a different approach to add leads to campaigns.")


if __name__ == "__main__":
    asyncio.run(debug_campaign_leads())
