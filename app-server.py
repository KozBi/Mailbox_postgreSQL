import socket
import json
from datetime import datetime
from login import Login_menager

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
VERSION = "1.0.1"
CREATION_DATE = datetime.now()

class Server:
    def __init__(self):
        self.login=Login_menager()

    response=None
    
    help_txt_js={"help": "Available command:\n'uptime'-return life time of server\n'info'-informs about server version\n'stop'-close the server"}

    def handle_command_dic(self,cmd):

                        # check login
        parts=cmd.strip().split()
        if len(parts)==2 and parts[0]== "login":          
            return self.login.check_login(parts[2])
        
        match str(cmd):
            case "uptime": 
                #calcute server date
                current_time=datetime.now()
                current_time=current_time-CREATION_DATE
                current_time= str(current_time).split('.')[0]
                return f"Server uptime: {current_time}"
            case "info": 
                return f"Server version: {VERSION}"
            case "help": 
                 return self.help_txt_js
            case "stop": 
                pass
            case _: #deafult case
                return "Uknown command, try 'help'"
            

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server started at {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr} and {conn}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8') # receive from client a task
                    self.response = self.handle_command_dic(command)
                    conn.sendall(json.dumps(self.response).encode('utf-8'))
                    
                    if command == "stop":
                        print("Shutting down server by user")
                        break
                    
if __name__ == "__main__":
    server=Server()
    server.start_server()

