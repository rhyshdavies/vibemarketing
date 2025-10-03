"""
Test the complete ICP-driven campaign creation flow:
1. Analyze URL for ICPs
2. Select ICP and search for leads
3. Preview leads
4. Generate email variants
5. Match DFY domains
6. Create campaign with everything
"""
import asyncio
import httpx
import json

BASE_URL = "http://localhost:8000"
TEST_URL = "https://www.instantly.ai"
USER_ID = "test_user_123"


async def test_icp_flow():
    print("🎯 ICP-DRIVEN CAMPAIGN CREATION FLOW TEST")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=120.0) as client:

        # Step 1: Analyze URL for ICPs
        print("\n✅ Step 1: Analyzing URL for ICP suggestions...")
        response = await client.post(
            f"{BASE_URL}/api/icp/analyze",
            json={"url": TEST_URL}
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        data = response.json()
        icps = data.get("icps", [])
        print(f"   Found {len(icps)} ICP suggestions:")
        for idx, icp in enumerate(icps):
            print(f"   {idx + 1}. {icp.get('name')}: {icp.get('description')}")

        # Select the first ICP
        selected_icp = icps[0]
        print(f"\n   ✅ Selected ICP: {selected_icp.get('name')}")
        print(f"   Target Audience: {selected_icp.get('target_audience')}")

        # Step 2: Search for leads based on selected ICP
        print(f"\n✅ Step 2: Searching for leads matching selected ICP...")
        response = await client.post(
            f"{BASE_URL}/api/icp/search-leads",
            json={
                "url": TEST_URL,
                "target_audience": selected_icp.get("target_audience"),
                "lead_count": 3  # Just 3 leads for testing
            }
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        data = response.json()
        enrichment_id = data.get("enrichment_id")
        print(f"   ✅ Lead search started!")
        print(f"   Enrichment ID: {enrichment_id}")
        print(f"   Search Filters: {json.dumps(data.get('search_filters', {}), indent=2)}")

        # Step 3: Get lead preview (with polling)
        print(f"\n✅ Step 3: Waiting for leads to be ready...")
        max_retries = 18  # 18 * 5 seconds = 90 seconds
        leads = []

        for retry in range(max_retries):
            await asyncio.sleep(5)
            print(f"   Polling for leads... (attempt {retry + 1}/{max_retries})")

            response = await client.get(
                f"{BASE_URL}/api/icp/leads/{enrichment_id}",
                params={"limit": 3}
            )

            if response.status_code != 200:
                print(f"❌ Error: {response.text}")
                continue

            data = response.json()
            if data.get("success") and len(data.get("leads", [])) > 0:
                leads = data.get("leads", [])
                print(f"   ✅ Got {len(leads)} leads!")
                for idx, lead in enumerate(leads):
                    print(f"   {idx + 1}. {lead.get('first_name')} {lead.get('last_name')} - {lead.get('email')}")
                    print(f"      Company: {lead.get('company_name')} | Title: {lead.get('title')}")
                break

        if not leads:
            print(f"   ⚠️  No leads found after {max_retries * 5} seconds. Enrichment may still be in progress.")
            print(f"   You can check later using enrichment_id: {enrichment_id}")
            return

        # Step 4: Generate email variants for the ICP
        print(f"\n✅ Step 4: Generating email variants for selected ICP...")
        response = await client.post(
            f"{BASE_URL}/api/icp/generate-emails",
            json={
                "url": TEST_URL,
                "selected_icp": selected_icp
            }
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        data = response.json()
        variants = data.get("variants", [])
        print(f"   ✅ Generated {len(variants)} email variants:")
        for idx, variant in enumerate(variants):
            print(f"\n   Variant {idx + 1}:")
            print(f"   Subject: {variant.get('subject')}")
            print(f"   Body (first 150 chars): {variant.get('body')[:150]}...")

        # Step 5: Match DFY domains
        print(f"\n✅ Step 5: Finding best DFY email domains...")
        response = await client.post(
            f"{BASE_URL}/api/icp/match-domains",
            json={"url": TEST_URL}
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        data = response.json()
        matched_domains = data.get("matched_domains", [])

        if not matched_domains:
            print(f"   ⚠️  No pre-warmed domains currently available")
            print(f"   Skipping domain selection...")
            selected_domains = []
        else:
            print(f"   ✅ Found {len(matched_domains)} matched domains:")
            for idx, domain_info in enumerate(matched_domains):
                print(f"   {idx + 1}. {domain_info.get('domain')} (Score: {domain_info.get('score')})")
                print(f"      Reasoning: {domain_info.get('reasoning')}")
                print(f"      Suggested Use: {domain_info.get('suggested_use')}")

            # Select top 2 domains
            selected_domains = [d.get("domain") for d in matched_domains[:2]]
            print(f"\n   ✅ Selected domains: {', '.join(selected_domains)}")

        # Step 6: Create the campaign with everything
        print(f"\n✅ Step 6: Creating campaign with all components...")

        response = await client.post(
            f"{BASE_URL}/api/icp/create-campaign",
            json={
                "campaign_name": f"ICP Test - {selected_icp.get('name')}",
                "url": TEST_URL,
                "user_id": USER_ID,
                "selected_icp": selected_icp,
                "enrichment_id": enrichment_id,
                "lead_count": len(leads),
                "approved_variants": variants,  # Using all 3 generated variants
                "selected_domains": selected_domains
            }
        )

        if response.status_code != 200:
            print(f"❌ Error: {response.text}")
            return

        print(f"   📡 Streaming campaign creation progress...")

        # Stream the SSE response
        async for line in response.aiter_lines():
            if line.startswith("data: "):
                data_str = line[6:]  # Remove "data: " prefix
                try:
                    event_data = json.loads(data_str)
                    step = event_data.get("step")
                    status = event_data.get("status")
                    message = event_data.get("message")
                    log = event_data.get("log")

                    if status == "in_progress":
                        print(f"   ⏳ {message}")
                    elif status == "completed":
                        print(f"   ✅ {message}")
                        if log:
                            print(f"      {log}")
                    elif status == "warning":
                        print(f"   ⚠️  {message}")
                        if log:
                            print(f"      {log}")
                    elif status == "error":
                        print(f"   ❌ Error: {message}")
                    elif step == "done" and status == "success":
                        campaign_data = event_data.get("data", {})
                        campaign_id = campaign_data.get("campaign_id")
                        print(f"\n🎉 SUCCESS!")
                        print(f"   Campaign ID: {campaign_id}")
                        print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
                        print(f"   ICP: {selected_icp.get('name')}")
                        print(f"   Leads: {len(leads)}")
                        print(f"   Email Variants: {len(variants)}")
                        if selected_domains:
                            print(f"   Selected Domains: {', '.join(selected_domains)}")
                except json.JSONDecodeError:
                    pass

    print("\n" + "=" * 80)


if __name__ == "__main__":
    asyncio.run(test_icp_flow())
