#!/usr/bin/env python3
"""
Test script to verify DFY domains API is working
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.domain_service import DomainService

load_dotenv()

async def test_dfy_domains():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    print("="*70)
    print("Testing DFY Domains API")
    print("="*70)

    domain_service = DomainService(api_key)

    try:
        print("\n📋 Fetching pre-warmed domains...")
        domains = await domain_service.get_prewarmed_domains(
            extensions=["com", "org", "co"]
        )

        print(f"\n{'='*70}")
        print(f"RESULTS:")
        print(f"  Total domains: {len(domains)}")
        print(f"{'='*70}")

        if domains:
            print(f"\n✅ SUCCESS! Found {len(domains)} pre-warmed domains:")
            for i, domain in enumerate(domains[:10], 1):
                print(f"   {i}. {domain}")
            if len(domains) > 10:
                print(f"   ... and {len(domains) - 10} more")
        else:
            print(f"\n⚠️ No domains returned from API")
            print(f"   This might mean:")
            print(f"   - The API endpoint is correct but returns empty list")
            print(f"   - Check the Instantly dashboard DFY page to confirm domains exist")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_dfy_domains())
