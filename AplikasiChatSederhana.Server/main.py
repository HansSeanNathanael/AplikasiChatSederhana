from Aplikasi.Koneksi.server import Server
from Aplikasi.Koneksi.server_untuk_realm_eksternal import ServerUntukRealmEksternal
from Pengaturan.pengaturan import Pengaturan
from Aplikasi.Koneksi.daftar_klien import DaftarKlien
from Aplikasi.Koneksi.daftar_realm import DaftarRealm

from Aplikasi.Chat.Autentikasi.autentikasi import Autentikasi
from Aplikasi.Chat.Grup.manajemen_grup import ManajemenGrup
from Aplikasi.Chat.Pesan.manajemen_pesan import ManajemenPesan

from Aplikasi.Chat.Grup.manajemen_grup_eksternal import ManajemenGrupEksternal
from Aplikasi.Chat.Pesan.manajemen_pesan_eksternal import ManajemenPesanEksternal

from Aplikasi.Repository.koneksi_database import KoneksiDatabase
from Aplikasi.Repository.repository_akun import RepositoryAkun
from Aplikasi.Repository.repository_grup import RepositoryGrup
from Aplikasi.Repository.repository_pesan import RepositoryPesan

from Aplikasi.Chat.Pesan.pengirim_pesan import PengirimPesan


if __name__=="__main__":
    pengaturan = Pengaturan.load_pengaturan()
    
    daftar_klien = DaftarKlien()
    koneksi_database = KoneksiDatabase(pengaturan)
    server = Server(
        pengaturan, daftar_klien, Autentikasi(pengaturan["domain"], daftar_klien, RepositoryAkun(koneksi_database)),
        ManajemenGrup(pengaturan["domain"], None, RepositoryAkun(koneksi_database), RepositoryGrup(koneksi_database)),
        ManajemenPesan(
            pengaturan["domain"], PengirimPesan(daftar_klien), None, 
            RepositoryAkun(koneksi_database), RepositoryPesan(koneksi_database), RepositoryGrup(koneksi_database)
        )
    )
    
    server.start()
    
    server_untuk_realm_eksternal = ServerUntukRealmEksternal(
        pengaturan, ManajemenGrupEksternal(RepositoryAkun(koneksi_database), RepositoryGrup(koneksi_database)),
        ManajemenPesanEksternal(
            pengaturan["domain"], PengirimPesan(daftar_klien), None,
            RepositoryAkun(koneksi_database), RepositoryPesan(koneksi_database), RepositoryGrup(koneksi_database)
        )
    )
    
    server_untuk_realm_eksternal.start()
    