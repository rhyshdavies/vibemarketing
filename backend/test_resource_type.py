"""
Test using resource_id and resource_type to target campaign directly
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx

load_dotenv()


async def test_resource_type():
    """Test enriching leads directly into campaign using resource_type=1"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 TEST - resource_type=1 (Campaign)")
    print("=" * 80)

    # Step 1: Create campaign
    print(f"\n✅ Step 1: Create campaign")
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp for resource_type test"
    )
    campaign_data = await instantly_service.create_campaign(
        name="RESOURCE_TYPE TEST",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test resource_type",
                "body": "Hi {{firstName}},\\n\\nTest.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Enrich leads directly into campaign
    print(f"\n✅ Step 2: Enrich leads with resource_id={campaign_id}, resource_type=1")

    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    try:
        enrichment = await instantly_service.search_leads_supersearch(
            search_filters=search_filters,
            limit=3,
            work_email_enrichment=True,
            campaign_id=campaign_id  # This will set resource_id and resource_type=1
        )

        enrichment_id = enrichment.get("id") or enrichment.get("resource_id")
        print(f"   ✅ Enrichment created: {enrichment_id}")

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return

    # Step 3: Wait and verify
    print(f"\n✅ Step 3: Wait 90 seconds for enrichment")
    print(f"   (Enrichment takes 2-5 minutes, but we'll check at 90s)")
    await asyncio.sleep(90)

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
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads enriched directly into campaign!")
                print(f"\n   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Leads were created WITH the correct campaign_id from the start!")
                print(f"   ✅ No more '👋 Add some leads to get started'!")

                print(f"\n   Sample leads:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n⏳ Enrichment still in progress...")
                print(f"   Wait 2-3 more minutes then check: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_resource_type())
