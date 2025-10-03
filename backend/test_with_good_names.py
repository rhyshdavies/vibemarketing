import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json
from datetime import datetime

load_dotenv()

async def test_with_good_names():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    # Test cases with different ICPs
    test_cases = [
        {
            "icp": "CTOs at Series A SaaS startups in San Francisco",
            "expected": "Tech leaders in SF Bay Area"
        },
        {
            "icp": "Marketing directors at B2B companies in London",
            "expected": "Marketing leaders in London"
        },
        {
            "icp": "Founders of early-stage fintech companies",
            "expected": "Fintech founders"
        },
        {
            "icp": "Sales managers at enterprise software companies",
            "expected": "Enterprise sales managers"
        },
        {
            "icp": "CEOs of AI startups in New York",
            "expected": "AI startup CEOs in NYC"
        }
    ]

    print(f"\n{'='*80}")
    print(f"Creating {len(test_cases)} lead lists with descriptive names")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")

    results = []

    for i, test in enumerate(test_cases, 1):
        icp = test["icp"]

        print(f"\n[{i}/{len(test_cases)}] ICP: {icp}")
        print(f"{'─'*80}")

        # Generate filters
        filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")

        # Show what filters were generated
        filter_summary = []
        if filters.get("title", {}).get("include"):
            filter_summary.append(f"Titles: {', '.join(filters['title']['include'][:2])}")
        if filters.get("locations"):
            loc = filters['locations'][0]
            city = loc.get('city', '').strip()
            country = loc.get('country', '').strip()
            loc_str = city if city else country
            if loc_str:
                filter_summary.append(f"Location: {loc_str}")
        if filters.get("employee_count"):
            filter_summary.append(f"Size: {filters['employee_count'][0]}")

        print(f"Filters: {' | '.join(filter_summary)}")

        # Create the list
        try:
            result = await instantly_service.search_leads_supersearch(
                search_filters=filters,
                limit=10
            )

            list_id = result.get('resource_id')
            list_name = result.get('list_name', 'Unknown')

            print(f"✅ Created: '{list_name}'")
            print(f"   List ID: {list_id}")

            results.append({
                "icp": icp,
                "list_name": list_name,
                "list_id": list_id,
                "filters": filter_summary
            })

        except Exception as e:
            print(f"❌ Error: {str(e)}")
            results.append({
                "icp": icp,
                "error": str(e)
            })

    # Summary
    print(f"\n{'='*80}")
    print(f"SUMMARY - {len(results)} lists created")
    print(f"{'='*80}\n")

    for i, res in enumerate(results, 1):
        if "error" not in res:
            print(f"{i}. '{res['list_name']}'")
            print(f"   {res['icp']}")
            print(f"   ID: {res['list_id']}")
            print()

    print(f"{'='*80}")
    print(f"✅ Check your Instantly dashboard in 2-5 minutes:")
    print(f"   https://app.instantly.ai/app/lead-finder")
    print(f"\nLook for these list names to find your leads!")
    print(f"{'='*80}\n")

if __name__ == "__main__":
    asyncio.run(test_with_good_names())
