"""Test the exact bulk create format with completely fresh emails"""
import asyncio
import httpx
import os
import uuid
from dotenv import load_dotenv

load_dotenv()

async def test():
    api_key = os.getenv('INSTANTLY_API_KEY')

    # Create campaign first
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    print("Creating test campaign...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        # Create temp list
        list_response = await client.post(
            'https://api.instantly.ai/api/v2/lead-lists',
            headers=headers,
            json={'name': 'Temp for bulk test'}
        )
        temp_list_id = list_response.json().get('id')

        # Create campaign
        campaign_response = await client.post(
            'https://api.instantly.ai/api/v2/campaigns',
            headers=headers,
            json={
                'name': 'BULK CREATE TEST',
                'lead_list_ids': [temp_list_id],
                'variants': [{'subject': 'Test', 'body': 'Hi {{firstName}}'}]
            }
        )
        campaign_id = campaign_response.json().get('id')

        print(f"Campaign created: {campaign_id}")
        print(f"URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
        print()

        # Now test bulk create with completely fresh emails
        print("Testing bulk create with 2 fresh emails...")

        payload = {
            'campaign_id': campaign_id,
            'skip_if_in_workspace': True,
            'leads': [
                {
                    'email': f'fresh-{uuid.uuid4()}@example.com',
                    'first_name': 'Test',
                    'last_name': 'User1',
                    'company': 'Test Co',
                    'custom_variables': {'source': 'test'}
                },
                {
                    'email': f'fresh-{uuid.uuid4()}@example.com',
                    'first_name': 'Test',
                    'last_name': 'User2',
                    'company': 'Test Co',
                    'custom_variables': {'source': 'test'}
                }
            ]
        }

        print(f"Payload:")
        import json
        print(json.dumps(payload, indent=2)[:500])
        print()

        bulk_response = await client.post(
            'https://api.instantly.ai/api/v2/leads/list',
            headers=headers,
            json=payload
        )

        print(f"Response status: {bulk_response.status_code}")
        print(f"Response:")
        print(bulk_response.text[:1000])
        print()

        if bulk_response.status_code in [200, 201]:
            result = bulk_response.json()
            print(f"Response type: {type(result)}")
            if isinstance(result, dict):
                print(f"Response keys: {result.keys()}")

asyncio.run(test())
