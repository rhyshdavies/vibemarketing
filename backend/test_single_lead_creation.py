"""
Test creating a single lead with campaign_id to see the exact response
"""
import asyncio
import os
from dotenv import load_dotenv
import httpx
import uuid

load_dotenv()


async def test_single_lead():
    api_key = os.getenv("INSTANTLY_API_KEY")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    # Use a completely unique email that definitely doesn't exist
    unique_email = f"test-{uuid.uuid4()}@example.com"
    campaign_id = "test-campaign-123"

    print(f"Creating lead with:")
    print(f"  Email: {unique_email}")
    print(f"  Campaign ID: {campaign_id}")
    print()

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "https://api.instantly.ai/api/v2/leads",
            headers=headers,
            json={
                "email": unique_email,
                "first_name": "Test",
                "last_name": "User",
                "campaign_id": campaign_id
            }
        )

        print(f"Response status: {response.status_code}")
        print(f"Response body:")
        print(response.text)

        if response.status_code in [200, 201]:
            data = response.json()
            print()
            print(f"Campaign field in response: {data.get('campaign')}")
            print(f"Campaign ID we sent: {campaign_id}")
            print(f"Do they match? {data.get('campaign') == campaign_id}")


if __name__ == "__main__":
    asyncio.run(test_single_lead())
