"""
Test with title + keyword filter
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def test_with_keyword():
    """Test with title + keyword"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Title + Keyword Filter\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Title + Keyword
    payload = {
        "api_key": api_key,
        "search_filters": {
            "title": {
                "include": ["CEO"],
                "exclude": []
            },
            "keyword_filter": {
                "include": ["cybersecurity"],
                "exclude": ""
            }
        },
        "limit": 3,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Test - CEO + Cybersecurity"
    }

    print("Creating enrichment with CEO + cybersecurity keyword...")
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
        print(f"   Keyword: cybersecurity (in company description filter)")
        print(f"   Limit: 3")
        print(f"\nLet me know if it returns leads!")


if __name__ == "__main__":
    asyncio.run(test_with_keyword())
