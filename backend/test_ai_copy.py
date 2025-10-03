"""
Test AI copy generation with web search
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService

load_dotenv()

async def test_ai_copy():
    """Test generating email copy with website analysis"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return

    print("🔑 OpenAI API Key found")
    print("\n" + "="*60)
    print("Testing AI Copy Generation with Web Search")
    print("="*60 + "\n")

    # Initialize service
    ai_service = AICopyService(api_key)

    # Test parameters
    url = "https://ofi.co.uk"
    target_audience = "Construction companies in the UK. Heads of HR"

    print(f"📍 URL: {url}")
    print(f"🎯 Target Audience: {target_audience}")
    print("\n" + "-"*60)
    print("Generating email variants (this may take 30-60 seconds)...")
    print("-"*60 + "\n")

    try:
        # Generate email copy
        variants = await ai_service.generate_email_copy(url, target_audience)

        print("\n" + "="*60)
        print(f"✅ SUCCESS! Generated {len(variants)} email variants")
        print("="*60 + "\n")

        # Display each variant
        for i, variant in enumerate(variants, 1):
            print(f"\n{'='*60}")
            print(f"VARIANT {i}")
            print('='*60)
            print(f"\n📧 Subject: {variant.get('subject', 'N/A')}")
            print(f"\n📝 Body:\n{variant.get('body', 'N/A')}")
            print(f"\n{'='*60}\n")

        # Check if these are fallback variants (generic)
        first_body = variants[0].get('body', '')
        if "streamline their workflows" in first_body or "We've helped similar companies" in first_body:
            print("⚠️  WARNING: These appear to be FALLBACK variants (generic templates)")
            print("   The AI web search might not be working properly.")
        else:
            print("✅ These appear to be CUSTOM variants based on website analysis!")
            print("   Look for specific references to the company's actual services.")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        print("\nFull traceback:")
        print(traceback.format_exc())

if __name__ == "__main__":
    asyncio.run(test_ai_copy())
