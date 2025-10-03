import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

async def check_lists():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("Fetching all lead lists from Instantly...")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.get(
            f"{base_url}/lead-lists",
            headers=headers,
            params={"api_key": api_key, "limit": 50}
        )
        
        if response.status_code == 200:
            data = response.json()
            lists = data.get("items", [])
            
            print(f"\n✅ Found {len(lists)} lead lists:\n")
            
            for i, lst in enumerate(lists, 1):
                print(f"{i}. {lst.get('name')} (ID: {lst.get('id')})")
                print(f"   Created: {lst.get('timestamp_created')}")
                print(f"   Has enrichment: {lst.get('has_enrichment_task', False)}\n")
        else:
            print(f"❌ Error: {response.text}")

asyncio.run(check_lists())
