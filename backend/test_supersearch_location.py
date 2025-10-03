#!/usr/bin/env python3
"""
Test SuperSearch with location filter to verify leads match the search criteria
"""
import asyncio
import os
import json
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()

async def test_supersearch_with_location():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found in environment")
        return

    print(f"✅ API key found (length: {len(api_key)})")

    instantly = InstantlyService(api_key)

    # Create a very specific search: CTOs in San Francisco
    search_filters = {
        "locations": [
            {
                "city": "San Francisco",
                "state": "California",
                "country": "United States"
            }
        ],
        "title": {
            "include": ["CTO", "Chief Technology Officer"],
            "exclude": []
        },
        "employee_count": ["25 - 100"]
    }

    print("\n🔍 Creating SuperSearch with filters:")
    print(json.dumps(search_filters, indent=2))
    print("\n⏳ Starting SuperSearch enrichment (limit: 5 leads)...")

    try:
        # Step 1: Create SuperSearch enrichment
        result = await instantly.search_leads_supersearch(
            search_filters=search_filters,
            limit=5,
            work_email_enrichment=True,
            list_name="Test: CTOs in San Francisco"
        )

        print(f"\n📋 SuperSearch created successfully!")
        print(f"   Enrichment ID: {result.get('id')}")
        print(f"   Resource ID (list): {result.get('resource_id')}")
        print(f"   Search filters saved: {result.get('search_filters')}")

        resource_id = result.get('resource_id') or result.get('id')

        # Step 2: Wait a bit for enrichment to process
        print(f"\n⏳ Waiting 15 seconds for enrichment to process...")
        await asyncio.sleep(15)

        # Step 3: Fetch leads from the list
        print(f"\n📥 Fetching leads from list {resource_id}...")
        leads = await instantly.get_leads_from_list(resource_id, limit=10)

        if not leads:
            print("\n⚠️ No leads returned yet. Try running this again in a few seconds.")
            print(f"   You can check the Instantly dashboard for list: {resource_id}")
            return

        print(f"\n✅ Got {len(leads)} leads! Verifying they match our search criteria...\n")

        # Step 4: Verify each lead matches our criteria
        for i, lead in enumerate(leads, 1):
            email = lead.get('email', 'N/A')
            first_name = lead.get('first_name', 'N/A')
            last_name = lead.get('last_name', 'N/A')
            title = lead.get('title', 'N/A')
            company = lead.get('company_name', 'N/A')
            city = lead.get('city', 'N/A')
            state = lead.get('state', 'N/A')
            country = lead.get('country', 'N/A')

            print(f"{i}. {first_name} {last_name}")
            print(f"   Email: {email}")
            print(f"   Title: {title}")
            print(f"   Company: {company}")
            print(f"   Location: {city}, {state}, {country}")

            # Verify location matches
            if city == "San Francisco" or state == "California":
                print(f"   ✅ Location MATCHES filter!")
            else:
                print(f"   ❌ Location DOES NOT match filter (expected San Francisco, CA)")

            print()

        print("\n" + "="*60)
        print("SUMMARY:")
        print(f"  Total leads fetched: {len(leads)}")
        sf_count = sum(1 for lead in leads if lead.get('city') == 'San Francisco' or lead.get('state') == 'California')
        print(f"  Leads from San Francisco/California: {sf_count}")

        if sf_count == len(leads):
            print("  ✅ ALL leads match the location filter!")
        else:
            print(f"  ⚠️ Only {sf_count}/{len(leads)} leads match the location filter")
        print("="*60)

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("="*60)
    print("SuperSearch Location Filter Test")
    print("="*60)
    asyncio.run(test_supersearch_with_location())
