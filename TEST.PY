import json

message_data="Jsondata/Messages.json"
messages={}
dic={}
max_messages_id=5
username="Iga"
def _msg_content(file):
        pass

def _search_next_id(file,username):
    with open(file, mode="r", encoding="utf-8") as f:
            messages=json.load(f)
            try:
                used_ids={list_element["id"] for list_element in messages[username]}      
                id=1
                while id in used_ids:
                        id+=1        
                return id
            except: return 1


def number_message(file,username):
    with open(file, mode="r", encoding="utf-8") as f:
        file=json.load(f)
        try:
            file=file[username]
            return print(f"You have {(len(file))} messagnes")   
        except: print("empty")

def read_message_all(file,username):
    with open(file, mode="r", encoding="utf-8") as f:
            messages=json.load(f)
            msgs=""
            try:
                for list_element in  messages[username]:       
                    msgs+= f"Message number:{list_element['id']} from {list_element['from']}: {list_element['content']}\n"            
                return print(msgs)    
            except: print("empty")
    
def write_message(file,username,message,receiver):
    with open(file, mode="r+", encoding="utf-8") as f:
        messages_file= json.load(f)
        #check if key exist
        if receiver not in messages_file:
            messages_file[receiver] = []
        new_message={"id":_search_next_id(file,receiver), "from":username, "content":message}
        print(type(messages_file))
        messages_file[receiver].append(new_message)

        f.seek(0)  # comeback to start
        json.dump(messages_file, f, indent=2)
        f.truncate()  # clear the rest file
        

#read_message_all(message_data,username)
#number_message(message_data,username)
#write_message(message_data,"Iga","Hello Iga", "Adam")
#write_message(message_data,"Paweł","Hello Iga tu Paweł", "Iga")
#write_message(message_data,"Damian","Hello Iga tu Damian", "Iga")

read_message_all(message_data,username)
number_message(message_data,username)
