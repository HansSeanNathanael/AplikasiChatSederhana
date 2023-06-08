from ...Repository.repository_akun import RepositoryAkun
from ...Repository.repository_grup import RepositoryGrup

from ..Autentikasi.Data.akun import Akun

class ManajemenGrupEksternal:
    def __init__(self, repository_akun : RepositoryAkun, repository_grup : RepositoryGrup):
        self.repository_akun = repository_akun
        self.repository_grup = repository_grup
    
    
    
    def gabung_grup(self, id_user : str, id_grup : str, password : str) -> dict:
        
        grup_tujuan = self.repository_akun.ambil_dari_id(id_grup)
        if grup_tujuan is None:
            return {"error" : "grup tidak ada"}
        
        if grup_tujuan.grup != "grup":
            return {"error" : "grup tidak ada"}
        
        if grup_tujuan.id != id_grup or grup_tujuan.password != password:
            return {"error" : "salah"}
        
        self.repository_grup.tambah_anggota(id_grup, id_user)
        return {"success" : "berhasil bergabung"}
    
    
    
    def keluar_grup(self, id_user : str, id_grup : str) -> dict:
        
        self.repository_grup.hapus_angggota(id_grup, id_user)
        
        return {"success" : "berhasil keluar dari grup"}
    
    