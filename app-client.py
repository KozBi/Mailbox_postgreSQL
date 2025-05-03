import socket
import json

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

class Clinet:
    def __init__(self):
        pass
                
    def start_clinet(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            print("Connected to server. Type 'help' for available commands.")
            while True:
                s.sendall(b"uptime")
                data = s.recv(1024)
                response = json.loads(data.decode('utf-8'))
                print(json.dumps(response, indent=2))


if __name__=="__main__":
    client=Clinet()
    client.start_clinet()
