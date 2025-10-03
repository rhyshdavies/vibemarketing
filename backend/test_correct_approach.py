"""
Test the CORRECT approach: Create enrichment targeted at campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx

load_dotenv()


async def test_correct_approach():
    """Test creating enrichment targeted at campaign (not list)"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 CORRECT APPROACH - Enrich Directly Into Campaign")
    print("=" * 80)

    # Step 1: Create campaign
    print(f"\n✅ Step 1: Create campaign")
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp for correct approach"
    )
    campaign_data = await instantly_service.create_campaign(
        name="CORRECT APPROACH TEST",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test correct approach",
                "body": "Hi {{firstName}},\\n\\nTest.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Create SuperSearch enrichment TARGETED AT CAMPAIGN
    print(f"\n✅ Step 2: Create SuperSearch enrichment for campaign")

    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    try:
        enrichment = await instantly_service.create_supersearch_enrichment_for_campaign(
            campaign_id=campaign_id,
            search_filters=search_filters,
            limit=3,
            work_email_enrichment=True,
        )

        enrichment_id = enrichment.get("id") or enrichment.get("resource_id")
        print(f"   ✅ Enrichment created: {enrichment_id}")
        print(f"   Enrichment targeting campaign: {campaign_id}")

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return

    # Step 3: Wait and verify
    print(f"\n✅ Step 3: Wait 60 seconds for enrichment")
    await asyncio.sleep(60)

    print(f"\n✅ Step 4: Check campaign for leads")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "campaign_ids": [campaign_id],
                "limit": 100
            },
        )

        if response.status_code == 200:
            data = response.json()
            campaign_leads = data.get("items", [])
            actual_campaign_leads = [l for l in campaign_leads if l.get("campaign") == campaign_id]

            print(f"   Total items returned: {len(campaign_leads)}")
            print(f"   Leads with campaign={campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads directly in campaign!")
                print(f"\n   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Leads were created WITH the correct campaign_id from the start!")

                print(f"\n   Sample leads:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n⏳ Enrichment still in progress...")
                print(f"   Check again in 2-3 minutes: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_correct_approach())
