"""
Test the PRACTICAL RECIPE that works:
1. Create campaign
2. Run SuperSearch → get a list
3. Fetch list rows; drop any emails that already exist in workspace
4. Create remaining (fresh) emails with POST /leads/list and campaign_id
5. Confirm by reading /api/v2/campaigns/analytics
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx

load_dotenv()


async def test_practical_recipe():
    """Test the practical recipe for adding leads to campaigns"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 PRACTICAL RECIPE TEST")
    print("=" * 80)

    # Step 1: Create campaign
    print(f"\n✅ Step 1: Create campaign")
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp for practical recipe"
    )
    campaign_data = await instantly_service.create_campaign(
        name="PRACTICAL RECIPE TEST",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test practical recipe",
                "body": "Hi {{firstName}},\\n\\nTest.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 2: Run SuperSearch → get a list
    print(f"\n✅ Step 2: Run SuperSearch enrichment into a list")

    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    try:
        # Enrich into a LIST (not campaign)
        enrichment = await instantly_service.search_leads_supersearch(
            search_filters=search_filters,
            limit=5,  # Small number for testing
            work_email_enrichment=True,
            list_name="Practical Recipe Test List"
        )

        lead_list_id = enrichment.get("resource_id")
        print(f"   ✅ SuperSearch enrichment created")
        print(f"   Lead List ID: {lead_list_id}")

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return

    # Wait for enrichment
    print(f"\n✅ Wait 90 seconds for enrichment to complete")
    await asyncio.sleep(90)

    # Step 3-4: Use move_leads_to_campaign (implements the practical recipe)
    print(f"\n✅ Step 3-4: Apply practical recipe (fetch → dedupe → create)")

    try:
        success = await instantly_service.move_leads_to_campaign(
            campaign_id=campaign_id,
            lead_list_id=lead_list_id
        )

        if not success:
            print(f"   ⚠️ Practical recipe returned False")
            return

    except Exception as e:
        print(f"   ❌ Failed: {str(e)}")
        return

    # Step 5: Confirm by reading campaign analytics
    print(f"\n✅ Step 5: Verify using campaign analytics")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Check campaign analytics
        analytics_response = await client.get(
            f"https://api.instantly.ai/api/v2/campaigns/analytics",
            headers=headers,
            params={"id": campaign_id}
        )

        if analytics_response.status_code == 200:
            analytics_data = analytics_response.json()

            # Handle if response is array or object
            if isinstance(analytics_data, list) and len(analytics_data) > 0:
                analytics = analytics_data[0]
            elif isinstance(analytics_data, dict):
                analytics = analytics_data
            else:
                analytics = {}

            leads_count = analytics.get("leads_count", 0)

            print(f"   Campaign analytics:")
            print(f"   - leads_count: {leads_count}")
            print(f"   - status: {analytics.get('status')}")

            if leads_count > 0:
                print(f"\n🎉 SUCCESS! Campaign has {leads_count} leads!")
                print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Dashboard should show these leads (no more '👋 Add some leads')!")
            else:
                print(f"\n⚠️ Campaign created but leads_count is still 0")
                print(f"   Check dashboard: https://app.instantly.ai/app/campaigns/{campaign_id}")
        else:
            print(f"   ❌ Failed to fetch analytics: {analytics_response.status_code}")

        # Also check leads directly
        print(f"\n   Double-checking with leads/list endpoint:")
        leads_response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={
                "campaign_ids": [campaign_id],
                "limit": 100
            }
        )

        if leads_response.status_code == 200:
            leads_data = leads_response.json()
            campaign_leads = [l for l in leads_data.get("items", []) if l.get("campaign") == campaign_id]
            print(f"   - Leads with campaign={campaign_id}: {len(campaign_leads)}")

            if campaign_leads:
                print(f"\n   Sample leads:")
                for lead in campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')} {lead.get('last_name', 'N/A')})")

    print(f"\n" + "=" * 80)
    print(f"✅ Test complete!")
    print(f"   Campaign: https://app.instantly.ai/app/campaigns/{campaign_id}")


if __name__ == "__main__":
    asyncio.run(test_practical_recipe())
