import json

class MessagingService():
    def __init__(self,f_message):
        self.f_message=f_message #f_message message
        self._write_m_tpl=None #wrtie message tuple - help variable for write message


    def _load_messages(self):
        with open(self.f_message, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _save_messages(self, data):
        with open(self.f_message, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def _search_next_id(self,username):
        messages=self._load_messages()
        try:
            used_ids={list_element["id_msg"] for list_element in messages[username]}      
            id=1
            while id in used_ids:
                    id+=1        
            return id
        except: return 1

    def number_message(self,user_id):
        f_message=self._load_messages()
        try:
            file_u=f_message[str(user_id)]
            return f"You have {(len(file_u))} messages" 
        except: return "You don't have messages"

    def read_message_all(self,user_id,Umenager):
        messages=self._load_messages()
        try:
            msgs=""
            u_message=messages[str(user_id)]
            for t_dict in (u_message):    
                #String concatenation 
                msgs+= f"Message number:{t_dict ['id_msg']} from {Umenager.get_user_by_id((t_dict ['from']))}: {t_dict ['content']}\n"            
            return msgs   
        except: print("empty")
        
    def receiver_found(self,user_id,receiver,Umenager):
        _receiver=Umenager.get_id_by_user(receiver)
        if _receiver:
            self._write_m_tpl=(user_id,_receiver)
            return f"User: {receiver} found, please type a message --- max 255 of characters"
        else:
            self._write_m_tpl=None
            return f"{receiver} not found in userlist"
 
    def write_message(self,sender,receiver,message,Umenager):
        if len(message) > 255:
            return "Message too long (max 255 characters)."

        messages_file= self._load_messages()
        #check if key exist
        if receiver not in messages_file:
            messages_file[receiver] = []
        new_message={"id_msg":self._search_next_id(receiver),
                    "from":sender,
                    "content":message}              
        messages_file[receiver].append(new_message)

        self._save_messages(messages_file)
        self._write_m_tpl=None
        return "Message sent"

    def delete_message(self,username,id):
        data = self._load_messages()

        # do not copy message if id equel id
        # list comprehension
        if username in data:
            data[username] = [msg for msg in data[username] if msg['id'] != id]
            # write a new f_message
            try:
                self._save_messages(data)
                return f"Message {id} has been deleted"
            except: return f"Message {id} cannot be been deleted. Please conntact KozBi"

    def handle_message_command(self,command,user_id,UserMenage):

        if self._write_m_tpl:
            return self.write_message(self._write_m_tpl[0],self._write_m_tpl[1],command,UserMenage)

        parts=command.split() #split string
        
        if parts[0]=="msg" and user_id:
            return f"Nummber of messages for {UserMenage.get_user_by_id(user_id)} : {self.number_message(user_id)}"
        
        if parts[0]=="rd":
            return self.read_message_all(user_id,UserMenage)
        
        if parts[0]=="w":
                return self.receiver_found(user_id,parts[1],UserMenage)
        
        if parts[0]=="del":
            try:   
                return self.delete_message(user_id,parts[1])
            except: return "Wrong parameter with command 'del', please inster message number also"
        else:
            return None