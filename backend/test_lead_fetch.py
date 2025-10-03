#!/usr/bin/env python3
"""
Test script to verify lead fetching from SuperSearch list
This will help debug if list_id filter is working correctly
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()

async def test_lead_fetch():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found in environment")
        return

    print(f"✅ API key found (length: {len(api_key)})")

    instantly = InstantlyService(api_key)

    # You'll need to replace this with an actual resource_id from a SuperSearch
    # Run a SuperSearch first, check the dashboard, and get the list ID
    test_resource_id = input("\nEnter the resource_id from a SuperSearch (visible in dashboard URL): ").strip()

    if not test_resource_id:
        print("❌ No resource_id provided. Run a SuperSearch first and copy the list ID from the dashboard.")
        return

    print(f"\n🔍 Testing lead fetch for resource_id: {test_resource_id}")
    print("This should return the leads you see in the Instantly dashboard...\n")

    try:
        # Test method 1: Get from SuperSearch history
        print("📋 Method 1: get_supersearch_enrichment_history()")
        leads_history = await instantly.get_supersearch_enrichment_history(test_resource_id)
        print(f"   Returned {len(leads_history)} leads")
        if leads_history:
            for i, lead in enumerate(leads_history[:3], 1):
                email = lead.get('email', 'N/A')
                name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
                company = lead.get('company_name', 'N/A')
                print(f"   {i}. {email} - {name} at {company}")

        print(f"\n📋 Method 2: get_leads_from_list()")
        leads_list = await instantly.get_leads_from_list(test_resource_id, limit=10)
        print(f"   Returned {len(leads_list)} leads")
        if leads_list:
            for i, lead in enumerate(leads_list[:3], 1):
                email = lead.get('email', 'N/A')
                name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip()
                company = lead.get('company_name', 'N/A')
                print(f"   {i}. {email} - {name} at {company}")

        print("\n✅ Test complete!")
        print("\n💡 Compare these results with what you see in the Instantly dashboard.")
        print("   The emails should match!")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_lead_fetch())
