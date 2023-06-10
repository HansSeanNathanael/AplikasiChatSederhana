import socket
import threading
import json

class Server():
    def __init__(self, SERVER:str, PORT:int):
        self.FORMAT='utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.isListening = True
        self.thread = threading.Thread(target=self.listen, daemon=True)

    # FORMAT = 'utf-8'
    # PORT = 16590
    # SERVER = '0.tcp.ap.ngrok.io'
    # ADDR = (SERVER, PORT)
    # client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # client.connect(ADDR)
    
    def listen(self):
        while self.isListening:
            msg = self.client.recv(128).decode(self.FORMAT)
            print(f"[BROADCAST] {msg}")

    def send(self, msg):
        msg = msg.replace(' ',"\r\n") + '\r\n\r\n'
        message = msg.encode(self.FORMAT)
        self.client.send(message)

    def startListen(self):
        self.thread.start()

    def stopListen(self):
        self.isListening = False

    def sign_in(self, user:str, password:str):
        self.send(f"LOGIN {user} {password}")
        status = self.client.recv(128).decode(self.FORMAT)
        return json.loads(status)
    
    def sign_up(self, user:str, password:str):
        self.send(f"REGISTER {user} {password}")
        status = self.client.recv(128).decode(self.FORMAT)
        return json.loads(status)
    
    def logout(self, token:str):
        self.send(f"LOGOUT {token}")
        status = self.client.recv(128).decode(self.FORMAT)
        return json.loads(status)
    
    def create_group(self, token:str):
        self.send(f"LOGOUT {token}")
        status = self.client.recv(128).decode(self.FORMAT)
        return json.loads(status)