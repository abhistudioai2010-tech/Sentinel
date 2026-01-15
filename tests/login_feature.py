# Simulated User Database
USER_DB = {
    "admin": "x8s7#dP2",
    "user1": "welcome2026"
}

def login(username, input_password):
    """
    Verifies user credentials against the secure database.
    """
    # 1. Input Sanitization
    if not username or not input_password:
        return False
        
    # 2. User Lookup
    if username not in USER_DB:
        return False
        
    # 3. Secure Verification
    stored_password = USER_DB[username]
    if input_password == stored_password:
        return True
        
    return False
