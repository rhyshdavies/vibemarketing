#!/usr/bin/env python3
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {api_key}"}
    
    test_email = "rhys@tryjarvisapp.info"  # Real account from your workspace
    
    payload = {
        "name": "Test Email List",
        "sequences": [{"position": 1, "steps": [{"type": "email", "delay": 0, "variants": [{"subject": "Test", "body": "Test"}]}]}],
        "email_list": [test_email],
        "campaign_schedule": {"schedules": [{"name": "Default", "timing": {"from": "09:00", "to": "17:00"}, "days": {"1": True, "2": True, "3": True, "4": True, "5": True}, "timezone": "Etc/GMT+12"}]}
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print(f"🔍 Creating campaign with email_list: [{test_email}]...")
        
        resp = await client.post(f"{base_url}/campaigns", headers=headers, json=payload)
        print(f"📊 Status: {resp.status_code}")
        
        if resp.status_code in [200, 201]:
            data = resp.json()
            campaign_id = data.get("id")
            email_list_in_response = data.get("email_list", [])
            
            print(f"✅ Campaign: {campaign_id}")
            print(f"📧 email_list in response: {email_list_in_response}")
            
            if test_email in email_list_in_response:
                print(f"\n🎉 SUCCESS! Account added via email_list!")
            
            # Cleanup
            await client.delete(f"{base_url}/campaigns/{campaign_id}", headers=headers)
        else:
            print(f"❌ Error: {resp.text}")

asyncio.run(test())
