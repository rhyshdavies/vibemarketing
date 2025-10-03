import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def analyze_filters():
    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))

    # The ones that WORKED
    working = [
        "Sales managers at enterprise software companies",
        "Founders of early-stage fintech companies"
    ]

    # The ones that FAILED
    failed = [
        "CTOs at Series A SaaS startups in San Francisco",
        "Marketing directors at B2B companies in London",
        "CEOs of AI startups in New York"
    ]

    print("\n" + "="*80)
    print("ANALYZING: What worked vs what failed")
    print("="*80)

    print("\n✅ WORKED - These found 10 leads:")
    print("-"*80)
    for icp in working:
        filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")
        print(f"\nICP: {icp}")
        print(json.dumps(filters, indent=2))

    print("\n\n❌ FAILED - These were empty:")
    print("-"*80)
    for icp in failed:
        filters = await ai_service.generate_supersearch_filters(icp, "sendcupcake.com")
        print(f"\nICP: {icp}")
        print(json.dumps(filters, indent=2))

    print("\n\n" + "="*80)
    print("HYPOTHESIS:")
    print("="*80)
    print("""
The FAILED ones all have LOCATIONS specified:
- San Francisco
- London
- New York

The WORKING ones have NO location filters.

THEORY: Location filtering might be too restrictive when combined with job titles.
Instantly's database might not have enough leads in those specific cities.

SOLUTION: Make location filters BROADER or OPTIONAL.
- Instead of "San Francisco" → try "California" or "USA"
- Instead of "London" → try "UK"
- Or remove location entirely and rely on job title + company size
    """)

if __name__ == "__main__":
    asyncio.run(analyze_filters())
