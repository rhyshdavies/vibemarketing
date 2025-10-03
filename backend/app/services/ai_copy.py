import httpx
from typing import List, Dict
import json
import os


class AICopyService:
    """
    Service for generating email copy using OpenAI with web search
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.openai.com/v1"

    async def generate_email_copy(self, url: str, target_audience: str) -> List[Dict]:
        """
        Generate multiple email variants for A/B testing using web search to analyze the URL
        Returns: [{"subject": "...", "body": "..."}, ...]
        """

        prompt = f"""Visit {url} using web search to analyze what this product/service does. Then create 3 cold email variants for: {target_audience}

Each email must:
- Have a subject line under 50 characters
- Be 150-200 words
- Open with {{{{firstName}}}} and {{{{company}}}}
- Identify a SPECIFIC pain point for {target_audience}
- Present the product as the solution using website insights
- Include a clear CTA
- Be conversational (NO generic phrases like "streamline workflows")

Variant 1: Pain point → Solution
Variant 2: Benefit/outcome-focused
Variant 3: Question/curiosity approach

CRITICAL: Return ONLY the JSON array below. NO explanations, NO markdown, NO extra text. Start your response with [ and end with ]:

[
  {{
    "subject": "subject line here",
    "body": "email body with {{{{firstName}}}} and {{{{company}}}}"
  }},
  {{
    "subject": "second subject",
    "body": "second email body"
  }},
  {{
    "subject": "third subject",
    "body": "third email body"
  }}
]"""

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Use Responses API for web search
            response = await client.post(
                f"{self.base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "tools": [{"type": "web_search"}],
                    "input": prompt
                }
            )

            if response.status_code != 200:
                # Return fallback variants if API fails
                print(f"OpenAI API error: {response.text}")
                return self._get_fallback_variants(url, target_audience)

            result = response.json()

            # Extract text from Responses API format
            # The response has: output[...] with type "message" containing content[0].text
            output_text = None
            for item in result.get("output", []):
                if item.get("type") == "message":
                    content = item.get("content", [])
                    if content and content[0].get("type") == "output_text":
                        output_text = content[0].get("text")
                        break

            if not output_text:
                print("No text output from Responses API")
                return self._get_fallback_variants(url, target_audience)

            try:
                # Extract JSON from the response (might be wrapped in markdown or text)
                cleaned_text = output_text.strip()

                # Remove markdown code blocks if present
                if "```json" in cleaned_text:
                    start = cleaned_text.find("```json") + 7
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()
                elif "```" in cleaned_text:
                    start = cleaned_text.find("```") + 3
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()

                # Find JSON array in the text - be aggressive about extracting it
                if "[" in cleaned_text and "]" in cleaned_text:
                    json_start = cleaned_text.find("[")
                    json_end = cleaned_text.rfind("]") + 1
                    cleaned_text = cleaned_text[json_start:json_end]

                # Parse JSON response
                variants = json.loads(cleaned_text)
                if isinstance(variants, list) and len(variants) > 0:
                    # Validate that variants have required fields
                    valid_variants = []
                    for v in variants:
                        if isinstance(v, dict) and "subject" in v and "body" in v:
                            valid_variants.append(v)

                    if valid_variants:
                        print(f"✅ Successfully parsed {len(valid_variants)} AI-generated email variants")
                        return valid_variants[:3]  # Return max 3 variants

                print(f"Response not a valid list: {output_text[:200]}")
                return self._get_fallback_variants(url, target_audience)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Failed to parse AI response as JSON: {output_text[:500]}")
                print(f"Error: {str(e)}")
                return self._get_fallback_variants(url, target_audience)

    def _get_fallback_variants(self, url: str, target_audience: str) -> List[Dict]:
        """
        Fallback email variants if AI generation fails
        """
        return [
            {
                "subject": "Quick question about {{company}}",
                "body": f"""Hi {{{{firstName}}}},

I noticed {{{{company}}}} is in the {target_audience} space and thought you might be interested in {url}.

We've helped similar companies streamline their workflows and save time on repetitive tasks.

Would you be open to a quick 15-min chat to see if this could work for {{{{company}}}}?

