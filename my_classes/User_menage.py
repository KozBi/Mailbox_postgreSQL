import json

class User_menager():
    def __init__(self):
        self.pending_user = None  # login in progress
        self.logged_in = None     # fully authenticated user

    userfile="Users.json"

    def create_user(self,name, password):
        with open("Users.json", mode="r", encoding="utf-8") as read_file:
            users = json.load(read_file)
            if name in users:
                return "User already exists, try another name"
            # Add a new user to dict and write
        users[name] = str(password)
        with open("Users.json", mode="w", encoding="utf-8") as write_file:
            json.dump(users, write_file, indent=2)
            return f"User '{name}' created successfully."
            

    def check_login(self,username):
        if not self.pending_user:
            with open("Users.json", mode="r", encoding="utf-8") as read_file:
                users_pass = json.load(read_file)
                try:
                    if users_pass[username]:
                        self.pending_user=username
                        return "Login found, please insert password"       
                except:
                    return "User doesn't exist"
                
    def check_passowrd(self,pasw):
        with open("Users.json", mode="r", encoding="utf-8") as read_file:
            users_pass = json.load(read_file)
            if users_pass[self.pending_user] == pasw:
                    self.pending_user = None  # login in progress
                    self.logged_in = True    # fully authenticated user
                    return "User succesfully login"
            else: 
                self.pending_user = None  # login in progress
                self.logged_in = False   # fully authenticated user
                return "Incorrect password"
                

