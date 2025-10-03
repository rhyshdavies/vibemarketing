#!/usr/bin/env python3
"""
Test updating/patching a campaign with email accounts
"""
import asyncio
import os
import httpx
import json
from dotenv import load_dotenv

load_dotenv()

async def test_patch_campaign_accounts():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # First, create a test campaign
    campaign_payload = {
        "name": "Test Campaign for Accounts",
        "sequences": [
            {
                "position": 1,
                "steps": [
                    {
                        "type": "email",
                        "delay": 0,
                        "variants": [{"subject": "Test", "body": "Test"}]
                    }
                ]
            }
        ],
        "campaign_schedule": {
            "schedules": [{
                "name": "Default",
                "timing": {"from": "09:00", "to": "17:00"},
                "days": {"1": True, "2": True, "3": True, "4": True, "5": True},
                "timezone": "Etc/GMT+12"
            }]
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Create campaign
        print("🔍 Creating test campaign...")
        response = await client.post(
            f"{base_url}/campaigns",
            headers=headers,
            json=campaign_payload
        )
        
        if response.status_code not in [200, 201]:
            print(f"❌ Failed to create campaign: {response.text}")
            return
            
        campaign_id = response.json().get("id")
        print(f"✅ Campaign created: {campaign_id}")
        
        # Try different PATCH/PUT patterns
        account_email = "leo@jarvisvoiceapp.info"
        
        endpoints_to_try = [
            # Pattern 1: PATCH campaign with account_emails
            ("PATCH", f"{base_url}/campaigns/{campaign_id}", {"account_emails": [account_email]}),
            # Pattern 2: PUT campaign with account_emails  
            ("PUT", f"{base_url}/campaigns/{campaign_id}", {"account_emails": [account_email]}),
            # Pattern 3: POST to add accounts
            ("POST", f"{base_url}/campaigns/{campaign_id}/accounts", {"emails": [account_email]}),
            # Pattern 4: POST to add accounts (different payload)
            ("POST", f"{base_url}/campaigns/{campaign_id}/accounts", {"account_emails": [account_email]}),
            # Pattern 5: POST to assign accounts
            ("POST", f"{base_url}/campaigns/{campaign_id}/assign-accounts", {"emails": [account_email]}),
            # Pattern 6: PATCH with email field
            ("PATCH", f"{base_url}/campaigns/{campaign_id}", {"emails": [account_email]}),
        ]
        
        for method, url, payload in endpoints_to_try:
            print(f"\n🔍 Trying: {method} {url}")
            print(f"   Payload: {json.dumps(payload)}")
            
            try:
                if method == "PATCH":
                    resp = await client.patch(url, headers=headers, json=payload)
                elif method == "PUT":
                    resp = await client.put(url, headers=headers, json=payload)
                else:
                    resp = await client.post(url, headers=headers, json=payload)
                
                print(f"   📊 Status: {resp.status_code}")
                print(f"   📄 Response: {resp.text[:300]}")
                
                if resp.status_code in [200, 201, 204]:
                    print(f"   ✅ SUCCESS! Checking if account was assigned...")
                    
                    # Check if account was assigned
                    check = await client.get(
                        f"{base_url}/account-campaign-mappings/{account_email}",
                        headers=headers
                    )
                    
                    if check.status_code == 200:
                        campaigns = check.json().get('items', [])
                        our_campaign = [c for c in campaigns if c.get('campaign_id') == campaign_id]
                        if our_campaign:
                            print(f"   🎉 VERIFIED! Account is now assigned to campaign!")
                            print(f"   📄 This is the working endpoint!")
                            break
                        else:
                            print(f"   ⚠️ Request succeeded but account not in campaign yet")
                    
            except Exception as e:
                print(f"   ❌ Error: {str(e)}")
        
        # Clean up
        print(f"\n🗑️ Note: Campaign {campaign_id} created for testing")
        print(f"   You can delete it manually from the dashboard if needed")

asyncio.run(test_patch_campaign_accounts())
