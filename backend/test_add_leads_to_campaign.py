"""
Test adding leads from a SuperSearch list to a campaign
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import json

load_dotenv()


async def test_add_leads():
    """Test the full flow of creating enrichment, fetching leads, and adding to campaign"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly_service = InstantlyService(api_key)

    print("🔍 Step 1: Create SuperSearch enrichment")

    # Create a simple search
    search_filters = {
        "title": {"include": ["CEO"], "exclude": []},
        "locations": [{"city": "", "state": "", "country": "United Kingdom"}],
        "industry": {"include": ["Real Estate & Construction"], "exclude": []}
    }

    search_result = await instantly_service.search_leads_supersearch(
        search_filters=search_filters,
        limit=2,
        work_email_enrichment=True,
        list_name="Test - Add Leads to Campaign"
    )

    list_id = search_result.get("resource_id")
    print(f"✅ Created list: {list_id}")

    # Wait for enrichment
    print("\n⏳ Step 2: Wait for enrichment (30 seconds)")
    await asyncio.sleep(30)

    # Get leads from list
    print(f"\n📋 Step 3: Fetch leads from list {list_id}")
    leads = await instantly_service.get_leads_from_list(list_id, limit=100)

    if not leads or len(leads) == 0:
        print("❌ No leads found in list yet - enrichment still in progress")
        print("   Try checking the list in Instantly dashboard")
        return

    print(f"✅ Found {len(leads)} leads in list")
    print(f"   Sample lead: {json.dumps(leads[0], indent=2)}")

    # Create a campaign
    print("\n📧 Step 4: Create campaign")
    campaign_data = await instantly_service.create_campaign(
        name="Test Campaign - Lead Addition",
        lead_list_id=list_id,
        variants=[
            {
                "subject": "Test Subject",
                "body": "Hi {{firstName}},\n\nThis is a test email.\n\nBest regards"
            }
        ]
    )

    campaign_id = campaign_data.get("id")
    print(f"✅ Created campaign: {campaign_id}")

    # Extract lead IDs
    lead_ids = [lead.get("_id") for lead in leads if lead.get("_id")]
    print(f"\n📝 Extracted {len(lead_ids)} lead IDs from {len(leads)} leads")

    # Add leads to campaign
    print(f"\n➕ Step 5: Add {len(lead_ids)} leads to campaign {campaign_id}")
    added = await instantly_service.add_leads_to_campaign(
        campaign_id=campaign_id,
        lead_ids=lead_ids
    )

    if added:
        print(f"✅ SUCCESS! Added {len(leads)} leads to campaign")
        print(f"\n👉 Check campaign {campaign_id} in Instantly dashboard")
        print(f"   It should now show {len(leads)} leads instead of 'Add leads'")
    else:
        print("❌ Failed to add leads to campaign")
        print("   Check backend logs for error details")


if __name__ == "__main__":
    asyncio.run(test_add_leads())
