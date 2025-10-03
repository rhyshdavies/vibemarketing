"""
Production test - Create campaign with SuperSearch leads enriching directly into it
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_production_flow():
    api_key = os.getenv('INSTANTLY_API_KEY')
    service = InstantlyService(api_key)

    print("🎯 PRODUCTION FLOW TEST - Real Campaign Creation")
    print("=" * 80)

    # Step 1: Create campaign
    print("\n✅ Step 1: Creating campaign...")
    campaign = await service.create_campaign(
        name="Production Test - Check Dashboard",
        variants=[
            {
                "subject": "Quick question about {{company}}",
                "body": "Hi {{firstName}},\n\nI noticed {{company}} and wanted to reach out.\n\nBest regards"
            }
        ]
    )
    campaign_id = campaign.get("id")

    print(f"   ✅ Campaign created!")
    print(f"   Campaign ID: {campaign_id}")
    print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Run SuperSearch to enrich leads DIRECTLY into campaign
    print(f"\n✅ Step 2: Running SuperSearch to find and enrich leads into campaign...")

    search_filters = {
        "title": {"include": ["CEO", "Founder", "Co-Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
        "employee_count": ["25 - 100", "100 - 250"],  # Mid-size companies
    }

    search_result = await service.search_leads_supersearch(
        search_filters=search_filters,
        limit=10,  # 10 fresh leads
        work_email_enrichment=True,
        campaign_id=campaign_id  # KEY: Enrich directly into campaign
    )

    enrichment_id = search_result.get("id") or search_result.get("resource_id")

    print(f"   ✅ SuperSearch enrichment started!")
    print(f"   Enrichment ID: {enrichment_id}")
    print(f"   Target: Campaign {campaign_id}")
    print(f"   Finding: 10 CEOs/Founders at US companies (25-250 employees)")

    # Step 3: Instructions for user
    print(f"\n" + "=" * 80)
    print(f"✅ CAMPAIGN CREATED SUCCESSFULLY!")
    print(f"\n📋 Campaign Details:")
    print(f"   Name: Production Test - Check Dashboard")
    print(f"   ID: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    print(f"\n⏳ What's Happening Now:")
    print(f"   1. SuperSearch is finding 10 fresh CEO/Founder leads at US companies")
    print(f"   2. Emails are being verified and enriched with company data")
    print(f"   3. Leads are being created DIRECTLY in your campaign (not a list)")
    print(f"   4. This takes 2-5 minutes to complete")

    print(f"\n👀 How to Verify:")
    print(f"   1. Open the campaign URL above in your browser")
    print(f"   2. Wait 2-3 minutes")
    print(f"   3. Refresh the page")
    print(f"   4. You should see leads appearing in the campaign")
    print(f"   5. The '👋 Add some leads to get started' message will disappear")

    print(f"\n✅ Once leads appear, you can activate the campaign and start sending!")
    print(f"\n" + "=" * 80)

    return campaign_id


if __name__ == "__main__":
    campaign_id = asyncio.run(test_production_flow())
    print(f"\n🔗 Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
