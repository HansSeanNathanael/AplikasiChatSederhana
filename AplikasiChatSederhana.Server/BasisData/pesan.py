def up() -> str:
    return """
        CREATE TABLE pesan (
            id TEXT PRIMARY KEY,
            id_tujuan TEXT NOT NULL,
            id_pengirim TEXT NOT NULL,
            id_grup TEXT,
            tipe_pesan TEXT NOT NULL,
            tanggal_terima TEXT NOT NULL
        )
    """
    
def down() -> str:
    return """
        DROP TABLE pesan;
    """