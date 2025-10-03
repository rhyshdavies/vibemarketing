"""
Test AI location filter generation with various geographic targeting scenarios
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService

load_dotenv()


async def test_location_extraction():
    """Test generating SuperSearch location filters from different target audience descriptions"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return

    print("🔑 OpenAI API Key found")
    print("\n" + "="*80)
    print("Testing Location Filter Extraction")
    print("="*80 + "\n")

    # Initialize service
    ai_service = AICopyService(api_key)

    # Test cases with various location formats
    test_cases = [
        {
            "name": "City + State (US)",
            "url": "https://example.com",
            "target_audience": "SaaS founders in San Francisco with 1-10 employees"
        },
        {
            "name": "City Only (UK)",
            "url": "https://example.com",
            "target_audience": "HR managers at construction companies in London, 100-500 employees"
        },
        {
            "name": "City + State Abbreviation",
            "url": "https://example.com",
            "target_audience": "Marketing VPs in New York, NY at enterprise companies"
        },
        {
            "name": "Country Only",
            "url": "https://example.com",
            "target_audience": "CTOs in United Kingdom with Series A funding"
        },
        {
            "name": "Multiple Cities",
            "url": "https://example.com",
            "target_audience": "Sales directors in San Francisco, London, or Berlin"
        },
        {
            "name": "No Location",
            "url": "https://example.com",
            "target_audience": "Small business owners"
        },
        {
            "name": "State Only",
            "url": "https://example.com",
            "target_audience": "Healthcare executives in California"
        },
        {
            "name": "Country + Industry",
            "url": "https://example.com",
            "target_audience": "CEOs at financial services firms in Germany"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print('='*80)
        print(f"Target Audience: {test_case['target_audience']}")
        print(f"\n⏳ Generating filters...")

        try:
            filters = await ai_service.generate_supersearch_filters(
                test_case['target_audience'],
                test_case['url']
            )

            print(f"\n✅ Generated Filters:")
            import json
            print(json.dumps(filters, indent=2))

            # Analyze location filters specifically
            print(f"\n📍 Location Analysis:")
            if "locations" in filters:
                for loc in filters['locations']:
                    city = loc.get('city', '')
                    state = loc.get('state', '')
                    country = loc.get('country', '')

                    if city and state:
                        print(f"   - {city}, {state}, {country}")
                    elif city:
                        print(f"   - {city}, {country}")
                    elif state:
                        print(f"   - {state}, {country}")
                    else:
                        print(f"   - {country}")

                    # Validate structure
                    if 'city' not in loc or 'state' not in loc or 'country' not in loc:
                        print(f"   ⚠️  WARNING: Missing required fields in location object")
            else:
                print("   No locations specified")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())

    print(f"\n{'='*80}")
    print("Location Testing Complete!")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(test_location_extraction())
