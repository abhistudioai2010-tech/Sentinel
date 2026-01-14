import os

def process_payment():
    # This is a generic "password" that GitHub doesn't care about.
    # But Gemini will see "password" and "hardcoded" and scream!
    app_password = "my_unsafe_admin_password"
    
    print(f"Login with: {app_password}")
    return "Done"            