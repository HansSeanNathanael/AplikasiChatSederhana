import sqlite3

class KoneksiDatabase:
    def __init__(self, pengaturan) -> None:
        self.koneksi_database = sqlite3.connect(pengaturan["basis_data"])
        
    def koneksi(self) -> sqlite3.Connection:
        return self.koneksi_database