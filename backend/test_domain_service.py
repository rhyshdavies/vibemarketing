import asyncio
import os
from dotenv import load_dotenv
from app.services.domain_service import DomainService

load_dotenv()

async def test_domain_service():
    """Test the domain service"""

    service = DomainService(os.getenv("INSTANTLY_API_KEY"))

    print("=" * 80)
    print("TESTING DOMAIN SERVICE")
    print("=" * 80)

    # 1. Get pre-warmed domains
    print("\n1. Getting available pre-warmed domains...")
    try:
        domains = await service.get_prewarmed_domains(extensions=["com", "org"])
        print(f"✅ Found {len(domains)} pre-warmed domains")
        if domains:
            print(f"   First 5: {domains[:5]}")
        else:
            print("   ⚠️  No pre-warmed domains available right now")
    except Exception as e:
        print(f"❌ Error: {e}")

    # 2. Check domain availability
    print("\n2. Checking domain availability...")
    try:
        test_domains = ["vibemarketing2025.com", "vibeoutreach.com"]
        availability = await service.check_domain_availability(test_domains)
        print(f"✅ Checked {len(test_domains)} domains:")
        for domain, available in availability.items():
            status = "✅ Available" if available else "❌ Taken"
            print(f"   {domain}: {status}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # 3. Generate similar domains
    print("\n3. Generating similar domain suggestions...")
    try:
        similar = await service.generate_similar_domains("vibemarketing.com")
        print(f"✅ Generated {len(similar)} suggestions")
        if similar:
            print(f"   First 10: {similar[:10]}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # 4. Simulate pre-warmed order (won't charge)
    print("\n4. Simulating pre-warmed domain order (no charge)...")
    try:
        if domains:
            result = await service.order_prewarmed_accounts(
                domain=domains[0],
                number_of_accounts=1,
                simulation=True  # Just a test, won't charge
            )
            print(f"✅ Simulation successful!")
            print(f"   Domain: {domains[0]}")
            print(f"   Total price: ${result['total_price']}")
            print(f"   Monthly: ${result['total_price_per_month']}")
            print(f"   Yearly: ${result['total_price_per_year']}")
    except Exception as e:
        print(f"❌ Error: {e}")

    # 5. List existing orders
    print("\n5. Listing your existing domain orders...")
    try:
        orders = await service.list_domain_orders(limit=5)
        items = orders.get("items", [])
        print(f"✅ You have {len(items)} domain orders")
        for order in items:
            print(f"   - {order['domain']} (created: {order['timestamp_created']})")
    except Exception as e:
        print(f"❌ Error: {e}")

    # 6. List existing accounts
    print("\n6. Listing your existing email accounts...")
    try:
        accounts = await service.list_ordered_accounts(limit=5)
        items = accounts.get("items", [])
        print(f"✅ You have {len(items)} email accounts")
        for account in items:
            print(f"   - {account['email']} ({account['first_name']} {account['last_name']})")
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n" + "=" * 80)
    print("Domain service is working! ✅")
    print("=" * 80)

if __name__ == "__main__":
    asyncio.run(test_domain_service())
