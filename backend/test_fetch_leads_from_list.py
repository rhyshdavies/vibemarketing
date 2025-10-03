"""
Try to fetch leads from specific list IDs
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def fetch_leads_from_lists():
    """Try different API endpoints to get leads from lists"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Fetching Leads from Lists\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Try a few different list IDs
    list_ids = [
        ("San Francisco", "d0d97221-4e90-4ff7-8642-69f37deaf0ab"),
        ("London Software", "b11cb275-4f8b-4ce8-b411-1b042379a637"),
        ("Software C-Level", "5af6c9a9-b9ff-4e46-885b-9c492940d426"),
    ]

    async with httpx.AsyncClient(timeout=60.0) as client:
        for name, list_id in list_ids:
            print(f"\n{'='*80}")
            print(f"List: {name}")
            print(f"ID: {list_id}")
            print('='*80)

            # Try different endpoints
            endpoints = [
                f"/leads?list_id={list_id}",
                f"/lead-lists/{list_id}/leads",
                f"/lead-lists/{list_id}",
            ]

            for endpoint in endpoints:
                print(f"\nTrying: {endpoint}")

                try:
                    response = await client.get(
                        f"{base_url}{endpoint}",
                        headers=headers,
                        params={"api_key": api_key, "limit": 5}
                    )

                    print(f"Status: {response.status_code}")

                    if response.status_code == 200:
                        data = response.json()

                        # Check if we got leads
                        leads = None
                        if isinstance(data, list):
                            leads = data
                        elif isinstance(data, dict):
                            if 'leads' in data:
                                leads = data['leads']
                            elif 'items' in data:
                                leads = data['items']

                        if leads and len(leads) > 0:
                            print(f"✅ Found {len(leads)} leads!")
                            lead = leads[0]
                            print(f"\nFirst lead:")
                            print(json.dumps(lead, indent=2))
                            break
                        elif leads is not None:
                            print(f"⚠️  Endpoint works but returned 0 leads")
                        else:
                            print(f"⚠️  Response format:")
                            print(json.dumps(data, indent=2)[:500])
                    else:
                        print(f"❌ {response.text[:200]}")

                except Exception as e:
                    print(f"❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(fetch_leads_from_lists())
