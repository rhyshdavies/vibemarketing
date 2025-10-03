#!/usr/bin/env python3
"""
Check the full lead data structure including payload
"""
import asyncio
import os
import json
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()

async def check_lead_full_data():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly = InstantlyService(api_key)

    # The "CTOs in San Francisco" list
    list_id = "4ed83d39-9d41-4fa6-bc1a-d67e069d7aae"

    print("="*70)
    print("Fetching FULL lead data to see payload structure")
    print("="*70)

    leads = await instantly.get_leads_from_list(list_id, limit=2)

    if not leads:
        print("⚠️ No leads found")
        return

    print(f"\n✅ Got {len(leads)} leads. Showing full data structure:\n")

    for i, lead in enumerate(leads, 1):
        print(f"\n{'='*70}")
        print(f"Lead {i}: {lead.get('first_name')} {lead.get('last_name')}")
        print(f"{'='*70}")
        print(json.dumps(lead, indent=2, default=str))

        # Specifically check payload
        if 'payload' in lead and lead['payload']:
            print(f"\n📦 PAYLOAD OBJECT:")
            print(json.dumps(lead['payload'], indent=2, default=str))
        else:
            print(f"\n⚠️ No 'payload' field or it's empty")

        print("\n" + "-"*70)

if __name__ == "__main__":
    asyncio.run(check_lead_full_data())
