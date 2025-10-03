import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def test_without_locations():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    # Test the SAME ICPs that failed before
    test_cases = [
        "CTOs at Series A SaaS startups in San Francisco",
        "Marketing directors at B2B companies in London",
        "CEOs of AI startups in New York"
    ]

    print("\n" + "="*80)
    print("TESTING: Same ICPs but WITHOUT location filters")
    print("="*80 + "\n")

    for icp in test_cases:
        print(f"\nICP: {icp}")
        print("-"*80)

        # Generate filters (should now skip location)
        filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")

        # Check if location was included
        has_location = bool(filters.get("locations"))
        has_title = bool(filters.get("title", {}).get("include"))
        has_employee_count = bool(filters.get("employee_count"))

        print(f"✅ Title filter: {filters.get('title', {}).get('include', [])}")
        print(f"{'✅' if has_employee_count else '  '} Employee count: {filters.get('employee_count', [])}")
        print(f"{'❌ LOCATION REMOVED' if not has_location else '⚠️  Still has location'}: {filters.get('locations', [])}")

        filter_count = sum([has_title, has_employee_count, has_location])
        print(f"\n📊 Filter types used: {filter_count}")

        # Create the list
        try:
            result = await instantly_service.search_leads_supersearch(
                search_filters=filters,
                limit=10
            )

            list_id = result.get('resource_id')
            list_name = result.get('list_name')

            print(f"✅ List created: '{list_name}'")
            print(f"   ID: {list_id}")
            print(f"   → Should find leads now! (Check in 2-5 min)")

        except Exception as e:
            print(f"❌ Error: {str(e)}")

    print("\n" + "="*80)
    print("RESULT:")
    print("="*80)
    print("""
If locations were removed, these lists should now have REAL LEADS!

The tradeoff:
- ✅ More leads found (no location restriction)
- ℹ️  User gets broader results (can filter by location manually if needed)
- ℹ️  Or mention location in email copy to make it relevant

Check Instantly dashboard: https://app.instantly.ai/app/lead-finder
    """)

if __name__ == "__main__":
    asyncio.run(test_without_locations())
