#!/usr/bin/env python3
"""
Test adding email accounts to a campaign
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

async def test_add_accounts():
    api_key = os.getenv("INSTANTLY_API_KEY")
    
    # You'll need to provide a real campaign_id from your dashboard
    campaign_id = "test-campaign-id"  # Replace with actual campaign ID
    
    # Test endpoint variations
    endpoints = [
        f"https://api.instantly.ai/api/v2/campaigns/{campaign_id}/accounts",
        f"https://api.instantly.ai/api/v2/campaigns/{campaign_id}/email-accounts",
        "https://api.instantly.ai/api/v2/campaigns/add-accounts",
        "https://api.instantly.ai/api/v2/campaigns/assign-accounts",
    ]
    
    headers = {"Content-Type": "application/json"}
    
    test_payload = {
        "api_key": api_key,
        "campaign_id": campaign_id,
        "email": "test@example.com"
    }
    
    async with httpx.AsyncClient() as client:
        for endpoint in endpoints:
            print(f"\n🔍 Testing: {endpoint}")
            try:
                # Try POST
                response = await client.post(endpoint, headers=headers, json=test_payload, timeout=10.0)
                print(f"   POST {response.status_code}: {response.text[:200]}")
            except Exception as e:
                print(f"   POST Error: {e}")

asyncio.run(test_add_accounts())
