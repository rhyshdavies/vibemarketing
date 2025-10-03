"""
Check what leads SuperSearch is actually returning for Paris
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()


async def test_paris_leads():
    api_key = os.getenv('INSTANTLY_API_KEY')
    service = InstantlyService(api_key)

    print("🔍 CHECKING PARIS LEADS")
    print("=" * 80)

    # Search for Paris leads
    search_filters = {
        "title": {"include": ["CEO", "Founder"], "exclude": []},
        "locations": [{"city": "Paris", "state": "", "country": "France"}],
    }

    print("\n📋 Running SuperSearch...")
    search_result = await service.search_leads_supersearch(
        search_filters=search_filters,
        limit=10,
        work_email_enrichment=True,
        list_name="Paris Test List"
    )

    enrichment_id = search_result.get("id") or search_result.get("resource_id")
    print(f"   Enrichment ID: {enrichment_id}")

    # Wait for enrichment
    print("\n⏳ Waiting 15 seconds for enrichment...")
    await asyncio.sleep(15)

    # Fetch the actual leads
    print("\n📋 Fetching leads from list...")
    leads = await service.get_leads_from_list(enrichment_id, limit=10)

    print(f"\n✅ Found {len(leads)} leads:")
    print("-" * 80)

    for i, lead in enumerate(leads[:10], 1):
        email = lead.get("email", "N/A")
        first_name = lead.get("first_name", "N/A")
        last_name = lead.get("last_name", "N/A")
        company = lead.get("company_name", "N/A")
        location = lead.get("location", "N/A")

        print(f"\n{i}. {first_name} {last_name}")
        print(f"   Email: {email}")
        print(f"   Company: {company}")
        print(f"   Location: {location}")

    print("\n" + "=" * 80)
    print("❓ Do these leads look like Paris-based CEOs/Founders?")


if __name__ == "__main__":
    asyncio.run(test_paris_leads())
