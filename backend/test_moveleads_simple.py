"""
Simple test to verify moveleads API works with existing list
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import json

load_dotenv()


async def test_moveleads():
    """Test moveleads with an existing list that has enriched leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    # Use a list ID that we know has been enriching for a few minutes
    # This list was created earlier and should have leads by now
    list_id = "8fec331b-123f-4fa2-b34f-694c67ce694b"  # From backend logs

    print(f"🔍 Step 1: Check leads in list {list_id}")
    leads = await instantly_service.get_leads_from_list(list_id, limit=100)

    if not leads or len(leads) == 0:
        print("❌ No leads found in this list")
        print("   Please wait a few more minutes for enrichment to complete")
        print("   Or manually check the list in Instantly dashboard")
        return

    print(f"✅ Found {len(leads)} leads in list")
    print(f"\n📋 Sample lead data:")
    print(json.dumps(leads[0], indent=2))

    # Extract lead IDs
    lead_ids = [lead.get("_id") for lead in leads if lead.get("_id")]
    print(f"\n📝 Extracted {len(lead_ids)} lead IDs")

    # Create a new campaign
    print(f"\n📧 Step 2: Create campaign")
    campaign_data = await instantly_service.create_campaign(
        name="Test Campaign - MoveLleads Validation",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Quick question",
                "body": "Hi {{firstName}},\n\nI had a quick question for you.\n\nBest regards"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"✅ Created campaign: {campaign_id}")

    # Add leads to campaign using moveleads
    print(f"\n➕ Step 3: Move {len(lead_ids)} leads to campaign using moveleads API")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        lead_ids=lead_ids
    )

    if added:
        print(f"\n✅ SUCCESS! Moved {len(lead_ids)} leads to campaign")
        print(f"\n👉 Check campaign {campaign_id} in Instantly dashboard")
        print(f"   It should now show {len(lead_ids)} leads instead of '👋 Add some leads'")
    else:
        print("\n❌ Failed to move leads to campaign")
        print("   Check the error message above")


if __name__ == "__main__":
    asyncio.run(test_moveleads())
