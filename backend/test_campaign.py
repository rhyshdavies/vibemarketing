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

    # Test 1: Create lead list
    print("Creating lead list...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/lead-lists",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Lead List"
            }
        )
        print(f"Lead list response: {response.status_code}")
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"Lead list ID: {lead_list_id}")
        else:
            print(f"Error: {response.text}")
            return

    # Test 2: Try different timezone values
    # Testing: lowercase, numeric offsets, null, abbreviations, alternative formats
    timezones = [
        # Numeric offsets
        "-05:00",
        "-04:00",
        "+00:00",
        "-08:00",
        # Lowercase
        "america/new_york",
        "utc",
        # Short codes
        "US/Eastern",
        "US/Pacific",
        "US/Central",
        # Alternative formats
        "Eastern Standard Time",
        "Pacific Standard Time",
        "Coordinated Universal Time",
        # Try with None/null
        None,
        # Original IANA formats (retry for completeness)
        "America/New_York",
        "UTC"
    ]

    for tz in timezones:
        print(f"\nTrying timezone: {tz}")
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/campaigns",
                headers=headers,
                json={
                    "api_key": api_key,
                    "name": f"Test Campaign - {tz}",
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
                        "timezone": tz,
                        "schedules": [
                            {
                                "name": "Weekday Schedule",
                                "timezone": tz,
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
                print(f"SUCCESS! Campaign created with timezone: {tz}")
                print(f"Response: {response.json()}")
                break
            else:
                print(f"Error: {response.text}")

asyncio.run(test_campaign())
