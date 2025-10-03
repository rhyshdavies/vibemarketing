"""
Test with title + city location filter
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def test_title_plus_city():
    """Test with title + city location"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Title + City Location Filter\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Title + City (San Francisco)
    payload = {
        "api_key": api_key,
        "search_filters": {
            "title": {
                "include": ["CEO"],
                "exclude": []
            },
            "locations": [
                {
                    "city": "San Francisco",
                    "state": "California",
                    "country": "United States"
                }
            ]
        },
        "limit": 3,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Test - CEO + San Francisco"
    }

    print("Creating enrichment with CEO + San Francisco...")
    print(json.dumps(payload["search_filters"], indent=2))
    print()

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return

        result = response.json()
        resource_id = result['resource_id']

        print(f"✅ Enrichment created")
        print(f"   Resource ID: {resource_id}")
        print(f"\nNow run this on the Instantly dashboard:")
        print(f"   Title: CEO")
        print(f"   City: San Francisco")
        print(f"   State: California")
        print(f"   Country: United States")
        print(f"   Limit: 3")
        print(f"\nLet me know if it returns leads!")


if __name__ == "__main__":
    asyncio.run(test_title_plus_city())
