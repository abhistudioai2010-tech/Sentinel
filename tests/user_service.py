def save_user_data(email, phone):
    # This should be flagged by EQUILEX
    temp_storage = {"user_email": email, "user_phone": phone}
    print("Saving plain text data...")
