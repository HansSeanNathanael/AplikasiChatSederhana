from ...Repository.repository_akun import RepositoryAkun
from ...Repository.repository_grup import RepositoryGrup

from ..Autentikasi.Data.akun import Akun

class ManajemenGrup:
    def __init__(self, domain : str, repository_akun : RepositoryAkun, repository_grup : RepositoryGrup):
        self.domain = domain
        self.repository_akun = repository_akun
        self.repository_grup = repository_grup
        
    def buat_grup(self, token : str, id_awalan_grup : str, password : str) -> dict:
        
        akun_pembuat = self.repository_akun.ambil_dari_token(token)
        if akun_pembuat is None:
            return {"error" : "autentikasi salah"}
        
        id_grup_penuh = id_awalan_grup + self.domain       
        grup_yang_akan_dibuat = self.repository_akun.ambil_dari_id(id_grup_penuh)
        
        if grup_yang_akan_dibuat is not None:
            return {"error" : "id telah digunakan"}
        
        self.repository_akun.buat_akun(Akun(id_grup_penuh, password, "grup"))
        self.repository_grup.tambah_anggota(id_grup_penuh, akun_pembuat.id)
        
        return {"id_grup" : id_grup_penuh}
    
    def gabung_grup(self, token : str, id_grup : str, password : str) -> dict:
        user = self.repository_akun.ambil_dari_token(token)
        if user is None:
            return {"error" : "autentikasi salah"}
        
        grup_tujuan = self.repository_akun.ambil_dari_id(id_grup)
        if grup_tujuan is None:
            return {"error" : "grup tidak ada"}
        
        if grup_tujuan.grup != "grup":
            return {"error" : "grup tidak ada"}
        
        if grup_tujuan.id != id_grup or grup_tujuan.password != password:
            return {"error" : "salah"}
        
        self.repository_grup.tambah_anggota(id_grup, user.id)
        return {"success" : "berhasil bergabung"}
    
    def keluar_grup(self, token : str, id_grup : str) -> dict:
        user = self.repository_akun.ambil_dari_token(token)
        
        if user is None:
            return {"error" : "autentikasi salah"}
        
        self.repository_grup.hapus_angggota(id_grup, user.id)
        
        return {"success" : "berhasil keluar dari grup"}
    
    