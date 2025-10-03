"""
Check the status of the enrichment and see if leads appeared
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def check_enrichment():
    api_key = os.getenv('INSTANTLY_API_KEY')
    service = InstantlyService(api_key)

    enrichment_id = "7824d4dd-8364-45d1-a9f2-4db213feddc8"
    campaign_id = "15ef2347-4ebf-40dd-9642-f02406b851f0"

    print("🔍 Checking enrichment status")
    print("=" * 80)

    # Check enrichment status
    status = await service.get_supersearch_enrichment_status(enrichment_id)
    print(f"\n📋 Enrichment Status:")
    print(f"   {status}")

    # Try to get leads
    print(f"\n📋 Trying to fetch leads from list...")
    leads = await service.get_leads_from_list(enrichment_id, limit=10)
    print(f"   Found {len(leads)} leads")

    if leads:
        print(f"\n✅ Leads are available! Moving to campaign...")
        success = await service.move_leads_to_campaign(campaign_id, enrichment_id)

        if success:
            print(f"\n🎉 SUCCESS! Check campaign:")
            print(f"   https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"\n⚠️ Move operation returned False")
    else:
        print(f"\n⏳ No leads available yet, enrichment still in progress")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(check_enrichment())
