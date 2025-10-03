import asyncio
import httpx
import json

async def test_fetch_enriched_leads():
    """
    Test fetching enriched leads from the SuperSearch list created in the last test
    List ID: 5c01a50d-5004-4184-a076-39f2c49b6dd5
    """

    # The list ID from the successful campaign creation
    list_id = "5c01a50d-5004-4184-a076-39f2c49b6dd5"

    print(f"\n{'='*80}")
    print(f"Testing /api/leads/{list_id}")
    print(f"{'='*80}\n")

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.get(f"http://localhost:8000/api/leads/{list_id}")

            print(f"Status Code: {response.status_code}")
            print(f"\nResponse:")
            print(json.dumps(response.json(), indent=2))

            data = response.json()

            if data.get("success"):
                print(f"\n✅ SUCCESS: Found {data.get('lead_count')} enriched leads")
                print(f"\nFirst 3 leads:")
                for i, lead in enumerate(data.get("leads", [])[:3], 1):
                    print(f"\nLead {i}:")
                    print(f"  Email: {lead.get('email', 'N/A')}")
                    print(f"  Name: {lead.get('first_name', '')} {lead.get('last_name', '')}")
                    print(f"  Company: {lead.get('company_name', 'N/A')}")
                    print(f"  Title: {lead.get('title', 'N/A')}")
            else:
                print(f"\n⏳ {data.get('message')}")
                print(f"\nEnrichment Status:")
                print(json.dumps(data.get("enrichment_status", {}), indent=2))

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_fetch_enriched_leads())
