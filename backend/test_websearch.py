import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
import json

load_dotenv()

async def test_email_generation():
    """Test email generation with web search"""

    print("Testing email generation with web search...")
    print("=" * 80)

    ai_service = AICopyService(os.getenv("OPENAI_API_KEY"))

    url = "https://sendcupcake.com"
    target_audience = "SaaS founders in software"

    print(f"URL: {url}")
    print(f"ICP: {target_audience}")
    print("-" * 80)

    variants = await ai_service.generate_email_copy(url, target_audience)

    print(f"\n✅ Generated {len(variants)} email variants:")
    for i, variant in enumerate(variants, 1):
        print(f"\n--- Variant {i} ---")
        print(f"Subject: {variant['subject']}")
        print(f"Body:\n{variant['body']}")

if __name__ == "__main__":
    asyncio.run(test_email_generation())
