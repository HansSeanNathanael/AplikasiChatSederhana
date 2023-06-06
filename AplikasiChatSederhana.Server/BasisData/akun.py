def up() -> str:
    return """
        CREATE TABLE akun (
            id_akun TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            grup TEXT NOT NULL
        );
    """

def down() -> str:
    return """
        DROP TABLE akun;
    """