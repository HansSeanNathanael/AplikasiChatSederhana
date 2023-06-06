from .pesan import Pesan

class PesanChat:
    def __init__(self, pesan : Pesan, isi_pesan : str) -> None:
        self.pesan = pesan
        self.isi_pesan = isi_pesan