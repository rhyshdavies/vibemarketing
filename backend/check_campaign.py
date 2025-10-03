"""
Check if leads have been enriched into the campaign
"""
import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

campaign_id = "f9c429c6-a055-4628-a9ec-f8268571d8fc"

async def check():
    api_key = os.getenv("INSTANTLY_API_KEY")
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

            print(f"Total items returned: {len(campaign_leads)}")
            print(f"Leads with campaign={campaign_id}: {len(actual_campaign_leads)}")

            if actual_campaign_leads:
                print(f"\n🎉 SUCCESS! Leads are in the campaign:")
                for lead in actual_campaign_leads[:5]:
                    print(f"  - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n⏳ Still enriching... check again in a minute")
        else:
            print(f"Error: {response.text}")

asyncio.run(check())
