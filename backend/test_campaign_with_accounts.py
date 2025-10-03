#!/usr/bin/env python3
"""
Test creating a campaign with email accounts specified
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_create_campaign_with_accounts():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    
    # Test payload with account_emails field
    payload = {
        "name": "Test Campaign with Accounts",
        "sequences": [
            {
                "position": 1,
                "steps": [
                    {
                        "type": "email",
                        "delay": 0,
                        "variants": [
                            {
                                "subject": "Test",
                                "body": "Test body"
                            }
                        ]
                    }
                ]
            }
        ],
        # Try different field names for accounts
        "account_emails": ["leo@jarvisvoiceapp.info"],
        "campaign_schedule": {
            "schedules": [{
                "name": "Default",
                "timing": {"from": "09:00", "to": "17:00"},
                "days": {"1": True, "2": True, "3": True, "4": True, "5": True, "0": False, "6": False},
                "timezone": "Etc/GMT+12"
            }]
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        print("🔍 Testing campaign creation with account_emails field...")
        print(f"   Endpoint: {base_url}/campaigns")
        
        try:
            response = await client.post(
                f"{base_url}/campaigns",
                headers=headers,
                json=payload
            )
            
            print(f"\n📊 Response status: {response.status_code}")
            print(f"📄 Response body: {response.text[:500]}")
            
            if response.status_code in [200, 201]:
                data = response.json()
                campaign_id = data.get("id")
                print(f"\n✅ Campaign created: {campaign_id}")
                
                # Now check if accounts were assigned
                print(f"\n🔍 Checking if account was assigned to campaign...")
                check_response = await client.get(
                    f"{base_url}/account-campaign-mappings/leo@jarvisvoiceapp.info",
                    headers=headers
                )
                
                print(f"📊 Check status: {check_response.status_code}")
                mapping_data = check_response.json()
                print(f"📄 Campaigns for this account: {len(mapping_data.get('items', []))}")
                
                # Check if our campaign is in the list
                our_campaign = [c for c in mapping_data.get('items', []) if c.get('campaign_id') == campaign_id]
                if our_campaign:
                    print(f"✅ SUCCESS! Account was automatically assigned to campaign!")
                else:
                    print(f"❌ Account was NOT assigned automatically")
                
                # Clean up - delete test campaign
                print(f"\n🗑️ Cleaning up test campaign...")
                delete_response = await client.delete(
                    f"{base_url}/campaigns/{campaign_id}",
                    headers=headers
                )
                print(f"   Delete status: {delete_response.status_code}")
            else:
                print(f"\n❌ Failed to create campaign")
                
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

asyncio.run(test_create_campaign_with_accounts())
