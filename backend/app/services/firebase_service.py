import firebase_admin
from firebase_admin import credentials, firestore
from typing import List, Dict, Optional
from datetime import datetime
import os


class FirebaseService:
    """
    Service for interacting with Firebase Firestore database
    """

    def __init__(self, credentials_path: Optional[str] = None):
        """
        Initialize Firebase Admin SDK

        Args:
            credentials_path: Path to Firebase service account JSON file
                             If None, will look for GOOGLE_APPLICATION_CREDENTIALS env var
        """
        # Initialize Firebase app if not already initialized
        if not firebase_admin._apps:
            if credentials_path and os.path.exists(credentials_path):
                cred = credentials.Certificate(credentials_path)
                firebase_admin.initialize_app(cred)
            else:
                # Use default credentials from environment or skip if not available
                try:
                    firebase_admin.initialize_app()
                except Exception as e:
                    print(f"⚠️  Warning: Firebase credentials not found. Some features may not work. Error: {e}")
                    # Initialize with a dummy app to prevent errors
                    firebase_admin.initialize_app(options={'projectId': 'dummy-project'})

        try:
            self.db = firestore.client()
        except Exception as e:
            print(f"⚠️  Warning: Could not connect to Firestore. Database features disabled. Error: {e}")
            self.db = None

    async def save_campaign(
        self,
        user_id: str,
        campaign_id: str,
        url: str,
        target_audience: str,
        copy_variants: List[Dict],
        supersearch_list_id: Optional[str] = None
    ) -> Dict:
        """
        Save a new campaign to Firestore
        """
        if not self.db:
            print("⚠️  Firebase not available, skipping campaign save")
            return {"id": campaign_id, "status": "pending"}

        data = {
            "user_id": user_id,
            "campaign_id": campaign_id,
            "url": url,
            "target_audience": target_audience,
            "copy_variants": copy_variants,
            "status": "active",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "sent": 0,
            "opened": 0,
            "clicked": 0,
            "replied": 0,
            "bounced": 0,
            "open_rate": 0,
            "click_rate": 0,
            "reply_rate": 0
        }

        # Add supersearch_list_id if provided
        if supersearch_list_id:
            data["supersearch_list_id"] = supersearch_list_id

        # Save to Firestore using campaign_id as document ID
        doc_ref = self.db.collection("campaigns").document(campaign_id)
        doc_ref.set(data)

        # Return data with Firestore ID
        data["id"] = campaign_id
        data["created_at"] = data["created_at"].isoformat()
        data["updated_at"] = data["updated_at"].isoformat()

        return data

    async def get_user_campaigns(self, user_id: str) -> List[Dict]:
        """
        Get all campaigns for a user
        """
        if not self.db:
            return []

        campaigns_ref = self.db.collection("campaigns")
        query = campaigns_ref.where("user_id", "==", user_id)

        campaigns = []
        for doc in query.stream():
            campaign_data = doc.to_dict()
            campaign_data["id"] = doc.id

            # Convert datetime objects to ISO strings
            if isinstance(campaign_data.get("created_at"), datetime):
                campaign_data["created_at"] = campaign_data["created_at"].isoformat()
            if isinstance(campaign_data.get("updated_at"), datetime):
                campaign_data["updated_at"] = campaign_data["updated_at"].isoformat()

            campaigns.append(campaign_data)

        # Sort in Python instead of Firestore (no index needed)
        campaigns.sort(key=lambda x: x.get("created_at", ""), reverse=True)

        return campaigns

    async def get_campaign(self, user_id: str, campaign_id: str) -> Optional[Dict]:
        """
        Get a specific campaign
        """
        if not self.db:
            return None

        doc_ref = self.db.collection("campaigns").document(campaign_id)
        doc = doc_ref.get()

        if doc.exists:
            campaign_data = doc.to_dict()
            campaign_data["id"] = doc.id

            # Convert datetime objects to ISO strings
            if isinstance(campaign_data.get("created_at"), datetime):
                campaign_data["created_at"] = campaign_data["created_at"].isoformat()
            if isinstance(campaign_data.get("updated_at"), datetime):
                campaign_data["updated_at"] = campaign_data["updated_at"].isoformat()

            return campaign_data

        return None

    async def update_campaign_stats(self, campaign_id: str, analytics: Dict) -> Dict:
        """
        Update campaign statistics
        """
        doc_ref = self.db.collection("campaigns").document(campaign_id)

        update_data = {
            "sent": analytics.get("sent", 0),
            "opened": analytics.get("opened", 0),
            "clicked": analytics.get("clicked", 0),
            "replied": analytics.get("replied", 0),
            "bounced": analytics.get("bounced", 0),
            "open_rate": analytics.get("open_rate", 0),
            "click_rate": analytics.get("click_rate", 0),
            "reply_rate": analytics.get("reply_rate", 0),
            "updated_at": datetime.utcnow()
        }

        doc_ref.update(update_data)

        # Return updated campaign
        return await self.get_campaign(campaign_id)

    async def update_campaign_status(self, campaign_id: str, status: str) -> Dict:
        """
        Update campaign status (active, paused, completed)
        """
        doc_ref = self.db.collection("campaigns").document(campaign_id)

        update_data = {
            "status": status,
            "updated_at": datetime.utcnow()
        }

        doc_ref.update(update_data)

        # Return updated campaign
        return await self.get_campaign(campaign_id)

    async def delete_campaign(self, campaign_id: str) -> bool:
        """
        Delete a campaign
        """
        try:
            doc_ref = self.db.collection("campaigns").document(campaign_id)
            doc_ref.delete()
            return True
        except Exception:
            return False

    async def save_email_account(self, user_id: str, account_data: Dict) -> Dict:
        """
        Save email account information
        """
        data = {
            "user_id": user_id,
            "email": account_data.get("email"),
            "status": account_data.get("status", "active"),
            "warmup_enabled": account_data.get("warmup_enabled", True),
            "created_at": datetime.utcnow()
        }

        # Auto-generate ID for email account
        doc_ref = self.db.collection("email_accounts").document()
        doc_ref.set(data)

        data["id"] = doc_ref.id
        data["created_at"] = data["created_at"].isoformat()

        return data

    async def get_user_email_accounts(self, user_id: str) -> List[Dict]:
        """
        Get all email accounts for a user
        """
        accounts_ref = self.db.collection("email_accounts")
        query = accounts_ref.where("user_id", "==", user_id)

        accounts = []
        for doc in query.stream():
            account_data = doc.to_dict()
            account_data["id"] = doc.id

            if isinstance(account_data.get("created_at"), datetime):
                account_data["created_at"] = account_data["created_at"].isoformat()

            accounts.append(account_data)

        return accounts

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
            "created_at": datetime.utcnow()
        }

        doc_ref = self.db.collection("lead_lists").document()
        doc_ref.set(data)

        data["id"] = doc_ref.id
        data["created_at"] = data["created_at"].isoformat()

        return data

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
            "created_at": datetime.utcnow(),
            "plan": "free"
        }

        doc_ref = self.db.collection("users").document(user_id)
        doc_ref.set(data)

        data["id"] = user_id
        data["created_at"] = data["created_at"].isoformat()

        return data

    async def get_user_profile(self, user_id: str) -> Optional[Dict]:
        """
        Get user profile
        """
        doc_ref = self.db.collection("users").document(user_id)
        doc = doc_ref.get()

        if doc.exists:
            user_data = doc.to_dict()
            user_data["id"] = doc.id

            if isinstance(user_data.get("created_at"), datetime):
                user_data["created_at"] = user_data["created_at"].isoformat()

            return user_data

        return None
