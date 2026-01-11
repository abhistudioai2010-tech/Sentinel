import os  # <--- Add this line first!
from dotenv import load_dotenv

# 1. Load the secrets
load_dotenv()

from fastapi import FastAPI, Request, BackgroundTasks
from supabase import create_client, Client
from github import Github

app = FastAPI(title="Sentinel-Ghost MVP")

# Initialize GitHub Client
g = Github(os.getenv("GITHUB_TOKEN"))

@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        # Extract GitHub details from the webhook
        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        
        # 1. Fetch the REAL code diff from GitHub
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        real_diff = ""
        for file in pr.get_files():
            real_diff += f"File: {file.filename}\n{file.patch}\n"
        
        # 2. Fetch Requirement from Supabase
        res = supabase.table("requirements").select("*").limit(1).execute()
        req = res.data[0] if res.data else None
        
        if req and real_diff:
            # 3. Trigger the AI Audit with REAL data
            background_tasks.add_task(run_audit, req, real_diff)
            
    return {"status": "Real Audit Started"}