"""
Simplest possible test - check if enrichment returns ANY results
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json
import time

load_dotenv()


async def test_simple():
    """Test with absolute minimum filters"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Testing Simplest Enrichment\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    # Absolute simplest filter
    payload = {
        "api_key": api_key,
        "search_filters": {
            "level": ["C-Level"]
        },
        "limit": 3,
        "work_email_enrichment": True,
        "fully_enriched_profile": False,
        "skip_rows_without_email": True,
        "list_name": "Simple Test - C-Level Only"
    }

    print("Creating enrichment with ONLY C-Level filter...")
    print(f"Limit: 3 leads\n")

    async with httpx.AsyncClient(timeout=120.0) as client:
        # Create enrichment
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

        print(f"✅ Enrichment created")
        print(f"   Resource ID: {resource_id}")
        print(f"   List ID: {list_id}")

        # Wait and check multiple times
        print(f"\n⏳ Checking status every 3 seconds for 30 seconds...\n")

        for i in range(10):  # Check 10 times over 30 seconds
            await asyncio.sleep(3)

            status_response = await client.get(
                f"{base_url}/supersearch-enrichment/status/{resource_id}",
                headers=headers,
                params={"api_key": api_key}
            )

            if status_response.status_code == 200:
                status = status_response.json()

                print(f"[{(i+1)*3}s] Status check:")
                print(f"   in_progress: {status.get('in_progress', 'unknown')}")
                print(f"   exists: {status.get('exists', 'unknown')}")

                # Check for leads
                if 'leads' in status:
                    leads = status['leads']
                    print(f"   ✅ LEADS FOUND: {len(leads)}")

                    if len(leads) > 0:
                        print("\n📋 Lead Details:")
                        for j, lead in enumerate(leads, 1):
                            print(f"\n   Lead {j}:")
                            print(f"   Name: {lead.get('first_name', '')} {lead.get('last_name', '')}")
                            print(f"   Email: {lead.get('email', 'N/A')}")
                            print(f"   Title: {lead.get('title', 'N/A')}")
                            print(f"   Company: {lead.get('company_name', 'N/A')}")
                            print(f"   Location: {lead.get('location', 'N/A')}")
                        return
                    else:
                        print(f"   ⚠️  Leads array exists but is empty")
                else:
                    print(f"   No 'leads' field yet")

                if not status.get('in_progress', True):
                    print(f"\n✅ Enrichment completed")
                    if 'leads' not in status:
                        print(f"⚠️  But no leads in final response")
                    return
            else:
                print(f"   ❌ Status check failed: {status_response.status_code}")

            print()

        print("\n⏱️  Finished checking - enrichment may still be processing")


if __name__ == "__main__":
    asyncio.run(test_simple())
