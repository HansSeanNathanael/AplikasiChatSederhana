from .Grup.manajemen_grup_eksternal import ManajemenGrupEksternal
from .Pesan.manajemen_pesan_eksternal import ManajemenPesanEksternal

class ChatManagerEksternal:
    def __init__(self, manajemen_grup_eksternal : ManajemenGrupEksternal, manajemen_pesan_eksternal : ManajemenPesanEksternal):
        self.manajemen_grup_eksternal = manajemen_grup_eksternal
        self.manajemen_pesan_eksternal = manajemen_pesan_eksternal
    
    def proses_request(self, request_str : str):
        request = request_str.split("\r\n")
        
        try:
            perintah = request[0].strip().upper()
            if perintah == "GABUNG_GRUP_EKSTERNAL":
                id_user_eksternal = request[1].strip()
                id_grup = request[2].strip()
                password = request[3].strip()
                return self.manajemen_grup_eksternal.gabung_grup(id_user_eksternal, id_grup, password)
            
            
            elif perintah == "KELUAR_GRUP_EKSTERNAL":
                id_user_eksternal = request[1].strip()
                id_grup = request[2].strip()
                return self.manajemen_grup_eksternal.keluar_grup(id_user_eksternal, id_grup)
            
            
            elif perintah == "CHAT_EKSTERNAL":
                id_pengirim_eksternal = request[1].strip()
                id_tujuan = request[2].strip()
                isi_chat = request[3].strip()
                return self.manajemen_pesan_eksternal.mengirim_chat(id_pengirim_eksternal, id_tujuan, None, isi_chat)
                        
                        
            elif perintah == "FILE_EKSTERNAL":
                id_pengirim_eksternal = request[1].strip()
                id_tujuan = request[2].strip()
                nama_file = request[3].strip()
                isi_file = request[3].strip()
                return self.manajemen_pesan_eksternal.mengirim_file(id_pengirim_eksternal, id_tujuan, None, nama_file, isi_file)
            
            
            elif perintah == "CHAT_GRUP_EKSTERNAL":
                id_pengirim_eksternal = request[1].strip()
                id_tujuan = request[2].strip()
                id_grup = request[3].strip()
                isi_chat = request[4].strip()
                return self.manajemen_pesan_eksternal.mengirim_chat(id_pengirim_eksternal, id_tujuan, id_grup, isi_chat)
                        
                        
            elif perintah == "FILE_GRUP_EKSTERNAL":
                id_pengirim_eksternal = request[1].strip()
                id_tujuan = request[2].strip()
                id_grup = request[3].strip()
                nama_file = request[4].strip()
                isi_file = request[5].strip()
                return self.manajemen_pesan_eksternal.mengirim_file(id_pengirim_eksternal, id_tujuan, id_grup, nama_file, isi_file)
            
            
            else:
                return {"error" : "request tidak ada"}
            
        except KeyError:
            return { 'error' : 'Informasi tidak ditemukan'}
        except IndexError:
            return {'error': 'Protokol salah'}