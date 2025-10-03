import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def test_simplified_filters():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    test_icps = [
        "CTOs at Series A SaaS startups in San Francisco",
        "Marketing directors in the UK",
        "Founders of early-stage tech companies"
    ]

    for icp in test_icps:
        print(f"\n{'='*80}")
        print(f"ICP: {icp}")
        print(f"{'='*80}\n")

        # Generate filters with new simplified approach
        filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")

        print("Generated Filters:")
        print(json.dumps(filters, indent=2))

        # Count how many filter types are used
        filter_count = 0
        if filters.get("title", {}).get("include"):
            filter_count += 1
            print(f"\n✅ Title filter: {filters['title']['include']}")

        if filters.get("locations"):
            filter_count += 1
            print(f"✅ Location filter: {filters['locations']}")

        if filters.get("employee_count"):
            filter_count += 1
            print(f"✅ Employee count filter: {filters['employee_count']}")

        if filters.get("level"):
            filter_count += 1
            print(f"✅ Level filter: {filters['level']}")

        if filters.get("department"):
            filter_count += 1
            print(f"⚠️  Department filter: {filters['department']}")

        if filters.get("revenue"):
            filter_count += 1
            print(f"⚠️  Revenue filter: {filters['revenue']}")

        print(f"\n📊 Total filter types used: {filter_count}")

        if filter_count <= 3:
            print("✅ Good! Using 3 or fewer filter types")
        else:
            print("❌ Too many filters! Should use max 3 types")

        # Create the list
        try:
            result = await instantly_service.search_leads_supersearch(
                search_filters=filters,
                limit=10
            )
            print(f"\n✅ List created: {result.get('resource_id')}")
            print(f"   Check this list in Instantly dashboard in 2-5 minutes")
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_simplified_filters())
