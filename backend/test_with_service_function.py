"""Test using the updated move_leads_to_campaign service function"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test():
    api_key = os.getenv('INSTANTLY_API_KEY')
    service = InstantlyService(api_key)

    print("🎯 TEST WITH UPDATED SERVICE FUNCTION")
    print("=" * 80)

    # Step 1: Create campaign
    print("\n✅ Step 1: Create campaign")
    campaign = await service.create_campaign(
        name="Service Function Test",
        variants=[{"subject": "Test", "body": "Hi {{firstName}}"}]
    )
    campaign_id = campaign.get("id")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Run SuperSearch enrichment
    print("\n✅ Step 2: Run SuperSearch enrichment")
    search_result = await service.search_leads_supersearch(
        search_filters={
            "title": {"include": ["CEO", "Founder"], "exclude": []},
            "locations": [{"city": "", "state": "", "country": "United States"}],
        },
        limit=3,
        work_email_enrichment=True,
        list_name="Service Test List"
    )
    lead_list_id = search_result.get("resource_id")
    print(f"   Lead List ID: {lead_list_id}")

    # Step 3: Wait for enrichment
    print("\n✅ Step 3: Wait 60 seconds for enrichment")
    await asyncio.sleep(60)

    # Step 4: Move leads to campaign (uses updated function with all fixes)
    print("\n✅ Step 4: Move leads to campaign")
    success = await service.move_leads_to_campaign(
        campaign_id=campaign_id,
        lead_list_id=lead_list_id
    )

    if success:
        print(f"\n🎉 SUCCESS!")
        print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")
    else:
        print(f"\n⚠️ Move operation returned False")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(test())
