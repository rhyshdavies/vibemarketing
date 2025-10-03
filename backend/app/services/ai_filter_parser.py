"""
AI-powered service to parse target audience descriptions into SuperSearch filters
"""
import json
from typing import Dict, Any, List, Optional
from openai import OpenAI


class AIFilterParser:
    """Parse natural language target audience descriptions into structured SuperSearch filters"""

    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    async def parse_audience_to_filters(self, target_audience: str) -> Dict[str, Any]:
        """
        Convert a natural language target audience description into SuperSearch API filters

        Args:
            target_audience: Natural language description (e.g., "SaaS founders in US, 1-10 employees")

        Returns:
            Dictionary of SuperSearch filters
        """

        prompt = f"""Convert this target audience description into SuperSearch API filters.

Target Audience: "{target_audience}"

Return ONLY a JSON object with these possible filters (omit any that don't apply):

{{
  "level": [],  // Options: "C-Level", "VP-Level", "Director-Level", "Manager-Level", "Staff", "Entry level", "Mid-Senior level", "Director", "Associate", "Owner", "Partner", "Intern", "Executive", "Senior", "Lead", "Specialist", "Consultant", "Coordinator"
  "department": [],  // Options: "Engineering", "Finance & Administration", "Human Resources", "IT & IS", "Marketing", "Operations", "Sales", "Support", "Other"
  "employee_count": [],  // Options: "0 - 25", "25 - 100", "100 - 250", "250 - 1000", "1K - 10K", "10K - 50K", "50K - 100K", "> 100K"
  "revenue": [],  // Options: "$0 - 1M", "$1 - 10M", "$10 - 50M", "$50 - 100M", "$100 - 250M", "$250 - 500M", "$500M - 1B", "> $1B"
  "title": {{"include": [], "exclude": []}},  // Job titles to include/exclude (e.g., ["CEO", "Founder"])
  "keyword_filter": {{"include": [], "exclude": []}},  // Keywords for company descriptions (e.g., ["SaaS", "software"])
  "industry": {{"include": [], "exclude": []}},  // Industries (e.g., ["Technology", "Healthcare"])
  "funding_type": [],  // Options: "angel", "seed", "pre_seed", "series_a", "series_b", "series_c", "series_d", "series_e", "series_f", "series_g", "series_h", "series_i", "debt_financing", "convertible_note", "equity_crowdfunding", "product_crowdfunding", "secondary_market", "grant", "corporate_round", "private_equity", "initial_coin_offering", "non_equity_assistance", "post_ipo_equity", "post_ipo_debt", "post_ipo_secondary", "undisclosed"
  "news": [],  // Options: "launches", "expands_offices_to", "hires", "partners_with", "leaves", "receives_financing", "recognized_as", "closes_offices_in", "is_developing", "has_issues_with", "acquires", "is_acquired_by", "goes_public", "files_for_bankruptcy", "reports_earnings", "announces_layoffs", "announces_new_product", "announces_new_feature", "announces_new_partnership", "announces_new_office", "announces_new_funding", "announces_new_executive", "announces_new_board_member", "announces_new_investor", "announces_new_customer", "announces_new_integration", "announces_new_certification"
}}

CRITICAL RULES:
1. Return ONLY the JSON object, no explanations
2. Use EXACT values from the options provided
3. Omit filters that don't apply (don't include empty arrays)
4. For "title", be specific and extract actual job titles
5. For "keyword_filter", extract industry keywords, technologies, or company types
6. For "level", map general terms: "founder" -> "C-Level" & "Owner", "executive" -> "C-Level", "senior" -> "Senior", etc.
7. For "employee_count" and "revenue", map ranges appropriately

Examples:
- "SaaS founders in US, 1-10 employees" -> {{"level": ["C-Level", "Owner"], "employee_count": ["0 - 25"], "keyword_filter": {{"include": ["SaaS"]}}}}
- "CTOs at B2B companies with Series A funding" -> {{"level": ["C-Level"], "title": {{"include": ["CTO"]}}, "funding_type": ["series_a"], "keyword_filter": {{"include": ["B2B"]}}}}
- "HR managers at construction companies, 100-500 employees" -> {{"level": ["Manager-Level"], "department": ["Human Resources"], "employee_count": ["100 - 250", "250 - 1000"], "keyword_filter": {{"include": ["construction"]}}}}
"""

        try:
            # Call OpenAI to parse the audience
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a precise API filter generator. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more consistent output
            )

            content = response.choices[0].message.content.strip()

            # Extract JSON from response
            # Find the first { and last }
            start_idx = content.find('{')
            end_idx = content.rfind('}')

            if start_idx == -1 or end_idx == -1:
                print(f"⚠️ No JSON found in AI response, using default filters")
                return self._get_default_filters()

            json_str = content[start_idx:end_idx + 1]
            filters = json.loads(json_str)

            # Remove empty arrays/objects to keep the API call clean
            filters = self._clean_filters(filters)

            print(f"✅ AI parsed filters from '{target_audience}':")
            print(json.dumps(filters, indent=2))

            return filters

        except Exception as e:
            print(f"❌ Error parsing audience with AI: {str(e)}")
            print(f"Falling back to default filters")
            return self._get_default_filters()

    def _clean_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Remove empty arrays and objects from filters"""
        cleaned = {}

        for key, value in filters.items():
            if isinstance(value, list) and len(value) > 0:
                cleaned[key] = value
            elif isinstance(value, dict):
                # For nested objects like title, keyword_filter, industry
                nested_cleaned = {k: v for k, v in value.items() if v and len(v) > 0}
                if nested_cleaned:
                    cleaned[key] = nested_cleaned
            elif value:  # For other non-empty values
                cleaned[key] = value

        return cleaned

    def _get_default_filters(self) -> Dict[str, Any]:
        """Return default filters when AI parsing fails"""
        return {
            "level": ["C-Level", "VP-Level"],
            "employee_count": ["25 - 100", "100 - 250"]
        }
