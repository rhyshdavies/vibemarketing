#!/usr/bin/env python3
"""
Check what leads are actually in the lists we created
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()

async def check_recent_lists():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly = InstantlyService(api_key)

    # These are the resource_ids from our recent tests
    test_lists = [
        ("4ed83d39-9d41-4fa6-bc1a-d67e069d7aae", "CTOs in San Francisco"),
        ("f9ae3455-bfd2-4c62-b108-5d39de4d6305", "London Software C-Level")
    ]

    print("="*70)
    print("Checking leads in recently created SuperSearch lists")
    print("="*70)

    for list_id, list_name in test_lists:
        print(f"\n📋 List: {list_name}")
        print(f"   ID: {list_id}")
        print("   " + "-"*60)

        # Wait a bit for enrichment
        print("   ⏳ Waiting 5 seconds for enrichment...")
        await asyncio.sleep(5)

        leads = await instantly.get_leads_from_list(list_id, limit=10)

        if not leads:
            print("   ⚠️  No leads found yet\n")
            continue

        print(f"   ✅ Found {len(leads)} leads:\n")

        for i, lead in enumerate(leads, 1):
            email = lead.get('email', 'N/A')
            name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}".strip() or 'N/A'
            company = lead.get('company_name', 'N/A')
            title = lead.get('title', 'N/A')
            location = lead.get('location', 'N/A')
            linkedin = lead.get('linkedin', 'N/A')

            print(f"   {i}. {name} - {title}")
            print(f"      {email}")
            print(f"      {company}")
            print(f"      📍 {location}")
            if linkedin != 'N/A':
                print(f"      🔗 {linkedin}")
            print()

    print("="*70)
    print("\nNow check the Instantly dashboard at:")
    print("https://app.instantly.ai/app/leads")
    print("\nCompare the leads shown here with what you see in the dashboard.")
    print("Do they match? Are they filtered by location/title?")
    print("="*70)

if __name__ == "__main__":
    asyncio.run(check_recent_lists())
