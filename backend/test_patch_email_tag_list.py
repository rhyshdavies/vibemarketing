"""
Test attaching a lead list to a campaign using PATCH with email_tag_list
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import httpx
import json

load_dotenv()


async def test_patch_email_tag_list():
    """Test attaching a lead list to a campaign using the correct PATCH approach"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"  # Existing list with enriched leads

    print("🎯 TEST - Attach Lead List to Campaign Using PATCH")
    print("=" * 80)

    print(f"\n✅ Step 1: Create new campaign")
    campaign_data = await instantly_service.create_campaign(
        name="PATCH TEST - email_tag_list",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Test email_tag_list",
                "body": "Hi {{firstName}},\n\nThis is a test.\n\nBest"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"   Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    print(f"\n✅ Step 2: Upload leads to campaign using POST with campaign_id")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        lead_list_id=list_id
    )

    if added:
        print(f"   ✅ Lead list attachment successful!")
    else:
        print(f"   ❌ Failed to attach lead list")
        return

    # Verify leads were added
    print(f"\n✅ Step 3: Verify leads appear in campaign")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    await asyncio.sleep(2)  # Wait for API to process

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
            # Filter to leads that actually have our campaign_id
            actual_campaign_leads = [l for l in campaign_leads if l.get("campaign") == campaign_id]
            print(f"   Leads with campaign field = {campaign_id}: {len(actual_campaign_leads)}")

            if len(actual_campaign_leads) > 0:
                print(f"\n🎉 SUCCESS! {len(actual_campaign_leads)} leads were attached to campaign!")
                print(f"\n   Campaign: {campaign_id}")
                print(f"   Name: PATCH TEST - email_tag_list")
                print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                print(f"\n   ✅ The campaign should now show {len(actual_campaign_leads)} leads")
                print(f"   ✅ No more '👋 Add some leads to get started'")

                print(f"\n   Sample leads:")
                for lead in actual_campaign_leads[:5]:
                    print(f"     - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n❌ Leads were NOT attached to campaign")
                print(f"   Campaign still shows: '👋 Add some leads to get started'")
        else:
            print(f"   ❌ Failed to verify: {response.text}")


if __name__ == "__main__":
    asyncio.run(test_patch_email_tag_list())
