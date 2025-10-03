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

    # Create lead list
    print("Creating lead list...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/lead-lists",
            headers=headers,
            json={
                "api_key": api_key,
                "name": "Test Lead List v3"
            }
        )
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"✅ Lead list ID: {lead_list_id}\n")
        else:
            print(f"❌ Error: {response.text}")
            return

    # Try common email marketing platform timezone formats
    timezones = [
        # Simple names (what UI might use)
        "Eastern",
        "Pacific",
        "Central",
        "Mountain",
        "Alaska",
        "Hawaii",
        # With Time appended
        "Eastern Time",
        "Pacific Time",
        "Central Time",
        # Abbreviated
        "ET",
        "PT",
        "CT",
        "MT",
        # With (US & Canada)
        "Eastern Time (US & Canada)",
        "Pacific Time (US & Canada)",
        "Central Time (US & Canada)",
        # Rails-style identifiers
        "Eastern Time (US and Canada)",
        "Pacific Time (US and Canada)",
        # Just the city names
        "New York",
        "Los Angeles",
        "Chicago",
        # International common ones
        "London",
        "Paris",
        "Tokyo",
        "Sydney",
        # Try empty string
        "",
    ]

    for tz in timezones:
        print(f"Testing: '{tz}'")
        async with httpx.AsyncClient() as client:
            payload = {
                "api_key": api_key,
                "name": f"Test - {tz or 'empty'}",
                "lead_list_ids": [lead_list_id],
                "sequences": [
                    {
                        "position": 1,
                        "subject": "Test",
                        "body": "Test",
                        "wait_days": 0
                    }
                ],
                "daily_limit": 50,
                "campaign_schedule": {
                    "timezone": tz,
                    "schedules": [
                        {
                            "name": "Schedule",
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

            response = await client.post(
                f"{base_url}/campaigns",
                headers=headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                print(f"  ✅ SUCCESS WITH: '{tz}'")
                print(f"  Campaign ID: {response.json().get('id')}")
                print(f"\n🎉 WORKING TIMEZONE FORMAT: '{tz}'")
                return
            else:
                error_msg = response.json().get("message", response.text)
                print(f"  ❌ {error_msg}")

    print("\n😞 None of the timezone formats worked")

asyncio.run(test_campaign())
