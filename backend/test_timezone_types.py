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
                "name": "Timezone Type Test"
            }
        )
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"✅ Lead list ID: {lead_list_id}\n")
        else:
            print(f"❌ Error: {response.text}")
            return

    # Try timezone as NUMBER (maybe it's an ID?)
    timezone_tests = [
        1, 2, 3, 4, 5, 10, 100,
        # Try negative
        -5, -4, -8,
        # Try float
        -5.0, -4.0,
        # Try as string numbers
        "1", "2", "5",
        # Try IANA with underscores
        "America_New_York",
        "America_Los_Angeles",
        # Try Region/City format
        "US/Eastern",
        "US/Pacific",
    ]

    for tz in timezone_tests:
        print(f"Testing timezone: {tz} (type: {type(tz).__name__})")

        payload = {
            "api_key": api_key,
            "name": f"Test TZ {tz}",
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/campaigns",
                headers=headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                print(f"  ✅ SUCCESS! Working timezone: {tz}")
                print(f"  Campaign ID: {response.json().get('id')}")
                print(f"\n🎉 FOUND IT: timezone = {tz} (type: {type(tz).__name__})\n")
                return
            else:
                error_msg = response.json().get("message", response.text)
                if "timezone" in error_msg:
                    print(f"  ❌ {error_msg}")
                else:
                    print(f"  ❌ Different error: {error_msg}")

    print("\n😞 None worked")

asyncio.run(test_campaign())
