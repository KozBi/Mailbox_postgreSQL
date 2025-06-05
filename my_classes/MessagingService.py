from my_classes.UserMenager import UserMenager as UM
from my_classes.DataBaseService import DataBaseService


class MessagingService():
    def __init__(self,database:DataBaseService):
        self.database=database 
        self._write_m_tpl=None #wrtie message tuple - help variable for write message

        self.max_messages=5

    def _load_messages(self,id):
        with open(self.f_message, 'r', encoding='utf-8') as f:
            return json.load(f)

    # def _save_messages(self, data):
    #     with open(self.f_message, 'w', encoding='utf-8') as f:
    #         json.dump(data, f, indent=2, ensure_ascii=False)

    # def _search_next_id(self,username):
    #     messages=self._load_messages()
    #     try:
    #         used_ids={list_element["id_msg"] for list_element in messages[username]}      
    #         id=1
    #         while id in used_ids:
    #                 id+=1        
    #         return id
    #     except(KeyError, TypeError): return 1

    def _count_message_num(self,user_id):
        return self.database.msg_count(user_id)

    def number_message(self,user_id):
            _num=self._count_message_num(user_id)   
            if _num<self.max_messages:
                return f"You have {_num} messages" 
            elif _num==0:
                return "You don't have messages" 
            else: return f"You have {_num} messages. Your box messages is full. Please delete messages using del command"

    def read_message_all(self,Umenager:UM,user_id=None):
        messages=self._load_messages()
        msgs=""
        if not user_id:
            user_id=Umenager.logged_user_id
        try:
            u_message=messages[str(user_id)]
            for t_dict in (u_message):    
                #String concatenation 
                msgs+= f"Message number:{t_dict ['id_msg']} from {Umenager.get_user_by_id((t_dict ['from']))}: {t_dict ['content']}\n"    
            if msgs!="":
                if self._count_message_num(u_message)>=self.max_messages:
                    return f"{msgs} +  Your's box messages is full. Please delete messages using del command"
                else: return msgs   
            else: return "You dont have any messages"
        except(KeyError): return f"This user doesn't exist:{user_id}"
        
    def receiver_found(self,receiver,Umenager:UM):
        _receiver=Umenager.get_id_by_user(receiver)
        user_id=Umenager.logged_user_id
        if _receiver:
            self._write_m_tpl=(user_id,_receiver)
            return f"User: {receiver} found, please type a message --- max 255 of characters"
        else:
            self._write_m_tpl=None
            return f"{receiver} not found in userlist"
 
    def write_message(self,sender,receiver,message):
        if len(message) > 255:
            self._write_m_tpl=None
            return "Message too long (max 255 characters)."

        messages_file= self._load_messages()
        #check if key exist
        if receiver not in messages_file:
            messages_file[receiver] = []
        if self._count_message_num(messages_file[receiver])>=5:
            self._write_m_tpl=None
            return "The recipient's message box is full. You cannot send a message"
        new_message={"id_msg":self._search_next_id(receiver),
                    "from":sender,
                    "content":message}              
        messages_file[receiver].append(new_message)

        self._save_messages(messages_file)
        self._write_m_tpl=None
        return "Message sent"

    def delete_message(self,id,Umenager:UM,username=None):
        data = self._load_messages()
        new_data=[]
        if not username:
            username=str(Umenager.logged_user_id)
        if username in data:
            if id=="-a":
                new_data=[]
            else:
                for msg in data[username]:
                    if str(msg['id_msg']) != id:
                        new_data.append(msg)
            data[username]=new_data
            self._save_messages(data)
            if id=="-a":
                return f"All messages has been deleted"
            return f"Message {id} has been deleted"

    def handle_message_command(self,command,UserMenage:UM):

        if self._write_m_tpl:
            return self.write_message(self._write_m_tpl[0],self._write_m_tpl[1],command)

        parts=command.split() #split string
        
        if parts[0]=="msg" and UserMenage.logged_user_id:
            return f"Nummber of messages for {UserMenage.logged_user} : {self.number_message(UserMenage.logged_user_id)}"
        
        if parts[0]=="rd":
            return self.read_message_all(UserMenage)
        
        if parts[0]=="w" and len(parts)>1:
                return self.receiver_found(parts[1],UserMenage)
        elif parts[0]=="w": return "Please specify a user to write to"
        
        if parts[0]=="del" and len(parts)>1:
            return self.delete_message(parts[1],UserMenage)
        elif parts[0]=="del":
            return "Wrong parameter with command 'del', please enter message number also ['-a' delete all message]"
        
        #admin accees:
        if UserMenage.logged_admin:
            
            if parts[0]=="admin_rd" and len(parts)>1:
                who=UserMenage.get_id_by_user(parts[1])
                if who:
                    return self.read_message_all(UserMenage,who)
                else:
                    return "Please eneter correct username -- admin_rd 'username'"
            elif parts[0]=="admin_rd":
                return "Please eneter username -- admin_rd 'username'"
            
            if parts[0]=="admin_del" and len(parts)>2:
                who=UserMenage.get_id_by_user(parts[1])
                if who:
                    return self.delete_message(parts[2],UserMenage,who)
                else: return "This user doesn't exist"
            elif parts[0]=="admin_del":
                return "admin_del-- admin_del 'username' 'message_number_to_delete - ['-a' delete all message]"
        
        else:
            return None