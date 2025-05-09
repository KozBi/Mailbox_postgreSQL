import json

class User_menager():
    def __init__(self):
        self.pending_user = None # login in progress
        self.pending_cr_user = None #on fucntion create -> pending user name
        self.pending_cr_password = None #on fucntion create -> insert sencond time passoword
        self.logged_in = None     # fully authenticated user

    userfile="Users.json"

    def _create_user(self,name, password):
        with open("Users.json", mode="r", encoding="utf-8") as read_file:
            users = json.load(read_file)
            if name in users:
                return "User already exists, try another name"
            # save password as pennding 
        self.pending_cr_password=password
        self.pending_cr_user = name
        return "Please insert password once again to confirm your password"
        
    def _create_user_passw(self,password):
        if password==self.pending_cr_password:
            with open("Users.json", mode="r+", encoding="utf-8") as f:
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

    def _check_login(self,username):
        if not self.pending_user:
            with open("Users.json", mode="r", encoding="utf-8") as read_file:
                users_pass = json.load(read_file)
                try:
                    if users_pass[username]:
                        self.pending_user=username
                        return "Login found, please insert password"       
                except:
                    return "User doesn't exist"
                
    def _check_passowrd(self,pasw):
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
            
    def handle_user_command(self, cmd):

        
        parts=cmd.split() #split string

        #check pennding password in account create process
        if self.pending_cr_password:
            return self._create_user_passw(cmd)
            
        # check create a new user
        if len(parts)==3 and parts[0]== "create":  # if 3 strings and first "create" check user in json file        
            return self._create_user(parts[1], parts[2])
        
        # check login
        if not self.pending_user:
            parts=cmd.split() #split string
            if len(parts)==2 and parts[0]== "login":  # if 2 strings and first "login" check user in json file        
                return self._check_login(parts[1])
            
        # check passowrd
        if self.pending_user:     
                return self._check_passowrd(cmd) 
        
        # command not related to this class
        return None               

