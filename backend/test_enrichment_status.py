"""
Test if enrichment status endpoint exists in Instantly.ai API v2
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


async def test_enrichment_endpoints():
    api_key = os.getenv('INSTANTLY_API_KEY')
    base_url = 'https://api.instantly.ai/api/v2'
    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    # First, let's list all lead lists to find a recent one
    print("🔍 Testing Instantly.ai API v2 enrichment endpoints")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Test 1: Get lead lists
        print("\n📋 Test 1: Get lead lists")
        response = await client.get(
            f'{base_url}/lead-lists',
            headers=headers,
            params={'api_key': api_key}
        )
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            lists = data if isinstance(data, list) else data.get('items', [])
            print(f"   Found {len(lists)} lead lists")

            if lists:
                # Get the most recent list
                recent_list = lists[0]
                list_id = recent_list.get('id') if isinstance(recent_list, dict) else recent_list
                print(f"   Most recent list ID: {list_id}")

                # Test 2: Try to get enrichment status
                print(f"\n📋 Test 2: Try GET /supersearch-enrichment/{list_id}")
                status_response = await client.get(
                    f'{base_url}/supersearch-enrichment/{list_id}',
                    headers=headers
                )
                print(f"   Status: {status_response.status_code}")
                if status_response.status_code == 200:
                    print(f"   ✅ Endpoint exists!")
                    print(f"   Response: {status_response.text[:500]}")
                else:
                    print(f"   ❌ Endpoint returned: {status_response.text[:200]}")

                # Test 3: Try to get leads with filtering
                print(f"\n📋 Test 3: Try GET /leads with list_id filter")
                leads_response = await client.get(
                    f'{base_url}/leads',
                    headers=headers,
                    params={
                        'list_id': list_id,
                        'limit': 5
                    }
                )
                print(f"   Status: {leads_response.status_code}")
                if leads_response.status_code == 200:
                    print(f"   ✅ Endpoint works!")
                    leads_data = leads_response.json()
                    items = leads_data.get('items', [])
                    print(f"   Got {len(items)} leads")
                else:
                    print(f"   Response: {leads_response.text[:200]}")

                # Test 4: Try POST /leads/list with list_ids filter
                print(f"\n📋 Test 4: Try POST /leads/list with list_ids filter")
                post_leads_response = await client.post(
                    f'{base_url}/leads/list',
                    headers=headers,
                    json={
                        'list_ids': [list_id],
                        'limit': 5
                    }
                )
                print(f"   Status: {post_leads_response.status_code}")
                if post_leads_response.status_code == 200:
                    print(f"   ✅ Endpoint works!")
                    post_data = post_leads_response.json()
                    items = post_data.get('items', [])
                    print(f"   Got {len(items)} leads")
                else:
                    print(f"   Response: {post_leads_response.text[:200]}")
        else:
            print(f"   Error: {response.text}")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(test_enrichment_endpoints())
