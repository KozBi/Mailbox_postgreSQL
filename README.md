🔌 Python Client-Server Application with User Management and Messaging
This project is a socket-based client-server application written in Python, designed for local TCP communication. Beyond basic command processing, it introduces user authentication and a simple private messaging system, simulating a minimalistic chat environment.

🧠 Key Features

TCP socket communication over localhost (127.0.0.1)

User system with registration, login, and session handling. All data are stored in Json files.

Private messaging between connected users

Command interface with built-in server commands:

help – display available commands

uptime – show how long the server has been running

info – return server version

stop – safely shut down the server

⚙️ How it works
Clients connect to the server and authenticate using a simple text-based protocol. After logging in, users can interact via commands or send messages to other online users.