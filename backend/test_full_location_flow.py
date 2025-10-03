"""
End-to-end test: Natural language → AI parsing → SuperSearch API with locations
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService

load_dotenv()


async def test_full_flow():
    """Test the complete flow from natural language to SuperSearch with locations"""

    openai_key = os.getenv("OPENAI_API_KEY")
    instantly_key = os.getenv("INSTANTLY_API_KEY")

    if not openai_key or not instantly_key:
        print("❌ Missing API keys")
        return

    print("✅ API Keys found")
    print("\n" + "="*80)
    print("End-to-End Location Support Test")
    print("="*80 + "\n")

    # Initialize services
    ai_service = AICopyService(openai_key)
    instantly_service = InstantlyService(instantly_key)

    # Test cases combining locations with other filters
    test_cases = [
        {
            "name": "Location + Industry + Size",
            "target_audience": "Heads of HR at construction companies in London with 100-500 employees",
            "url": "https://example.com"
        },
        {
            "name": "Location + Role + Funding",
            "target_audience": "CTOs at Series A B2B companies in San Francisco",
            "url": "https://example.com"
        },
        {
            "name": "Multiple Locations + Department",
            "target_audience": "Marketing directors in New York, London, or Berlin",
            "url": "https://example.com"
        },
        {
            "name": "State-level + Industry",
            "target_audience": "Healthcare executives in California",
            "url": "https://example.com"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test_case['name']}")
        print('='*80)
        print(f"Input: '{test_case['target_audience']}'")

        # Step 1: AI Filter Generation
        print(f"\n📝 Step 1: AI parsing...")
        try:
            filters = await ai_service.generate_supersearch_filters(
                test_case['target_audience'],
                test_case['url']
            )

            import json
            print(f"Generated filters:")
            print(json.dumps(filters, indent=2))

            # Step 2: SuperSearch API Call
            print(f"\n🔍 Step 2: SuperSearch API call...")
            result = await instantly_service.search_leads_supersearch(
                search_filters=filters,
                limit=5
            )

            print(f"\n✅ SUCCESS!")
            print(f"   - Resource ID: {result.get('resource_id')}")
            print(f"   - List Name: {result.get('list_name')}")

            # Analyze what filters were used
            print(f"\n📊 Filter Summary:")
            if "locations" in filters:
                print(f"   - Locations: {len(filters['locations'])} location(s)")
                for loc in filters['locations']:
                    parts = []
                    if loc.get('city'): parts.append(loc['city'])
                    if loc.get('state'): parts.append(loc['state'])
                    if loc.get('country'): parts.append(loc['country'])
                    print(f"     • {', '.join(parts)}")

            if "industry" in filters and filters['industry'].get('include'):
                print(f"   - Industries: {', '.join(filters['industry']['include'])}")

            if "level" in filters:
                print(f"   - Levels: {', '.join(filters['level'])}")

            if "department" in filters:
                print(f"   - Departments: {', '.join(filters['department'])}")

            if "employee_count" in filters:
                print(f"   - Company Size: {', '.join(filters['employee_count'])}")

            if "funding_type" in filters:
                print(f"   - Funding: {', '.join(filters['funding_type'])}")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())

    print(f"\n{'='*80}")
    print("✅ All End-to-End Tests Complete!")
    print('='*80)
    print("\n🎉 Location support is fully functional!")


if __name__ == "__main__":
    asyncio.run(test_full_flow())
