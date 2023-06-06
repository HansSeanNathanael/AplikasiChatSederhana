import json

class Pengaturan:
    
    @staticmethod
    def load_pengaturan() -> dict:
        
        lokasi_file : str = "./pengaturan/pengaturan.json"

        with open(lokasi_file) as file_pengaturan:
            data_pengaturan = json.load(file_pengaturan)
        return data_pengaturan