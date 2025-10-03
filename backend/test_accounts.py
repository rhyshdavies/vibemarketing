#!/usr/bin/env python3
"""
Test fetching accounts from Instantly
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService

load_dotenv()

async def test_get_accounts():
    api_key = os.getenv("INSTANTLY_API_KEY")
    if not api_key:
        print("❌ INSTANTLY_API_KEY not found")
        return

    instantly = InstantlyService(api_key)

    print("="*70)
    print("Testing Get Accounts API")
    print("="*70)

    try:
        print("\n📧 Fetching active accounts...")
        accounts = await instantly.get_accounts(limit=100, status=1)

        print(f"\n{'='*70}")
        print(f"RESULTS:")
        print(f"  Total accounts: {len(accounts)}")
        print(f"{'='*70}")

        if accounts:
            print(f"\n✅ SUCCESS! Found {len(accounts)} active accounts:")
            for i, acc in enumerate(accounts[:10], 1):
                email = acc.get('email', 'N/A')
                name = f"{acc.get('first_name', '')} {acc.get('last_name', '')}".strip()
                warmup = "✓ Warmed" if acc.get('warmup_status') == 1 else "✗ Not warmed"
                print(f"   {i}. {email} - {name} [{warmup}]")
            if len(accounts) > 10:
                print(f"   ... and {len(accounts) - 10} more")

            # Extract unique domains
            domains = list(set(acc.get('email', '').split('@')[1] for acc in accounts if '@' in acc.get('email', '')))
            print(f"\n📊 Unique domains: {len(domains)}")
            for domain in domains[:10]:
                print(f"   • {domain}")
        else:
            print(f"\n⚠️ No accounts returned")

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_get_accounts())
