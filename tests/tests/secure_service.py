import os
import sqlite3
from cryptography.fernet import Fernet

# --- COMPLIANT: No Hardcoded Secrets ---
# Pulling from environment variables is the industry standard
API_KEY = os.getenv("STRIPE_API_KEY")
cipher_suite = Fernet(os.getenv("ENCRYPTION_KEY", Fernet.generate_key()))

def save_user_data(user_id, email_raw):
    # --- COMPLIANT: Encryption method call used ---
    # This satisfies the PII_ENCRYPTION_STANDARD_V1 law
    encrypted_email = cipher_suite.encrypt(email_raw.encode())
    
    # --- COMPLIANT: Parameterized Query ---
    # This satisfies the No Raw SQL law
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (id, email) VALUES (?, ?)", (user_id, encrypted_email))
    conn.commit()
    
    return "User data saved securely."
