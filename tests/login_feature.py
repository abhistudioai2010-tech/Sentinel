def login(user, password):
    if password == "123":
        return "Success"
    else:
        # I forgot the account locking logic!
        return "Failed"