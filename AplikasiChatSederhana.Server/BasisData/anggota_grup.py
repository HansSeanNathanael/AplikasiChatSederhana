def up() -> str:
    return """
        CREATE TABLE anggota_grup (
            id_grup TEXT NOT NULL,
            id_user TEXT NOT NULL,
            
            PRIMARY KEY (id_grup, id_user)
        );
    """
    
def down() -> str:
    return """
        DROP TABLE anggota_grup;
    """