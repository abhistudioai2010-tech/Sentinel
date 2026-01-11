import httpx
# This simulates a GitHub "Pull Request Opened" event
data = {"action": "opened", "pull_request": {"title": "Test PR"}}
httpx.post("http://127.0.0.1:8000/webhook", json=data)
print("Simulation Sent!")