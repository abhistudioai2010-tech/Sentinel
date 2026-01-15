def login(user, password):
    if not user or not password:
        return False
    if password == "secret":
        return True
    return False
