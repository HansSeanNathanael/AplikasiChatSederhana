import threading
import uuid

from .koneksi_database import KoneksiDatabase
from ..Chat.Autentikasi.Data.akun import Akun

class RepositoryAkun:
    def __init__(self, koneksi : KoneksiDatabase, lock_koneksi : threading.Lock):
        self.koneksi = koneksi.koneksi()
        self.lock_koneksi = lock_koneksi
        
        
        
    def buat_akun(self, user : Akun) -> None:
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script : str = """
            INSERT INTO akun VALUES (?, ?, ?);
        """
        
        cursor.execute(script, (user.id, user.password, user.grup,))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        
        
        
    def ambil_dari_id(self, id_akun : str) -> Akun|None:
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script : str = """
            SELECT a.id_akun, a.password, a.grup FROM akun AS a WHERE a.id_akun = ?;
        """
        
        cursor.execute(script, (id_akun,))
        hasil = cursor.fetchall()
        cursor.close()
        self.lock_koneksi.release()
        
        if len(hasil) == 0:
            return None
        
        return Akun(hasil[0][0], hasil[0][1], hasil[0][2])
    
    
    
    def buat_token(self, id_akun : str) -> str:
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script : str = """
            INSERT INTO token VALUES (?, ?, 0);
        """
        
        token : str = str(uuid.uuid4())
        cursor.execute(script, (token, id_akun,))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        
        return token
        
        
        
    def ambil_dari_token(self, token : str) -> Akun|None:
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script : str = """
            SELECT a.id_akun, a.password, a.grup FROM token AS t INNER JOIN akun AS a ON t.id_user = a.id_akun 
            WHERE t.token = ? AND t.deleted = 0;
        """
        
        cursor.execute(script, (token,))
        hasil = cursor.fetchall()
        cursor.close()
        self.lock_koneksi.release()
        
        if len(hasil) == 0:
            return None
        
        return Akun(hasil[0][0], hasil[0][1], hasil[0][2])
    
    
    
    def hapus_token(self, token : str) -> None:
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script : str = """
            UPDATE token SET deleted = 1 WHERE token = ? ;
        """
        
        cursor.execute(script, (token,))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        