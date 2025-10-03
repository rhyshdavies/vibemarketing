"""
Final validation - test AI-generated filters with real API
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService
from app.services.instantly import InstantlyService
import json

load_dotenv()


async def test_final_validation():
    """Test AI filter generation with real API calls"""

    openai_key = os.getenv("OPENAI_API_KEY")
    instantly_key = os.getenv("INSTANTLY_API_KEY")

    if not openai_key or not instantly_key:
        print("❌ Missing API keys")
        return

    print("🔑 Final Validation - AI Generated Filters → API\n")

    ai_service = AICopyService(openai_key)
    instantly_service = InstantlyService(instantly_key)

    # Diverse test cases
    test_cases = [
        {
            "name": "1. Tech Founders",
            "target_audience": "Founders at tech startups in San Francisco"
        },
        {
            "name": "2. Marketing VPs - UK",
            "target_audience": "VP of Marketing at SaaS companies in London"
        },
        {
            "name": "3. Healthcare Executives",
            "target_audience": "Healthcare executives in the United States"
        },
        {
            "name": "4. Construction Managers",
            "target_audience": "Senior project managers at construction companies with 100-500 employees"
        },
        {
            "name": "5. Cybersecurity CEOs",
            "target_audience": "CEOs at cybersecurity companies"
        }
    ]

    for i, test in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST {i}: {test['name']}")
        print('='*80)
        print(f"Target Audience: '{test['target_audience']}'")

        try:
            # Generate filters with AI
            print(f"\n⏳ Generating filters with AI...")
            filters = await ai_service.generate_supersearch_filters(
                test['target_audience'],
                "https://example.com"
            )

            print(f"\n✅ AI Generated Filters:")
            print(json.dumps(filters, indent=2))

            # Create enrichment via API
            print(f"\n⏳ Creating enrichment via Instantly API...")
            result = await instantly_service.search_leads_supersearch(
                search_filters=filters,
                limit=3
            )

            resource_id = result.get('resource_id')
            list_name = result.get('list_name')

            print(f"\n✅ Enrichment created successfully!")
            print(f"   Resource ID: {resource_id}")
            print(f"   List Name: {list_name}")

            # Summary of filters used
            print(f"\n📋 Filter Summary:")
            if 'title' in filters and filters['title'].get('include'):
                print(f"   ✓ Title: {', '.join(filters['title']['include'])}")
            if 'level' in filters:
                print(f"   ✓ Level: {', '.join(filters['level'])}")
            if 'locations' in filters:
                loc = filters['locations'][0]
                loc_str = f"{loc.get('city', '')}, {loc.get('state', '')}, {loc.get('country', '')}".strip(', ')
                print(f"   ✓ Location: {loc_str}")
            if 'industry' in filters and filters['industry'].get('include'):
                print(f"   ✓ Industry: {', '.join(filters['industry']['include'])}")
            if 'employee_count' in filters:
                print(f"   ✓ Company Size: {', '.join(filters['employee_count'])}")
            if 'department' in filters:
                print(f"   ✓ Department: {', '.join(filters['department'])}")

            print(f"\n👉 Please check resource {resource_id} in Instantly dashboard")
            print(f"   and let me know if it returns leads!")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print(traceback.format_exc())

    print(f"\n{'='*80}")
    print("All tests completed!")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(test_final_validation())
