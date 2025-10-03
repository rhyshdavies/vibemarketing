"""
Service for managing DFY email accounts and pre-warmed domains via Instantly.ai
"""
import httpx
from typing import List, Dict, Optional


class DomainService:
    """
    Service for purchasing and managing pre-warmed domains and email accounts
    """

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.instantly.ai/api/v2"

    async def get_ordered_dfy_accounts(
        self,
        limit: int = 100,
        only_prewarmed: bool = False
    ) -> List[Dict]:
        """
        Get list of DFY email accounts that have been ordered/purchased

        Args:
            limit: Maximum number of accounts to return
            only_prewarmed: If True, only return pre-warmed accounts

        Returns:
            List of ordered DFY account dictionaries with domain, email, etc.
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            print(f"🔍 Fetching ordered DFY accounts...")
            print(f"   Endpoint: {self.base_url}/dfy-email-account-orders/accounts")

            response = await client.get(
                f"{self.base_url}/dfy-email-account-orders/accounts",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                params={
                    "limit": limit,
                    "with_passwords": False
                }
            )

            print(f"📊 Response status: {response.status_code}")

            if response.status_code != 200:
                print(f"❌ Error response: {response.text}")
                raise Exception(f"Failed to get ordered DFY accounts: {response.text}")

            data = response.json()
            print(f"📦 Response data keys: {list(data.keys())}")

            accounts = data.get("items", [])
            print(f"✅ Found {len(accounts)} DFY accounts")

            # Filter by pre-warmed if requested
            if only_prewarmed:
                accounts = [acc for acc in accounts if acc.get("is_pre_warmed_up")]
                print(f"   {len(accounts)} are pre-warmed")

            return accounts

    async def get_prewarmed_domains(
        self,
        extensions: Optional[List[str]] = None,
        search: Optional[str] = None
    ) -> List[str]:
        """
        Get list of YOUR ordered pre-warmed domains (extracted from DFY accounts)

        Args:
            extensions: List of domain extensions to filter by (e.g., ["com", "org"])
            search: Search string to filter domains

        Returns:
            List of unique domain names from your pre-warmed DFY accounts
        """
        # Get all ordered accounts
        accounts = await self.get_ordered_dfy_accounts(limit=100, only_prewarmed=True)

        # Extract unique domains
        domains = list(set(acc.get("domain") for acc in accounts if acc.get("domain")))

        # Filter by extensions if provided
        if extensions:
            filtered_domains = []
            for domain in domains:
                ext = domain.split(".")[-1]
                if ext in extensions:
                    filtered_domains.append(domain)
            domains = filtered_domains

        # Filter by search if provided
        if search:
            domains = [d for d in domains if search.lower() in d.lower()]

        print(f"✅ Extracted {len(domains)} unique pre-warmed domains")
        if domains:
            print(f"   Sample: {domains[:5]}")

        return domains

    async def check_domain_availability(self, domains: List[str]) -> Dict[str, bool]:
        """
        Check if domains are available for purchase

        Args:
            domains: List of domain names to check (max 50)

        Returns:
            Dict mapping domain name to availability status
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dfy-email-account-orders/domains/check",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "domains": domains[:50]  # Max 50 domains
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to check domain availability: {response.text}")

            data = response.json()
            # Convert results array to dict
            availability = {}
            for result in data.get("results", []):
                availability[result["domain"]] = result["is_available"]

            return availability

    async def generate_similar_domains(
        self,
        domain: str,
        tlds: Optional[List[str]] = None
    ) -> List[str]:
        """
        Generate similar available domains based on a given domain

        Args:
            domain: The base domain to generate suggestions from
            tlds: List of TLDs to use (default: ["com", "org"])

        Returns:
            List of similar available domain names (max 66 per TLD)
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dfy-email-account-orders/domains/similar",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "domain": domain,
                    "tlds": tlds or ["com", "org"]
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to generate similar domains: {response.text}")

            data = response.json()
            return data.get("domains", [])

    async def order_prewarmed_accounts(
        self,
        domain: str,
        number_of_accounts: int = 1,
        forwarding_domain: Optional[str] = None,
        simulation: bool = False
    ) -> Dict:
        """
        Order pre-warmed email accounts for a domain

        Args:
            domain: The pre-warmed domain to order (must be from get_prewarmed_domains)
            number_of_accounts: Number of accounts (1-5)
            forwarding_domain: Optional domain to forward emails to
            simulation: If True, just get pricing without placing order

        Returns:
            Order details including pricing and account info
        """
        if number_of_accounts < 1 or number_of_accounts > 5:
            raise ValueError("Number of accounts must be between 1 and 5")

        order_data = {
            "items": [
                {
                    "domain": domain,
                    "email_provider": 1,  # Google
                    "forwarding_domain": forwarding_domain
                }
            ],
            "order_type": "pre_warmed_up",
            "simulation": simulation
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dfy-email-account-orders",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=order_data
            )

            if response.status_code != 200:
                raise Exception(f"Failed to order pre-warmed accounts: {response.text}")

            return response.json()

    async def order_custom_domain_accounts(
        self,
        domain: str,
        accounts: List[Dict[str, str]],
        forwarding_domain: Optional[str] = None,
        simulation: bool = False
    ) -> Dict:
        """
        Order DFY email accounts with a custom domain

        Args:
            domain: The custom domain name (.com or .org only)
            accounts: List of account dicts with first_name, last_name, email_address_prefix
                     Example: [{"first_name": "John", "last_name": "Doe", "email_address_prefix": "john.doe"}]
            forwarding_domain: Optional domain to forward emails to
            simulation: If True, just get pricing without placing order

        Returns:
            Order details including pricing and account info
        """
        if len(accounts) < 1 or len(accounts) > 5:
            raise ValueError("Must provide between 1 and 5 accounts")

        order_data = {
            "items": [
                {
                    "domain": domain,
                    "email_provider": 1,  # Google
                    "accounts": accounts,
                    "forwarding_domain": forwarding_domain
                }
            ],
            "order_type": "dfy",
            "simulation": simulation
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dfy-email-account-orders",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=order_data
            )

            if response.status_code != 200:
                raise Exception(f"Failed to order custom domain accounts: {response.text}")

            return response.json()

    async def list_ordered_accounts(
        self,
        limit: int = 10,
        starting_after: Optional[str] = None,
        with_passwords: bool = False
    ) -> Dict:
        """
        List all DFY email accounts you've ordered

        Args:
            limit: Number of items to return (1-100)
            starting_after: Pagination cursor
            with_passwords: Whether to include account passwords

        Returns:
            Dict with 'items' (list of accounts) and 'next_starting_after' (pagination)
        """
        params = {"limit": min(limit, 100)}
        if starting_after:
            params["starting_after"] = starting_after
        if with_passwords:
            params["with_passwords"] = "true"

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/dfy-email-account-orders/accounts",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                },
                params=params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to list ordered accounts: {response.text}")

            return response.json()

    async def list_domain_orders(
        self,
        limit: int = 10,
        starting_after: Optional[str] = None
    ) -> Dict:
        """
        List all DFY domain orders

        Args:
            limit: Number of items to return (1-100)
            starting_after: Pagination cursor

        Returns:
            Dict with 'items' (list of orders) and 'next_starting_after' (pagination)
        """
        params = {"limit": min(limit, 100)}
        if starting_after:
            params["starting_after"] = starting_after

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/dfy-email-account-orders",
                headers={
                    "Authorization": f"Bearer {self.api_key}"
                },
                params=params
            )

            if response.status_code != 200:
                raise Exception(f"Failed to list domain orders: {response.text}")

            return response.json()

    async def cancel_accounts(self, account_emails: List[str]) -> Dict:
        """
        Cancel DFY email accounts

        Args:
            account_emails: List of email addresses to cancel

        Returns:
            Dict with 'items' containing the cancelled accounts
        """
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/dfy-email-account-orders/accounts/cancel",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "accounts": account_emails
                }
            )

            if response.status_code != 200:
                raise Exception(f"Failed to cancel accounts: {response.text}")

            return response.json()
