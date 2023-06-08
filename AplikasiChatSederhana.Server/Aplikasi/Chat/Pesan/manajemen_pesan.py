import datetime
import re
import uuid

from .pengirim_pesan import PengirimPesan
from ...InterfacesJembatan.interface_manajer_jembatan import InterfaceManajerJembatan

from ...Repository.repository_akun import RepositoryAkun
from ...Repository.repository_pesan import RepositoryPesan
from ...Repository.repository_grup import RepositoryGrup

from ..Pesan.Data.pesan import Pesan
from ..Pesan.Data.pesan_chat import PesanChat
from ..Pesan.Data.pesan_file import PesanFile

class ManajemenPesan:
    def __init__(self, domain : str, pengirim_pesan : PengirimPesan, interface_manajer_jembatan : InterfaceManajerJembatan,  repository_akun : RepositoryAkun, repository_pesan : RepositoryPesan, repository_grup : RepositoryGrup) -> None:
        self.domain = domain
        self.pengirim_pesan = pengirim_pesan
        self.interface_manajer_jembatan = interface_manajer_jembatan
        self.repository_akun = repository_akun
        self.repository_pesan = repository_pesan
        self.repository_grup = repository_grup
        
    def dapatkan_realm_tujuan(self, id_user : str) -> str:
        pattern = r"(?<=@)(\S+)"
        return re.search(pattern, id_user).group()
        
    def mengirim_chat(self, token : str, id_tujuan : str, isi_chat : str) -> dict:
        
        pengirim = self.repository_akun.ambil_dari_token(token)
        
        if pengirim is None:
            return {"error" : "autentikasi salah"}
        
        domain_tujuan = self.dapatkan_realm_tujuan(id_tujuan)
        
        if domain_tujuan != self.domain:
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "chat", tanggal_diterima)
            pesan_chat_baru = PesanChat(data_pesan, isi_chat)
            return self.interface_manajer_jembatan.kirim_pesan_chat(pesan_chat_baru)
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now()
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "chat", tanggal_diterima)
            pesan_chat_baru = PesanChat(data_pesan, isi_chat)
            
            if not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru):
                self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != pengirim.id:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_anggota, tujuan.id, "chat", tanggal_diterima)
                    pesan_chat_baru = PesanChat(data_pesan, isi_chat)
                    
                    if domain_tujuan != self.domain:
                        self.interface_manajer_jembatan.kirim_pesan_chat(pesan_chat_baru)
                    
                    else:
                        if not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru):
                            self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}
    
    
    
    def mengirim_file(self, token : str, id_tujuan : str, nama_file : str, isi_file_base64 : str) -> dict:
        
        pengirim = self.repository_akun.ambil_dari_token(token)
        
        if pengirim is None:
            return {"error" : "autentikasi salah"}
        
        domain_tujuan = self.dapatkan_realm_tujuan(id_tujuan)
        
        if domain_tujuan != self.domain:
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "file", tanggal_diterima)
            pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
            return self.interface_manajer_jembatan.kirim_pesan_file(pesan_file_baru)
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now()
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "file", tanggal_diterima)
            pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
            
            if not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru):
                self.repository_pesan.tambah_pesan_file(pesan_file_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != pengirim.id:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_anggota, tujuan.id, "file", tanggal_diterima)
                    pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
                    
                    if domain_tujuan != self.domain:
                        return self.interface_manajer_jembatan.kirim_pesan_file(pesan_file_baru)
                    else:
                        if not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru):
                            self.repository_pesan.tambah_pesan_file(pesan_file_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}
    
    
    
    def compare(item1 : PesanChat|PesanFile, item2 : PesanChat|PesanFile):
        data_tanggal_item1 = item1.pesan.tanggal_terima
        data_tanggal_item2 = item2.pesan.tanggal_terima
        
        if data_tanggal_item1 < data_tanggal_item2:
            return -1
        else:
            return 1
        
        
        
    def ambil_inbox(self, token : str) -> dict:
        
        user = self.repository_akun.ambil_dari_token(token)
        
        if user is None:
            return {"error" : "autentikasi salah"}
        
        daftar_chat = self.repository_pesan.ambil_daftar_pesan_chat_dari_id_user_tujuan(user.id)
        daftar_file = self.repository_pesan.ambil_daftar_pesan_file_dari_id_user_tujuan(user.id)
        
        self.repository_pesan.hapus_pesan_dari_id_user(user.id)
        
        daftar_chat_lengkap : list[PesanChat|PesanFile] = []
        daftar_chat_lengkap.extend(daftar_chat)
        daftar_chat_lengkap.extend(daftar_file)
        daftar_chat_lengkap.sort(key=self.compare)
        
        respon : dict[str, list[dict[str, str]]] = {}
        
        for chat in daftar_chat_lengkap:
            if type(chat) is PesanChat:
                respon_pesan = {
                    "id_tujuan" : chat.pesan.id_tujuan,
                    "id_pengirim" : chat.pesan.id_pengirim,
                    "keperluan" : "PRIVATE",
                    "bentuk_chat" : "CHAT",
                    "chat" : chat.isi_pesan,
                    "tanggal_diterima" : chat.pesan.tanggal_terima.strftime("%d-%m-%Y %H:%M:%S")
                }
        
                if chat.pesan.id_grup is not None:
                    respon_pesan["keperluan"] = "GRUP"
                    respon_pesan["id_grup"] = chat.pesan.id_grup
                
                daftar_pesan_pengirim = respon.get(chat.pesan.id_pengirim)
                
                if daftar_pesan_pengirim is None:
                    daftar_pesan_pengirim = []
                    respon[chat.pesan.id_pengirim] = daftar_pesan_pengirim
                    
                daftar_pesan_pengirim.append(respon_pesan)
                
                
            elif type(chat) is PesanFile:
                respon_pesan = {
                    "id_tujuan" : chat.pesan.id_tujuan,
                    "id_pengirim" : chat.pesan.id_pengirim,
                    "keperluan" : "PRIVATE",
                    "bentuk_chat" : "FILE",
                    "nama_file" : chat.nama_file,
                    "isi_file" : chat.isi_file_base64,
                    "tanggal_diterima" : chat.pesan.tanggal_terima.strftime("%d-%m-%Y %H:%M:%S")
                }
        
                if chat.pesan.id_grup is not None:
                    respon_pesan["keperluan"] = "GRUP"
                    respon_pesan["id_grup"] = chat.pesan.id_grup
                
                daftar_pesan_pengirim = respon.get(chat.pesan.id_pengirim)
                
                if daftar_pesan_pengirim is None:
                    daftar_pesan_pengirim = []
                    respon[chat.pesan.id_pengirim] = daftar_pesan_pengirim
                    
                daftar_pesan_pengirim.append(respon_pesan)
        
        
        return respon