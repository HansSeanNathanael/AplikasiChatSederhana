import logging
import socket

class DaftarRealm:
    def __init__(self):
        self.daftar_realm : dict[str, socket.socket|None]= {
            "kelompok5" : None,
            "kelompok6" : None,
            "kelompok7" : None
        }
        self.daftar_address : dict[str, (str, int)|None] = {
            "kelompok5" : None,
            "kelompok6" : ("0.tcp.ap.ngrok.io", 11883),
            "kelompok7" : None

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
    
    def connect_socket(self, realm : str) -> None:
        new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        new_sock.connect(self.daftar_address[realm])
        self.pasangkan_socket_pada_realm(realm, new_sock)
    
    def reconnect_all(self):
        for realm in self.daftar_realm:
            self.connect_socket(realm)