import asyncio
import httpx
import json

async def test_campaign_stream():
    """Test the campaign creation stream with SuperSearch"""

    url = "http://localhost:8000/api/create-campaign-stream"
    payload = {
        "url": "example.com",
        "target_audience": "CTOs at Series A SaaS startups in San Francisco",
        "user_id": "demo_user_123"
    }

    print("Testing campaign creation with SuperSearch integration...")
    print(f"Target audience: {payload['target_audience']}\n")

    async with httpx.AsyncClient(timeout=120.0) as client:
        async with client.stream("POST", url, json=payload) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    data = json.loads(line[6:])

                    step = data.get("step", "?")
                    status = data.get("status", "?")
                    message = data.get("message", "")
                    log = data.get("log", "")

                    print(f"[Step {step}] {status}: {message}")
                    if log:
                        print(f"  Log: {log[:200]}")

                    # Show SuperSearch list ID
                    if "supersearch_list_id" in data:
                        print(f"  ✅ SuperSearch List ID: {data['supersearch_list_id']}")

                    # Show final result
                    if step == "done":
                        result_data = data.get("data", {})
                        print(f"\n✅ CAMPAIGN CREATED SUCCESSFULLY!")
                        print(f"  Campaign ID: {result_data.get('campaign_id')}")
                        print(f"  Lead List ID: {result_data.get('lead_list_id')}")
                        print(f"  Variants: {len(result_data.get('variants', []))}")
                        break

                    # Show errors
                    if step == "error":
                        print(f"\n❌ ERROR: {message}")
                        break

asyncio.run(test_campaign_stream())
