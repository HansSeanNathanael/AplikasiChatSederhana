from .pesan import Pesan

class PesanFile:
    def __init__(self, pesan : Pesan, nama_file : str, isi_file_base64) -> None:
        self.pesan = pesan
        self.nama_file = nama_file
        self.isi_file_base64 = isi_file_base64