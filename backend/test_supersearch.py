import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_supersearch():
    api_key = os.getenv("INSTANTLY_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("Testing SuperSearch API...")

    # Simple search filters (removing industry for now as it needs specific values)
    search_filters = {
        "level": ["C-Level"],
        "department": ["Engineering"],
        "employee_count": ["25 - 100"],
        "title": {"include": ["CEO", "CTO"], "exclude": []}
    }

    payload = {
        "api_key": api_key,
        "search_filters": search_filters,
        "limit": 5,
        "work_email_enrichment": True,
        "skip_rows_without_email": True,
        "list_name": "Test SuperSearch"
    }

    print(f"\n1. Sending SuperSearch request...")
    print(f"Filters: {json.dumps(search_filters, indent=2)}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
            headers=headers,
            json=payload
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"\n✅ SuperSearch Response:")
            print(json.dumps(result, indent=2))

            # Extract the resource_id (list ID)
            list_id = result.get("resource_id") or result.get("id")
            print(f"\n2. List ID created: {list_id}")

            # Wait for enrichment
            print(f"\n3. Waiting 15 seconds for enrichment to complete...")
            await asyncio.sleep(15)

            # Try to get the lead list details
            print(f"\n4. Fetching lead list details...")
            response2 = await client.get(
                f"{base_url}/lead-lists/{list_id}",
                headers=headers,
                params={"api_key": api_key}
            )

            if response2.status_code == 200:
                list_data = response2.json()
                print(f"\n✅ Lead List Details:")
                print(json.dumps(list_data, indent=2))
            else:
                print(f"\n❌ Failed to get list details: {response2.text}")

            # Try to get enrichment status
            print(f"\n5. Checking enrichment status...")
            response3 = await client.get(
                f"{base_url}/supersearch-enrichment/{list_id}",
                headers=headers
            )

            if response3.status_code == 200:
                enrichment_data = response3.json()
                print(f"\n✅ Enrichment Status:")
                print(json.dumps(enrichment_data, indent=2))
            else:
                print(f"\n❌ Failed to get enrichment status: {response3.text}")

        else:
            print(f"\n❌ SuperSearch Failed:")
            print(response.text)

asyncio.run(test_supersearch())
