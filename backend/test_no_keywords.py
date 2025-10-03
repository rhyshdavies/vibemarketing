import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def test_no_keywords():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    test_icp = "CTOs at Series A SaaS startups in San Francisco"

    print(f"\n{'='*80}")
    print(f"Testing ICP: {test_icp}")
    print(f"{'='*80}\n")

    # Generate filters
    filters = await ai_service.generate_supersearch_filters(test_icp, "sendcupcake.com")

    print("Generated Filters:")
    print(json.dumps(filters, indent=2))

    # Verify keyword_filter is empty
    keyword_include = filters.get("keyword_filter", {}).get("include", "")
    keyword_exclude = filters.get("keyword_filter", {}).get("exclude", "")

    print(f"\n{'='*80}")
    print("Verification:")
    print(f"{'='*80}")
    print(f"keyword_filter.include: '{keyword_include}'")
    print(f"keyword_filter.exclude: '{keyword_exclude}'")

    if keyword_include == "" and keyword_exclude == "":
        print("✅ PASS: keyword_filter is empty (as expected)")
    else:
        print("❌ FAIL: keyword_filter should be empty!")

    # Now test with Instantly SuperSearch
    print(f"\n{'='*80}")
    print("Creating SuperSearch list without keywords...")
    print(f"{'='*80}\n")

    try:
        result = await instantly_service.search_leads_supersearch(
            search_filters=filters,
            limit=10
        )
        print(f"✅ List created: {result.get('resource_id')}")
        print(f"\nCheck Instantly dashboard in 2-5 minutes:")
        print(f"https://app.instantly.ai/")
        print(f"\nThis list should have leads since we removed keyword restrictions!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_no_keywords())
