import os
from dotenv import load_dotenv

# 1. Load Secrets
load_dotenv()

from fastapi import FastAPI, Request, BackgroundTasks
from supabase import create_client, Client
from github import Github
from app.core.ai_brain import SentinelBrain

app = FastAPI(title="Sentinel-Ghost MVP")

# 2. Initialize The Brain
brain = SentinelBrain()

# 3. Initialize The Memory (Supabase)
sb_url = os.getenv("SUPABASE_URL")
sb_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(sb_url, sb_key)

# 4. Initialize The Eyes (GitHub)
g = Github(os.getenv("GITHUB_TOKEN"))

@app.get("/")
def read_root():
    return {"status": "Sentinel-Ghost is Online"}

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        # Extract GitHub details
        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        
        # A. Fetch the REAL code diff from GitHub
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        real_diff = ""
        for file in pr.get_files():
            real_diff += f"File: {file.filename}\n{file.patch}\n"
        
        # B. Fetch ALL Requirements from Supabase (The Upgrade)
        # We removed .limit(1) so it grabs everything
        res = supabase.table("requirements").select("*").execute()
        all_rules = res.data
        
        if all_rules and real_diff:
            print(f"DEBUG: Found {len(all_rules)} rules. Starting comprehensive audit...")
            
            # C. Trigger an AI Audit for EVERY rule found
            for req in all_rules:
                background_tasks.add_task(run_audit, req, real_diff, pr)
            
    return {"status": "Multi-Rule Audit Started"}

# --- THE AUDITOR FUNCTION ---
def run_audit(req, diff, pr):
    try:
        print(f"DEBUG: Auditing against rule: '{req['title']}'...")
        
        system_p = "You are a logic auditor. Answer only with PASS or FAIL, followed by a 1-sentence explanation."
        user_p = f"REQUIREMENT: {req['description']}\nCODE: {diff}"
        
        # 1. Get the Verdict
        response = brain.ask(system_p, user_p) 
        print(f"DEBUG: Verdict for '{req['title']}': {response}")
        
        # 2. Update Supabase
        status = "verified" if "PASS" in response.upper() else "failed"
        supabase.table("requirements").update({"status": status}).eq("id", req["id"]).execute()
        
        # 3. Comment on GitHub if failed
        if status == "failed":
            comment = f"👻 **Sentinel Alert**\n\nI detected a violation of the rule: *{req['title']}*.\n\n**AI Feedback:** {response}"
            pr.create_issue_comment(comment)
            print(f"SUCCESS: Alert posted for '{req['title']}'")
            
    except Exception as e:
        print(f"ERROR processing rule {req.get('id')}: {str(e)}")