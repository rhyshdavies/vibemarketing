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
                "name": "Minimal Test"
            }
        )
        if response.status_code in [200, 201]:
            lead_list_id = response.json().get("id")
            print(f"✅ Lead list ID: {lead_list_id}\n")
        else:
            print(f"❌ Error: {response.text}")
            return

    # Test with the absolute minimum fields required
    print("=" * 60)
    print("TEST: Absolute minimum campaign")
    print("=" * 60)

    payload = {
        "api_key": api_key,
        "name": "Minimal Campaign Test",
        "lead_list_ids": [lead_list_id],
        "sequences": [
            {
                "position": 1,
                "subject": "Test Subject",
                "body": "Test Body {{firstName}}",
                "wait_days": 0
            }
        ]
    }

    print("\nPayload:")
    print(json.dumps(payload, indent=2))
    print()

    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{base_url}/campaigns",
            headers=headers,
            json=payload
        )

        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code in [200, 201]:
            print(f"\n✅ SUCCESS!")
            result = response.json()
            print(f"Campaign ID: {result.get('id')}")
            print(json.dumps(result, indent=2))
        else:
            error = response.json()
            print(f"\n❌ Error: {error.get('message')}")

            # If it requires campaign_schedule, let's build it step by step
            if "campaign_schedule" in error.get("message", ""):
                print("\n" + "=" * 60)
                print("campaign_schedule is required. Testing with minimal schedule...")
                print("=" * 60)

                payload["daily_limit"] = 50
                payload["campaign_schedule"] = {
                    "schedules": []
                }

                response = await client.post(
                    f"{base_url}/campaigns",
                    headers=headers,
                    json=payload
                )

                print(f"\nStatus: {response.status_code}")
                print(f"Response: {response.text}")

asyncio.run(test_campaign())
