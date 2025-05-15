import json

class MessagingService():
    def __init__(self,file):
        self.file=file

    def _search_next_id(self,username):
        with open(self.file, mode="r", encoding="utf-8") as f:
                messages=json.load(f)
                try:
                    used_ids={list_element["id"] for list_element in messages[username]}      
                    id=1
                    while id in used_ids:
                            id+=1        
                    return id
                except: return 1


    def number_message(self,user_id):
        with open(self.file, mode="r", encoding="utf-8") as f:
            file=json.load(f)
           # try:
            file_u=file[str(user_id)]
            return f"You have {(len(file_u[user_id]))} messages" 
         #   except: return "|Error file reading|"

    def read_message_all(self,user_id,umenager):
        with open(self.file, mode="r", encoding="utf-8") as f:
                messages=json.load(f)
                try:
                    msgs=""
                    u_message=messages[str(user_id)]
                    for _numb,t_dict in  enumerate(u_message):    
                       #String concatenation 
                        msgs+= f"Message number:{_numb+1} from {umenager.get_user_by_id((t_dict ['from']))}: {t_dict ['content']}\n"            
                    return msgs   
                except: print("empty")
        
    def write_message(self,username,receiver,message):
        with open(self.file, mode="r+", encoding="utf-8") as f:
            messages_file= json.load(f)
            #check if key exist
            if receiver not in messages_file:
                messages_file[receiver] = []
            new_message={"id":self._search_next_id(self.file,receiver), "from":username, "content":message}
            print(type(messages_file))
            messages_file[receiver].append(new_message)

            f.seek(0)  # comeback to start
            json.dump(messages_file, f, indent=2)
            f.truncate()  # clear the rest file

    def delete_message(self,username,id):
        with open(self.file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # do not copy message if id equel id
        # list comprehension
        if username in data:
            data[username] = [msg for msg in data[username] if msg['id'] != id]
            # write a new file
            try:
                with open(self.file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2,ensure_ascii=False)
                return f"Message {id} has been deleted"
            except: return f"Message {id} cannot be been deleted. Please conntact KozBi"


    def handle_message_command(self,cmd,user_id,UserMenage):
        parts=cmd.split() #split string
        
        if parts[0]=="msg" and user_id:
            return f"Nummber of messages for {user_id} : {self.number_message(user_id)}"
        
        # if (parts[0]=="msg" or parts[0]=="r" or parts[0]=="w" or parts[0]=="del" ) and not user_id:
        #     return "Plase login"
        
        if parts[0]=="rd":
            return self.read_message_all(user_id,UserMenage)
        
        if parts[0]=="w":
            try:
                return self.write_message(user_id,parts[1],parts[2])
            except:
                return "You are missing receiver or message text."
        
        if parts[0]=="del":
            try:   
                return self.delete_message(user_id,parts[1])
            except: return "Wrong parametr with command 'del', please inster message number also"
        else:
            return None