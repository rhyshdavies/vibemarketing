import asyncio
import os
import json
from dotenv import load_dotenv
import httpx

load_dotenv()

API = "https://api.instantly.ai/api/v2"


async def run():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # 1) Create SuperSearch list for 10 leads (simple broad filters)
    filters = {
        "level": ["C-Level", "Owner"],
        "employee_count": ["0 - 25", "25 - 100"],
        "locations": [{"city": "", "state": "", "country": "United States"}],
    }

    payload = {
        "api_key": api_key,
        "search_filters": filters,
        "limit": 10,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Verify Leads - 10",
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        print("📥 Creating SuperSearch list (limit=10)...")
        resp = await client.post(
            f"{API}/supersearch-enrichment/enrich-leads-from-supersearch",
            headers=headers,
            json=payload,
        )
        if resp.status_code not in [200, 201]:
            print(f"❌ Failed to create SuperSearch list: {resp.text}")
            return
        data = resp.json()
        list_id = data.get("resource_id") or data.get("id")
        print(f"✅ List ID: {list_id}")

    # 2) Short wait for enrichment to start
    await asyncio.sleep(5)

    # 3) Create campaign with that list using a known-good timezone
    campaign_payload = {
        "api_key": api_key,
        "name": "Verify Leads Campaign - 10",
        "lead_list_ids": [list_id],
        "sequences": [
            {
                "position": 1,
                "steps": [
                    {
                        "type": "email",
                        "delay": 0,
                        "variants": [
                            {
                                "subject": "Quick hello",
                                "body": "Hi {{firstName}},\n\nQuick hello from us.\n\nBest",
                            }
                        ],
                    }
                ],
            }
        ],
        "daily_limit": 25,
        "campaign_schedule": {
            "schedules": [
                {
                    "name": "Default",
                    "timing": {"from": "09:00", "to": "17:00"},
                    "days": {
                        "monday": True,
                        "tuesday": True,
                        "wednesday": True,
                        "thursday": True,
                        "friday": True,
                        "saturday": False,
                        "sunday": False,
                    },
                    "timezone": "America/Chicago",
                }
            ]
        },
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        print("\n📧 Creating campaign...")
        resp = await client.post(
            f"{API}/campaigns", headers=headers, json=campaign_payload
        )
        print(f"Status: {resp.status_code}")
        if resp.status_code not in [200, 201]:
            print(f"❌ Failed to create campaign: {resp.text}")
            return
        camp = resp.json()
        campaign_id = camp.get("id")
        print(f"✅ Campaign ID: {campaign_id}")
        print(f"URL: https://app.instantly.ai/app/campaigns/{campaign_id}")

    # 4) Query leads filtered by campaign_id
    await asyncio.sleep(2)  # small delay for processing
    async with httpx.AsyncClient(timeout=120.0) as client:
        print("\n🔍 Checking leads in campaign via /leads/list filter...")
        resp = await client.post(
            f"{API}/leads/list",
            headers=headers,
            json={"campaign_ids": [campaign_id], "limit": 100},
        )
        print(f"Status: {resp.status_code}")
        if resp.status_code != 200:
            print(f"❌ Error fetching leads: {resp.text}")
            return
        res = resp.json()
        items = res.get("items", []) if isinstance(res, dict) else []
        print(f"📊 Leads returned: {len(items)}")
        if items:
            for i, lead in enumerate(items[:5], 1):
                print(
                    f"  {i}. {lead.get('email')} - {lead.get('title')} @ {lead.get('company_name')}"
                )
        else:
            print("⚠️ No leads returned yet (enrichment may still be processing)")


if __name__ == "__main__":
    asyncio.run(run())
