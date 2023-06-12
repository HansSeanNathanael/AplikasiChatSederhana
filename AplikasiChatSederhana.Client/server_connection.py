import socket
import threading
import json
import re
import base64
from time import sleep
from database import *

isListening = False
gblMsg = ""
gblBool = ""
gblIsSendChat = False

class Server():
    def __init__(self, SERVER:str, PORT:int):
        self.FORMAT='utf-8'
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((SERVER, PORT))
        # self.isListening = True
        # self.thread = threading.Thread(target=self.listen, daemon=True)
        self.receiveSize = 32

    def getGlobalMsg(self):
        global gblBool
        return gblBool
    
    def setGlobalMsgEmpty(self):
        global gblBool
        gblBool = ""

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
            print("Masuk receivel all data\n")
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
        global gblMsg
        global gblBool
        global gblIsSendChat
        print("[THREAD STOP]")
        while True:
            # if self.isListening == False:
            #     break
            if isListening == False:
                break
            print("Tes Befire")
            print("gblMsg is " + gblMsg)
            while(gblMsg != ""):
                sleep(2)
            gblMsg = self.receive_all_data_listen()
            sleep(5)
            if(gblMsg != ""):
                print("[LIVECHAT]" + gblMsg)
                print(gblIsSendChat)
                if (gblIsSendChat == False):
                    gblBool = json.loads(gblMsg)
                sleep(2)
                print("[REWRITE gblMsg] ")
                gblMsg = ""
        print("[THREAD STOP]")

    def send(self, msg):
        msg = msg.replace(' ',"\r\n") + '\r\n\r\n'
        message = msg.encode(self.FORMAT)
        self.client.send(message)

    def startListen(self):
        # self.isListening = True
        global isListening
        if (isListening == False):
            isListening = True
            print("[LISTENING]")
            # self.thread.start()
            threading.Thread(target=self.listen, daemon=True).start()

    def stopListen(self):
        # self.isListening = False
        global isListening
        isListening = False
        print("[STOP LISTENING]")

    def sign_in(self, user:str, password:str):
        self.send(f"LOGIN {user} {password}")
        status = self.receive_all_data()

        print("LOGIN STATUS = " + status)
        
        return json.loads(status)
    
    def sign_up(self, user:str, password:str):
        self.send(f"REGISTER {user} {password}")

        status = self.receive_all_data()

        print("REGISTER STATUS = " + status)
        
        return json.loads(status)
    
    def logout(self, token:str):

        self.send(f"LOGOUT {token}")
        global gblMsg
        # status = self.receive_all_data()

        print("[LOGOUT gblMsg 1]" + gblMsg)
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        while(gblMsg == ""):
            sleep(2)
        print("[LOGOUT gblMsg 2]" + gblMsg)
        
        
        temp = gblMsg
        self.stopListen()
        gblMsg = ""
        print("[LOGOUT]" + temp)
        return json.loads(temp)
    
    def create_group(self, token:str, email:str, password:str):
        # self.stopListen()

        self.send(f"BUAT_GRUP {token} {self.get_awalan_id(email)} {password}")
        global gblMsg
        # status = self.receive_all_data()
        # 
        # print(gblMsg)        
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        while(gblMsg == ""):
            sleep(2)


        # self.startListen()
        
        
        temp = gblMsg
        gblMsg = ""
        return json.loads(temp)
    
    def join_group(self, token:str, id_grup:str, password:str):
        # self.stopListen()
        
        self.send(f"GABUNG_GRUP {token} {id_grup} {password}")
        global gblMsg
        # status = self.receive_all_data()

        print(gblMsg)
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        while(gblMsg == ""):
            sleep(2)


        # self.startListen()
        
        
        temp = gblMsg
        gblMsg = ""
        return json.loads(temp)
    
    def keluar_group(self, token:str, id_grup:str):
        # self.stopListen()

        self.send(f"KELUAR_GRUP {token} {id_grup}")
        global gblMsg
        # status = self.receive_all_data()

        print(gblMsg)
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        while(gblMsg == ""):
            sleep(2)

        
        
        temp = gblMsg
        gblMsg = ""
        return json.loads(temp)
    
    def send_chat(self, token:str, email_tujuan:str, chat_content:str):
        # self.stopListen()

        s = "\r\n"
        msg = f"CHAT{s}{token}{s}{email_tujuan}{s}{chat_content}{s}{s}"
        message = msg.encode(self.FORMAT)
        global gblIsSendChat
        gblIsSendChat = True
        self.client.send(message)
        
        # status = self.receive_all_data()

        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        global gblMsg

        # nunggu sampai tidak kosong
        while(gblMsg == ""):
            sleep(2)

        print("[SENDCHAT]" + gblMsg + "\n")
        # self.startListen()
        
        
        temp = gblMsg
        gblMsg = ""
        gblIsSendChat = False
        return json.loads(temp)
    
    def send_file(self, token:str, email_tujuan:str, nama_file:str, isi_file:str):
        # self.stopListen()
        global gblIsSendChat
        gblIsSendChat = True
        self.send(f"FILE {token} {email_tujuan} {nama_file} {isi_file}")
        global gblMsg
        # status = self.receive_all_data()

        print(gblMsg)
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        while(gblMsg == ""):
            sleep(2)


        # self.startListen()
        
        
        temp = gblMsg
        gblMsg = ""
        gblIsSendChat = False
        return json.loads(temp)
    
    def get_inbox(self, token:str):
        self.send(f"INBOX {token}")
        # global gblMsg
        status = self.receive_all_data()

        # print(gblMsg)
        # status = self.client.recv(self.receiveSize).decode(self.FORMAT)
        # while(gblMsg == ""):
        #     sleep(2)

        
        self.startListen()
        return json.loads(status)