Best,
[Your Name]"""
            },
            {
                "subject": "Solving a problem for {{company}}",
                "body": f"""Hey {{{{firstName}}}},

Most {target_audience} teams struggle with [specific pain point]. We built {url} specifically to solve this.

Curious if this is something {{{{company}}}} is dealing with?

If so, I'd love to show you how we're helping similar companies save [X hours/dollars] per week.

Worth a quick call?

Cheers,
[Your Name]"""
            },
            {
                "subject": "{{company}} + [Your Product]?",
                "body": f"""{{{{firstName}}}},

I've been following {{{{company}}}}'s work and impressed with what you're building.

We created {url} to help {target_audience} teams like yours scale faster without adding overhead.

Would you be interested in seeing how it works? Happy to do a personalized demo.

Let me know!

Best,
[Your Name]"""
            }
        ]

    async def generate_followup_email(self, original_email: str, context: str) -> str:
        """
        Generate a follow-up email based on the original email
        """
        prompt = f"""
Generate a short follow-up email (50-75 words) for this original cold email:

{original_email}

Context: {context}

The follow-up should:
- Be brief and non-pushy
- Reference the original email subtly
- Have a clear CTA
- Use {{{{firstName}}}} placeholder

Return only the email body, no subject line.
"""

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a cold email expert."},
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 200
                }
            )

            if response.status_code != 200:
                return "Hi {{firstName}},\n\nJust wanted to bump this up in your inbox. Let me know if you're interested in learning more!\n\nBest,\n[Your Name]"

            result = response.json()
            return result["choices"][0]["message"]["content"].strip()

    async def analyze_target_audience(self, url: str) -> str:
        """
        Analyze a URL and suggest target audience characteristics
        """
        prompt = f"""
Analyze this product/service URL: {url}

Based on the URL and what you can infer about the product, suggest:
1. Ideal target audience (job titles, company size, industry)
2. Main pain points this product likely solves
3. Key value propositions to highlight in cold outreach

Keep the response concise (under 150 words).
"""

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 300
                }
            )

            if response.status_code != 200:
                return "Unable to analyze target audience at this time."

            result = response.json()
            return result["choices"][0]["message"]["content"].strip()

    async def generate_supersearch_filters(self, target_audience: str, url: str) -> Dict:
        """
        Use AI to convert ICP description into Instantly SuperSearch filters

        Returns filters in format:
        {
            "locations": [{"city": "...", "state": "...", "country": "..."}],
            "department": ["Engineering", "Marketing"],
            "level": ["C-Level", "VP-Level"],
            "employee_count": ["25 - 100"],
            "revenue": ["$1 - 10M"],
            "title": {"include": ["CEO"], "exclude": []},
            "company_name": {"include": [], "exclude": []},
            "industry": {"include": ["Software"], "exclude": []},
            "keyword_filter": {"include": [], "exclude": []},
            "funding_type": ["seed", "series_a"],
            "news": ["launches", "receives_financing"]
        }
        """

        prompt = f"""Convert this target audience description into SuperSearch API filters.

