import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def test_3_leads():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    icp = "CTOs at SaaS companies"

    print(f"\n{'='*80}")
    print(f"Testing with 3 leads (to save credits)")
    print(f"ICP: {icp}")
    print(f"{'='*80}\n")

    # Generate filters
    filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")

    print("Filters generated:")
    print(json.dumps(filters, indent=2))

    # Create list with only 3 leads
    try:
        result = await instantly_service.search_leads_supersearch(
            search_filters=filters,
            limit=3,  # Only 3 leads to save money!
            work_email_enrichment=True
        )

        list_id = result.get('resource_id')
        list_name = result.get('list_name')

        print(f"\n✅ Created: '{list_name}'")
        print(f"   List ID: {list_id}")
        print(f"   Lead count: 3 (cost-effective!)")
        print(f"\nCheck Instantly dashboard in 2-5 minutes:")
        print(f"https://app.instantly.ai/app/lead-finder")
        print(f"\nYou should see 3 enriched CTOs with:")
        print(f"  - Verified work emails")
        print(f"  - Company names")
        print(f"  - Job titles")
        print(f"  - LinkedIn profiles")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_3_leads())
