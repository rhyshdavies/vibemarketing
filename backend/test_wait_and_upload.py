"""
Test waiting for enrichment then uploading to campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx

load_dotenv()


async def test_wait_and_upload():
    """Test waiting for enriched leads then uploading to campaign"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🎯 TEST - Wait for Enrichment, Then Upload")
    print("=" * 80)

    # Use an existing enriched list
    # You mentioned leads are already enriched in dashboard
    # Let's use list: 8fec331b-123f-4fa2-b34f-694c67ce694b
    existing_list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"

    print(f"\n✅ Step 1: Check if leads exist in list {existing_list_id}")
    leads = await instantly_service.get_leads_from_list(existing_list_id, limit=10)
    print(f"   Found {len(leads)} enriched leads")

    if len(leads) == 0:
        print("   ❌ No leads in this list. Try another list ID.")
        return

    # Show sample leads
    print(f"\n   Sample leads:")
    for lead in leads[:3]:
        print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")

    # Step 2: Create new campaign
    print(f"\n✅ Step 2: Create new campaign")
    temp_list_id = await instantly_service.create_lead_list(
        name="Temp for wait test"
    )
    campaign_data = await instantly_service.create_campaign(
        name="TEST - Wait and Upload",
        lead_list_id=temp_list_id,
        variants=[
            {
                "subject": "Test",
                "body": "Hi {{firstName}},\\n\\nTest.\\n\\nBest"
            }
        ]
    )
    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # Step 3: Upload enriched leads to campaign
    print(f"\n✅ Step 3: Upload {len(leads)} enriched leads to campaign")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        lead_list_id=existing_list_id
    )

    if not added:
        print("   ❌ Upload failed")
        return

    # Step 4: Verify
    print(f"\n✅ Step 4: Verify leads are in campaign")
    await asyncio.sleep(3)

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

            print(f"   Total leads returned: {len(campaign_leads)}")
            print(f"   Leads with campaign={campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads in campaign!")
                print(f"\n   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"   ✅ Check the dashboard - leads should be visible!")

                print(f"\n   Leads in campaign:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n❌ Leads were NOT added to campaign")
                if campaign_leads:
                    print(f"   First lead has campaign: {campaign_leads[0].get('campaign')}")
        else:
            print(f"   ❌ Failed: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_wait_and_upload())
