# Sentinel-Ghost MVP

## Overview
A FastAPI-based webhook server that audits GitHub pull requests against business requirements using AI.

## Project Structure
```
app/
├── main.py              # FastAPI application with webhook endpoint
├── core/
│   ├── ai_brain.py      # AI interface using OpenRouter API
│   ├── ghost_operator.py # Supabase operations
│   └── logic.py         # Code analysis logic
tests/
└── test_webhook.py      # Test file
requirements.txt         # Python dependencies
```

## How It Works
1. Receives GitHub webhook events on POST /webhook
2. When a PR is opened or synchronized, fetches the code diff
3. Retrieves business requirements from Supabase
4. Uses AI (via OpenRouter) to analyze if the code matches requirements
5. Updates the requirement status in Supabase

## Required Environment Variables
- `GITHUB_TOKEN` - GitHub personal access token for API access
- `SUPABASE_URL` - Supabase project URL
- `SUPABASE_KEY` - Supabase API key
- `OPENROUTER_API_KEY` - OpenRouter API key for AI calls

## Running the Application
The server runs on port 5000 using uvicorn:
```
uvicorn app.main:app --host 0.0.0.0 --port 5000 --reload
```

## API Endpoints
- GET / - Health check, returns status
- POST /webhook - GitHub webhook receiver

## Recent Changes
- 2026-01-11: Initial setup in Replit environment
