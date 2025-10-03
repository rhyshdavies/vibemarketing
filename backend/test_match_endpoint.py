#!/usr/bin/env python3
"""
Test the match-domains endpoint directly
"""
import asyncio
import httpx
import json

async def test_endpoint():
    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(
            "http://localhost:8000/api/icp/match-domains",
            json={"url": "instantly.ai"}
        )

        print(f"Status: {response.status_code}")
        data = response.json()

        print(f"\nResponse keys: {list(data.keys())}")
        print(f"\nmatched_domains: {len(data.get('matched_domains', []))}")
        print(f"existing_accounts: {len(data.get('existing_accounts', []))}")
        print(f"existing_account_domains: {len(data.get('existing_account_domains', []))}")

        if data.get('existing_accounts'):
            print(f"\nFirst 3 accounts:")
            for acc in data['existing_accounts'][:3]:
                print(f"  - {acc['email']} ({acc['first_name']} {acc['last_name']})")

asyncio.run(test_endpoint())
