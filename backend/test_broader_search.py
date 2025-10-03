import asyncio
import os
from dotenv import load_dotenv
from app.services.instantly import InstantlyService
import json

load_dotenv()

async def test_broader_search():
    """
    Test with progressively broader filters to find what works
    """
    instantly_service = InstantlyService(os.getenv("INSTANTLY_API_KEY"))

    # Test 1: Very specific (what you're using now)
    print("\n" + "="*80)
    print("TEST 1: Current filters (very specific)")
    print("="*80)

    filters_specific = {
        "department": ["IT & IS"],
        "level": ["C-Level"],
        "employee_count": ["25 - 100", "100 - 250"],
        "revenue": ["$1 - 10M", "$10 - 50M"],
        "title": {
            "include": ["CTO", "CEO", "VP Engineering", "Head of Product"],
            "exclude": []
        },
        "company_name": {
            "include": [],
            "exclude": ["sendcupcake.com"]
        },
        "keyword_filter": {
            "include": "SaaS",
            "exclude": ""
        },
        "locations": [
            {
                "city": "San Francisco",
                "state": "California",
                "country": "USA"
            }
        ]
    }

    try:
        result1 = await instantly_service.search_leads_supersearch(
            search_filters=filters_specific,
            limit=10
        )
        print(f"✅ List created: {result1.get('resource_id')}")
        print(f"Response: {json.dumps(result1, indent=2)}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Test 2: Remove revenue filter
    print("\n" + "="*80)
    print("TEST 2: Remove revenue filter")
    print("="*80)

    filters_no_revenue = {
        "department": ["IT & IS"],
        "level": ["C-Level"],
        "employee_count": ["25 - 100", "100 - 250"],
        "title": {
            "include": ["CTO", "CEO", "VP Engineering"],
            "exclude": []
        },
        "keyword_filter": {
            "include": "SaaS, B2B, Software",
            "exclude": ""
        },
        "locations": [
            {
                "city": "San Francisco",
                "state": "California",
                "country": "USA"
            }
        ]
    }

    try:
        result2 = await instantly_service.search_leads_supersearch(
            search_filters=filters_no_revenue,
            limit=10
        )
        print(f"✅ List created: {result2.get('resource_id')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Test 3: Broader - just titles and location
    print("\n" + "="*80)
    print("TEST 3: Just titles + San Francisco (broader)")
    print("="*80)

    filters_broad = {
        "title": {
            "include": ["CTO", "CEO", "Founder"],
            "exclude": []
        },
        "keyword_filter": {
            "include": "SaaS, software, technology",
            "exclude": ""
        },
        "locations": [
            {
                "city": "San Francisco",
                "state": "California",
                "country": "USA"
            }
        ]
    }

    try:
        result3 = await instantly_service.search_leads_supersearch(
            search_filters=filters_broad,
            limit=10
        )
        print(f"✅ List created: {result3.get('resource_id')}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    # Test 4: Very broad - just titles, any location
    print("\n" + "="*80)
    print("TEST 4: Just SaaS founders (no location)")
    print("="*80)

    filters_very_broad = {
        "title": {
            "include": ["Founder", "CEO"],
            "exclude": []
        },
        "keyword_filter": {
            "include": "SaaS",
            "exclude": ""
        },
        "employee_count": ["0 - 25", "25 - 100"]
    }

    try:
        result4 = await instantly_service.search_leads_supersearch(
            search_filters=filters_very_broad,
            limit=10
        )
        print(f"✅ List created: {result4.get('resource_id')}")
        print("\n🎯 This one should definitely find leads!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

    print("\n" + "="*80)
    print("Check Instantly dashboard in 2-5 minutes to see which lists have leads")
    print("="*80)

if __name__ == "__main__":
    asyncio.run(test_broader_search())
