"""
Check lead lists to see completed enrichments and their results
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv
import json

load_dotenv()


async def check_lead_lists():
    """Get all lead lists to see which have leads"""

    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("🔑 Checking Lead Lists\n")

    base_url = "https://api.instantly.ai/api/v2"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Get all lead lists
        response = await client.get(
            f"{base_url}/lead-lists",
            headers=headers,
            params={"api_key": api_key}
        )

        if response.status_code != 200:
            print(f"❌ Failed: {response.text}")
            return

        lists = response.json()

        if isinstance(lists, list):
            print(f"📊 Found {len(lists)} lead lists\n")

            # Show recent lists
            for i, lead_list in enumerate(lists[:20], 1):
                list_id = lead_list.get('id', 'N/A')
                name = lead_list.get('name', 'Unnamed')
                lead_count = lead_list.get('leads_count', lead_list.get('total_leads', 0))

                print(f"{i}. {name}")
                print(f"   ID: {list_id}")
                print(f"   Leads: {lead_count}")

                # If it has leads, try to get one lead to verify
                if lead_count > 0 and i <= 5:  # Check first 5 lists with leads
                    # Try to get leads from this list
                    leads_response = await client.get(
                        f"{base_url}/leads",
                        headers=headers,
                        params={
                            "api_key": api_key,
                            "list_id": list_id,
                            "limit": 1
                        }
                    )

                    if leads_response.status_code == 200:
                        leads_data = leads_response.json()
                        if isinstance(leads_data, list) and len(leads_data) > 0:
                            lead = leads_data[0]
                            print(f"   Sample: {lead.get('first_name', '')} {lead.get('last_name', '')} | {lead.get('company_name', 'N/A')}")
                        elif isinstance(leads_data, dict) and 'leads' in leads_data:
                            lead = leads_data['leads'][0]
                            print(f"   Sample: {lead.get('first_name', '')} {lead.get('last_name', '')} | {lead.get('company_name', 'N/A')}")

                print()
        elif isinstance(lists, dict):
            print("Response:")
            print(json.dumps(lists, indent=2))


if __name__ == "__main__":
    asyncio.run(check_lead_lists())
