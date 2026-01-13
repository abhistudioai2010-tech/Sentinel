import os
import json
from fastapi import FastAPI, Request
from supabase import create_client, Client

# --- CONFIGURATION ---
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Sentinel Ghost is Awake"}

@app.post("/webhook")
async def handle_webhook(request: Request):
    print("\n🚨 WEBHOOK RECEIVED! STARTING FORENSICS...")
    
    # 1. Parse the incoming crime report from GitHub
    payload = await request.json()
    
    # Check if this is a push event
    if "commits" not in payload:
        print("ℹ️  Not a push event. Skipping.")
        return {"message": "Ignored"}

    print(f"🔍 Analyzing {len(payload['commits'])} new commits...")

    # 2. Fetch the Laws (Rules) from Database
    print("📚 Fetching laws from Supabase...")
    response = supabase.table("requirements").select("*").execute()
    rules = response.data

    # 3. Simulate the Scan (For MVP, we check for 'test_crime.py')
    # In the full version, we would use the AI Brain here.
    # For now, we will HARD-CODE the detection to verify the DB updates.
    
    modified_files = []
    for commit in payload['commits']:
        modified_files.extend(commit.get('added', []) + commit.get('modified', []))
    
    print(f"📂 Modified files: {modified_files}")

    violation_detected = False
    
    # SIMPLE LOGIC: If 'test_crime.py' is touched, trigger the alarm!
    for file in modified_files:
        if "test_crime.py" in file:
            print("❌ CRIME FOUND: test_crime.py was modified!")
            violation_detected = True
            
            # 4. Update Database Status
            print("⚡ UPDATING DASHBOARD TO CRITICAL...")
            
            # Find the 'No Empty Functions' rule and mark it FAILED
            # (Make sure the title matches exactly what is in your DB)
            supabase.table("requirements").update({"status": "failed"}).eq("title", "No Empty Functions").execute()
            
            # Create a log entry
            supabase.table("logs").insert({
                "file_name": "test_crime.py",
                "violation": "Empty function detected",
                "status": "active"
            }).execute()

    if violation_detected:
        return {"status": "VIOLATION_REPORTED"}
    else:
        print("✅ No crimes found in this push.")
        return {"status": "CLEAN"}