from ..Chat.Pesan.Data.pesan_chat import PesanChat
from ..Chat.Pesan.Data.pesan_file import PesanFile

class InterfaceManajerJembatan:

    def gabung_grup(self, id_user : str, id_grup : str, password : str) -> dict:
        pass

    def keluar_grup(self, id_user : str, id_grup : str) -> dict:
        pass
    
    def kirim_pesan_chat(self, pesan_chat : PesanChat) -> dict:
        pass
    
    def kirim_pesan_file(self, pesan_file : PesanFile) -> dict:
        pass
    
    