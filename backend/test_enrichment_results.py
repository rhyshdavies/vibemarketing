"""
Test getting actual enrichment results to see if filters are working
"""
import asyncio
import os
import time
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_enrichment_results():
    """Test getting actual results from enrichment to verify filters work"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Enrichment Results\n")
    instantly_service = InstantlyService(api_key)

    # Test with a simple filter that should definitely return results
    test_cases = [
        {
            "name": "C-Level in USA (no location filter)",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["100 - 250"]
            }
        },
        {
            "name": "C-Level in San Francisco",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["100 - 250"],
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
            "name": "Software & Internet industry",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["100 - 250"],
                "industry": {
                    "include": ["Software & Internet"],
                    "exclude": []
                }
            }
        }
    ]

    for test in test_cases:
        print(f"\n{'='*80}")
        print(f"Test: {test['name']}")
        print('='*80)

        import json
        print(f"Filters:")
        print(json.dumps(test['filters'], indent=2))

        try:
            # Start the enrichment
            result = await instantly_service.search_leads_supersearch(
                search_filters=test['filters'],
                limit=10
            )

            resource_id = result.get('resource_id')
            print(f"\n✅ Enrichment started")
            print(f"   Resource ID: {resource_id}")
            print(f"   List ID: {result.get('id')}")

            # Wait a bit for enrichment to process
            print(f"\n⏳ Waiting 15 seconds for enrichment...")
            await asyncio.sleep(15)

            # Get the enrichment status
            status = await instantly_service.get_supersearch_enrichment_status(resource_id)
            print(f"\n📊 Enrichment Status:")
            print(json.dumps(status, indent=2))

            # Check if we got leads
            if 'leads' in status:
                lead_count = len(status['leads'])
                print(f"\n✅ Found {lead_count} leads")

                if lead_count > 0:
                    print("\nSample leads:")
                    for i, lead in enumerate(status['leads'][:3], 1):
                        name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
                        title = lead.get('title', 'N/A')
                        company = lead.get('company_name', 'N/A')
                        location = lead.get('location', 'N/A')
                        print(f"{i}. {name} | {title} at {company} | {location}")
            elif 'status' in status:
                print(f"\n⏳ Status: {status['status']}")
                if status['status'] == 'completed':
                    print(f"   Total leads found: {status.get('total_leads', 0)}")
                elif status['status'] == 'in_progress':
                    print(f"   Progress: {status.get('progress', 'unknown')}")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(test_enrichment_results())
