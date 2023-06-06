class Pesan:
    def __init__(self, id_pesan : str, id_pengirim : str, id_tujuan : str, id_grup : str|None, tipe_pesan : str, tanggal_terima : str) -> None:
        self.id_pesan = id_pesan
        self.id_pengirim = id_pengirim
        self.id_tujuan = id_tujuan
        self.id_grup = id_grup
        self.tipe_pesan = tipe_pesan
        self.tanggal_terima = tanggal_terima