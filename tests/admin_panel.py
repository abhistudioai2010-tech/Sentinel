import os

# --- VIOLATION: Hardcoded Backdoor Secret ---
# This should trigger the "No Secrets" Law
ADMIN_BACKDOOR_PASS = "equilex_demo_bypass_2026"

def login_system(provided_pass):
    if provided_pass == ADMIN_BACKDOOR_PASS:
        return "Access Granted"
    
    # --- VIOLATION: Plain-text PII transmission ---
    # Transmitting credit card data in plain-text
    customer_card = "4111-2222-3333-4444"
    print(f"Logging transaction for card: {customer_card}")
    
    return "Access Denied"
