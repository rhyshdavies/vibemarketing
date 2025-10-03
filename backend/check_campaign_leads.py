"""Quick check if leads are in the campaign"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def check():
    api_key = os.getenv('INSTANTLY_API_KEY')
    campaign_id = '75cb2077-4784-4595-8e55-d77dcba9bc3e'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        print(f'🔍 Checking campaign {campaign_id}')
        print(f'   URL: https://app.instantly.ai/app/campaigns/{campaign_id}')
        print()

        # Check leads directly
        leads_response = await client.post(
            'https://api.instantly.ai/api/v2/leads/list',
            headers=headers,
            json={'campaign_ids': [campaign_id], 'limit': 100}
        )

        if leads_response.status_code == 200:
            data = leads_response.json()
            items = data.get('items', [])
            campaign_leads = [l for l in items if l.get('campaign') == campaign_id]

            print(f'✅ Leads check:')
            print(f'   Total items returned: {len(items)}')
            print(f'   Leads with campaign={campaign_id}: {len(campaign_leads)}')

            if campaign_leads:
                print(f'\n🎉 SUCCESS! Found {len(campaign_leads)} leads in campaign!')
                print(f'\n   Sample leads:')
                for lead in campaign_leads[:10]:
                    print(f'     - {lead.get("email")} ({lead.get("first_name", "N/A")} {lead.get("last_name", "N/A")})')
            else:
                print(f'\n⚠️ No leads found in campaign')
        else:
            print(f'❌ Error: {leads_response.status_code} - {leads_response.text}')

asyncio.run(check())
