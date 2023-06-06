import re

from ...Koneksi.daftar_klien import DaftarKlien

from ...Repository.repository_akun import RepositoryAkun
from ..Autentikasi.Data.akun import Akun

class Autentikasi:
    
    def __init__(self, domain : str, daftar_klien : DaftarKlien, repository_akun : RepositoryAkun) -> None:
        self.domain = domain
        self.daftar_klien = daftar_klien
        self.repository_akun = repository_akun

    
    def register(self, awalan_id : str, password : str) -> dict:
        id_penuh : str = awalan_id + self.domain
        
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if re.match(pattern, id_penuh) is None:
            return {"error" : "format id salah"}
        
        data_user = self.repository_akun.ambil_dari_id(id_penuh)
        if data_user is not None:
            return {"error" : "id telah digunakan"}
        
        self.repository_akun.buat_user(Akun(id_penuh, password, "personal"))
        
        return {"id_akun" : id_penuh}
        
        
        
    def login(self, id : str, password : str, io_stream) -> dict:
        data_user = self.repository_akun.ambil_dari_id(id)
        
        if data_user is None:
            return {"error" : "akun tidak ada"}
        
        if data_user.grup != "personal" or data_user.id != id or data_user.password != password:
            return {"error" : "salah"}
        
        token = self.repository_akun.buat_token(data_user.id)
        
        self.daftar_klien.pasangkan_user_dengan_socket(id, io_stream)
        
        return {"token" : token}
    
    
    
    def logout(self, token : str, io_stream) -> dict:
        self.repository_akun.hapus_token(token)
        
        self.daftar_klien.hapus_pasangan_user_dengan_socket(io_stream)
        
        return {"success" : "token telah hangus"}