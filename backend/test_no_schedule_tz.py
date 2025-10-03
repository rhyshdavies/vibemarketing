import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_without_schedule_tz():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Get existing lead list
    lead_list_id = "532dc39c-63ec-442b-a4de-829e11617cad"

    tz = "America/New_York"
    print(f"Testing WITHOUT schedule-level timezone, only top-level: {tz}")

    payload = {
        "api_key": api_key,
        "name": f"Test No Schedule TZ",
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
                    # NO TIMEZONE HERE
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
            print(f"  ✅✅✅ SUCCESS without schedule timezone!")
            result = response.json()
            print(json.dumps(result, indent=2))
        else:
            print(f"  ❌ Failed: {response.text}")

asyncio.run(test_without_schedule_tz())
