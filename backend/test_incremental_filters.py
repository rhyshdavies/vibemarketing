"""
Test filters incrementally to find which one causes no results
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def test_incremental_filters():
    """Add filters one by one and check results after each"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Filters Incrementally\n")
    print("Will add filters one at a time and wait for results\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Test cases - adding filters incrementally
    test_cases = [
        {
            "name": "1. Just level (C-Level)",
            "filters": {
                "level": ["C-Level"]
            }
        },
        {
            "name": "2. Level + Company size",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["25 - 100"]
            }
        },
        {
            "name": "3. Level + Size + Location (USA)",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["25 - 100"],
                "locations": [
                    {
                        "city": "",
                        "state": "",
                        "country": "United States"
                    }
                ]
            }
        },
        {
            "name": "4. Level + Size + Location (San Francisco)",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["25 - 100"],
                "locations": [
                    {
                        "city": "San Francisco",
                        "state": "California",
                        "country": "United States"
                    }
                ]
            }
        },
        {
            "name": "5. Level + Size + Industry (Software & Internet)",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["25 - 100"],
                "industry": {
                    "include": ["Software & Internet"],
                    "exclude": []
                }
            }
        },
        {
            "name": "6. Level + Size + Location (UK)",
            "filters": {
                "level": ["C-Level"],
                "employee_count": ["25 - 100"],
                "locations": [
                    {
                        "city": "",
                        "state": "",
                        "country": "United Kingdom"
                    }
                ]
            }
        },
    ]

    async with httpx.AsyncClient(timeout=180.0) as client:
        for i, test in enumerate(test_cases, 1):
            print(f"\n{'='*80}")
            print(f"TEST {i}: {test['name']}")
            print('='*80)
            print("Filters:")
            print(json.dumps(test['filters'], indent=2))

            # Create enrichment
            payload = {
                "api_key": api_key,
                "search_filters": test['filters'],
                "limit": 3,  # Only 3 leads to save credits
                "work_email_enrichment": True,
                "fully_enriched_profile": False,
                "skip_rows_without_email": True,
                "list_name": f"Test {i} - {test['name'][:30]}"
            }

            try:
                print("\n⏳ Creating enrichment...")
                response = await client.post(
                    f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
                    headers=headers,
                    json=payload,
                )

                if response.status_code != 200:
                    print(f"❌ Failed to create: {response.text}")
                    continue

                result = response.json()
                resource_id = result['resource_id']
                print(f"✅ Created - Resource ID: {resource_id}")

                # Wait and poll for completion
                print("⏳ Waiting for enrichment to complete...")
                max_wait = 10  # 10 seconds
                poll_interval = 2  # 2 seconds
                elapsed = 0

                lead_count = None
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

                        # Check if we have leads in the response
                        if 'leads' in status:
                            lead_count = len(status['leads'])
                            print(f"\n✅ FOUND {lead_count} LEADS!")

                            if lead_count > 0:
                                print("\nLead details:")
                                for j, lead in enumerate(status['leads'], 1):
                                    name = f"{lead.get('first_name', '')} {lead.get('last_name', '')}"
                                    title = lead.get('title', 'N/A')
                                    company = lead.get('company_name', 'N/A')
                                    location = lead.get('location', 'N/A')
                                    industry = lead.get('industry', 'N/A')
                                    size = lead.get('company_size', 'N/A')

                                    print(f"\n  {j}. {name} - {title}")
                                    print(f"     Company: {company}")
                                    print(f"     Location: {location}")
                                    print(f"     Industry: {industry}")
                                    print(f"     Size: {size}")
                            else:
                                print("\n❌ ZERO LEADS RETURNED - This filter combination returns no results!")

                            break

                        if not in_progress:
                            print(f"\n✅ Enrichment completed")
                            # Even if completed, if we haven't seen leads yet, it might be 0
                            if lead_count is None:
                                print("⚠️  Job completed but no leads in status response")
                                print("This might mean 0 leads found")
                            break

                if elapsed >= max_wait:
                    print(f"\n⏱️  Timeout after {max_wait}s - still in progress")

            except Exception as e:
                print(f"\n❌ ERROR: {str(e)}")
                import traceback
                print(traceback.format_exc())

            # Small delay between tests
            print("\n⏸️  Waiting 5 seconds before next test...")
            await asyncio.sleep(5)

    print(f"\n{'='*80}")
    print("Testing Complete!")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(test_incremental_filters())
