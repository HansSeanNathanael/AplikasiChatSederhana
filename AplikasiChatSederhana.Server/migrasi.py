import importlib
import inspect
import os
import sqlite3
from Pengaturan.pengaturan import Pengaturan

if __name__=="__main__":
    
    pengaturan = Pengaturan.load_pengaturan()
    
    koneksi_database = sqlite3.connect(pengaturan["basis_data"])
    
    cursor = koneksi_database.cursor()
    
    path_migrasi = "./BasisData"

    for nama_file in os.listdir(path_migrasi):
        if nama_file.endswith('.py'):
            nama_file_modul = nama_file[:-3]
            modul = importlib.import_module("BasisData." + nama_file_modul)

            for nama_objek, objek in inspect.getmembers(modul):
                if inspect.isfunction(objek) and nama_objek == "up":
                    cursor.execute(objek())
                    koneksi_database.commit()