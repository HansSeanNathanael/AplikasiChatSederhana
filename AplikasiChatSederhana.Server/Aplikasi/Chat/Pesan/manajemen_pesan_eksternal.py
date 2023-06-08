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

class ManajemenPesanEksternal:
    def __init__(self, domain : str, pengirim_pesan : PengirimPesan, interface_manajer_jembatan : InterfaceManajerJembatan, repository_akun : RepositoryAkun, repository_pesan : RepositoryPesan, repository_grup : RepositoryGrup) -> None:
        self.domain = domain
        self.pengirim_pesan = pengirim_pesan
        self.interface_manajer_jembatan = interface_manajer_jembatan
        self.repository_akun = repository_akun
        self.repository_pesan = repository_pesan
        self.repository_grup = repository_grup
        
        
        
    def mengirim_chat(self, id_pengirim : str, id_tujuan : str, id_grup : str|None, isi_chat : str) -> dict:
        # id grup bila None artinya bukan diteruskan dari grup realm eksternal.
        # Fungsi digunakan untuk chat eksternal dan chat grup eksternal.
        
        # Karena chat grup eksternal adalah menerima chat yang diteruskan dari grup eksternal,
        # maka tujuannya pasti menuju akun personal sehingga untuk memudahkan sistem
        # kedua request menggunakan satu method yang sama  
        
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now()
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), id_pengirim, id_tujuan, id_grup, "chat", tanggal_diterima)
            pesan_chat_baru = PesanChat(data_pesan, isi_chat)
            
            if not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru):
                self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != id_pengirim:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    data_pesan = Pesan(uuid.uuid4(), id_pengirim, id_anggota, tujuan.id, "chat", tanggal_diterima)
                    pesan_chat_baru = PesanChat(data_pesan, isi_chat)
                    
                    if domain_tujuan != self.domain:
                        self.interface_manajer_jembatan.kirim_pesan_chat(pesan_chat_baru)
                    else:
                        if not self.pengirim_pesan.kirim_pesan_chat(pesan_chat_baru):
                            self.repository_pesan.tambah_pesan_chat(pesan_chat_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}
    
    
    
    def mengirim_file(self, id_pengirim : str, id_tujuan : str, id_grup : str|None, nama_file : str, isi_file_base64 : str) -> dict:
        # id grup bila None artinya bukan diteruskan dari grup realm eksternal.
        # Fungsi digunakan untuk file eksternal dan file grup eksternal.
        
        # Karena file grup eksternal adalah menerima file yang diteruskan dari grup eksternal,
        # maka tujuannya pasti menuju akun personal sehingga untuk memudahkan sistem
        # kedua request menggunakan satu method yang sama 
        
        
        tujuan = self.repository_akun.ambil_dari_id(id_tujuan)
        if tujuan is None:
            return {"error" : "tujuan tidak ada"}
        
        tanggal_diterima = datetime.datetime.now()
        
        if tujuan.grup == "personal":
            data_pesan = Pesan(uuid.uuid4(), id_pengirim, id_tujuan, id_grup, "file", tanggal_diterima)
            pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
            
            if not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru):
                self.repository_pesan.tambah_pesan_file(pesan_file_baru)
        
        
        elif tujuan.grup == "grup":
            daftar_anggota_grup = self.repository_grup.ambil_daftar_anggota(tujuan.id)
            
            for id_anggota in daftar_anggota_grup.daftar_anggota:
                
                if id_anggota != id_pengirim:
                    domain_tujuan = self.dapatkan_realm_tujuan(id_anggota)
                    
                    data_pesan = Pesan(uuid.uuid4(), id_pengirim, id_anggota, tujuan.id, "file", tanggal_diterima)
                    pesan_file_baru = PesanFile(data_pesan, nama_file, isi_file_base64)
                    
                    if domain_tujuan != self.domain:
                        self.interface_manajer_jembatan.kirim_pesan_file(pesan_file_baru)
                    else:
                        if not self.pengirim_pesan.kirim_pesan_file(pesan_file_baru):
                            self.repository_pesan.tambah_pesan_file(pesan_file_baru)
                            
                            
        return {"success" : "pesan berhasil dikirim", "waktu_dikirim" : tanggal_diterima}
    