import logging
import socket
import threading
import datetime

from .daftar_klien import DaftarKlien
from .proses_klien import ProsesKlien
from ..Chat.chat_manager import ChatManager
from ..Chat.Autentikasi.autentikasi import Autentikasi
from ..Chat.Grup.manajemen_grup import ManajemenGrup
from ..Chat.Pesan.manajemen_pesan import ManajemenPesan

class Server(threading.Thread):
    
    def __init__(self, pengaturan : dict, daftar_klien : DaftarKlien, autentikasi : Autentikasi, manajemen_grup : ManajemenGrup, manajemen_pesan : ManajemenPesan):
        
        self.daftar_klien = daftar_klien
        self.autentikasi = autentikasi
        self.manajemen_grup = manajemen_grup
        self.manajemen_pesan = manajemen_pesan
        
        self.domain = pengaturan["domain"]
        self.alamat_server = ("0.0.0.0", pengaturan["port"])
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        self.socket_berdasarkan_id = {}
        self.id_berdasarkan_socket = {}
        
        threading.Thread.__init__(self)
        
    def run(self):
        self.socket.bind(self.alamat_server)
        self.socket.listen(5)
        
        while True:
            io_stream, alamat_klien = self.socket.accept()
            logging.warning(f"Koneksi masuk dari {alamat_klien} {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            self.daftar_klien.tambah_socket(io_stream)
            proses_klien = ProsesKlien(io_stream, alamat_klien, self.daftar_klien, ChatManager(io_stream, self.autentikasi, self.manajemen_grup, self.manajemen_pesan))
            proses_klien.start()
            