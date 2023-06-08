import threading
import datetime

from .koneksi_database import KoneksiDatabase

from ..Chat.Pesan.Data.pesan import Pesan
from ..Chat.Pesan.Data.pesan_chat import PesanChat
from ..Chat.Pesan.Data.pesan_file import PesanFile

class RepositoryPesan:
    
    def __init__(self, koneksi : KoneksiDatabase, lock_koneksi : threading.Lock) -> None:
        self.koneksi = koneksi.koneksi()
        self.lock_koneksi = lock_koneksi
        
    def tambah_pesan(self, pesan : Pesan) -> None:
        self.lock_koneksi.acquire()
        
        cursor = self.koneksi.cursor()
        
        script = """
            INSERT INTO pesan VALUES (?, ?, ?, ?, ?, ?);
        """
        
        cursor.execute(script, (pesan.id_pesan, pesan.id_tujuan, pesan.id_pengirim, pesan.id_grup, pesan.tipe_pesan, pesan.tanggal_terima.strftime("%Y-%m-%d %H:%M:%S"),))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        
        
    
    def tambah_pesan_chat(self, pesan_chat : PesanChat) -> None:
        self.tambah_pesan(pesan_chat.pesan)
        
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script = """
            INSERT INTO pesan_chat VALUES (?, ?);
        """
        
        cursor.execute(script, (pesan_chat.pesan.id_pesan, pesan_chat.isi_pesan,))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        
        
    
    def tambah_pesan_file(self, pesan_file : PesanFile) -> None:
        self.tambah_pesan(pesan_file.pesan)
        
        self.lock_koneksi.acquire()
        
        cursor = self.koneksi.cursor()
        
        script = """
            INSERT INTO pesan_file VALUES (?, ?, ?);
        """
        
        cursor.execute(script, (pesan_file.pesan.id_pesan, pesan_file.nama_file, pesan_file.isi_file_base64,))
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()
        
        
    
    def ambil_daftar_pesan_chat_dari_id_user_tujuan(self, id_user_tujuan : str) -> list[PesanChat]:
        self.lock_koneksi.acquire()
        
        cursor = self.koneksi.cursor()
        
        script = """
            SELECT p.id, p.id_pengirim, p.id_tujuan, p.id_grup, p.tipe_pesan, p.tanggal_terima, pc.isi_pesan FROM pesan AS p
            INNER JOIN pesan_chat AS pc ON p.id = pc.id_pesan WHERE p.id_tujuan = ?
            ORDER BY datetime(p.tanggal_terima) ASC;
        """
        
        cursor.execute(script, (id_user_tujuan,))
        hasil = cursor.fetchall()
        cursor.close()
        self.lock_koneksi.release()
        
        daftar_pesan : list[PesanChat] = []
        for pesan in hasil:
            daftar_pesan.append(PesanChat(Pesan(pesan[0], pesan[1], pesan[2], pesan[3], pesan[4], datetime.datetime.strptime(pesan[5], "%Y-%m-%d %H:%M:%S")), pesan[6]))
        
        return daftar_pesan
    
    
    
    def ambil_daftar_pesan_file_dari_id_user_tujuan(self, id_user_tujuan : str) -> list[PesanFile]:
        self.lock_koneksi.acquire()
        
        cursor = self.koneksi.cursor()
        
        script = """
            SELECT p.id, p.id_pengirim, p.id_tujuan, p.id_grup, p.tipe_pesan, p.tanggal_terima, 
                pf.nama_file, pf.isi_file_base64 FROM pesan AS p
            INNER JOIN pesan_file AS pf ON p.id = pf.id_pesan WHERE p.id_tujuan = ?
            ORDER BY datetime(p.tanggal_terima) ASC;
        """
        
        cursor.execute(script, (id_user_tujuan,))
        hasil = cursor.fetchall()
        cursor.close()
        self.lock_koneksi.release()
        
        daftar_pesan : list[PesanFile] = []
        for pesan in hasil:
            daftar_pesan.append(PesanFile(Pesan(pesan[0], pesan[1], pesan[2], pesan[3], pesan[4], datetime.datetime.strptime(pesan[5], "%Y-%m-%d %H:%M:%S")), pesan[6], pesan[7]))
        
        return daftar_pesan
    
    def hapus_pesan_dari_id_user(self, id_user : str):
        self.lock_koneksi.acquire()
        cursor = self.koneksi.cursor()
        
        script_hapus_pesan_chat = """
            DELETE FROM pesan_chat WHERE id_pesan IN (SELECT p.id FROM pesan AS p WHERE p.id_tujuan = ?);
        """
        cursor.execute(script_hapus_pesan_chat, (id_user,))
        
        script_hapus_pesan_file = """
            DELETE FROM pesan_file WHERE id_pesan IN (SELECT p.id FROM pesan AS p WHERE p.id_tujuan = ?);
        """
        cursor.execute(script_hapus_pesan_file, (id_user,))
        
        script_hapus_pesan = """
            DELETE FROM pesan WHERE id_tujuan = ?;
        """
        cursor.execute(script_hapus_pesan, (id_user,))
        
        self.koneksi.commit()
        cursor.close()
        self.lock_koneksi.release()