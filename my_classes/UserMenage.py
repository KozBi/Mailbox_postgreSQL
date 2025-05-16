import json
import hashlib
from my_classes.MessagingService import MessagingService

class UserMenager():
    def __init__(self):
        self.pending_user = None # login in progress
        self.pending_user_id = None # login in progress
        self.pending_admin = None # login in progress
        self.pending_cr_user = None #on fucntion create -> pending user name
        self.pending_cr_user_id = None #on fucntion create -> pending user name id
        self.pending_cr_password = None #on fucntion create -> insert sencond time passoword
        self.logged_user= None # already login user
        self.logged_user_id= None # already login user
        self.logged_admin= None # already login user

    userfile="Jsondata/Users.json"
    adminfile="Jsondata/Admin.json"
    passfile="Jsondata/Passwords.json"

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def get_user_by_id(self,id):
         with open(self.userfile, mode="r", encoding="utf-8") as u:
            users = json.load(u)
            for user in users:
                if user["id"]==id:
                    return user["username"]

            print("get_user_id no Value") 
            return None
         
    def get_id_by_user(self,username):
        with open(self.userfile, mode="r", encoding="utf-8") as u:
            users = json.load(u)
            for user in users:
                if user["username"]==username:
                    return str(user["id"])

            print("get_id_by_user no Value") 
            return None
    

    def create_user(self,name, password):
        with open(self.userfile, mode="r", encoding="utf-8") as u:
            users = json.load(u)
            if name in [user["username"] for user in users]:
                return "User already exists, try another name"            
            else: 
                #find max id and +1. Generator used here!
                new_id = max((user["id"] for user in users), default=0) + 1
            # save password as pennding 
            self.pending_cr_password=password
            self.pending_cr_user = name
            self.pending_cr_user_id = new_id
        return "Please insert password once again to confirm your password"
        
    def create_user_passw(self,password):
        if password==self.pending_cr_password:
            # first create a user
            with open(self.userfile, mode="r+", encoding="utf-8") as u:
                users = json.load(u)
                    #find max id and +1. Generator used here!
                new_dic={"id": self.pending_cr_user_id , "username":self.pending_cr_user}
                users.append(new_dic)
                u.seek(0)  # comeback to start
                json.dump(users, u, indent=2)
                u.truncate()  # clear the rest file

            # create a pasword
            with open(self.passfile, mode="r+", encoding="utf-8") as p:
                json_users = json.load(p)
                new_dic={"user_id": self.pending_cr_user_id, "pass":self._hash_password(password)}
                json_users.append(new_dic)
                p.seek(0)  # comeback to start
                json.dump(json_users, p, indent=2)
                p.truncate()  # clear the rest file

            _username=self.pending_cr_user
            self.pending_cr_user = None
            self.pending_cr_user_id = None
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
                
            for user in users_namesjson:
                if user["username"]==username:
                    self.pending_user=username
                    self.pending_user_id=user["id"]
                    return "Login found, please insert password"       
            return "User doesn't exist"            
        except:
            return "User data corrupted or not found"
                    
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
                            return "You are already logged in as an admin"
                    else: 
                        self.pending_admin= None  # login in progress
                        return "Incorrect password"
            except:
                return "User data corrupted or not found"
            #user password

        with open(self.passfile, mode="r", encoding="utf-8") as read_file:
            users_pass = json.load(read_file)
            for pw in users_pass:
                if pw["user_id"]==self.pending_user_id:
                    if pw["pass"]==self._hash_password(pasw):
                        self.logged_user=self.pending_user # fully authenticated user
                        self.logged_user_id=self.pending_user_id # fully authenticated user
                        self.pending_user = None  # login in progress
                        self.pending_user_id = None  # login in progress
                        return f"You are logged in as {self.logged_user}"

            self.pending_user = None  # login in progress
            return "Incorrect password"

    def logout(self):
        self.logged_user= None
        self.logged_user_id= None
        return "User succesfully logout"
                  

    def status(self):
        if self.logged_user:
            return f"You are already logged in as {self.logged_user}"
        else:
            return "You are not logged in, please type your login and password"
            