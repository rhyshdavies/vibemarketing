"""
Test the updated flow: SuperSearch -> Poll for completion -> Move leads to campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_updated_flow():
    api_key = os.getenv('INSTANTLY_API_KEY')
    service = InstantlyService(api_key)

    print("🎯 UPDATED FLOW TEST - SuperSearch with Auto Lead Movement")
    print("=" * 80)

    # Step 1: Create campaign
    print("\n✅ Step 1: Creating campaign...")
    campaign = await service.create_campaign(
        name="Paris CTOs Test - Auto Leads",
        variants=[
            {
                "subject": "Quick question about {{company}}",
                "body": "Hi {{firstName}},\n\nI noticed {{company}} and wanted to reach out about your tech stack.\n\nBest regards"
            }
        ]
    )
    campaign_id = campaign.get("id")

    print(f"   ✅ Campaign created!")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Run SuperSearch to create a lead list
    print(f"\n✅ Step 2: Running SuperSearch to find leads...")

    # Use Paris CTOs - definitely not in workspace yet
    search_filters = {
        "title": {"include": ["CTO", "Chief Technology Officer"], "exclude": []},
        "locations": [{"city": "Paris", "state": "", "country": "France"}],
    }

    search_result = await service.search_leads_supersearch(
        search_filters=search_filters,
        limit=2,  # Just 2 leads to minimize cost
        work_email_enrichment=True,
        list_name="Updated Flow Test List"
    )

    enrichment_id = search_result.get("id") or search_result.get("resource_id")

    print(f"   ✅ SuperSearch started!")
    print(f"   Enrichment ID: {enrichment_id}")
    print(f"   Finding: 2 CTOs in Paris, France")

    # Step 3: Wait for enrichment to actually complete
    print(f"\n✅ Step 3: Waiting for enrichment to complete...")

    enrichment_complete = await service.wait_for_supersearch_completion(
        resource_id=enrichment_id,
        expected_count=2,  # We requested 2 leads
        max_wait_seconds=90  # Enrichment usually completes in 10-30 seconds
    )

    if not enrichment_complete:
        print(f"\n⏳ Enrichment still in progress after 5 minutes")
        print(f"   This is normal for larger lead counts")
        print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")
        print(f"   Lead List ID: {enrichment_id}")
        return

    # Step 4: Move leads to campaign (only fetch 2 leads, not 100)
    print(f"\n✅ Step 4: Moving enriched leads to campaign...")

    success = await service.move_leads_to_campaign(
        campaign_id=campaign_id,
        lead_list_id=enrichment_id,
        limit=2  # Only get the 2 Paris leads we requested
    )

    if success:
        print(f"\n🎉 SUCCESS!")
        print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")
        print(f"   Leads should now appear in the campaign dashboard!")
    else:
        print(f"\n⚠️ Move operation returned False")
        print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")
        print(f"   Lead List ID: {enrichment_id}")
        print(f"   Check if leads already existed in workspace")

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(test_updated_flow())
