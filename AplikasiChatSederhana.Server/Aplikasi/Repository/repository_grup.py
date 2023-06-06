from .koneksi_database import KoneksiDatabase
from ..Chat.Grup.Data.anggota_grup import AnggotaGrup

class RepositoryGrup:
    def __init__(self, koneksi : KoneksiDatabase):
        self.koneksi = koneksi.koneksi()
        
    def ambil_daftar_anggota(self, id_grup : str) -> AnggotaGrup|None:
        cursor = self.koneksi.cursor()
        
        script : str = """
            SELECT ag.id_user FROM anggota_grup AS ag WHERE ag.id_grup = ?
        """
        
        cursor.execute(script, (id_grup))
        hasil = cursor.fetchall()
        
        daftar_anggota : list[str] = []
        for anggota in hasil:
            daftar_anggota.append(anggota[1])
        
        return AnggotaGrup(id_grup, daftar_anggota)
        
    def tambah_anggota(self, id_grup : str, id_user : str) -> None:
        cursor = self.koneksi.cursor()
        
        script : str = """
            INSERT INTO anggota_grup VALUES (?, ?)
        """
        
        cursor.execute(script, (id_grup, id_user))
        self.koneksi.commit()

    def hapus_angggota(self, id_grup : str, id_user : str) -> None:
        cursor = self.koneksi.cursor()
        
        script : str = """
            DELETE FROM anggota_grup WHERE id_grup = ? AND id_user = ?
        """
        
        cursor.execute(script, (id_grup, id_user))
        self.koneksi.commit()