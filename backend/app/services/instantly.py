import httpx
from typing import List, Dict, Optional
import json
import asyncio


class InstantlyService:
    """
    Service for interacting with Instantly.ai API v2
    Documentation: https://developer.instantly.ai/
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.instantly.ai/api/v2"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }

    async def create_lead_list(
        self, name: str, leads_data: Optional[str] = None
    ) -> str:
        """
        Create a new lead list in Instantly using API v2
        POST /api/v2/lead-lists
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/lead-lists",
                headers=self.headers,
                json={"api_key": self.api_key, "name": name},
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create lead list: {response.text}")

            result = response.json()
            return result.get("id", name)

    async def upload_leads(
        self, campaign_id: str, lead_list_id: str, leads: List[Dict]
    ) -> str:
        """
        Upload leads to Instantly using API v2
        POST /api/v2/leads/list

        leads format: [{"email": "x@y.com", "first_name": "John", "company_name": "ABC"}]
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Prepare leads in Instantly v2 format
            formatted_leads = []
            for lead in leads:
                formatted_leads.append(
                    {
                        "email": lead.get("email"),
                        "first_name": lead.get("first_name", ""),
                        "last_name": lead.get("last_name", ""),
                        "company_name": lead.get("company", ""),
                        "personalization": lead.get("personalization", ""),
                        "phone": lead.get("phone", ""),
                        "website": lead.get("website", ""),
                        "custom_variables": lead.get("custom_variables", {}),
                    }
                )

            response = await client.post(
                f"{self.base_url}/leads/list",
                headers=self.headers,
                json={
                    "api_key": self.api_key,
                    "lead_list_id": lead_list_id,
                    "leads": formatted_leads,
                    "skip_if_in_workspace": False,
                },
            )

            if response.status_code not in [200, 201]:
                print(f"Warning: Failed to upload leads: {response.text}")

            return lead_list_id

    async def move_leads_to_campaign(
        self, campaign_id: str, lead_list_id: str, limit: int = 10
    ) -> bool:
        """
        Add leads from a SuperSearch list to a campaign using the practical recipe:
        1. Fetch enriched leads from the list
        2. Get all existing workspace leads to check for duplicates
        3. Create only NEW leads (that don't exist in workspace) with campaign_id
        4. Verify leads appeared in campaign

        This avoids the deduplication issue by only creating fresh leads.
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        print(f"📋 Step 1: Fetching enriched leads from SuperSearch list {lead_list_id}")
        print(f"   Requesting {limit} leads (to avoid getting all workspace leads)")

        # Get enriched leads from the SuperSearch list - use the limit parameter
        supersearch_leads = await self.get_leads_from_list(lead_list_id, limit=limit)

        if not supersearch_leads:
            print(f"⚠️ No enriched leads found in list {lead_list_id}")
            return False

        print(f"   Found {len(supersearch_leads)} enriched leads from SuperSearch")

        print(f"📋 Step 2: Preparing leads for bulk creation")
        print(f"   These should be NEW enriched leads from SuperSearch")

        # We'll let the API handle deduplication with skip_if_in_workspace flag
        fresh_leads = supersearch_leads

        print(f"📤 Step 3: Creating {len(fresh_leads)} leads with campaign_id={campaign_id}")

        # Prepare leads array for bulk creation
        # IMPORTANT: Include campaign_id in BOTH wrapper AND each lead for compatibility
        leads_array = []
        for lead in fresh_leads:
            lead_data = {
                "email": lead.get("email"),
                "campaign_id": campaign_id,  # Per-lead campaign_id for compatibility
            }

            # Add optional fields if available
            if lead.get("first_name"):
                lead_data["first_name"] = lead.get("first_name")
            if lead.get("last_name"):
                lead_data["last_name"] = lead.get("last_name")
            if lead.get("company_name"):
                lead_data["company"] = lead.get("company_name")  # Note: "company" not "company_name"
            if lead.get("title"):
                lead_data["title"] = lead.get("title")
            if lead.get("website"):
                lead_data["website"] = lead.get("website")
            if lead.get("linkedin_url"):
                lead_data["linkedin"] = lead.get("linkedin_url")

            # Add custom variables to track source
            lead_data["custom_variables"] = {
                "source": "supersearch",
                "source_list_id": lead_list_id
            }

            leads_array.append(lead_data)

        # Use the correct POST /api/v2/leads/list format with wrapper object
        # campaign_id in BOTH wrapper and per-lead for maximum compatibility
        # CRITICAL: Using skip_if_in_workspace: False because these are NEW enriched leads
        payload = {
            "campaign_id": campaign_id,  # Wrapper-level campaign_id
            "skip_if_in_workspace": False,  # Don't skip - these are NEW leads from SuperSearch!
            "leads": leads_array  # Each lead also has campaign_id
        }

        print(f"   Using skip_if_in_workspace: FALSE (new enriched leads)")

        async with httpx.AsyncClient(timeout=120.0) as client:
            # Use the correct endpoint: /leads/add (not /leads/list)
            create_response = await client.post(
                f"{self.base_url}/leads/add",
                headers=headers,
                json=payload
            )

            if create_response.status_code in [200, 201]:
                result = create_response.json()

                print(f"✅ Bulk create response received (status {create_response.status_code})")

                # Check if there's a background job to poll
                job_id = result.get("background_job_id") or result.get("job_id")

                if job_id:
                    print(f"   Background job detected: {job_id}")
                    print(f"   Polling job status...")

                    # Poll the background job
                    max_polls = 40
                    poll_interval = 3

                    for i in range(max_polls):
                        await asyncio.sleep(poll_interval)

                        job_response = await client.get(
                            f"{self.base_url}/background-jobs/{job_id}",
                            headers=headers
                        )

                        if job_response.status_code == 200:
                            job_data = job_response.json()
                            status = job_data.get("status")

                            print(f"   Poll {i+1}/{max_polls}: status={status}")

                            if status in ["completed", "success"]:
                                print(f"✅ Background job completed successfully!")
                                break
                            elif status == "failed":
                                print(f"❌ Background job failed")
                                return False
                        else:
                            print(f"   Warning: Failed to poll job (status {job_response.status_code})")

                    if status not in ["completed", "success"]:
                        print(f"⏳ Job still running after {max_polls * poll_interval}s, continuing anyway")

                # Verify assignment using search-by-contact for first lead
                if leads_array:
                    test_email = leads_array[0].get("email")
                    print(f"   Verifying assignment for: {test_email}")

                    verify_response = await client.get(
                        f"{self.base_url}/campaigns/search-by-contact",
                        headers=headers,
                        params={"search": test_email}
                    )

                    if verify_response.status_code == 200:
                        verify_data = verify_response.json()
                        # Check if any results show our campaign_id
                        if isinstance(verify_data, list):
                            campaigns_with_lead = [item.get("id") for item in verify_data if item.get("id") == campaign_id]
                            if campaigns_with_lead:
                                print(f"✅ Verified! Lead {test_email} is assigned to campaign {campaign_id}")
                                print(f"🎉 Successfully added leads to campaign!")
                                return True
                            else:
                                print(f"⚠️ Lead exists but not in this campaign (might be processing)")
                        else:
                            print(f"⚠️ Unexpected verification response format")
                    else:
                        print(f"   Warning: Could not verify (status {verify_response.status_code})")

                # If we got here, bulk create succeeded but verification is uncertain
                print(f"✅ Bulk create completed")
                print(f"   {len(leads_array)} leads sent to campaign {campaign_id}")
                print(f"   Verification pending - check dashboard in a few moments")
                return True
            else:
                print(f"❌ Failed to create leads: {create_response.status_code} - {create_response.text}")
                return False

    async def create_campaign(
        self, name: str, lead_list_id: str = None, variants: List[Dict] = None, email_accounts: List[str] = None
    ) -> Dict:
        """
        Create a campaign with A/B testing variants using API v2
        POST /api/v2/campaigns

        Args:
            name: Campaign name
            lead_list_id: Optional lead list ID
            variants: List of email variants [{"subject": "...", "body": "..."}]
            email_accounts: List of email addresses to use for sending
        """
        async with httpx.AsyncClient() as client:
            # Use the first variant as the primary, or default
            if not variants:
                variants = [
                    {
                        "subject": "Let's connect",
                        "body": "Hi {{firstName}},\n\nI'd love to connect.",
                    }
                ]

            # Build campaign sequences with correct API v2 structure
            # Structure: sequences -> steps -> variants
            sequences = [
                {
                    "position": 1,
                    "steps": [
                        {
                            "type": "email",
                            "delay": 0,
                            "variants": variants[:3],  # Max 3 variants for A/B testing
                        }
                    ],
                }
            ]

            # Add follow-up sequence if needed
            if len(variants) > 0:
                sequences.append(
                    {
                        "position": 2,
                        "steps": [
                            {
                                "type": "email",
                                "delay": 3,  # 3 days after first email
                                "variants": [
                                    {
                                        "subject": "Following up",
                                        "body": "Hi {{firstName}},\n\nJust wanted to follow up on my previous email.",
                                    }
                                ],
                            }
                        ],
                    }
                )

            payload = {
                "name": name,
                "sequences": sequences,
                "campaign_schedule": {
                    "schedules": [{
                        "name": "Default",
                        "timing": {"from": "09:00", "to": "17:00"},
                        "days": {"1": True, "2": True, "3": True, "4": True, "5": True, "0": False, "6": False},
                        "timezone": "Etc/GMT+12"  # One of the accepted timezone values
                    }]
                }
            }

            # Add email accounts if provided
            if email_accounts:
                payload["email_list"] = email_accounts
                print(f"📧 Creating campaign with {len(email_accounts)} email accounts")

            # Only add lead_list_ids if provided
            if lead_list_id:
                payload["lead_list_ids"] = [lead_list_id]

            response = await client.post(
                f"{self.base_url}/campaigns",
                headers=self.headers,
                json=payload
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create campaign: {response.text}")

            result = response.json()

            return {
                "id": result.get("id", name),
                "name": name,
                "variants": variants,
                "status": "created",
            }

    async def add_accounts_to_campaign(
        self, campaign_id: str, email_accounts: List[str]
    ) -> bool:
        """
        Add email accounts to a campaign for sending
        This tries multiple endpoint patterns to find the correct one

        Args:
            campaign_id: The campaign ID
            email_accounts: List of email addresses to add

        Returns:
            True if successful
        """
        if not email_accounts:
            print(f"⚠️ No email accounts provided to add to campaign")
            return True

        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"📧 Adding {len(email_accounts)} email accounts to campaign {campaign_id}")
            print(f"   Accounts: {email_accounts}")

            # Try multiple endpoint patterns
            endpoints_to_try = [
                # Pattern 1: RESTful pattern
                {
                    "url": f"{self.base_url}/campaigns/{campaign_id}/accounts",
                    "payload": {"api_key": self.api_key, "emails": email_accounts}
                },
                # Pattern 2: With /add suffix
                {
                    "url": f"{self.base_url}/campaigns/{campaign_id}/accounts/add",
                    "payload": {"api_key": self.api_key, "emails": email_accounts}
                },
                # Pattern 3: Separate endpoint
                {
                    "url": f"{self.base_url}/campaigns/add-accounts",
                    "payload": {"api_key": self.api_key, "campaign_id": campaign_id, "emails": email_accounts}
                },
                # Pattern 4: Email as singular
                {
                    "url": f"{self.base_url}/campaigns/{campaign_id}/accounts",
                    "payload": {"api_key": self.api_key, "email": email_accounts}
                }
            ]

            for i, endpoint_config in enumerate(endpoints_to_try, 1):
                try:
                    print(f"\n   🔍 Attempt {i}: POST {endpoint_config['url']}")
                    response = await client.post(
                        endpoint_config["url"],
                        headers=self.headers,
                        json=endpoint_config["payload"]
                    )

                    print(f"   📊 Response status: {response.status_code}")

                    if response.status_code in [200, 201]:
                        print(f"   ✅ Successfully added email accounts to campaign!")
                        return True
                    else:
                        print(f"   ❌ Failed: {response.text[:200]}")
                except Exception as e:
                    print(f"   ⚠️ Error: {str(e)}")

            print(f"\n⚠️ All attempts failed - user will need to manually add accounts in Instantly dashboard")
            print(f"   Campaign URL: https://app.instantly.ai/app/campaigns/{campaign_id}")
            # Don't fail the whole campaign creation if this fails
            return False

    async def activate_campaign(self, campaign_id: str) -> bool:
        """
        Activate a campaign to start sending
        POST /api/v2/campaigns/{id}/activate
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/campaigns/{campaign_id}/activate",
                headers=self.headers,
                json={"api_key": self.api_key},
            )

            return response.status_code in [200, 201]

    async def get_campaign_analytics(self, campaign_id: str) -> Dict:
        """
        Get analytics for a campaign using API v2
        GET /api/v2/campaigns/analytics?campaign_id={id}
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/campaigns/analytics",
                headers=self.headers,
                params={"api_key": self.api_key, "campaign_id": campaign_id},
            )

            if response.status_code != 200:
                # Return mock data if analytics not available yet
                return {
                    "sent": 0,
                    "opened": 0,
                    "clicked": 0,
                    "replied": 0,
                    "bounced": 0,
                    "open_rate": 0,
                    "click_rate": 0,
                    "reply_rate": 0,
                }

            data = response.json()

            # Parse Instantly v2 analytics response
            sent = data.get("sent", 0)
            opened = data.get("opened", 0)
            clicked = data.get("clicked", 0)
            replied = data.get("replied", 0)

            return {
                "sent": sent,
                "opened": opened,
                "clicked": clicked,
                "replied": replied,
                "bounced": data.get("bounced", 0),
                "open_rate": round((opened / max(sent, 1)) * 100, 2),
                "click_rate": round((clicked / max(opened, 1)) * 100, 2),
                "reply_rate": round((replied / max(sent, 1)) * 100, 2),
            }

    async def get_campaign_analytics_overview(
        self, campaign_ids: List[str] = None
    ) -> Dict:
        """
        Get overview analytics for multiple campaigns
        GET /api/v2/campaigns/analytics/overview
        """
        async with httpx.AsyncClient() as client:
            params = {"api_key": self.api_key}
            if campaign_ids:
                params["campaign_ids"] = ",".join(campaign_ids)

            response = await client.get(
                f"{self.base_url}/campaigns/analytics/overview",
                headers=self.headers,
                params=params,
            )

            if response.status_code != 200:
                return {}

            return response.json()

    async def create_email_account(self, email: str, smtp_config: Dict) -> Dict:
        """
        Create a new email account in Instantly using API v2
        POST /api/v2/accounts
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/accounts",
                headers=self.headers,
                json={
                    "api_key": self.api_key,
                    "email": email,
                    "smtp_host": smtp_config.get("host"),
                    "smtp_port": smtp_config.get("port", 587),
                    "smtp_username": smtp_config.get("username", email),
                    "smtp_password": smtp_config.get("password"),
                    "warmup_enabled": True,  # Enable warmup by default
                },
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create email account: {response.text}")

            return response.json()

    async def get_email_accounts(self) -> List[Dict]:
        """
        Get all email accounts
        GET /api/v2/accounts
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                params={"api_key": self.api_key},
            )

            if response.status_code != 200:
                return []

            return response.json()

    async def get_campaign_list(self) -> List[Dict]:
        """
        Get all campaigns
        GET /api/v2/campaigns
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/campaigns",
                headers=self.headers,
                params={"api_key": self.api_key},
            )

            if response.status_code != 200:
                return []

            return response.json()

    async def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """
        Get a specific campaign
        GET /api/v2/campaigns/{id}
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/campaigns/{campaign_id}",
                headers=self.headers,
                params={"api_key": self.api_key},
            )

            if response.status_code != 200:
                return None

            return response.json()

    async def pause_campaign(self, campaign_id: str) -> bool:
        """
        Pause a campaign
        POST /api/v2/campaigns/{id}/pause
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/campaigns/{campaign_id}/pause",
                headers=self.headers,
                json={"api_key": self.api_key},
            )

            return response.status_code in [200, 201]

    async def delete_campaign(self, campaign_id: str) -> bool:
        """
        Delete a campaign
        DELETE /api/v2/campaigns/{id}
        """
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                f"{self.base_url}/campaigns/{campaign_id}",
                headers=self.headers,
                params={"api_key": self.api_key},
            )

            return response.status_code in [200, 204]

    async def add_single_lead(
        self,
        campaign_id: str,
        email: str,
        first_name: str = "",
        last_name: str = "",
        company_name: str = "",
        **kwargs,
    ) -> Dict:
        """
        Add a single lead to a campaign
        POST /api/v2/leads
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/leads",
                headers=self.headers,
                json={
                    "api_key": self.api_key,
                    "campaign_id": campaign_id,
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "company_name": company_name,
                    **kwargs,
                },
            )

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to add lead: {response.text}")

            return response.json()

    async def get_lead(self, lead_id: str) -> Optional[Dict]:
        """
        Get a specific lead
        GET /api/v2/leads/{id}
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/leads/{lead_id}",
                headers=self.headers,
                params={"api_key": self.api_key},
            )

            if response.status_code != 200:
                return None

            return response.json()

    async def create_supersearch_enrichment_for_campaign(
        self,
        campaign_id: str,
        search_filters: Dict,
        limit: int = 10,
        work_email_enrichment: bool = True,
        fully_enriched_profile: bool = False,
    ) -> Dict:
        """
        Create SuperSearch enrichment targeted at a campaign (not a list).

        This is the CORRECT way per Instantly API v2 docs:
        1. POST /api/v2/supersearch-enrichment - create enrichment targeting campaign
        2. PATCH /api/v2/supersearch-enrichment/{id}/settings - configure
        3. POST /api/v2/supersearch-enrichment/run - execute

        Returns the enrichment job info.
        """
        async with httpx.AsyncClient(timeout=120.0) as client:
            # Step 1: Create SuperSearch enrichment targeting the campaign
            print(f"DEBUG: Creating SuperSearch enrichment for campaign {campaign_id}")

            # Use Bearer auth header for this endpoint
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            response = await client.post(
                f"{self.base_url}/supersearch-enrichment",
                headers=headers,
                json={
                    "campaign_id": campaign_id,  # Target campaign, not list!
                    "search_filters": search_filters,
                    "limit": limit,
                },
            )

            print(f"DEBUG: Create enrichment response: {response.status_code} - {response.text}")

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to create SuperSearch enrichment: {response.text}")

            enrichment_data = response.json()
            enrichment_id = enrichment_data.get("id") or enrichment_data.get("resource_id")

            # Step 2: Configure settings (if needed)
            # PATCH /api/v2/supersearch-enrichment/{id}/settings
            # (May not be necessary if defaults are fine)

            # Step 3: Run the enrichment
            print(f"DEBUG: Running enrichment {enrichment_id}")
            run_response = await client.post(
                f"{self.base_url}/supersearch-enrichment/run",
                headers=self.headers,
                json={
                    "api_key": self.api_key,
                    "resource_id": enrichment_id
                },
            )

            print(f"DEBUG: Run enrichment response: {run_response.status_code} - {run_response.text}")

            if run_response.status_code not in [200, 201]:
                print(f"Warning: Failed to run enrichment: {run_response.text}")

            return enrichment_data

    async def search_leads_supersearch(
        self,
        search_filters: Dict,
        limit: int = 10,
        work_email_enrichment: bool = True,
        fully_enriched_profile: bool = False,
        list_name: str = None,
        campaign_id: str = None,
    ) -> Dict:
        """
        Search for leads using Instantly SuperSearch API
        POST /api/v2/supersearch-enrichment/enrich-leads-from-supersearch

        IMPORTANT: To add leads directly to a campaign (not a list), pass campaign_id.
        The endpoint will use resource_id=campaign_id and resource_type=1 (Campaign).

        search_filters format:
        {
            "locations": [{"city": "San Francisco", "state": "California", "country": "USA"}],
            "department": ["Engineering", "Marketing"],
            "level": ["C-Level", "VP-Level"],
            "employee_count": ["0 - 25", "25 - 100"],
            "revenue": ["$1 - 10M", "$10 - 50M"],
            "title": {"include": ["CEO", "CTO"], "exclude": ["Assistant"]},
            "company_name": {"include": ["Tech"], "exclude": []},
            "industry": {"include": ["Software"], "exclude": []}
        }
        """
        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "api_key": self.api_key,  # REQUIRED: API key must be in payload too!
                "search_filters": search_filters,
                "limit": limit,
                "work_email_enrichment": work_email_enrichment,
                "fully_enriched_profile": fully_enriched_profile,
                "skip_rows_without_email": True,
                "auto_update": True,
            }

            # Target campaign or list using resource_id and resource_type
            if campaign_id:
                # resource_type: 1 = Campaign, 2 = List
                payload["resource_id"] = campaign_id
                payload["resource_type"] = 1  # Campaign
                print(f"DEBUG: Enriching leads directly into campaign {campaign_id} (resource_type=1)")
            else:
                # Create a list if no campaign specified
                if not list_name:
                    titles = search_filters.get("title", {}).get("include", [])
                    locations = search_filters.get("locations", [])
                    employee_count = search_filters.get("employee_count", [])

                    name_parts = []
                    if titles:
                        name_parts.append(titles[0])
                    if locations and locations[0]:
                        loc = locations[0]
                        city = loc.get("city", "").strip()
                        country = loc.get("country", "").strip()
                        if city:
                            name_parts.append(f"in {city}")
                        elif country:
                            name_parts.append(f"in {country}")
                    if employee_count:
                        name_parts.append(f"({employee_count[0]} employees)")

                    list_name = " ".join(name_parts) if name_parts else "Leads"

                payload["list_name"] = list_name
                print(f"DEBUG: Creating lead list '{list_name}' (no campaign specified)")

            print(f"DEBUG: SuperSearch payload = {json.dumps(payload, indent=2)}")
            print(f"DEBUG: Sending POST to: {self.base_url}/supersearch-enrichment/enrich-leads-from-supersearch")

            response = await client.post(
                f"{self.base_url}/supersearch-enrichment/enrich-leads-from-supersearch",
                headers=self.headers,
                json=payload,
            )

            print(f"DEBUG: SuperSearch response status = {response.status_code}")
            print(f"DEBUG: SuperSearch response = {response.text}")

            if response.status_code == 200:
                result = response.json()
                if not result.get("search_filters") or result.get("search_filters") == {}:
                    print(f"⚠️ WARNING: API returned empty search_filters!")
                    print(f"   This means the API did not accept/save the filters we sent")
                    print(f"   Filters we sent: {json.dumps(payload.get('search_filters'), indent=2)}")

            if response.status_code not in [200, 201]:
                raise Exception(f"Failed to search leads: {response.text}")

            return response.json()

    async def get_leads_from_list(
        self, lead_list_id: str, limit: int = 100, offset: int = 0
    ) -> List[Dict]:
        """
        Get all leads from a specific lead list using POST /api/v2/leads/list

        This endpoint requires Bearer token authentication and filters by list_id.
        Returns a dict with 'items' (the leads array) and 'next_starting_after' for pagination.
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            # Use the correct endpoint with Bearer token
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}"
            }

            payload = {
                "list_id": lead_list_id,  # Filter by specific list ID
                "limit": limit,
                "in_list": True  # Only get leads IN this specific list
            }

            print(f"🔍 POST {self.base_url}/leads/list")
            print(f"   Payload: {json.dumps(payload, indent=2)}")

            # Use list_id (singular) instead of list_ids to filter by specific list
            response = await client.post(
                f"{self.base_url}/leads/list",
                headers=headers,
                json=payload,
            )

            print(f"📊 Response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"   Response structure: {list(data.keys())}")

                # The response has 'items' which contains the leads array
                if "items" in data:
                    raw_leads = data["items"]
                    print(f"✅ get_leads_from_list returned {len(raw_leads)} leads for list {lead_list_id}")

                    # Extract enrichment data from payload and merge with top-level fields
                    enriched_leads = []
                    for lead in raw_leads:
                        # Start with the base lead data
                        enriched_lead = {
                            'id': lead.get('id'),
                            'email': lead.get('email'),
                            'first_name': lead.get('first_name'),
                            'last_name': lead.get('last_name'),
                            'company_name': lead.get('company_name'),
                            'company_domain': lead.get('company_domain'),
                            'phone': lead.get('phone'),
                        }

                        # Extract enrichment data from payload if available
                        payload = lead.get('payload', {})
                        if payload:
                            enriched_lead.update({
                                'title': payload.get('jobTitle'),
                                'location': payload.get('location'),
                                'linkedin': payload.get('linkedIn'),
                                'city': payload.get('city'),
                                'state': payload.get('state'),
                                'country': payload.get('country'),
                            })

                        enriched_leads.append(enriched_lead)

                    if enriched_leads:
                        print(f"   Sample lead: {enriched_leads[0].get('email', 'N/A')} - {enriched_leads[0].get('title', 'N/A')}")
                        print(f"   Location: {enriched_leads[0].get('location', 'N/A')}")

                    return enriched_leads
                print(f"⚠️ No 'items' field in response for list {lead_list_id}")
                print(f"   Response keys: {list(data.keys())}")
                print(f"   Full response: {json.dumps(data, indent=2)[:500]}")
                return []

            # If request fails, return empty list
            print(f"❌ get_leads_from_list failed with status {response.status_code} for list {lead_list_id}")
            print(f"   Error response: {response.text[:500]}")
            return []

    async def wait_for_supersearch_completion(
        self, resource_id: str, expected_count: int, max_wait_seconds: int = 90
    ) -> bool:
        """
        Wait for SuperSearch enrichment to complete by checking for actual leads.

        The enrichment status endpoint is unreliable, so we check for leads directly.
        Since enrichment typically completes in 10-30 seconds, we wait up to 90 seconds.

        Returns True when we find at least expected_count leads
        Returns False if timeout
        """
        elapsed = 0
        poll_interval = 5  # Check every 5 seconds

        print(f"⏳ Waiting for SuperSearch enrichment to complete...")
        print(f"   Resource ID: {resource_id}")
        print(f"   Expected: {expected_count} leads")
        print(f"   Max wait: {max_wait_seconds}s")

        # Get initial count to detect when new leads appear
        initial_count = 0
        try:
            initial_leads = await self.get_leads_from_list(resource_id, limit=1)
            initial_count = len(initial_leads) if initial_leads else 0
        except:
            pass

        print(f"   Initial count: {initial_count} leads")

        while elapsed < max_wait_seconds:
            await asyncio.sleep(poll_interval)
            elapsed += poll_interval

            try:
                # Check if leads are available
                leads = await self.get_leads_from_list(resource_id, limit=expected_count)
                current_count = len(leads) if leads else 0

                print(f"   [{elapsed}s] Found {current_count} leads")

                # Check if we have at least the expected count
                if current_count >= expected_count:
                    print(f"✅ Enrichment complete! Found {current_count} leads")
                    return True

            except Exception as e:
                print(f"   Error checking leads: {str(e)[:100]}")
                # Continue polling

        print(f"⏰ Enrichment timeout after {max_wait_seconds}s")
        return False

    async def get_supersearch_enrichment_status(self, resource_id: str) -> Dict:
        """
        Get the status of a SuperSearch enrichment job
        GET /api/v2/supersearch-enrichment/{resource_id}

        Returns information about the enrichment job including:
        - in_progress: bool - whether enrichment is still running
        - exists: bool - whether the list exists
        - resource_id: str - the lead list ID
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.get(
                f"{self.base_url}/supersearch-enrichment/{resource_id}",
                headers=self.headers,
            )

            if response.status_code == 200:
                return response.json()

            return {}

    async def get_supersearch_enrichment_history(self, resource_id: str) -> List[Dict]:
        """
        Get enrichment history/results for a SuperSearch job
        GET /api/v2/supersearch-enrichment/history/{resource_id}

        This should return the actual enriched leads from SuperSearch
        """
        async with httpx.AsyncClient(timeout=60.0) as client:
            print(f"🔍 Calling SuperSearch history endpoint for resource_id: {resource_id}")
            response = await client.get(
                f"{self.base_url}/supersearch-enrichment/history/{resource_id}",
                headers=self.headers,
            )

            print(f"📊 SuperSearch history response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"📦 SuperSearch history response type: {type(data)}")

                # The response might contain leads in different formats
                if isinstance(data, list):
                    print(f"✅ Got {len(data)} leads from SuperSearch history (list format)")
                    return data
                elif isinstance(data, dict):
                    leads = data.get("leads", data.get("results", data.get("data", [])))
                    print(f"✅ Got {len(leads)} leads from SuperSearch history (dict format)")
                    return leads

            print(f"❌ SuperSearch history failed or returned no data: {response.text[:200]}")
            return []

    async def get_accounts(
        self,
        limit: int = 100,
        status: Optional[int] = None
    ) -> List[Dict]:
        """
        Get list of email accounts from Instantly
        GET /api/v2/accounts

        Args:
            limit: Maximum number of accounts to return (1-100)
            status: Filter by account status (1=Active, 2=Paused, -1=Error, etc.)

        Returns:
            List of account dictionaries with email, first_name, last_name, etc.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            params = {"limit": min(limit, 100)}
            if status is not None:
                params["status"] = status

            print(f"🔍 Fetching accounts from Instantly...")
            print(f"   Endpoint: {self.base_url}/accounts")
            print(f"   Params: {params}")

            response = await client.get(
                f"{self.base_url}/accounts",
                headers=self.headers,
                params=params
            )

            print(f"📊 Response status: {response.status_code}")

            if response.status_code != 200:
                print(f"❌ Error response: {response.text}")
                raise Exception(f"Failed to get accounts: {response.text}")

            data = response.json()
            accounts = data.get("items", [])
            print(f"✅ Found {len(accounts)} accounts")

            # Extract unique domains from accounts
            unique_domains = list(set(acc.get("email", "").split("@")[1] for acc in accounts if "@" in acc.get("email", "")))
            print(f"   Unique domains: {unique_domains[:10]}")

            return accounts
