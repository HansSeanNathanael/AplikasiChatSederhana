import socket
import threading
import json
import re

isListening = True

class Server():
    def __init__(self, SERVER:str, PORT:int):
        self.FORMAT='utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        # self.isListening = True
        # self.thread = threading.Thread(target=self.listen, daemon=True)
        self.receiveSize = 32

    def receive_all_data(self):
        received_data = ""
        while True:
            data = self.client.recv(self.receiveSize)
            if not data:
                break

            d = data.decode(self.FORMAT)
            received_data = received_data + d

            if received_data[-4:] == '\r\n\r\n':
                break
        return received_data
    
    def receive_all_data_listen(self):
        received_data = ""
        while True and isListening == True:
            data = self.client.recv(self.receiveSize)
            if not data:
                break

            d = data.decode(self.FORMAT)
            received_data = received_data + d

            if received_data[-4:] == '\r\n\r\n':
                break
        return received_data

    def get_awalan_id(email:str):
        match = re.match(r'(.*?)@kelompok6\.co\.id', email)
        if match:
            return match.group(1)
        else:    
            return None
    
    def listen(self):
        global isListening
        while True:
            # if self.isListening == False:
            #     break
            if isListening == False:
                break
            print("Tes Befire")
            msg = self.receive_all_data_listen()
            print(f"[BROADCAST] {msg}")
        print("Thread Stop")

    def send(self, msg):
        msg = msg.replace(' ',"\r\n") + '\r\n\r\n'
        message = msg.encode(self.FORMAT)
        self.client.send(message)

    def startListen(self):
        # self.isListening = True
        global isListening
        if (isListening == False):
            isListening = True
            print("start listen")
            # self.thread.start()
            threading.Thread(target=self.listen, daemon=True).start()

    def stopListen(self):
        # self.isListening = False
        global isListening
        isListening = False
        print("stop listen")

    def sign_in(self, user:str, password:str):
        self.send(f"LOGIN {user} {password}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        print("LOGIN STATUS = " + status)
        return json.loads(status)
    
    def sign_up(self, user:str, password:str):
        self.send(f"REGISTER {user} {password}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        print("REGISTER STATUS = " + status)
        return json.loads(status)
    
    def logout(self, token:str):
        self.stopListen()

        self.send(f"LOGOUT {token}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def create_group(self, token:str, email:str, password:str):
        self.stopListen()

        self.send(f"BUAT_GRUP {token} {self.get_awalan_id(email)} {password}")
        status = self.receive_all_data()        
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)

        self.startListen()
        return json.loads(status)
    
    def join_group(self, token:str, id_grup:str, password:str):
        self.stopListen()
        
        self.send(f"GABUNG_GRUP {token} {id_grup} {password}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)

        self.startListen()
        return json.loads(status)
    
    def keluar_group(self, token:str, id_grup:str):
        self.stopListen()

        self.send(f"KELUAR_GRUP {token} {id_grup}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)
    
    def send_chat(self, token:str, email_tujuan:str, chat_content:str):
        self.stopListen()

        s = "\r\n"
        msg = f"CHAT{s}{token}{s}{email_tujuan}{s}{chat_content}{s}{s}"
        message = msg.encode(self.FORMAT)
        self.client.send(message)
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)

        self.startListen()
        return json.loads(status)
    
    def send_file(self, token:str, email_tujuan:str, nama_file:str, isi_file:str):
        self.stopListen()

        self.send(f"FILE {token} {email_tujuan} {nama_file} {isi_file}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)

        self.startListen()
        return json.loads(status)
    
    def get_inbox(self, token:str):
        self.send(f"INBOX {token}")
        status = self.receive_all_data()
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        return json.loads(status)