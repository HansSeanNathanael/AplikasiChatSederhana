import json
import logging
import threading

from .daftar_klien import DaftarKlien
from ..Chat.chat_manager import ChatManager


class ProsesKlien(threading.Thread):
    def __init__(self, io_stream, alamat, daftar_klien : DaftarKlien, chat_manager : ChatManager):
        
        self.io_stream = io_stream
        self.alamat = alamat
        self.daftar_klien = daftar_klien
        self.chat_manager = chat_manager
        
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
                
                logging.warning(f"data dari client: {self.alamat} {message}")
                
                hasil = json.dumps(self.chat_manager.proses_request(message))
                hasil=hasil+"\r\n\r\n"
                
                logging.warning(f"data menuju client: {self.alamat} {hasil}")
                self.io_stream.sendall(hasil.encode())
                message = ""
        
        try:
            self.io_stream.shutdown()
            self.io_stream.close()
        except Exception as e:
            pass
         
        self.daftar_klien.hapus_socket(self.io_stream)