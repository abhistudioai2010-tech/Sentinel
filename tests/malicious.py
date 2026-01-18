import os
import sqlite3

# --- VIOLATION 1: No Secrets ---
# Flag hardcoded API keys; secrets must use env variables.
STRIPE_API_KEY = "sk_live_51MzS2pLkd92jK09S88sh2" 
DB_PASSWORD = "super_secret_admin_password"

def handle_user_request(user_id, raw_input):
    # --- VIOLATION 2: PII_ENCRYPTION_STANDARD_V1 ---
    # Flag 'email' or 'phone_number' in plain-text without encrypt().
    user_email = "victim_user@example.com"
    phone_number = "+91-9876543210"
    print(f"Processing data for {user_email}")

    # --- VIOLATION 3: No Raw SQL ---
    # Flag queries using f-strings/formatting instead of parameters.
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}") 
    
    # --- VIOLATION 4: Dangerous Functions ---
    # Flag use of eval(), exec(), or os.system().
    result = eval(raw_input) #
    
    return result

if __name__ == "__main__":
    handle_user_request(1, "1 + 1")
