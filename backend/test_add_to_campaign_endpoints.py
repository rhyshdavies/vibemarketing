"""
Test different endpoints for adding leads to campaigns
"""
import asyncio
import os
from dotenv import load_dotenv
import httpx
import json

load_dotenv()


async def test_add_to_campaign_endpoints():
    """Test various endpoints to add leads to campaigns"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    # Use test IDs - replace with actual values
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"
    campaign_id = "2e2e645a-d37c-46b4-8235-8c2f7a1fa459"  # From previous test
    lead_id = "000332ff-689e-4505-ba08-607238b74a45"  # Sample lead ID

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Testing add-to-campaign endpoints")
    print(f"Campaign ID: {campaign_id}")
    print(f"Lead ID: {lead_id}\n")

    # Test 1: POST /api/v2/lead/moveleads
    print("=" * 80)
    print("Test 1: POST /api/v2/lead/moveleads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/lead/moveleads",
            headers=headers,
            json={
                "lead_ids": [lead_id],
                "campaign_id": campaign_id,
                "skip_if_in_campaign": False,
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")

    # Test 2: POST /api/v2/lead/bulkaddleads
    print("\n" + "=" * 80)
    print("Test 2: POST /api/v2/lead/bulkaddleads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/lead/bulkaddleads",
            headers=headers,
            json={
                "campaign_id": campaign_id,
                "leads": [
                    {
                        "id": lead_id,
                        "email": "carrie.cai@hungrystudio.com",
                        "first_name": "Carrie"
                    }
                ]
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")

    # Test 3: POST /api/v2/leads/bulk-add
    print("\n" + "=" * 80)
    print("Test 3: POST /api/v2/leads/bulk-add")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/leads/bulk-add",
            headers=headers,
            json={
                "campaign_id": campaign_id,
                "lead_ids": [lead_id]
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")

    # Test 4: POST /api/v2/campaigns/{id}/leads
    print("\n" + "=" * 80)
    print("Test 4: POST /api/v2/campaigns/{id}/leads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/campaigns/{campaign_id}/leads",
            headers=headers,
            json={
                "lead_ids": [lead_id]
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")

    # Test 5: POST /api/v2/campaigns/{id}/add-leads
    print("\n" + "=" * 80)
    print("Test 5: POST /api/v2/campaigns/{id}/add-leads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/campaigns/{campaign_id}/add-leads",
            headers=headers,
            json={
                "lead_ids": [lead_id]
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"Success: {response.json()}")
        else:
            print(f"Error: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_add_to_campaign_endpoints())
