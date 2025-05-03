import socket
import json
from datetime import datetime

HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
VERSION = "1.0.0"
CREATION_DATE = datetime.now()

class Server:
    def __init__(self):
        pass

    def handle_command(self,cmd,_current_time):

        match cmd:
            case "uptime": 
                return {"message1": "Server stands: ", "message2": str(_current_time)}
            case "info": 
                pass
            case "help": 
                {"message": "Aviable command: /"}
            case "stop": 
                pass
            case _: #deafult case
                return {"message": "Uknown command, try /help"}

    def start_server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            print(f"Server started at {HOST}:{PORT}")
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr} and {conn}")
                while True:
                    #server date
                    current_time=datetime.now()
                    current_time=current_time-CREATION_DATE

                    data = conn.recv(1024)
                    if not data:
                        break
                    command = data.decode('utf-8') # receive from client a task
                    response = self.handle_command(command,current_time)
                    conn.sendall(json.dumps(response).encode('utf-8'))
                    if command == "stop":
                        print("Shutting down server.")
                        break
                    
if __name__ == "__main__":
    server=Server()
    server.start_server()

