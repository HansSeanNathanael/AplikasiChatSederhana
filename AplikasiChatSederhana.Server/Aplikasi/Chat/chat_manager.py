from .Autentikasi.autentikasi import Autentikasi
from .Grup.manajemen_grup import ManajemenGrup
from .Pesan.manajemen_pesan import ManajemenPesan

class ChatManager:
    def __init__(self, io_stream, autentikasi : Autentikasi, manajemen_grup : ManajemenGrup, manajemen_pesan : ManajemenPesan):
        self.autentikasi = autentikasi
        self.manajemen_grup = manajemen_grup
        self.manajemen_pesan = manajemen_pesan
        self.io_stream = io_stream
    
    def proses_request(self, request_str : str):
        request = request_str.split("\r\n")
        
        try:
            perintah = request[0].strip().upper()
            if perintah == "REGISTER":
                awalan_id=request[1].strip()
                password=request[2].strip()
                return self.autentikasi.register(awalan_id, password)
                
            
            elif perintah == "LOGIN":
                id=request[1].strip()
                password=request[2].strip()
                return self.autentikasi.login(id, password, self.io_stream)    
            
            
            elif perintah == "LOGOUT":
                token = request[1].strip()
                return self.autentikasi.logout(token, self.io_stream)
            
            
            elif perintah == "BUAT_GRUP":
                token = request[1].strip()
                awalan_id = request[2].strip()
                password = request[3].strip()
                return self.manajemen_grup.buat_grup(token, awalan_id, password)
            
            
            elif perintah == "GABUNG_GRUP":
                token = request[1].strip()
                id_grup = request[2].strip()
                password = request[3].strip()
                return self.manajemen_grup.gabung_grup(token, id_grup, password)
            
            
            elif perintah == "KELUAR_GRUP":
                token = request[1].strip()
                id_grup = request[2].strip()
                return self.manajemen_grup.keluar_grup(token, id_grup)
            
            
            elif perintah == "CHAT":
                token = request[1].strip()
                id_tujuan = request[2].strip()
                isi_chat = request[3].strip()
                return self.manajemen_pesan.mengirim_chat(token, id_tujuan, isi_chat)
            
            
            elif perintah == "FILE":
                token = request[1].strip()
                id_tujuan = request[2].strip()
                nama_file = request[3].strip()
                isi_file = request[4].strip()
                return self.manajemen_pesan.mengirim_file(token, id_tujuan, nama_file, isi_file)
            
            elif perintah == "INBOX":
                token = request[1].strip()
                return self.manajemen_pesan.ambil_inbox(token)
            
        except KeyError:
            return { 'error' : 'Informasi tidak ditemukan'}
        except IndexError:
            return {'error': 'Protokol salah'}