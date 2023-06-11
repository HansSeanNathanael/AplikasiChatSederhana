import socket
import threading
import json
import re

class Server():
    def __init__(self, SERVER:str, PORT:int):
        self.FORMAT='utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        self.isListening = True
        self.thread = threading.Thread(target=self.listen, daemon=True)
        self.receiveSize = 8192

    def receive_all_data(self):
        received_data = ""
        while True:
            data = self.client.recv(self.receiveSize)
            if not data:
                break
            received_data += data.decode(self.FORMAT)
        print("KELUAR WHILE")
        return received_data

    def get_awalan_id(email:str):
        match = re.match(r'(.*?)@kelompok6\.co\.id', email)
        if match:
            return match.group(1)
        else:    
            return None
    
    def listen(self):
        while self.isListening:
            msg = self.client.recv(self.receiveSize).decode(self.FORMAT)
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
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def sign_up(self, user:str, password:str):
        self.send(f"REGISTER {user} {password}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        print("REGISTER STATUS = " + status)
        return json.loads(status)
    
    def logout(self, token:str):
        self.send(f"LOGOUT {token}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def create_group(self, token:str, email:str, password:str):
        self.send(f"BUAT_GRUP {token} {self.get_awalan_id(email)} {password}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def join_group(self, token:str, id_grup:str, password:str):
        self.send(f"GABUNG_GRUP {token} {id_grup} {password}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def join_group(self, token:str, id_grup:str):
        self.send(f"KELUAR_GRUP {token} {id_grup}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def send_chat(self, token:str, email_tujuan:str, chat_content:str):
        s = "\r\n"
        msg = f"CHAT{s}{token}{s}{email_tujuan}{s}{chat_content}{s}{s}"
        message = msg.encode(self.FORMAT)
        self.client.send(message)
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def send_file(self, token:str, email_tujuan:str, nama_file:str, isi_file):
        self.send(f"FILE {token} {email_tujuan} {nama_file} {isi_file}")
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def get_inbox(self, token:str):
        self.send(f"INBOX {token}")
        # status = self.receive_all_data()
        status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        # print(status)
        return json.loads(status)