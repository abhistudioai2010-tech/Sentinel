import os
from supabase import create_client, Client

class GhostOperator:
    def __init__(self):
        # These come from your .env file
        url: str = os.environ.get("SUPABASE_URL")
        key: str = os.environ.get("SUPABASE_KEY")
        self.supabase: Client = create_client(url, key)

    def get_latest_requirement(self):
        """
        Fetches the most recent requirement to validate against.
        """
        response = self.supabase.table("requirements") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        
        return response.data[0] if response.data else None

    def log_audit_result(self, requirement_id: str, verdict: str):
        """
        Logs whether the code passed or failed the AI audit.
        """
        status = "verified" if "PASS" in verdict else "failed"
        self.supabase.table("requirements") \
            .update({"status": status}) \
            .eq("id", requirement_id) \
            .execute()