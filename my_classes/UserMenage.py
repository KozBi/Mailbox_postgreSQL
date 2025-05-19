import json
import hashlib
#from my_classes.MessagingService import MessagingService

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
        self._pending_password_change=None

        self.userfile="Jsondata/Users.json"
        self.passfile="Jsondata/Passwords.json"

    @staticmethod
    def _hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _load_user_json(self):
        with open(self.userfile, 'r', encoding='utf-8') as f:
            return json.load(f)
        
    def _save_user_json(self, data):
        with open(self.userfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
        
    def _load_password_json(self):
        with open(self.passfile, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_password_json(self, data):
        with open(self.passfile, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def get_user_by_id(self,id):
        users = self._load_user_json()
        for user in users:
            if user["id"]==id:
                return user["username"]
        print(f"get_user_by_id:{id} no Value") 
        return None
         
    def get_id_by_user(self,username):
        users = self._load_user_json()
        for user in users:
            if user["username"]==username:
                return str(user["id"])
        print(f"get_id_by_user:{username} no Value") 
        return None
    

    def create_user(self,name, password):
        users = self._load_user_json()
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
            users = self._load_user_json()
                #find max id and +1. Generator used here!
            new_dic={"id": self.pending_cr_user_id , "username":self.pending_cr_user}
            users.append(new_dic)
            self._save_user_json(users)

            # create a pasword
            json_pass = self._load_password_json()
            json_pass[str(self.pending_cr_user_id)]=self._hash_password(password)
            self._save_password_json(json_pass)

            _username=self.pending_cr_user
            self.pending_cr_user = None
            self.pending_cr_user_id = None
            self.pending_cr_password = None
            return f"User '{_username}' created successfully."
        else:
            return "Passwords do not match"

    def check_login(self,username):       
        #login as user
        users_namesjson = self._load_user_json()
            
        for user in users_namesjson:
            if user["username"]==username: #dictionary.get(keyname, value), Optional. A value to return if the specified key does not exist.
                # check if user is admin
                if user.get("is_admin", False):
                    self.pending_admin=True
                    self.pending_user=username
                    self.pending_user_id=user["id"]
                    return "You are trying login as an admin, please insert password"  
                self.pending_user=username
                self.pending_user_id=user["id"]
                return "Login found, please insert password"       
        return "User doesn't exist"            
                    
    def check_password(self,pasw):
        _txt=""
        json_pasw = self._load_password_json()
        user_key=str(self.pending_user_id)
        if json_pasw.get(user_key, None):  
                if json_pasw[user_key]==self._hash_password(pasw):
                #login as admin
                    if self.pending_admin:
                        self.pending_admin= None
                        self.logged_admin = True  
                        _txt=" You are loged in as admin"

                    self.logged_user=self.pending_user # fully authenticated user
                    self.logged_user_id=self.pending_user_id # fully authenticated user
                    self.pending_user = None  # login in progress
                    self.pending_user_id = None  # login in progress
                    return f"You are logged in as {self.logged_user}{_txt}"

        self.pending_user = None  # login in progress
        return "Incorrect password"
        
    def change_password(self,pasw):
        #check if user is loged
        if not self.logged_user_id:
            return "You must be logged in to change your password."       
        #check if the 2nd password is the same like 1st
        elif self._pending_password_change and self._pending_password_change!=pasw:
            self._pending_password_change=None
            return "Passwords are not the same"       
        #password are the same, save new password
        elif self._pending_password_change and self._pending_password_change==pasw:
            data=self._load_password_json()
            user_key=str(self.logged_user_id)
            print(f"Key error{user_key}")
            if data.get(user_key, None):                
                data[user_key]=self._hash_password(pasw)
                self._save_password_json(data)
                self._pending_password_change=None
                return "Password has been changed"           
        #safe pending password
        else: 
            self._pending_password_change=pasw
            return "Please enter password once again"
        

    def logout(self):
        self.logged_user= None
        self.logged_user_id= None
        self.logged_admin = None
        return "User succesfully logout"
                  

    def status(self):
        if self.logged_user:
            return f"You are already logged in as {self.logged_user}"
        else:
            return "You are not logged in, please type your login and password"
        
    #admin acces 
    #     
    def admin_list_users(self):
        users="List of all users:\n"
        data=self._load_user_json()
        for user in data:
            user=user["username"]
            users+=f"{user}\n"
        return users


            