import json
import logging
import threading

from ..Chat.chat_manager_eksternal import ChatManagerEksternal


class ProsesRealmEksternal(threading.Thread):
    def __init__(self, io_stream, alamat, chat_manager_eksternal : ChatManagerEksternal):
        
        self.io_stream = io_stream
        self.alamat = alamat
        self.chat_manager_eksternal = chat_manager_eksternal
        
        threading.Thread.__init__(self)
        
    def run(self):
        message =""
        
        while True:
            sub_message = self.io_stream.recv(32)
            
            if not sub_message:
                break
            
            sub_message_decoded = sub_message.decode()
            message = message + sub_message_decoded
            
            if message[-4:]=='\r\n\r\n':
                
                logging.warning(f"data dari realm: {self.alamat} {message}")
                
                hasil = json.dumps(self.chat_manager_eksternal.proses_request(message))
                hasil=hasil+"\r\n\r\n"
                
                logging.warning(f"data menuju realm: {self.alamat} {hasil}")
                self.io_stream.sendall(hasil.encode())
                message = ""
        
        try:
            self.io_stream.shutdown()
            self.io_stream.close()
        except Exception as e:
            pass