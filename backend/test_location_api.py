"""
Test location filters with actual Instantly SuperSearch API
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_location_api():
    """Test that location filters work with the real Instantly API"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found in environment")
        return

    print("🔑 Instantly API Key found")
    print("\n" + "="*80)
    print("Testing Location Filters with Instantly API")
    print("="*80 + "\n")

    # Initialize service
    instantly_service = InstantlyService(api_key)

    # Test cases with various location formats
    test_cases = [
        {
            "name": "City + State + Country",
            "filters": {
                "level": ["C-Level"],
                "locations": [
                    {
                        "city": "San Francisco",
                        "state": "California",
                        "country": "United States"
                    }
                ]
            }
        },
        {
            "name": "City + Country (no state)",
            "filters": {
                "level": ["C-Level"],
                "locations": [
                    {
                        "city": "London",
                        "state": "",
                        "country": "United Kingdom"
                    }
                ]
            }
        },
        {
            "name": "Country Only",
            "filters": {
                "level": ["C-Level"],
                "locations": [
                    {
                        "city": "",
                        "state": "",
                        "country": "United Kingdom"
                    }
                ]
            }
        },
        {
            "name": "Multiple Locations",
            "filters": {
                "level": ["C-Level"],
                "locations": [
                    {
                        "city": "San Francisco",
                        "state": "California",
                        "country": "United States"
                    },
                    {
                        "city": "London",
                        "state": "",
                        "country": "United Kingdom"
                    }
                ]
            }
        },
        {
            "name": "State Only",
            "filters": {
                "level": ["C-Level"],
                "locations": [
                    {
                        "city": "",
                        "state": "California",
                        "country": "United States"
                    }
                ]
            }
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print('='*80)

        import json
        print(f"Filters:")
        print(json.dumps(test_case['filters'], indent=2))

        print(f"\n⏳ Searching leads...")

        try:
            result = await instantly_service.search_leads_supersearch(
                search_filters=test_case['filters'],
                limit=5  # Small limit for testing
            )

            if "leads" in result:
                lead_count = len(result.get("leads", []))
                print(f"\n✅ API Response: Found {lead_count} leads")

                # Show sample leads
                if lead_count > 0:
                    print("\nSample leads:")
                    for lead in result["leads"][:3]:
                        name = lead.get("first_name", "") + " " + lead.get("last_name", "")
                        title = lead.get("title", "N/A")
                        company = lead.get("company_name", "N/A")
                        location = lead.get("location", "N/A")
                        print(f"   - {name} | {title} at {company} | {location}")
                else:
                    print("   No leads found (filters may be too restrictive)")
            else:
                print(f"\n✅ API Response: {result}")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())

    print(f"\n{'='*80}")
    print("Location API Testing Complete!")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(test_location_api())
