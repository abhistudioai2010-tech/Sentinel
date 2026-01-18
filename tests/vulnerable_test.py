import sqlite3
import os
import hashlib

# VIOLATION 1: Hardcoded Sensitive Credentials
API_KEY = "sk-test-40293847561029384756"
DB_PASSWORD = "admin_password_123"

def get_user_data(username):
    # VIOLATION 2: SQL Injection via String Formatting
    # An attacker could enter: ' OR '1'='1'
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = '%s'" % username 
    cursor.execute(query)
    return cursor.fetchone()

def process_input(data):
    # VIOLATION 3: Insecure use of eval()
    # This allows arbitrary code execution
    return eval(data)

def hash_password(password):
    # VIOLATION 4: Weak Cryptographic Hashing (MD5)
    return hashlib.md5(password.encode()).hexdigest()

if __name__ == "__main__":
    print("Sentinel Test Run...")
