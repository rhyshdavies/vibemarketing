"""
Wait for enrichment to complete and check actual lead results
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def wait_and_check_results():
    """Create enrichment, wait for completion, check results"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Lead Results After Enrichment\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Create enrichment with specific filters
    payload = {
        "api_key": api_key,
        "search_filters": {
            "level": ["C-Level"],
            "employee_count": ["25 - 100"],  # More common size
            "industry": {
                "include": ["Software & Internet"],
                "exclude": []
            }
        },
        "limit": 10,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Test Software C-Level"
    }

    print("Creating enrichment with filters:")
    print(json.dumps(payload['search_filters'], indent=2))

    async with httpx.AsyncClient(timeout=120.0) as client:
        # Start enrichment
        response = await client.post(
            f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
            headers=headers,
            json=payload,
        )

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return

        result = response.json()
        resource_id = result['resource_id']
        list_id = result['id']

        print(f"\n✅ Enrichment started")
        print(f"   Resource ID: {resource_id}")
        print(f"   List ID: {list_id}")

        # Poll for completion
        max_wait = 120  # 2 minutes
        poll_interval = 10  # 10 seconds
        elapsed = 0

        print(f"\n⏳ Waiting for enrichment to complete...")

        while elapsed < max_wait:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            # Check status
            status_response = await client.get(
                f"{base_url}/supersearch-enrichment/status/{resource_id}",
                headers=headers,
                params={"api_key": api_key}
            )

            if status_response.status_code == 200:
                status = status_response.json()
                in_progress = status.get('in_progress', True)

                print(f"   [{elapsed}s] In progress: {in_progress}")

                if not in_progress:
                    print(f"\n✅ Enrichment completed!")

                    # Try to get the lead list
                    list_response = await client.get(
                        f"{base_url}/lead-lists/{list_id}",
                        headers=headers,
                        params={"api_key": api_key}
                    )

                    if list_response.status_code == 200:
                        list_data = list_response.json()
                        print(f"\n📊 Lead List Data:")
                        print(json.dumps(list_data, indent=2))

                        # Check leads
                        if 'leads' in list_data:
                            leads = list_data['leads']
                            print(f"\n✅ Found {len(leads)} leads")

                            if len(leads) > 0:
                                print("\nFirst 3 leads:")
                                for i, lead in enumerate(leads[:3], 1):
                                    name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
                                    title = lead.get('title', 'N/A')
                                    company = lead.get('company_name', 'N/A')
                                    industry = lead.get('industry', 'N/A')
                                    company_size = lead.get('company_size', 'N/A')
                                    location = lead.get('location', 'N/A')

                                    print(f"\n{i}. {name}")
                                    print(f"   Title: {title}")
                                    print(f"   Company: {company}")
                                    print(f"   Industry: {industry}")
                                    print(f"   Size: {company_size}")
                                    print(f"   Location: {location}")
                        else:
                            print("\n⚠️  No 'leads' field in response")
                    else:
                        print(f"\n❌ Failed to get lead list: {list_response.status_code}")
                        print(list_response.text)

                    break

        if elapsed >= max_wait:
            print(f"\n⏱️  Timeout after {max_wait}s - enrichment still in progress")


if __name__ == "__main__":
    asyncio.run(wait_and_check_results())
