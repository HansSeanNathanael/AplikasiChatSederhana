import logging
import socket

class DaftarRealm:
    def __init__(self):
        self.daftar_realm : dict[str, socket.socket|None]= {
            "kelompok..." : None,
            "kelompok...." : None,
            "kelompok....." : None
        }
        
    def pasangkan_socket_pada_realm(self, realm : str, io_stream : socket.socket) -> None:
        if realm in self.daftar_realm:
            self.daftar_realm[realm] = io_stream
            
    def hapus_pasangan_socket_dengan_realm(self, realm : str) -> None:
        if realm in self.daftar_realm:
            self.daftar_realm[realm] = None
    
    def dapatkan_socket_dari_realm(self, realm : str) -> socket.socket:
        if realm in self.daftar_realm:
            return self.daftar_realm[realm]
        return None