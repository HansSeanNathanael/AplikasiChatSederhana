import threading
import socket

class DaftarRealm:
    def __init__(self):
        self.daftar_realm : dict[str, socket.socket|None]= {
            "kelompok5" : None,
            "kelompok7" : None
        }
        self.daftar_address : dict[str, (str, int)|None] = {
            "kelompok5" : None,
            "kelompok7" : None
        }
        self.daftar_kunci_socket_realm : dict[str, threading.Lock] = {
            "kelompok5" : threading.Lock(),
            "kelompok7" : threading.Lock()
        }
        
    def pasangkan_socket_pada_realm(self, realm : str, io_stream : socket.socket) -> None:
        if realm in self.daftar_realm:
            self.daftar_realm[realm] = io_stream
            
    def hapus_pasangan_socket_dengan_realm(self, realm : str) -> None:
        if realm in self.daftar_realm:
            self.daftar_realm[realm] = None
    
    def kunci_socket_realm(self, realm : str) -> bool:
        if realm in self.daftar_kunci_socket_realm:
            self.daftar_kunci_socket_realm[realm].acquire()
            return True
        return False
    
    def lepas_kunci_socket_realm(self, realm : str) -> bool:
        if realm in self.daftar_kunci_socket_realm:
            self.daftar_kunci_socket_realm[realm].release()
            return True
        return False
    
    def dapatkan_socket_dari_realm(self, realm : str) -> socket.socket:
        self.kunci_socket_realm(realm)
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