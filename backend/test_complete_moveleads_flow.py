"""
Test the complete flow with moveleads:
1. Create campaign
2. Run SuperSearch enrichment into a list
3. Move leads from list to campaign using moveleads endpoint
4. Verify leads appear in campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx

load_dotenv()


async def test_complete_flow():
    """Test the complete moveleads flow"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 COMPLETE MOVELEADS FLOW TEST")
    print("=" * 80)

    # Step 1: Create campaign
    print(f"\n✅ Step 1: Create campaign")
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp for moveleads test"
    )
    campaign_data = await instantly_service.create_campaign(
        name="MOVELEADS FLOW TEST",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test moveleads flow",
                "body": "Hi {{firstName}},\\n\\nTest.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Create SuperSearch enrichment into a LIST (not campaign)
    print(f"\n✅ Step 2: Run SuperSearch enrichment into a list")

    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    try:
        # Enrich into a LIST (don't pass campaign_id)
        enrichment = await instantly_service.search_leads_supersearch(
            search_filters=search_filters,
            limit=3,
            work_email_enrichment=True,
            list_name="Moveleads Test List"
        )

        lead_list_id = enrichment.get("resource_id")
        print(f"   ✅ SuperSearch enrichment created")
        print(f"   Lead List ID: {lead_list_id}")

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return

    # Step 3: Wait for enrichment to complete
    print(f"\n✅ Step 3: Wait 90 seconds for enrichment to complete")
    print(f"   (This gives Instantly time to verify emails and populate the list)")
    await asyncio.sleep(90)

    # Step 4: Move leads from list to campaign
    print(f"\n✅ Step 4: Move leads from list to campaign using moveleads")

    try:
        success = await instantly_service.move_leads_to_campaign(
            campaign_id=campaign_id,
            lead_list_id=lead_list_id
        )

        if success:
            print(f"   ✅ Move operation completed successfully!")
        else:
            print(f"   ⚠️ Move operation completed with warnings")

    except Exception as e:
        print(f"   ❌ Move failed: {str(e)}")
        return

    # Step 5: Verify leads in campaign
    print(f"\n✅ Step 5: Verify leads are now in campaign")
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
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads are now in the campaign!")
                print(f"\n   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Dashboard should show leads (no more '👋 Add some leads to get started')!")

                print(f"\n   Sample leads:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')} {lead.get('last_name', 'N/A')})")
            else:
                print(f"\n⚠️ No leads found in campaign yet")
                print(f"   This might mean:")
                print(f"   1. Enrichment is still processing (wait a bit longer)")
                print(f"   2. Move operation didn't complete (check background job)")
                print(f"   3. No leads were found matching the filters")
                print(f"\n   Check dashboard: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Failed to fetch campaign leads: {response.text}")

    print(f"\n" + "=" * 80)
    print(f"✅ Test complete!")
    print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")
    print(f"   Lead List: {lead_list_id}")


if __name__ == "__main__":
    asyncio.run(test_complete_flow())
