"""
Test API payload to see exactly what we're sending
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def test_direct_api_call():
    """Make a direct API call and inspect the exact payload"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Direct API Call\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Test payload with explicit filters
    payload = {
        "api_key": api_key,
        "search_filters": {
            "level": ["C-Level"],
            "employee_count": ["100 - 250"],
            "industry": {
                "include": ["Software & Internet"],
                "exclude": []
            },
            "locations": [
                {
                    "city": "London",
                    "state": "",
                    "country": "United Kingdom"
                }
            ]
        },
        "limit": 5,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Test - London Software C-Level"
    }

    print("📤 Sending Payload:")
    print(json.dumps(payload, indent=2))
    print()

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
                headers=headers,
                json=payload,
            )

            print(f"📥 Response Status: {response.status_code}")
            print(f"📥 Response Body:")
            response_data = response.json()
            print(json.dumps(response_data, indent=2))

            # Check if search_filters are preserved in response
            if 'search_filters' in response_data:
                print(f"\n⚠️  search_filters in response: {response_data['search_filters']}")
                if not response_data['search_filters']:
                    print("❌ WARNING: search_filters is empty in response!")

        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            import traceback
            print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(test_direct_api_call())
