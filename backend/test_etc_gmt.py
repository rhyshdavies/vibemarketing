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
                "name": "Etc/GMT Test"
            }
        )
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"✅ Lead list ID: {lead_list_id}\n")
        else:
            print(f"❌ Error: {response.text}")
            return

    # Try Etc/GMT formats (from WebSearch result)
    timezone_tests = [
        # Etc/GMT formats (from search results)
        "Etc/GMT+12",
        "Etc/GMT+11",
        "Etc/GMT+10",
        "Etc/GMT+9",
        "Etc/GMT+8",
        "Etc/GMT+7",
        "Etc/GMT+6",
        "Etc/GMT+5",  # EST
        "Etc/GMT+4",
        "Etc/GMT+3",
        "Etc/GMT+2",
        "Etc/GMT+1",
        "Etc/GMT",
        "Etc/GMT-1",
        "Etc/GMT-2",
        "Etc/GMT-3",
        "Etc/GMT-4",
        "Etc/GMT-5",
        "Etc/GMT-6",
        "Etc/GMT-7",
        "Etc/GMT-8",
    ]

    for tz in timezone_tests:
        print(f"Testing: {tz}")

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
                                    "subject": "Test Subject",
                                    "body": "Test Body"
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

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{base_url}/campaigns",
                headers=headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                print(f"  ✅✅✅ SUCCESS! Working timezone: {tz}")
                result = response.json()
                print(f"  Campaign ID: {result.get('id')}")
                print(f"\n🎉🎉🎉 FOUND THE FORMAT: {tz}\n")
                print("Full response:")
                print(json.dumps(result, indent=2))
                return
            else:
                error_msg = response.json().get("message", "Unknown error")
                if "timezone" in error_msg:
                    print(f"  ❌ Timezone error")
                else:
                    print(f"  ❌ Other error: {error_msg}")

    print("\n😞 None of the Etc/GMT formats worked either")

asyncio.run(test_campaign())
