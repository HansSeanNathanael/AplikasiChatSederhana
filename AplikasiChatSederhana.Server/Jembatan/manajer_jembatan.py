import json
import re

from ..Aplikasi.InterfacesJembatan.interface_manajer_jembatan import InterfaceManajerJembatan

from ..Aplikasi.Chat.Pesan.Data.pesan_chat import PesanChat
from ..Aplikasi.Chat.Pesan.Data.pesan_file import PesanFile
from .daftar_realm import DaftarRealm

class ManajerJembatan(InterfaceManajerJembatan):
    def __init__(self):
        self.daftar_realm = DaftarRealm()
        InterfaceManajerJembatan.__init__(self)
    
    def dapatkan_realm_tujuan(self, id_user : str) -> str:
        pattern = r"(?<=@)(\S+)"
        return re.search(pattern, id_user).group()

    def gabung_grup(self, id_user : str, id_grup : str, password : str) -> dict:
        realm_tujuan = self.dapatkan_realm_tujuan(id_grup)

        if realm_tujuan not in self.daftar_realm.daftar_realm:
            return { 'error' : 'Domain Tidak Dikenal' }
        
        self.daftar_realm.kunci_socket_realm(realm_tujuan)
        sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)

        if sock is None:
            try:
                self.daftar_realm.connect_socket(realm_tujuan)
                sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)
            except Exception as e:
                self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
                self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                return { 'error' : 'Connection Error' }
            
        try:
            sock.sendall(f"############".encode())
            hasil = ""
            while True:
                data = sock.recv(64)
                if data is None:
                    break
                
                hasil += data.decode()
                if hasil[-4:] == "\r\n\r\n":
                    hasil_object = json.loads(hasil)
                    self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                    return hasil_object

        except Exception as e:
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
            self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
            return { 'error' : json.dumps(e) }
        
            
        # socket mati dari lawan
        try:
            sock.shutdown()
            sock.close()
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
        except Exception as e:
            pass
        self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
        return { 'error' : 'Connection Error' }

        

    
    def keluar_grup(self, id_user : str, id_grup : str) -> dict:
        realm_tujuan = self.dapatkan_realm_tujuan(id_grup)

        if realm_tujuan not in self.daftar_realm.daftar_realm:
            return { 'error' : 'Domain Tidak Dikenal' }
        
        self.daftar_realm.kunci_socket_realm(realm_tujuan)
        sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)

        if sock is None:
            try:
                self.daftar_realm.connect_socket(realm_tujuan)
                sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)
            except Exception as e:
                self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
                self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                return { 'error' : 'Connection Error' }
        
        try:
            sock.sendall(f"############".encode())
            hasil = ""
            while True:
                data = sock.recv(64)
                if data is None:
                    break
                hasil += data.decode()
                if hasil[-4:] == "\r\n\r\n":
                    hasil_object = json.loads(hasil)
                    self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                    return hasil_object

        except Exception as e:
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
            self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
            return { 'error' : json.dumps(e) }
        
            
        # socket mati dari lawan
        try:
            sock.shutdown()
            sock.close()
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
        except Exception as e:
            pass
        self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
        return { 'error' : 'Connection Error' }
    
    def kirim_pesan_chat(self, pesan_chat : PesanChat) -> dict:
        realm_tujuan = self.dapatkan_realm_tujuan(pesan_chat.pesan.id_tujuan)

        if realm_tujuan not in self.daftar_realm.daftar_realm:
            return { 'error' : 'Domain Tidak Dikenal' }
        
        self.daftar_realm.kunci_socket_realm(realm_tujuan)
        sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)

        if sock is None:
            try:
                self.daftar_realm.connect_socket(realm_tujuan)
                sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)
            except Exception as e:
                self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
                self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                return { 'error' : 'Connection Error' }
            
        try:
            sock.sendall(f"############".encode())
            hasil = ""
            while True:
                data = sock.recv(64)
                if data is None:
                    break
                hasil += data.decode()
                if hasil[-4:] == "\r\n\r\n":
                    hasil_object = json.loads(hasil)
                    self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                    return hasil_object

        except Exception as e:
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
            self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
            return { 'error' : json.dumps(e) }
        
            
        # socket mati dari lawan
        try:
            sock.shutdown()
            sock.close()
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
        except Exception as e:
            pass
        self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
        return { 'error' : 'Connection Error' }
    
    def kirim_pesan_file(self, pesan_file : PesanFile) -> dict:
        realm_tujuan = self.dapatkan_realm_tujuan(pesan_file.pesan.id_tujuan)

        if realm_tujuan not in self.daftar_realm.daftar_realm:
            return { 'error' : 'Domain Tidak Dikenal' }
        
        self.daftar_realm.kunci_socket_realm(realm_tujuan)
        sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)

        if sock is None:
            try:
                self.daftar_realm.connect_socket(realm_tujuan)
                sock = self.daftar_realm.dapatkan_socket_dari_realm(realm_tujuan)
            except Exception as e:
                self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
                self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                return { 'error' : 'Connection Error' }
        
        try:
            sock.sendall(f"############".encode())
            hasil = ""
            while True:
                data = sock.recv(64)
                if data is None:
                    break
                hasil += data.decode()
                if hasil[-4:] == "\r\n\r\n":
                    hasil_object = json.loads(hasil)
                    self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
                    return hasil_object

        except Exception as e:
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
            self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
            return { 'error' : json.dumps(e) }
        
            
        # socket mati dari lawan
        try:
            sock.shutdown()
            sock.close()
            self.daftar_realm.hapus_pasangan_socket_dengan_realm(realm_tujuan)
        except Exception as e:
            pass
        self.daftar_realm.lepas_kunci_socket_realm(realm_tujuan)
        return { 'error' : 'Connection Error' }
    
    