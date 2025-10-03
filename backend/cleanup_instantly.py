"""
Clean up Instantly workspace - delete all campaigns and lead lists
"""
import asyncio
import os
import httpx
from dotenv import load_dotenv

load_dotenv()


async def cleanup_instantly():
    api_key = os.getenv('INSTANTLY_API_KEY')
    BASE = 'https://api.instantly.ai/api/v2'
    HDRS = {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json'}

    print("🧹 INSTANTLY WORKSPACE CLEANUP")
    print("=" * 80)

    async with httpx.AsyncClient(timeout=60.0) as client:
        # Delete all campaigns
        print("\n📋 Step 1: Deleting all campaigns...")
        campaigns_res = await client.get(
            f'{BASE}/campaigns',
            headers=HDRS,
            params={'api_key': api_key}
        )

        if campaigns_res.status_code == 200:
            campaigns_data = campaigns_res.json()

            # Handle both array and object responses
            if isinstance(campaigns_data, dict):
                campaigns = campaigns_data.get('items', campaigns_data.get('campaigns', []))
            elif isinstance(campaigns_data, list):
                campaigns = campaigns_data
            else:
                campaigns = []

            print(f"   Found {len(campaigns)} campaigns")

            for i, campaign in enumerate(campaigns, 1):
                # Handle if campaign is string ID or object
                if isinstance(campaign, str):
                    campaign_id = campaign
                    campaign_name = campaign_id
                else:
                    campaign_id = campaign.get('id')
                    campaign_name = campaign.get('name', 'Unnamed')

                print(f"   [{i}/{len(campaigns)}] Pausing and deleting: {campaign_name} ({campaign_id})")

                # First pause the campaign
                pause_res = await client.post(
                    f'{BASE}/campaigns/{campaign_id}/pause',
                    headers=HDRS,
                    json={'api_key': api_key}
                )

                # Then delete (API v2 requires JSON body)
                delete_res = await client.delete(
                    f'{BASE}/campaigns/{campaign_id}',
                    headers=HDRS,
                    json={'api_key': api_key}
                )

                if delete_res.status_code in [200, 204]:
                    print(f"      ✅ Deleted")
                else:
                    print(f"      ❌ Delete failed: {delete_res.status_code} - {delete_res.text[:100]}")

            print(f"\n   ✅ Deleted {len(campaigns)} campaigns")
        else:
            print(f"   ❌ Failed to get campaigns: {campaigns_res.status_code}")

        # Delete all lead lists
        print("\n📋 Step 2: Deleting all lead lists...")

        # Try the lead-lists endpoint
        lists_res = await client.get(
            f'{BASE}/lead-lists',
            headers=HDRS,
            params={'api_key': api_key}
        )

        if lists_res.status_code == 200:
            lists_data = lists_res.json()

            # Handle both array and object responses
            if isinstance(lists_data, dict):
                lists = lists_data.get('items', lists_data.get('lists', []))
            elif isinstance(lists_data, list):
                lists = lists_data
            else:
                lists = []

            print(f"   Found {len(lists)} lead lists")

            for i, lead_list in enumerate(lists, 1):
                # Handle if list is string ID or object
                if isinstance(lead_list, str):
                    list_id = lead_list
                    list_name = list_id
                    leads_count = 0
                else:
                    list_id = lead_list.get('id')
                    list_name = lead_list.get('name', 'Unnamed')
                    leads_count = lead_list.get('leads_count', 0)

                print(f"   [{i}/{len(lists)}] Deleting: {list_name} ({list_id}) - {leads_count} leads")

                delete_res = await client.delete(
                    f'{BASE}/lead-lists/{list_id}',
                    headers=HDRS,
                    json={'api_key': api_key}
                )

                if delete_res.status_code in [200, 204]:
                    print(f"      ✅ Deleted")
                else:
                    print(f"      ❌ Failed: {delete_res.status_code}")

            print(f"\n   ✅ Deleted {len(lists)} lead lists")
        else:
            print(f"   ⚠️ Failed to get lead lists: {lists_res.status_code}")
            print(f"   Response: {lists_res.text[:200]}")

    print("\n" + "=" * 80)
    print("✅ Cleanup complete!")


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will delete ALL campaigns and lead lists!")
    response = input("Type 'yes' to confirm: ")

    if response.lower() == 'yes':
        asyncio.run(cleanup_instantly())
    else:
        print("Cancelled.")
