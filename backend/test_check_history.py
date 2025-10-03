"""
Check enrichment history to see which searches returned leads
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def check_enrichment_history():
    """Check recent enrichments to see which ones found leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Checking Enrichment History\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Get enrichment history
        response = await client.get(
            f"{base_url}/supersearch-enrichment/history",
            headers=headers,
            params={"api_key": api_key}
        )

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return

        history = response.json()
        print(f"📊 Found {len(history)} enrichment jobs\n")

        # Show recent jobs
        for i, job in enumerate(history[:10], 1):
            resource_id = job.get('resource_id', 'N/A')
            list_name = job.get('list_name', 'N/A')
            status = job.get('status', 'N/A')
            total_leads = job.get('total_leads', 0)

            print(f"\n{'='*80}")
            print(f"Job {i}: {list_name}")
            print('='*80)
            print(f"Resource ID: {resource_id}")
            print(f"Status: {status}")
            print(f"Total Leads: {total_leads}")

            # Get details for this job
            if resource_id != 'N/A':
                detail_response = await client.get(
                    f"{base_url}/supersearch-enrichment/status/{resource_id}",
                    headers=headers,
                    params={"api_key": api_key}
                )

                if detail_response.status_code == 200:
                    details = detail_response.json()

                    if 'leads' in details:
                        leads = details['leads']
                        print(f"\n✅ This job has {len(leads)} leads available")

                        if len(leads) > 0:
                            print("\nFirst lead:")
                            lead = leads[0]
                            print(f"  Name: {lead.get('first_name', '')} {lead.get('last_name', '')}")
                            print(f"  Title: {lead.get('title', 'N/A')}")
                            print(f"  Company: {lead.get('company_name', 'N/A')}")
                            print(f"  Industry: {lead.get('industry', 'N/A')}")
                            print(f"  Location: {lead.get('location', 'N/A')}")
                            print(f"  Company Size: {lead.get('company_size', 'N/A')}")
                    else:
                        print(f"\n⚠️  No leads in status response")
                        print(f"In progress: {details.get('in_progress', 'unknown')}")

if __name__ == "__main__":
    asyncio.run(check_enrichment_history())
