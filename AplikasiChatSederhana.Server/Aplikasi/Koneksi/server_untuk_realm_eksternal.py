import datetime
import logging
import socket
import threading

from .proses_realm_eksternal import ProsesRealmEksternal
from ..Chat.chat_manager_eksternal import ChatManagerEksternal
from ..Chat.Grup.manajemen_grup_eksternal import ManajemenGrupEksternal
from ..Chat.Pesan.manajemen_pesan_eksternal import ManajemenPesanEksternal

class ServerUntukRealmEksternal(threading.Thread):
    def __init__(self, pengaturan : dict, manajemen_grup_eksternal : ManajemenGrupEksternal, manajemen_pesan_eksternal : ManajemenPesanEksternal):
        self.manajemen_grup_eksternal = manajemen_grup_eksternal
        self.manajemen_pesan_eksternal = manajemen_pesan_eksternal
        
        self.domain = pengaturan["domain"]
        self.alamat_server = ("0.0.0.0", pengaturan["port_realm_eksternal"])
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        threading.Thread.__init__(self)
        
    def run(self):
        self.socket.bind(self.alamat_server)
        self.socket.listen(5)
        
        logging.warning(f"server untuk realm eksternal berjalan pada port: {self.alamat_server[1]}")
        
        while True:
            io_stream, alamat_realm = self.socket.accept()
            logging.warning(f"Koneksi masuk dari {alamat_realm} {datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            
            self.daftar_klien.tambah_socket(io_stream)
            proses_realm = ProsesRealmEksternal(io_stream, alamat_realm, ChatManagerEksternal(self.manajemen_grup_eksternal, self.manajemen_pesan_eksternal))
            proses_realm.start()