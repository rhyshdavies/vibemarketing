"""
Check specific enrichment results using resource IDs from earlier tests
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def check_specific_enrichments():
    """Check results from specific resource IDs"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Checking Specific Enrichment Results\n")
    instantly_service = InstantlyService(api_key)

    # Resource IDs from our tests (these should be completed by now)
    test_resources = [
        {
            "name": "Software & Internet industry",
            "resource_id": "c0836b75-9174-45e2-958d-bf3b40458662"
        },
        {
            "name": "C-Level in San Francisco",
            "resource_id": "d0d97221-4e90-4ff7-8642-69f37deaf0ab"
        },
        {
            "name": "C-Level USA (no filters)",
            "resource_id": "80a2c570-f9f8-45de-b3b5-baf7cf29176e"
        },
        {
            "name": "London Software C-Level",
            "resource_id": "b11cb275-4f8b-4ce8-b411-1b042379a637"
        }
    ]

    for test in test_resources:
        print(f"\n{'='*80}")
        print(f"Test: {test['name']}")
        print(f"Resource ID: {test['resource_id']}")
        print('='*80)

        try:
            # Get status
            status = await instantly_service.get_supersearch_enrichment_status(test['resource_id'])

            import json
            print(f"\nStatus Response:")
            print(json.dumps(status, indent=2))

            # Check for leads
            if 'leads' in status:
                leads = status['leads']
                print(f"\n✅ Found {len(leads)} leads")

                if len(leads) > 0:
                    print("\nFirst 3 leads:")
                    for i, lead in enumerate(leads[:3], 1):
                        name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
                        title = lead.get('title', 'N/A')
                        company = lead.get('company_name', 'N/A')
                        industry = lead.get('industry', 'N/A')
                        size = lead.get('company_size', 'N/A')
                        location = lead.get('location', 'N/A')

                        print(f"\n  {i}. {name}")
                        print(f"     Title: {title}")
                        print(f"     Company: {company}")
                        print(f"     Industry: {industry}")
                        print(f"     Size: {size}")
                        print(f"     Location: {location}")
                else:
                    print("\n❌ No leads found (empty result)")
            else:
                in_progress = status.get('in_progress', 'unknown')
                print(f"\n⏳ In progress: {in_progress}")
                if not in_progress:
                    print("⚠️  Job completed but no leads in response")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")


if __name__ == "__main__":
    asyncio.run(check_specific_enrichments())
