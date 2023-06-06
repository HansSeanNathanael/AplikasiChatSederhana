def up() -> str:
    return """
        CREATE TABLE pesan_chat (
            id_pesan TEXT PRIMARY KEY,
            isi_pesan TEXT NOT NULL
        )
    """
    
def down() -> str:
    return """
        DROP TABLE pesan_chat;
    """