import os
from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, Request, BackgroundTasks
from supabase import create_client, Client
from github import Github
from app.core.logic import analyze_code_logic

app = FastAPI(title="Sentinel-Ghost MVP")

g = Github(os.getenv("GITHUB_TOKEN"))

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key) if supabase_url and supabase_key else None


def run_audit(req: dict, code_diff: str):
    requirements_text = req.get("description", "")
    verdict = analyze_code_logic(requirements_text, code_diff)
    if supabase:
        status = "verified" if "PASS" in verdict else "failed"
        supabase.table("requirements").update({"status": status}).eq("id", req["id"]).execute()


@app.get("/")
async def root():
    return {"status": "Sentinel-Ghost MVP is running", "endpoints": ["/webhook"]}


@app.post("/webhook")
async def github_webhook(request: Request, background_tasks: BackgroundTasks):
    payload = await request.json()
    
    if payload.get("action") in ["opened", "synchronize"]:
        repo_name = payload["repository"]["full_name"]
        pr_number = payload["pull_request"]["number"]
        
        repo = g.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        real_diff = ""
        for file in pr.get_files():
            real_diff += f"File: {file.filename}\n{file.patch}\n"
        
        if supabase:
            res = supabase.table("requirements").select("*").limit(1).execute()
            req = res.data[0] if res.data else None
        else:
            req = None
        
        if req and real_diff:
            background_tasks.add_task(run_audit, req, real_diff)
            
    return {"status": "Real Audit Started"}