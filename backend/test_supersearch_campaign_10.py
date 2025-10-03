import asyncio
import os
import json
from dotenv import load_dotenv
import httpx

from app.services.instantly import InstantlyService
from app.services.ai_copy import AICopyService

load_dotenv()


async def run():
    api_key = os.getenv("INSTANTLY_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly = InstantlyService(api_key)
    ai = AICopyService(openai_key)

    # 1) Generate basic filters via AI from a simple ICP for predictable results
    url = "https://example.com"
    icp = "CTOs or founders at software startups in United States"
    print("🔎 Generating SuperSearch filters from ICP...")
    try:
        filters = await ai.generate_supersearch_filters(icp, url)
    except Exception as e:
        print(f"⚠️ AI filter generation failed, using fallback filters: {e}")
        filters = {
            "level": ["C-Level"],
            "employee_count": ["25 - 100"],
            "locations": [{"city": "", "state": "", "country": "United States"}],
        }

    print("Filters:")
    print(json.dumps(filters, indent=2))

    # 2) Create SuperSearch enrichment list for 10 leads
    print("\n📥 Creating SuperSearch enrichment list (limit=10)...")
    try:
        result = await instantly.search_leads_supersearch(
            search_filters=filters,
            limit=10,
            work_email_enrichment=True,
            fully_enriched_profile=False,
            list_name="Test - 10 leads",
        )
    except Exception as e:
        print(f"❌ Failed to start SuperSearch enrichment: {e}")
        return

    resource_id = result.get("resource_id") or result.get("id")
    if not resource_id:
        print(f"❌ No resource_id returned: {result}")
        return

    print(f"✅ SuperSearch started. Resource/List ID: {resource_id}")

    # 3) Poll enrichment status for up to ~90s
    print("⏳ Waiting for enrichment...")
    max_wait = 90
    interval = 5
    elapsed = 0

    leads_ready = False
    while elapsed < max_wait:
        await asyncio.sleep(interval)
        elapsed += interval

        status = await instantly.get_supersearch_enrichment_status(resource_id)
        in_progress = status.get("in_progress", True)
        print(f"  [{elapsed}s] in_progress={in_progress}")

        if not in_progress:
            leads_ready = True
            break

    if not leads_ready:
        print("⚠️ Enrichment still in progress, will continue anyway to create campaign")

    # Optionally attempt to read any available leads
    history = await instantly.get_supersearch_enrichment_history(resource_id)
    print(f"📊 History items: {len(history) if isinstance(history, list) else 'N/A'}")

    # 4) Create campaign with the list
    print("\n📧 Creating campaign with lead_list_ids...")
    variants = [
        {
            "subject": "Quick intro",
            "body": "Hi {{firstName}},\n\nWanted to quickly introduce our product.\n\nBest,\n{{senderName}}",
        }
    ]

    try:
        campaign = await instantly.create_campaign(
            name="SuperSearch Test - 10 leads",
            lead_list_id=resource_id,
            variants=variants,
        )
    except Exception as e:
        print(f"❌ Failed to create campaign: {e}")
        return

    campaign_id = campaign.get("id")
    print(f"✅ Campaign created: {campaign_id}")
    print(f"   URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # 5) Verify campaign exists and print minimal analytics/leads info if possible
    async with httpx.AsyncClient(timeout=60.0) as client:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

        # Fetch campaign
        resp = await client.get(
            f"https://api.instantly.ai/api/v2/campaigns/{campaign_id}", headers=headers
        )
        print(f"\n🔍 Campaign GET status: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"lead_list_ids: {data.get('lead_list_ids')}")
            print(f"status: {data.get('status')}")

    print("\n✅ Done")


if __name__ == "__main__":
    asyncio.run(run())
