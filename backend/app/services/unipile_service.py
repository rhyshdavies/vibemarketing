"""
Unipile service for LinkedIn integration
"""
import httpx
import json
from typing import List, Dict, Optional


class UnipileService:
    def __init__(self, api_key: str, subdomain: str = "api15", port: int = 14509):
        self.api_key = api_key
        self.base_url = f"https://{subdomain}.unipile.com:{port}/api/v1"
        self.headers = {
            "X-API-KEY": api_key,
            "accept": "application/json",
            "content-type": "application/json"
        }

    async def list_accounts(self) -> List[Dict]:
        """List all connected accounts"""
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/accounts",
                headers=self.headers
            )

            if response.status_code == 200:
                data = response.json()
                print(f"[DEBUG Unipile] Full response: {json.dumps(data, indent=2)}")
                accounts = data.get("items", [])
                print(f"[DEBUG Unipile] Extracted {len(accounts)} accounts")
                return accounts
            else:
                raise Exception(f"Failed to list accounts: {response.text}")

    async def get_linkedin_accounts(self) -> List[Dict]:
        """Get all connected LinkedIn accounts"""
        accounts = await self.list_accounts()
        # Filter by 'type' field, not 'provider' - Unipile uses 'type' for account type
        linkedin_accounts = [acc for acc in accounts if acc.get("type") == "LINKEDIN"]
        print(f"[DEBUG] Filtered LinkedIn accounts: {len(linkedin_accounts)} (from {len(accounts)} total)")
        return linkedin_accounts

    async def create_hosted_auth_link(
        self,
        provider: str = "LINKEDIN",
        success_redirect_url: Optional[str] = None,
        failure_redirect_url: Optional[str] = None
    ) -> str:
        """
        Create a hosted authentication link for connecting a LinkedIn account

        Returns: URL to redirect user to for authentication
        """
        from datetime import datetime, timedelta

        async with httpx.AsyncClient(timeout=30.0) as client:
            # Calculate expiration time (24 hours from now)
            expires_on = (datetime.utcnow() + timedelta(hours=24)).strftime("%Y-%m-%dT%H:%M:%S.000Z")

            # Required fields for Unipile hosted auth
            payload = {
                "name": "vibemarketing_user",
                "expiresOn": expires_on,
                "api_url": self.base_url.replace("/api/v1", ""),  # Remove /api/v1 from base_url
                "type": "create",
                "providers": ["LINKEDIN"]
            }

            # Add optional redirect URLs if provided
            if success_redirect_url:
                payload["success_redirect_url"] = success_redirect_url
            if failure_redirect_url:
                payload["failure_redirect_url"] = failure_redirect_url

            response = await client.post(
                f"{self.base_url}/hosted/accounts/link",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                data = response.json()
                return data.get("url")
            else:
                raise Exception(f"Failed to create auth link: {response.text}")

    async def send_linkedin_message(
        self,
        account_id: str,
        attendees: List[str],
        text: str
    ) -> Dict:
        """
        Send a LinkedIn message to a new or existing contact

        Args:
            account_id: Unipile account ID
            attendees: List of LinkedIn profile URLs or internal IDs
            text: Message text
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            # For new chats, use POST /chats endpoint
            payload = {
                "account_id": account_id,
                "attendees_ids": attendees,  # Use attendees_ids instead of attendees
                "text": text
            }

            response = await client.post(
                f"{self.base_url}/chats",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Failed to send message: {response.text}")

    async def get_linkedin_profile(
        self,
        account_id: str,
        identifier: str
    ) -> Dict:
        """
        Retrieve a LinkedIn user profile to get their provider_id

        Args:
            account_id: Unipile account ID
            identifier: LinkedIn profile URL, public identifier, or internal ID

        Returns:
            User profile with provider_id
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                f"{self.base_url}/users/{identifier}",
                headers=self.headers,
                params={"account_id": account_id}
            )

            if response.status_code == 200:
                return response.json()
            else:
                raise Exception(f"Failed to get LinkedIn profile: {response.text}")

    async def send_linkedin_connection_request(
        self,
        account_id: str,
        profile_identifier: str,
        message: Optional[str] = None
    ) -> Dict:
        """
        Send a LinkedIn connection request with an optional note

        Args:
            account_id: Unipile account ID
            profile_identifier: LinkedIn profile URL, slug, or provider ID
            message: Optional connection request message/note (max 300 characters)
        """
        async with httpx.AsyncClient(timeout=30.0) as client:
            # First, get the user's provider_id
            print(f"[DEBUG Unipile] Fetching profile for identifier: {profile_identifier}")
            profile = await self.get_linkedin_profile(account_id, profile_identifier)
            provider_id = profile.get("provider_id")
            print(f"[DEBUG Unipile] Got provider_id: {provider_id}")

            payload = {
                "account_id": account_id,
                "provider_id": provider_id
            }

            if message:
                # Truncate to 300 characters as per LinkedIn limits
                payload["message"] = message[:300] if len(message) > 300 else message

            response = await client.post(
                f"{self.base_url}/users/invite",
                headers=self.headers,
                json=payload
            )

            if response.status_code in [200, 201]:
                return response.json()
            else:
                raise Exception(f"Failed to send connection request: {response.text}")
