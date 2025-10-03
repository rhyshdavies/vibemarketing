"""
Test AI filter generation with various target audience descriptions
"""
import asyncio
import os
from dotenv import load_dotenv
from app.services.ai_copy import AICopyService

load_dotenv()


async def test_filter_generation():
    """Test generating SuperSearch filters from different ICP descriptions"""

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return

    print("🔑 OpenAI API Key found")
    print("\n" + "="*80)
    print("Testing AI Filter Generation")
    print("="*80 + "\n")

    # Initialize service
    ai_service = AICopyService(api_key)

    # Test cases with various ICP descriptions
    test_cases = [
        {
            "name": "SaaS Founders",
            "url": "https://example.com",
            "target_audience": "SaaS founders in the US with 1-10 employees, recently raised seed funding"
        },
        {
            "name": "Construction HR Heads",
            "url": "https://ofi.co.uk",
            "target_audience": "Heads of HR at construction companies in the UK with 100-500 employees"
        },
        {
            "name": "Tech CTOs",
            "url": "https://example.com",
            "target_audience": "CTOs at Series A B2B companies"
        },
        {
            "name": "Marketing VPs",
            "url": "https://example.com",
            "target_audience": "VP of Marketing at enterprise software companies with $10M-$50M revenue"
        },
        {
            "name": "Simple Description",
            "url": "https://example.com",
            "target_audience": "Small business owners"
        }
    ]

    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{'='*80}")
        print(f"TEST CASE {i}: {test_case['name']}")
        print('='*80)
        print(f"Target Audience: {test_case['target_audience']}")
        print(f"\n⏳ Generating filters...")

        try:
            filters = await ai_service.generate_supersearch_filters(
                test_case['target_audience'],
                test_case['url']
            )

            print(f"\n✅ Generated Filters:")
            import json
            print(json.dumps(filters, indent=2))

            # Analyze the filters
            print(f"\n📊 Filter Analysis:")
            if "level" in filters:
                print(f"   - Levels: {', '.join(filters['level'])}")
            if "department" in filters:
                print(f"   - Departments: {', '.join(filters['department'])}")
            if "employee_count" in filters:
                print(f"   - Company Size: {', '.join(filters['employee_count'])}")
            if "revenue" in filters:
                print(f"   - Revenue: {', '.join(filters['revenue'])}")
            if "title" in filters and filters['title'].get('include'):
                print(f"   - Job Titles: {', '.join(filters['title']['include'])}")
            if "keyword_filter" in filters and filters['keyword_filter'].get('include'):
                print(f"   - Keywords: {', '.join(filters['keyword_filter']['include'])}")
            if "industry" in filters and filters['industry'].get('include'):
                print(f"   - Industries: {', '.join(filters['industry']['include'])}")
            if "funding_type" in filters:
                print(f"   - Funding: {', '.join(filters['funding_type'])}")

            if not any(k in filters for k in ["level", "department", "title", "employee_count"]):
                print("   ⚠️  WARNING: No primary filters generated!")

        except Exception as e:
            print(f"\n❌ ERROR: {str(e)}")
            import traceback
            print("\nFull traceback:")
            print(traceback.format_exc())

    print(f"\n{'='*80}")
    print("Testing Complete!")
    print('='*80)


if __name__ == "__main__":
    asyncio.run(test_filter_generation())