Target Audience: "{target_audience}"
Product URL: {url} (this is the SENDER's product, NOT a company to search for)

Return ONLY a JSON object with these possible filters (omit any that don't apply):

{{
  "locations": [],  // Array of location objects. Format: [{{"city": "San Francisco", "state": "California", "country": "United States"}}, {{"city": "London", "state": "", "country": "United Kingdom"}}]. Use empty string "" for state if not applicable (e.g., UK cities). ALWAYS include city, state, and country fields.
  "level": [],  // Options: "Entry level", "Mid-Senior level", "Director", "Associate", "Owner", "Executive", "Manager", "Senior", "Chief X Officer (CxO)", "Internship", "Vice President (VP)", "Unpaid / Internship", "Partner"
  "department": [],  // Options: "Engineering", "Finance & Administration", "Human Resources", "IT & IS", "Marketing", "Operations", "Sales", "Support", "Other"
  "employee_count": [],  // Options: "0 - 25", "25 - 100", "100 - 250", "250 - 1000", "1K - 10K", "10K - 50K", "50K - 100K", "> 100K"
  "revenue": [],  // Options: "$0 - 1M", "$1 - 10M", "$10 - 50M", "$50 - 100M", "$100 - 250M", "$250 - 500M", "$500M - 1B", "> $1B"
  "title": {{"include": [], "exclude": []}},  // Job titles as PARTIAL MATCH strings (e.g., ["CEO", "Founder", "Marketing Director"]). Use specific titles when mentioned.
  "keyword_filter": {{"include": [], "exclude": ""}},  // Keywords for company descriptions. include is array, exclude is empty string. Use SPARINGLY - prefer industry/title filters.
  "industry": {{"include": [], "exclude": []}},  // MUST use EXACT industry names from this list: "Agriculture & Mining", "Business Services", "Computers & Electronics", "Consumer Services", "Education", "Energy & Utilities", "Financial Services", "Government", "Healthcare, Pharmaceuticals, & Biotech", "Manufacturing", "Media & Entertainment", "Non-Profit", "Other", "Real Estate & Construction", "Retail", "Software & Internet", "Telecommunications", "Transportation & Storage", "Travel, Recreation, and Leisure", "Wholesale & Distribution"
  "funding_type": [],  // Options: "angel", "seed", "pre_seed", "series_a", "series_b", "series_c", "series_d", "series_e", "debt_financing", "convertible_note", "equity_crowdfunding", "grant", "corporate_round", "private_equity", "post_ipo_equity"
  "news": []  // Options: "launches", "expands_offices_to", "hires", "partners_with", "receives_financing", "recognized_as", "closes_offices_in", "acquires", "is_acquired_by", "goes_public", "reports_earnings", "announces_layoffs", "announces_new_product"
}}

CRITICAL RULES:
1. Return ONLY the JSON object, no explanations
2. Use EXACT values from the options provided
3. Omit filters that don't apply (don't include empty arrays/objects)
4. For "locations", ALWAYS include all 3 fields (city, state, country). Use empty string "" for missing values
5. For "title", extract job titles and use them in include array. These are PARTIAL MATCH. Multiple titles: ["CEO", "Founder"]
6. For "level", use ALONGSIDE title when applicable: "founder" -> "Owner", "executive" -> "Executive", "VP" -> "Vice President (VP)", "CxO/C-suite" -> "Chief X Officer (CxO)", "senior" -> "Senior", "manager" -> "Manager", "director" -> "Director"
7. For "industry", map tech/software/SaaS -> "Software & Internet", cybersecurity -> "Software & Internet", construction -> "Real Estate & Construction", healthcare -> "Healthcare, Pharmaceuticals, & Biotech"
8. For "employee_count", be generous with ranges. "startup" -> ["0 - 25", "25 - 100"], "10-50" -> ["25 - 100"], "100-500" -> ["100 - 250", "250 - 1000"], "enterprise" -> ["1K - 10K", "10K - 50K", "50K - 100K", "> 100K"]
9. For "revenue", "Series A" startups typically -> ["$10 - 50M"], well-funded -> ["$50 - 100M", "$100 - 250M"]
10. For "keyword_filter", use VERY SPARINGLY - only for specific tech/products that don't fit elsewhere. Most things should go to industry/title
11. AVOID using keyword_filter for industries - use the industry filter instead

Examples (based on Instantly AI behavior):
- "CEOs at tech companies" -> {{"title": {{"include": ["CEO"]}}, "industry": {{"include": ["Computers & Electronics", "Software & Internet", "Telecommunications"]}}}}
- "Marketing directors in San Francisco" -> {{"title": {{"include": ["Marketing Director"]}}, "locations": [{{"city": "San Francisco", "state": "California", "country": "United States"}}]}}
- "CTOs at Series A startups in New York with 10-50 employees" -> {{"title": {{"include": ["CTO"]}}, "locations": [{{"city": "New York", "state": "New York", "country": "United States"}}], "employee_count": ["25 - 100"], "revenue": ["$10 - 50M"]}}
- "Founders at cybersecurity companies" -> {{"title": {{"include": ["Founder"]}}, "industry": {{"include": ["Software & Internet"]}}}}
- "CEOs and founders at SaaS companies" -> {{"title": {{"include": ["CEO", "Founder"]}}, "industry": {{"include": ["Software & Internet"]}}}}
- "Senior HR managers at construction companies" -> {{"title": {{"include": ["HR Manager"]}}, "level": ["Senior"], "department": ["Human Resources"], "industry": {{"include": ["Real Estate & Construction"]}}}}
- "VP of Sales at B2B software companies in London with 100-500 employees" -> {{"title": {{"include": ["VP of Sales"]}}, "locations": [{{"city": "London", "state": "", "country": "United Kingdom"}}], "industry": {{"include": ["Software & Internet"]}}, "employee_count": ["100 - 250", "250 - 1000"]}}
- "Chief Technology Officers at enterprise SaaS companies" -> {{"title": {{"include": ["Chief Technology Officer"]}}, "level": ["Chief X Officer (CxO)"], "industry": {{"include": ["Software & Internet"]}}, "employee_count": ["1K - 10K", "10K - 50K", "50K - 100K", "> 100K"]}}
"""

        async with httpx.AsyncClient(timeout=90.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are a B2B lead generation expert. You MUST return ONLY raw JSON with no markdown formatting, no code blocks, no explanations. Just the JSON object starting with { and ending with }."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    "temperature": 0.3,  # Lower temperature for more consistent output
                    "max_tokens": 800
                }
            )

            if response.status_code != 200:
                print(f"OpenAI API error: {response.text}")
                return self._get_default_filters(target_audience)

            result = response.json()
            content = result["choices"][0]["message"]["content"]

            try:
                # Strip markdown code blocks if present
                cleaned_content = content.strip()
                if cleaned_content.startswith("```json"):
                    cleaned_content = cleaned_content[7:]  # Remove ```json
                if cleaned_content.startswith("```"):
                    cleaned_content = cleaned_content[3:]  # Remove ```
                if cleaned_content.endswith("```"):
                    cleaned_content = cleaned_content[:-3]  # Remove ```
                cleaned_content = cleaned_content.strip()

                # Find JSON object in text
                start_idx = cleaned_content.find('{')
                end_idx = cleaned_content.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    cleaned_content = cleaned_content[start_idx:end_idx + 1]

                # Parse JSON response
                filters = json.loads(cleaned_content)

                # Remove empty arrays and objects to keep the API call clean
                filters = self._clean_supersearch_filters(filters)

                print(f"✅ AI parsed filters from '{target_audience}':")
                print(json.dumps(filters, indent=2))

                return filters

            except json.JSONDecodeError as e:
                print(f"Failed to parse AI response as JSON: {content}")
                print(f"Parse error: {str(e)}")
                return self._get_default_filters(target_audience)

    def _clean_supersearch_filters(self, filters: Dict) -> Dict:
        """Remove empty arrays and objects from filters"""

        # Valid industry categories from Instantly API (verified via testing)
        VALID_INDUSTRIES = {
            'Agriculture & Mining',
            'Business Services',
            'Computers & Electronics',
            'Consumer Services',
            'Education',
            'Energy & Utilities',
            'Financial Services',
            'Government',
            'Healthcare, Pharmaceuticals, & Biotech',
            'Manufacturing',
            'Media & Entertainment',
            'Non-Profit',
            'Other',
            'Real Estate & Construction',
            'Retail',
            'Software & Internet',
            'Telecommunications',
            'Transportation & Storage',
            'Travel, Recreation, and Leisure',
            'Wholesale & Distribution'
        }

        cleaned = {}

        for key, value in filters.items():
            # Handle industry filters - only use valid categories
            if key == "industry":
                if isinstance(value, dict) and value.get('include'):
                    # Filter to only valid industries
                    valid_industries = [
                        ind for ind in value['include']
                        if ind in VALID_INDUSTRIES
                    ]
                    invalid_industries = [
                        ind for ind in value['include']
                        if ind not in VALID_INDUSTRIES
                    ]

                    # Add valid industries to filter (don't include empty exclude array)
                    if valid_industries:
                        cleaned['industry'] = {'include': valid_industries}
                        print(f"✅ Using industry filter: {valid_industries}")

                    # Move invalid industries to keyword_filter as fallback
                    if invalid_industries:
                        print(f"⚠️  Unknown industry values {invalid_industries} - moving to keyword_filter")
                        if 'keyword_filter' not in cleaned:
                            cleaned['keyword_filter'] = {'include': [], 'exclude': []}
                        for industry in invalid_industries:
                            if industry.lower() not in cleaned['keyword_filter']['include']:
                                cleaned['keyword_filter']['include'].append(industry.lower())
                continue

            # Handle keyword_filter - exclude must be string, not array
            if key == "keyword_filter":
                if isinstance(value, dict):
                    kw_cleaned = {}
                    if value.get('include') and len(value['include']) > 0:
                        kw_cleaned['include'] = value['include']
                    if 'exclude' in value:
                        # Ensure exclude is empty string, not array
                        kw_cleaned['exclude'] = "" if not value['exclude'] else value['exclude']
                    if kw_cleaned and 'include' in kw_cleaned:
                        cleaned[key] = kw_cleaned
                continue

            if isinstance(value, list) and len(value) > 0:
                cleaned[key] = value
            elif isinstance(value, dict):
                # For nested objects like title, company_name, industry
                # Only include fields that have non-empty values
                nested_cleaned = {}
                for k, v in value.items():
                    if v and (isinstance(v, list) and len(v) > 0):
                        nested_cleaned[k] = v
                    elif v and not isinstance(v, list):
                        nested_cleaned[k] = v
                if nested_cleaned:
                    cleaned[key] = nested_cleaned
            elif value:  # For other non-empty values
                cleaned[key] = value

        return cleaned

    def _get_default_filters(self, target_audience: str) -> Dict:
        """
        Fallback filters based on simple keyword matching
        """
        filters = {
            "department": [],
            "level": [],
            "employee_count": [],
            "revenue": [],
            "title": {"include": [], "exclude": []},
            "company_name": {"include": [], "exclude": []},
            "keyword_filter": {"include": "", "exclude": ""},
            "locations": []
        }

        # Simple keyword matching
        audience_lower = target_audience.lower()

        # Level detection
        if any(word in audience_lower for word in ["ceo", "founder", "c-level", "chief"]):
            filters["level"].append("C-Level")
        if "vp" in audience_lower or "vice president" in audience_lower:
            filters["level"].append("VP-Level")
        if "director" in audience_lower:
            filters["level"].append("Director-Level")

        # Department detection
        if any(word in audience_lower for word in ["engineer", "cto", "technical", "developer"]):
            filters["department"].append("Engineering")
        if any(word in audience_lower for word in ["market", "cmo", "growth"]):
            filters["department"].append("Marketing")
        if any(word in audience_lower for word in ["sales", "revenue"]):
            filters["department"].append("Sales")

        # Company size
        if "startup" in audience_lower or "small" in audience_lower:
            filters["employee_count"] = ["0 - 25", "25 - 100"]
        elif "enterprise" in audience_lower or "large" in audience_lower:
            filters["employee_count"] = ["1K - 10K", "10K - 50K", "> 100K"]

        return filters

    async def suggest_three_icps(self, url: str) -> List[Dict]:
        """
        Analyze a website and suggest 10 Ideal Customer Profiles (ICPs)

        Returns: [
            {
                "name": "ICP Name",
                "description": "Brief description",
                "target_audience": "Format for supersearch filters",
                "pain_points": ["pain1", "pain2"],
                "company_size": "startup/mid-market/enterprise"
            },
            ...
        ]
        """

        prompt = f"""First, visit and thoroughly analyze this website: {url}

Read the homepage, about page, and product/services pages to understand:
- What product or service they offer
- Who their target customers are
- What problems they solve
- What industry they operate in

Then, based on ONLY what you learned from visiting {url}, suggest 10 different Ideal Customer Profiles (ICPs) that would benefit most from purchasing this company's products or services.

For each ICP, provide:
1. A short name (2-4 words, e.g., "SaaS Founders", "Enterprise CTOs")
2. A brief description (1-2 sentences) explaining who they are and why they would buy from {url}
3. Target audience in format suitable for lead search (include job title, company size, industry)
4. 2-3 specific pain points this ICP faces that {url} can solve
5. Company size category: "startup" (0-100 employees), "mid-market" (100-1000), or "enterprise" (1000+)

IMPORTANT: Base your ICPs ONLY on what you learned from visiting {url}. Do not make assumptions or use generic ICPs.

Return ONLY a JSON array with 10 ICPs. NO explanations, NO markdown, NO extra text:

[
  {{
    "name": "ICP Name Here",
    "description": "Who they are and why they would buy from this company",
    "target_audience": "Specific job titles at specific company types (e.g., 'Procurement Directors at mid-market food manufacturers with 100-500 employees')",
    "pain_points": ["First pain point this company solves", "Second pain point", "Third pain point"],
    "company_size": "mid-market"
  }},
  ...
]"""

        # Use gpt-5 for web search with low reasoning effort (per OpenAI docs)
        # Note: gpt-5 reasoning models can take 30-60+ seconds even with low effort
        async with httpx.AsyncClient(timeout=300.0) as client:
            print(f"🔍 Analyzing {url} with gpt-5 web search (low reasoning)...")
            print(f"⏱️  Note: This may take 30-60 seconds...")
            response = await client.post(
                f"{self.base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "gpt-5",
                    "reasoning": {"effort": "low"},
                    "tools": [{"type": "web_search"}],
                    "input": prompt
                }
            )

            print(f"✅ Response received with status: {response.status_code}")

            if response.status_code != 200:
                error_text = response.text
                print(f"❌ OpenAI API error (status {response.status_code}): {error_text}")
                print(f"Request URL: {url}")
                return self._get_fallback_icps(url)

            result = response.json()
            print(f"✅ OpenAI API response received (status 200)")
            print(f"Response keys: {list(result.keys())}")

            # Extract text from Responses API format
            output_text = None
            for item in result.get("output", []):
                if item.get("type") == "message":
                    content = item.get("content", [])
                    if content and content[0].get("type") == "output_text":
                        output_text = content[0].get("text")
                        break

            if not output_text:
                print("❌ No text output from Responses API")
                print(f"Full response structure: {json.dumps(result, indent=2)[:500]}")
                return self._get_fallback_icps(url)

            try:
                # Extract JSON from the response
                cleaned_text = output_text.strip()

                # Remove markdown code blocks if present
                if "```json" in cleaned_text:
                    start = cleaned_text.find("```json") + 7
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()
                elif "```" in cleaned_text:
                    start = cleaned_text.find("```") + 3
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()

                # Find JSON array in the text
                if "[" in cleaned_text and "]" in cleaned_text:
                    json_start = cleaned_text.find("[")
                    json_end = cleaned_text.rfind("]") + 1
                    cleaned_text = cleaned_text[json_start:json_end]

                # Parse JSON response
                icps = json.loads(cleaned_text)
                if isinstance(icps, list) and len(icps) > 0:
                    print(f"✅ Successfully parsed {len(icps)} ICP suggestions from {url}")
                    print(f"   ICPs: {', '.join([icp.get('name', '') for icp in icps])}")
                    return icps[:10]  # Return max 10 ICPs

                print(f"Response not a valid list: {output_text[:200]}")
                return self._get_fallback_icps(url)
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Failed to parse AI response as JSON: {output_text[:500]}")
                print(f"Error: {str(e)}")
                return self._get_fallback_icps(url)

    def _get_fallback_icps(self, url: str) -> List[Dict]:
        """Fallback ICPs if AI generation fails"""
        return [
            {
                "name": "Tech Startup Founders",
                "description": "Founders and CEOs at early-stage tech companies looking to scale efficiently",
                "target_audience": "Founders and CEOs at seed to Series B startups with 10-100 employees",
                "pain_points": [
                    "Limited resources to execute growth strategies",
                    "Need to move fast but lack specialized tools",
                    "Difficulty scaling operations efficiently"
                ],
                "company_size": "startup"
            },
            {
                "name": "Marketing Directors",
                "description": "Marketing leaders at growing companies seeking better campaign performance",
                "target_audience": "Marketing Directors and VPs at mid-market companies with 100-500 employees",
                "pain_points": [
                    "Struggle to generate quality leads consistently",
                    "Time-consuming manual campaign management",
                    "Difficulty measuring ROI accurately"
                ],
                "company_size": "mid-market"
            },
            {
                "name": "Enterprise Sales Leaders",
                "description": "Sales VPs and executives at large organizations optimizing outbound efforts",
                "target_audience": "VPs of Sales and Chief Revenue Officers at enterprise companies with 1000+ employees",
                "pain_points": [
                    "Low response rates from cold outreach",
                    "Inefficient lead qualification process",
                    "Challenges coordinating large sales teams"
                ],
                "company_size": "enterprise"
            }
        ]

    async def match_dfy_domains_to_business(self, url: str, available_domains: List[str]) -> List[Dict]:
        """
        Use AI to match and rank available DFY domains based on how well they fit the business

        Args:
            url: The client's business website
            available_domains: List of available DFY domain names

        Returns: [
            {
                "domain": "example.com",
                "score": 95,
                "reasoning": "Why this domain is a good fit",
                "suggested_use": "How to use this domain"
            },
            ...
        ]
        """

        if not available_domains:
            return []

        prompt = f"""Analyze this website using web search: {url}

Available pre-warmed email domains: {', '.join(available_domains[:20])}

Based on the business and its language/tone, rank the TOP 5 best-fitting domains for cold email outreach.

Consider:
- Domain names that sound professional and trustworthy
- Names that could relate to the industry/business
- Generic business-friendly names
- Avoid domains that sound spammy or unrelated

Return ONLY a JSON array of the top 5 domains with scores and reasoning:

[
  {{
    "domain": "domain-name.com",
    "score": 95,
    "reasoning": "Why this domain fits well (1 sentence)",
    "suggested_use": "What type of sender persona to use (e.g., 'Business Development', 'Partnerships')"
  }},
  ...
]

NO explanations, NO markdown, NO extra text. Just the JSON array."""

        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                f"{self.base_url}/responses",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "tools": [{"type": "web_search"}],
                    "input": prompt
                }
            )

            if response.status_code != 200:
                print(f"OpenAI API error: {response.text}")
                # Return top 5 domains without ranking
                return [
                    {
                        "domain": domain,
                        "score": 70,
                        "reasoning": "Pre-warmed domain ready for outreach",
                        "suggested_use": "General Business Outreach"
                    }
                    for domain in available_domains[:5]
                ]

            result = response.json()

            # Extract text from Responses API format
            output_text = None
            for item in result.get("output", []):
                if item.get("type") == "message":
                    content = item.get("content", [])
                    if content and content[0].get("type") == "output_text":
                        output_text = content[0].get("text")
                        break

            if not output_text:
                print("No text output from Responses API")
                return [
                    {
                        "domain": domain,
                        "score": 70,
                        "reasoning": "Pre-warmed domain ready for outreach",
                        "suggested_use": "General Business Outreach"
                    }
                    for domain in available_domains[:5]
                ]

            try:
                # Extract JSON from the response
                cleaned_text = output_text.strip()

                # Remove markdown code blocks if present
                if "```json" in cleaned_text:
                    start = cleaned_text.find("```json") + 7
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()
                elif "```" in cleaned_text:
                    start = cleaned_text.find("```") + 3
                    end = cleaned_text.find("```", start)
                    cleaned_text = cleaned_text[start:end].strip()

                # Find JSON array in the text
                if "[" in cleaned_text and "]" in cleaned_text:
                    json_start = cleaned_text.find("[")
                    json_end = cleaned_text.rfind("]") + 1
                    cleaned_text = cleaned_text[json_start:json_end]

                # Parse JSON response
                ranked_domains = json.loads(cleaned_text)
                if isinstance(ranked_domains, list) and len(ranked_domains) > 0:
                    print(f"✅ Successfully ranked {len(ranked_domains)} DFY domains")
                    return ranked_domains[:5]  # Return top 5

                print(f"Response not a valid list: {output_text[:200]}")
                return [
                    {
                        "domain": domain,
                        "score": 70,
                        "reasoning": "Pre-warmed domain ready for outreach",
                        "suggested_use": "General Business Outreach"
                    }
                    for domain in available_domains[:5]
                ]
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Failed to parse AI response as JSON: {output_text[:500]}")
                print(f"Error: {str(e)}")
                return [
                    {
                        "domain": domain,
                        "score": 70,
                        "reasoning": "Pre-warmed domain ready for outreach",
                        "suggested_use": "General Business Outreach"
                    }
                    for domain in available_domains[:5]
                ]
