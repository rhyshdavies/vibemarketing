import asyncio
import httpx
import json
import os
from dotenv import load_dotenv

load_dotenv()

async def test_full_supersearch_flow():
    api_key = os.getenv("INSTANTLY_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    print("=" * 80)
    print("TESTING FULL SUPERSEARCH FLOW WITH AI")
    print("=" * 80)

    # Step 1: Use AI to generate search filters from ICP
    target_audience = "CTOs and VP of Engineering at Series A funded SaaS startups in San Francisco"
    url = "example.com"

    print(f"\n1. Generating search filters from ICP using AI...")
    print(f"   ICP: {target_audience}")

    async with httpx.AsyncClient(timeout=30.0) as client:
        # Call OpenAI to generate filters
        openai_response = await client.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {openai_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-4",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a B2B lead generation expert. Always return valid JSON matching the exact format requested."
                    },
                    {
                        "role": "user",
                        "content": f"""
Analyze this ICP (Ideal Customer Profile) and convert it into search filters.

ICP Description: {target_audience}
Product URL: {url}

Generate search filters with these constraints:

**Department**: Engineering, Marketing, Sales, etc.
**Level**: C-Level, VP-Level, Director-Level, etc.
**Employee Count**: "0 - 25", "25 - 100", "100 - 250", etc.
**Revenue**: "$1 - 10M", "$10 - 50M", etc.
**Title**: {{"include": ["CEO", "CTO"], "exclude": []}}
**Locations**: If mentioned, format as: [{{"city": "San Francisco", "state": "California", "country": "USA"}}]

Return ONLY valid JSON in this exact format:
{{
  "department": [],
  "level": [],
  "employee_count": [],
  "revenue": [],
  "title": {{"include": [], "exclude": []}},
  "company_name": {{"include": [], "exclude": []}},
  "keyword_filter": {{"include": [], "exclude": ""}},
  "locations": []
}}

Be selective - only include filters that are clearly indicated in the ICP.
"""
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 800
            }
        )

        ai_result = openai_response.json()
        filters_json = ai_result["choices"][0]["message"]["content"]
        search_filters = json.loads(filters_json)

        print(f"\n   ✅ AI Generated Filters:")
        print(json.dumps(search_filters, indent=2))

        # Fix keyword_filter format - convert arrays to comma-separated strings
        if "keyword_filter" in search_filters:
            if isinstance(search_filters["keyword_filter"].get("include"), list):
                search_filters["keyword_filter"]["include"] = ", ".join(search_filters["keyword_filter"]["include"])
            if isinstance(search_filters["keyword_filter"].get("exclude"), list):
                search_filters["keyword_filter"]["exclude"] = ", ".join(search_filters["keyword_filter"]["exclude"])

        print(f"\n   ✅ Filters after format conversion:")
        print(json.dumps(search_filters, indent=2))

    # Step 2: Use SuperSearch with AI-generated filters
    print(f"\n2. Calling Instantly SuperSearch API...")

    payload = {
        "api_key": api_key,
        "search_filters": search_filters,
        "limit": 10,
        "work_email_enrichment": True,
        "skip_rows_without_email": True,
        "list_name": "AI Generated Lead List"
    }

    print(f"\n   Request payload:")
    print(json.dumps(payload, indent=2))

    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            f"{base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
            headers=headers,
            json=payload
        )

        if response.status_code in [200, 201]:
            result = response.json()
            print(f"\n   ✅ SuperSearch Response:")
            print(json.dumps(result, indent=2))

            list_id = result.get("resource_id") or result.get("id")
            print(f"\n3. List ID created: {list_id}")

            # Wait for enrichment
            print(f"\n4. Waiting 20 seconds for enrichment to complete...")
            await asyncio.sleep(20)

            # Check enrichment status
            print(f"\n5. Checking enrichment status...")
            status_response = await client.get(
                f"{base_url}/supersearch-enrichment/{list_id}",
                headers=headers
            )

            if status_response.status_code == 200:
                status_data = status_response.json()
                print(f"\n   ✅ Enrichment Status:")
                print(json.dumps(status_data, indent=2))

                in_progress = status_data.get("in_progress", False)
                print(f"\n   Enrichment in progress: {in_progress}")
            else:
                print(f"\n   ❌ Failed to get enrichment status: {status_response.text}")

            # Try to get the lead list details
            print(f"\n6. Fetching lead list details...")
            list_response = await client.get(
                f"{base_url}/lead-lists/{list_id}",
                headers=headers,
                params={"api_key": api_key}
            )

            if list_response.status_code == 200:
                list_data = list_response.json()
                print(f"\n   ✅ Lead List Details:")
                print(json.dumps(list_data, indent=2))
            else:
                print(f"\n   ❌ Failed to get list details: {list_response.text}")

            print(f"\n{'=' * 80}")
            print(f"SUCCESS! Created lead list with ID: {list_id}")
            print(f"This list contains REAL leads from Instantly's database")
            print(f"You can now use this list_id in your campaigns!")
            print(f"{'=' * 80}")

        else:
            print(f"\n   ❌ SuperSearch Failed:")
            print(f"   Status Code: {response.status_code}")
            print(f"   Response: {response.text}")

asyncio.run(test_full_supersearch_flow())
