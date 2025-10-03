import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_fetch_leads_from_supersearch():
    """Test fetching leads from a SuperSearch enrichment job"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    # Use the list ID from the previous test
    list_id = "cce93abd-dd5c-423b-8133-9f5196f41529"

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("=" * 80)
    print("TESTING LEAD FETCH FROM SUPERSEARCH")
    print("=" * 80)
    print(f"\nList ID: {list_id}\n")

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test 1: Get enrichment status
        print("1. Testing GET /api/v2/supersearch-enrichment/{resource_id}")
        status_response = await client.get(
            f"{base_url}/supersearch-enrichment/{list_id}",
            headers=headers,
            params={"api_key": api_key}
        )

        print(f"   Status Code: {status_response.status_code}")
        if status_response.status_code == 200:
            status_data = status_response.json()
            print(f"   Response:")
            print(json.dumps(status_data, indent=2))
        else:
            print(f"   Error: {status_response.text}")

        print("\n" + "-" * 80 + "\n")

        # Test 2: Get enrichment history
        print("2. Testing GET /api/v2/supersearch-enrichment/history/{resource_id}")
        history_response = await client.get(
            f"{base_url}/supersearch-enrichment/history/{list_id}",
            headers=headers,
            params={"api_key": api_key}
        )

        print(f"   Status Code: {history_response.status_code}")
        if history_response.status_code == 200:
            history_data = history_response.json()
            print(f"   Response:")
            print(json.dumps(history_data, indent=2))

            # Check if leads are in the response
            if isinstance(history_data, list):
                print(f"\n   ✅ Found {len(history_data)} items in array")
                if history_data:
                    print(f"   Sample item: {json.dumps(history_data[0], indent=2)}")
            elif isinstance(history_data, dict):
                leads_fields = ["leads", "results", "data", "items"]
                for field in leads_fields:
                    if field in history_data:
                        print(f"\n   ✅ Found '{field}' field with {len(history_data[field])} items")
                        break
        else:
            print(f"   Error: {history_response.text}")

        print("\n" + "-" * 80 + "\n")

        # Test 3: Get lead list details
        print("3. Testing GET /api/v2/lead-lists/{id}")
        list_response = await client.get(
            f"{base_url}/lead-lists/{list_id}",
            headers=headers,
            params={"api_key": api_key}
        )

        print(f"   Status Code: {list_response.status_code}")
        if list_response.status_code == 200:
            list_data = list_response.json()
            print(f"   Response:")
            print(json.dumps(list_data, indent=2))

            # Check if leads are in the response
            if "leads" in list_data:
                print(f"\n   ✅ Found 'leads' field with {len(list_data['leads'])} items")
                if list_data['leads']:
                    print(f"   Sample lead: {json.dumps(list_data['leads'][0], indent=2)}")
        else:
            print(f"   Error: {list_response.text}")

        print("\n" + "-" * 80 + "\n")

        # Test 4: Try getting leads from campaign
        print("4. Testing if we need to get leads through a campaign")
        print("   (This might be the only way to access SuperSearch leads)")

asyncio.run(test_fetch_leads_from_supersearch())
