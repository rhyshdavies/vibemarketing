import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_timezones():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Get existing lead list
    lead_list_id = "532dc39c-63ec-442b-a4de-829e11617cad"

    # Test different timezone formats
    timezones_to_test = [
        "America/New_York",
        "US/Eastern",
        "EST",
        "EST5EDT",
        "UTC",
        "GMT",
        "Etc/UTC",
        "Etc/GMT",
        "Etc/GMT+0",
        "Etc/GMT-5",  # This is actually EST (confusing, I know)
        "+00:00",
        "-05:00",
    ]

    for tz in timezones_to_test:
        print(f"\nTesting: {tz}")

        payload = {
            "api_key": api_key,
            "name": f"Test {tz}",
            "lead_list_ids": [lead_list_id],
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
                                    "body": "Test"
                                }
                            ]
                        }
                    ]
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
                print(f"  ✅✅✅ SUCCESS: {tz}")
                result = response.json()
                print(f"  Campaign ID: {result.get('id')}")
            else:
                error = response.json().get("message", "Unknown")
                if "timezone" in error:
                    print(f"  ❌ Timezone error")
                else:
                    print(f"  ❌ Other: {error}")

asyncio.run(test_timezones())
