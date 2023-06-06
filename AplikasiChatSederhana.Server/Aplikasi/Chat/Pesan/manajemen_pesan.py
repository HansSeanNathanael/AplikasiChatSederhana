import datetime
import re
import uuid

from ...Koneksi.daftar_klien import DaftarKlien
from .pengirim_pesan import PengirimPesan

from ...Repository.repository_akun import RepositoryAkun
from ...Repository.repository_pesan import RepositoryPesan
from ...Repository.repository_grup import RepositoryGrup

from ..Pesan.Data.pesan import Pesan
from ..Pesan.Data.pesan_chat import PesanChat
from ..Pesan.Data.pesan_file import PesanFile

class ManajemenPesan:
    def __init__(self, domain : str, pengirim_pesan : PengirimPesan, daftar_klien : DaftarKlien, repository_akun : RepositoryAkun, repository_pesan : RepositoryPesan, repository_grup : RepositoryGrup) -> None:
        self.domain = domain
        self.pengirim_pesan = pengirim_pesan
        self.daftar_klien = daftar_klien
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
            # TODO
            # buat implementasi untuk mengirim menuju realm lain
            pass
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "chat", tanggal_diterima)
            pesan_chat_baru = PesanChat(data_pesan, isi_chat)
            
            io_stream_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(data_pesan.id_tujuan)
            if io_stream_tujuan is None:
                self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
            elif not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru, io_stream_tujuan):
                self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != pengirim.id:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    if domain_tujuan != self.domain:
                        # TODO
                        # buat implementasi untuk mengirim menuju realm lain
                        pass
                    
                    else:
                        data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_anggota, tujuan.id, "chat", tanggal_diterima)
                        pesan_chat_baru = PesanChat(data_pesan, isi_chat)
                        
                        io_stream_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(data_pesan.id_tujuan)
                        if io_stream_tujuan is None:
                            self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
                        elif not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru, io_stream_tujuan):
                            self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}
    
    
    
    def mengirim_file(self, token : str, id_tujuan : str, nama_file : str, isi_file_base64 : str) -> dict:
        
        pengirim = self.repository_akun.ambil_dari_token(token)
        
        if pengirim is None:
            return {"error" : "autentikasi salah"}
        
        domain_tujuan = self.dapatkan_realm_tujuan(id_tujuan)
        
        if domain_tujuan != self.domain:
            # TODO
            # buat implementasi untuk mengirim menuju realm lain
            pass
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_tujuan, None, "file", tanggal_diterima)
            pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
            
            io_stream_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(data_pesan.id_tujuan)
            if io_stream_tujuan is None:
                self.repository_pesan.tambah_pesan_file(pesan_file_baru)
            elif not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru, io_stream_tujuan):
                self.repository_pesan.tambah_pesan_file(pesan_file_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != pengirim.id:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    if domain_tujuan != self.domain:
                        # TODO
                        # buat implementasi untuk mengirim menuju realm lain
                        pass
                    
                    else:
                        data_pesan = Pesan(uuid.uuid4(), pengirim.id, id_anggota, tujuan.id, "file", tanggal_diterima)
                        pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
                        
                        io_stream_tujuan = self.daftar_klien.dapatkan_socket_berdasarkan_id(data_pesan.id_tujuan)
                        if io_stream_tujuan is None:
                            self.repository_pesan.tambah_pesan_file(pesan_file_baru)
                        elif not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru, io_stream_tujuan):
                            self.repository_pesan.tambah_pesan_file(pesan_file_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}