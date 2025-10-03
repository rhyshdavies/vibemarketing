"""
Test different country name formats to find what the API accepts
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_country_formats():
    """Test various country name formats"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Country Formats\n")
    instantly_service = InstantlyService(api_key)

    # Test different country formats
    test_cases = [
        {"name": "USA", "country": "USA"},
        {"name": "United States", "country": "United States"},
        {"name": "US", "country": "US"},
        {"name": "UK", "country": "UK"},
        {"name": "United Kingdom", "country": "United Kingdom"},
        {"name": "GB", "country": "GB"},
        {"name": "Germany", "country": "Germany"},
        {"name": "DE", "country": "DE"},
    ]

    for test in test_cases:
        print(f"\n{'='*60}")
        print(f"Testing: {test['name']}")
        print('='*60)

        try:
            result = await instantly_service.search_leads_supersearch(
                search_filters={
                    "level": ["C-Level"],
                    "locations": [
                        {
                            "city": "",
                            "state": "",
                            "country": test['country']
                        }
                    ]
                },
                limit=5
            )

            print(f"✅ SUCCESS - '{test['country']}' is accepted")
            print(f"   Resource ID: {result.get('resource_id')}")

            # Check if we can get the status to see if it found leads
            import json
            print(f"   Response: {json.dumps(result, indent=2)}")

        except Exception as e:
            print(f"❌ FAILED - '{test['country']}' rejected")
            print(f"   Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(test_country_formats())
