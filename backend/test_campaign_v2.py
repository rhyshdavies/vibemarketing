import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_campaign():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # First, try to get existing campaigns to see their structure
    print("=" * 60)
    print("STEP 1: Fetching existing campaigns to see timezone format...")
    print("=" * 60)
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{base_url}/campaigns",
            headers=headers,
            params={"api_key": api_key}
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            campaigns = response.json()
            if isinstance(campaigns, dict):
                campaigns = campaigns.get("data", [])
            print(f"\nFound {len(campaigns) if isinstance(campaigns, list) else 0} campaigns")
            if campaigns and isinstance(campaigns, list) and len(campaigns) > 0:
                print("\nFirst campaign structure:")
                print(json.dumps(campaigns[0], indent=2))
            else:
                print("No existing campaigns found to inspect")
        else:
            print(f"Error: {response.text}")

    print("\n" + "=" * 60)
    print("STEP 2: Creating lead list...")
    print("=" * 60)
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/lead-lists",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Lead List v2"
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"Lead list ID: {lead_list_id}")
        else:
            print(f"Error: {response.text}")
            return

    # Try different campaign_schedule structures
    print("\n" + "=" * 60)
    print("STEP 3: Testing campaign creation variations...")
    print("=" * 60)

    # Test 1: No timezone in schedule object (only top-level)
    print("\n--- Test 1: Timezone only at top level ---")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/campaigns",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Campaign - No Schedule Timezone",
                "lead_list_ids": [lead_list_id],
                "sequences": [
                    {
                        "position": 1,
                        "subject": "Test Subject",
                        "body": "Test Body",
                        "wait_days": 0
                    }
                ],
                "daily_limit": 50,
                "campaign_schedule": {
                    "timezone": "America/New_York",
                    "schedules": [
                        {
                            "name": "Weekday Schedule",
                            # NO timezone here
                            "days": {
                                "monday": True,
                                "tuesday": True,
                                "wednesday": True,
                                "thursday": True,
                                "friday": True,
                                "saturday": False,
                                "sunday": False
                            },
                            "start_hour": 9,
                            "end_hour": 17,
                            "timing": {
                                "from": "09:00",
                                "to": "17:00",
                                "type": "evenly_distributed",
                                "min_gap_minutes": 30,
                                "max_emails_per_day": 50
                            }
                        }
                    ]
                }
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS! Campaign created!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return
        else:
            print(f"❌ Error: {response.text}")

    # Test 2: Minimal schedule structure
    print("\n--- Test 2: Minimal schedule structure ---")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/campaigns",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Campaign - Minimal",
                "lead_list_ids": [lead_list_id],
                "sequences": [
                    {
                        "position": 1,
                        "subject": "Test Subject",
                        "body": "Test Body",
                        "wait_days": 0
                    }
                ],
                "daily_limit": 50,
                "campaign_schedule": {
                    "schedules": [
                        {
                            "name": "Default Schedule",
                            "days": ["monday", "tuesday", "wednesday", "thursday", "friday"],
                            "start_hour": 9,
                            "end_hour": 17
                        }
                    ]
                }
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS! Campaign created!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return
        else:
            print(f"❌ Error: {response.text}")

    # Test 3: Try without campaign_schedule entirely
    print("\n--- Test 3: No campaign_schedule (just daily_limit) ---")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/campaigns",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Campaign - No Schedule",
                "lead_list_ids": [lead_list_id],
                "sequences": [
                    {
                        "position": 1,
                        "subject": "Test Subject",
                        "body": "Test Body",
                        "wait_days": 0
                    }
                ],
                "daily_limit": 50
            }
        )
        print(f"Status: {response.status_code}")
        if response.status_code in [200, 201]:
            print(f"✅ SUCCESS! Campaign created!")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        else:
            print(f"❌ Error: {response.text}")

asyncio.run(test_campaign())
