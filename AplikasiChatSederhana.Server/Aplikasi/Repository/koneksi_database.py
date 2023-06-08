import sqlite3
import threading

class KoneksiDatabase:
    def __init__(self, pengaturan) -> None:
        self.koneksi_database = threading.local() 
        self.koneksi_database.koneksi = sqlite3.connect(pengaturan["basis_data"], check_same_thread=False)
        
    def koneksi(self) -> sqlite3.Connection:
        return self.koneksi_database.koneksi