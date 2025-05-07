import json

class Login_menager():
    def __init__(self):
        pass

    userfile="Users.json"

    def check_login(self,username):

            with open("Users.json", mode="r", encoding="utf-8") as read_file:
                users_pass = json.load(read_file)
                try:
                    if users_pass[username]:
                        return "Login found"
                except:
                    return "User doesn't exist"