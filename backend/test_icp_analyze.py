#!/usr/bin/env python3
"""
Quick test script to verify ICP analysis is working
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService

load_dotenv()

async def test_icp_analysis():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return

    print(f"✅ API key found (length: {len(api_key)})")

    ai_service = AICopyService(api_key)

    test_url = "https://instantly.ai"
    print(f"\n🔍 Testing ICP analysis for: {test_url}")
    print("This may take 30-60 seconds with gpt-5 web search...\n")

    try:
        icps = await ai_service.suggest_three_icps(test_url)
        print(f"\n✅ SUCCESS! Got {len(icps)} ICPs:")
        for i, icp in enumerate(icps, 1):
            print(f"\n{i}. {icp.get('name', 'Unknown')}")
            print(f"   Description: {icp.get('description', 'N/A')}")
            print(f"   Target: {icp.get('target_audience', 'N/A')}")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_icp_analysis())
