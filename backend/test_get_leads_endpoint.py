"""
Test different endpoints to find how to get leads from a list
"""
import asyncio
import os
from dotenv import load_dotenv
import httpx
import json

load_dotenv()


async def test_get_leads_endpoints():
    """Test various endpoints to fetch leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    # Test with a known list ID
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print(f"Testing endpoints for list: {list_id}\n")

    # Test 1: GET /api/v2/lead-lists/{id}
    print("=" * 80)
    print("Test 1: GET /api/v2/lead-lists/{id}")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{base_url}/lead-lists/{list_id}",
            headers=headers,
            params={"api_key": api_key},
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response keys: {data.keys()}")
            print(f"Full response:\n{json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")

    # Test 2: POST /api/v2/lead/get-leads
    print("\n" + "=" * 80)
    print("Test 2: POST /api/v2/lead/get-leads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/lead/get-leads",
            headers=headers,
            json={
                "api_key": api_key,
                "list_id": list_id,
                "limit": 10,
                "skip": 0
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            if isinstance(data, list):
                print(f"Found {len(data)} leads")
                if len(data) > 0:
                    print(f"\nFirst lead:\n{json.dumps(data[0], indent=2)}")
            elif isinstance(data, dict):
                print(f"Response keys: {data.keys()}")
                print(f"Full response:\n{json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")

    # Test 3: GET /api/v2/lead/get-leads with params
    print("\n" + "=" * 80)
    print("Test 3: GET /api/v2/lead/get-leads")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{base_url}/lead/get-leads",
            headers=headers,
            params={
                "api_key": api_key,
                "list_id": list_id,
                "limit": 10,
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            if isinstance(data, list):
                print(f"Found {len(data)} leads")
                if len(data) > 0:
                    print(f"\nFirst lead:\n{json.dumps(data[0], indent=2)}")
            elif isinstance(data, dict):
                print(f"Response keys: {data.keys()}")
                print(f"Full response:\n{json.dumps(data, indent=2)}")
        else:
            print(f"Error: {response.text}")

    # Test 4: POST /api/v2/leads/list (correct endpoint from docs)
    print("\n" + "=" * 80)
    print("Test 4: POST /api/v2/leads/list (with list_ids filter)")
    print("=" * 80)
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            f"{base_url}/leads/list",
            headers=headers,
            json={
                "list_ids": [list_id],
                "limit": 10
            },
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            if isinstance(data, dict):
                print(f"Response keys: {data.keys()}")
                if "leads" in data:
                    leads = data["leads"]
                    print(f"Found {len(leads)} leads")
                    if len(leads) > 0:
                        print(f"\nFirst lead (keys):\n{leads[0].keys()}")
                        print(f"\nFirst lead:\n{json.dumps(leads[0], indent=2)}")
                else:
                    print(f"Full response:\n{json.dumps(data, indent=2)}")
            elif isinstance(data, list):
                print(f"Found {len(data)} leads")
                if len(data) > 0:
                    print(f"\nFirst lead:\n{json.dumps(data[0], indent=2)}")
        else:
            print(f"Error: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_get_leads_endpoints())
