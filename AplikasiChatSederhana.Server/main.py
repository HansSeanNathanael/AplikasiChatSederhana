import threading

from Aplikasi.Koneksi.server import Server
from Aplikasi.Koneksi.server_untuk_realm_eksternal import ServerUntukRealmEksternal
from Pengaturan.pengaturan import Pengaturan
from Aplikasi.Koneksi.daftar_klien import DaftarKlien

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
from Jembatan.manajer_jembatan import ManajerJembatan


if __name__=="__main__":
    pengaturan = Pengaturan.load_pengaturan()
    
    daftar_klien = DaftarKlien()
    koneksi_database = KoneksiDatabase(pengaturan)
    lock_database = threading.Lock()
    server = Server(
        pengaturan, daftar_klien, Autentikasi(pengaturan["domain"], daftar_klien, RepositoryAkun(koneksi_database, lock_database)),
        ManajemenGrup(pengaturan["domain"], ManajerJembatan(), RepositoryAkun(koneksi_database, lock_database), RepositoryGrup(koneksi_database, lock_database)),
        ManajemenPesan(
            pengaturan["domain"], PengirimPesan(daftar_klien), ManajerJembatan(), 
            RepositoryAkun(koneksi_database, lock_database), RepositoryPesan(koneksi_database, lock_database), RepositoryGrup(koneksi_database, lock_database)
        )
    )
    
    server.start()
    
    server_untuk_realm_eksternal = ServerUntukRealmEksternal(
        pengaturan, ManajemenGrupEksternal(RepositoryAkun(koneksi_database, lock_database), RepositoryGrup(koneksi_database, lock_database)),
        ManajemenPesanEksternal(
            pengaturan["domain"], PengirimPesan(daftar_klien), ManajerJembatan(),
            RepositoryAkun(koneksi_database, lock_database), RepositoryPesan(koneksi_database, lock_database), RepositoryGrup(koneksi_database, lock_database)
        )
    )
    
    server_untuk_realm_eksternal.start()
    