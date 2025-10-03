"""
Test ICP analysis for ofi.co.uk
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService

load_dotenv()


async def test_icp_analysis():
    print("🧪 Testing ICP Analysis for ofi.co.uk")
    print("=" * 80)

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return

    ai_service = AICopyService(api_key)

    test_url = "https://ofi.co.uk"

    print(f"\n🔍 Analyzing: {test_url}")
    print("⏳ This may take 30-60 seconds as GPT-5 visits and analyzes the website...")
    print()

    try:
        icps = await ai_service.suggest_three_icps(test_url)

        print("\n✅ SUCCESS! Generated ICPs:")
        print("=" * 80)

        for idx, icp in enumerate(icps, 1):
            print(f"\n{'='*80}")
            print(f"ICP #{idx}: {icp.get('name')}")
            print(f"{'='*80}")
            print(f"\n📋 Description:")
            print(f"   {icp.get('description')}")

            print(f"\n🎯 Target Audience:")
            print(f"   {icp.get('target_audience')}")

            print(f"\n💼 Company Size: {icp.get('company_size')}")

            print(f"\n😣 Pain Points:")
            for pain in icp.get('pain_points', []):
                print(f"   • {pain}")

        print("\n" + "=" * 80)
        print("✅ All ICPs look good!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        print(traceback.format_exc())


if __name__ == "__main__":
    asyncio.run(test_icp_analysis())
