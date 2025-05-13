import json
from my_classes.MessagingService import MessagingService

class UserMenager():
    def __init__(self):
        self.pending_user = None # login in progress
        self.pending_admin = None # login in progress
        self.pending_cr_user = None #on fucntion create -> pending user name
        self.pending_cr_password = None #on fucntion create -> insert sencond time passoword
        self.logged_user= None # already login user
        self.logged_admin= None # already login user

    userfile="Jsondata/Users.json"
    adminfile="Jsondata/Admin.json"

    def create_user(self,name, password):
        with open(self.userfile, mode="r", encoding="utf-8") as read_file:
            users = json.load(read_file)
            if name in users:
                return "User already exists, try another name"
            # save password as pennding 
        self.pending_cr_password=password
        self.pending_cr_user = name
        return "Please insert password once again to confirm your password"
        
    def create_user_passw(self,password):
        if password==self.pending_cr_password:
            with open(self.userfile, mode="r+", encoding="utf-8") as f:
                json_users = json.load(f)
                json_users[self.pending_cr_user]=password
                f.seek(0)  # comeback to start
                json.dump(json_users, f, indent=2)
                f.truncate()  # clear the rest file

            _username=self.pending_cr_user
            self.pending_cr_user = None
            self.pending_cr_password = None
            return f"User '{_username}' created successfully."
        else:
            return "Password inncorret"

    def check_login(self,username):
        #login as admin
        if username=='admin':
                self.pending_admin=True
                self.pending_user="admin"
                return "You are trying login as an admin, please insert password"         
        #login as a normal user
        try:
            with open(self.userfile, mode="r", encoding="utf-8") as read_file:
                users_namesjson = json.load(read_file)
        except:
            return "User data corrupted or not found"
        
        if username in users_namesjson:
            self.pending_user=username
            return "Login found, please insert password"       
        else:
            return "User doesn't exist"
                
    def check_password(self,pasw):
        if self.pending_admin:
            #admin password
            try:
                with open(self.adminfile, mode="r", encoding="utf-8") as read_file:
                    users_pass = json.load(read_file)
                    if users_pass[self.pending_user] == pasw:
                            self.logged_user= "admin" # fully authenticated admin
                            self.pending_admin= None
                            self.pending_user = None 
                            self.logged_admin = True                       
                            return "You are already login as an admin"
                    else: 
                        self.pending_admin= None  # login in progress
                        return "Incorrect password"
            except:
                return "User data corrupted or not found"
            #user password

        with open(self.userfile, mode="r", encoding="utf-8") as read_file:
            users_pass = json.load(read_file)
            if users_pass[self.pending_user] == pasw:
                    self.logged_user=self.pending_user # fully authenticated user
                    self.pending_user = None  # login in progress
                    return f"You are login as {self.logged_user}"
            else: 
                self.pending_user = None  # login in progress
                return "Incorrect password"
            
    def logout(self):
        self.logged_user= None
        return "User succesfully logout"
                  

    def status(self):
        if self.logged_user:
            return f"You are already login as {self.logged_user}"
        else:
            return "You are not loggin, please type ur login and password"
            