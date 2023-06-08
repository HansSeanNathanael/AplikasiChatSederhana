import json

from .Data.pesan_chat import PesanChat
from .Data.pesan_file import PesanFile
from ...Koneksi.daftar_klien import DaftarKlien

class PengirimPesan:
    def __init__(self, daftar_klien : DaftarKlien):
        self.daftar_klien = daftar_klien
    
    
      
    def kirim_pesan_chat(self, pesan_chat : PesanChat) -> bool:
        
        socket_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(pesan_chat.pesan.id_tujuan)
        
        if socket_tujuan is None:
            return False
        
        objek_chat = {
            "id_tujuan" : pesan_chat.pesan.id_tujuan,
            "id_pengirim" : pesan_chat.pesan.id_pengirim,
            "keperluan" : "PRIVATE",
            "bentuk_chat" : "CHAT",
            "chat" : pesan_chat.isi_pesan,
            "tanggal_diterima" : pesan_chat.pesan.tanggal_terima.strftime("%d-%m-%Y %H:%M:%S")
        }
        
        if pesan_chat.pesan.id_grup is not None:
            objek_chat["keperluan"] = "GRUP"
            objek_chat["id_grup"] = pesan_chat.pesan.id_grup
        
        hasil = json.dumps(objek_chat)
        hasil = hasil + "\r\n\r\n"
        
        try:
            socket_tujuan.sendall(hasil.encode())
            return True
        except OSError:
            try:
                socket_tujuan.close()
            except Exception:
                pass
            
            self.daftar_klien.hapus_socket(socket_tujuan)
            return False
    
    
       
    def kirim_pesan_file(self, pesan_file : PesanFile) -> bool:
        
        socket_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(pesan_file.pesan.id_tujuan)
        
        if socket_tujuan is None:
            return False
        
        objek_chat = {
            "id_tujuan" : pesan_file.pesan.id_tujuan,
            "id_pengirim" : pesan_file.pesan.id_pengirim,
            "keperluan" : "PRIVATE",
            "bentuk_chat" : "FILE",
            "nama_file" : pesan_file.nama_file,
            "isi_file" : pesan_file.isi_file_base64,
            "tanggal_diterima" : pesan_file.pesan.tanggal_terima.strftime("%d-%m-%Y %H:%M:%S")
        }
        
        if pesan_file.pesan.id_grup is not None:
            objek_chat["keperluan"] = "GRUP"
            objek_chat["id_grup"] = pesan_file.pesan.id_grup
        
        hasil = json.dumps(objek_chat)
        hasil = hasil + "\r\n\r\n"
        
        try:
            socket_tujuan.sendall(hasil.encode())
            return True
        except OSError:
            try:
                socket_tujuan.shutdown()
                socket_tujuan.close()
            except Exception:
                pass
            
            self.daftar_klien.hapus_socket(socket_tujuan)
            return False
    
    