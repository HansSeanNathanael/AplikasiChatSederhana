def up() -> str:
    return """
        CREATE TABLE pesan_file (
            id_pesan TEXT PRIMARY KEY,
            nama_file TEXT NOT NULL,
            isi_file_base64 TEXT NOT NULL
        )
    """
    
def down() -> str:
    return """
        DROP TABLE pesan_file;
    """