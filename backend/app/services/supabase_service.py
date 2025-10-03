from supabase import create_client, Client
from typing import List, Dict, Optional
from datetime import datetime


class SupabaseService:
    """
    Service for interacting with Supabase database
    """

    def __init__(self, supabase_url: str, supabase_key: str):
        self.client: Client = create_client(supabase_url, supabase_key)

    async def save_campaign(
        self,
        user_id: str,
        campaign_id: str,
        url: str,
        target_audience: str,
        copy_variants: List[Dict]
    ) -> Dict:
        """
        Save a new campaign to the database
        """
        data = {
            "user_id": user_id,
            "campaign_id": campaign_id,
            "url": url,
            "target_audience": target_audience,
            "copy_variants": copy_variants,
            "status": "active",
            "created_at": datetime.utcnow().isoformat(),
            "sent": 0,
            "opened": 0,
            "clicked": 0,
            "replied": 0,
            "open_rate": 0,
            "click_rate": 0,
            "reply_rate": 0
        }

        result = self.client.table("campaigns").insert(data).execute()

        return result.data[0] if result.data else {}

    async def get_user_campaigns(self, user_id: str) -> List[Dict]:
        """
        Get all campaigns for a user
        """
        result = self.client.table("campaigns")\
            .select("*")\
            .eq("user_id", user_id)\
            .order("created_at", desc=True)\
            .execute()

        return result.data if result.data else []

    async def get_campaign(self, campaign_id: str) -> Optional[Dict]:
        """
        Get a specific campaign
        """
        result = self.client.table("campaigns")\
            .select("*")\
            .eq("campaign_id", campaign_id)\
            .execute()

        return result.data[0] if result.data else None

    async def update_campaign_stats(self, campaign_id: str, analytics: Dict) -> Dict:
        """
        Update campaign statistics
        """
        data = {
            "sent": analytics.get("sent", 0),
            "opened": analytics.get("opened", 0),
            "clicked": analytics.get("clicked", 0),
            "replied": analytics.get("replied", 0),
            "bounced": analytics.get("bounced", 0),
            "open_rate": analytics.get("open_rate", 0),
            "click_rate": analytics.get("click_rate", 0),
            "reply_rate": analytics.get("reply_rate", 0),
            "updated_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("campaigns")\
            .update(data)\
            .eq("campaign_id", campaign_id)\
            .execute()

        return result.data[0] if result.data else {}

    async def update_campaign_status(self, campaign_id: str, status: str) -> Dict:
        """
        Update campaign status (active, paused, completed)
        """
        data = {
            "status": status,
            "updated_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("campaigns")\
            .update(data)\
            .eq("campaign_id", campaign_id)\
            .execute()

        return result.data[0] if result.data else {}

    async def delete_campaign(self, campaign_id: str) -> bool:
        """
        Delete a campaign
        """
        result = self.client.table("campaigns")\
            .delete()\
            .eq("campaign_id", campaign_id)\
            .execute()

        return len(result.data) > 0 if result.data else False

    async def save_email_account(self, user_id: str, account_data: Dict) -> Dict:
        """
        Save email account information
        """
        data = {
            "user_id": user_id,
            "email": account_data.get("email"),
            "status": account_data.get("status", "active"),
            "warmup_enabled": account_data.get("warmup_enabled", True),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("email_accounts").insert(data).execute()

        return result.data[0] if result.data else {}

    async def get_user_email_accounts(self, user_id: str) -> List[Dict]:
        """
        Get all email accounts for a user
        """
        result = self.client.table("email_accounts")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()

        return result.data if result.data else []

    async def save_lead_list(
        self,
        user_id: str,
        campaign_id: str,
        leads: List[Dict]
    ) -> Dict:
        """
        Save a lead list
        """
        data = {
            "user_id": user_id,
            "campaign_id": campaign_id,
            "leads": leads,
            "total_leads": len(leads),
            "created_at": datetime.utcnow().isoformat()
        }

        result = self.client.table("lead_lists").insert(data).execute()

        return result.data[0] if result.data else {}

    async def get_user_stats(self, user_id: str) -> Dict:
        """
        Get aggregate stats for a user across all campaigns
        """
        campaigns = await self.get_user_campaigns(user_id)

        total_sent = sum(c.get("sent", 0) for c in campaigns)
        total_opened = sum(c.get("opened", 0) for c in campaigns)
        total_clicked = sum(c.get("clicked", 0) for c in campaigns)
        total_replied = sum(c.get("replied", 0) for c in campaigns)

        return {
            "total_campaigns": len(campaigns),
            "active_campaigns": len([c for c in campaigns if c.get("status") == "active"]),
            "total_sent": total_sent,
            "total_opened": total_opened,
            "total_clicked": total_clicked,
            "total_replied": total_replied,
            "avg_open_rate": round((total_opened / max(total_sent, 1)) * 100, 2),
            "avg_reply_rate": round((total_replied / max(total_sent, 1)) * 100, 2)
        }

    async def create_user_profile(self, user_id: str, email: str, name: str = "") -> Dict:
        """
        Create a user profile
        """
        data = {
            "user_id": user_id,
            "email": email,
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "plan": "free"
        }

        result = self.client.table("users").insert(data).execute()

        return result.data[0] if result.data else {}

    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile
        """
        result = self.client.table("users")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()

        return result.data[0] if result.data else None
