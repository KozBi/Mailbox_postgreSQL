import json

class MessagingService():
    def __init__(self):
        self.message_data="Jsondata/Messages.json"



    def check_num_message(self,username):
        with open(self.message_data, mode="r", encoding="utf-8") as f:
            messages=json.load(f)
            messagne_num=len(messages[username])
            if messagne_num:
                return f"{messagne_num}"
            else:
                return "File corrupted"
        

    def write_messagage(self,message):
        pass

    def read_message(self):
        with open(self.message_data, mode="r", encoding="utf-8") as f:           
            pass

    def handel_message_command(self,cmd,username):
        parts=cmd.split() #split string

        if parts[0]=="msg" and username:
            return f"Nummber of messages for {username} : {self.check_num_message(username)}"
        
        if parts[0]=="msg" and not username:
            return "Plase login"
        else:
            return None