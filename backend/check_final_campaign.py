"""Check if leads appeared in the campaign"""
import asyncio
import os
from dotenv import load_dotenv
import httpx

load_dotenv()

campaign_id = "aab3a7f0-1a74-4233-9272-9ea028cf98bc"

async def check():
    api_key = os.getenv("INSTANTLY_API_KEY")
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads/list",
            headers=headers,
            json={"campaign_ids": [campaign_id], "limit": 100},
        )

        if response.status_code == 200:
            data = response.json()
            campaign_leads = data.get("items", [])
            actual = [l for l in campaign_leads if l.get("campaign") == campaign_id]

            print(f"Campaign: {campaign_id}")
            print(f"URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
            print(f"\nLeads with campaign_id={campaign_id}: {len(actual)}")

            if actual:
                print(f"\n🎉 SUCCESS! Leads are in campaign:")
                for lead in actual[:10]:
                    print(f"  - {lead.get('email')} ({lead.get('first_name', 'N/A')})")
            else:
                print(f"\n⏳ Still enriching... run again in 1-2 minutes")

asyncio.run(check())
