def up() -> str:
    return """
        CREATE TABLE token (
            token TEXT PRIMARY KEY,
            id_user TEXT NOT NULL,
            deleted INTEGER NOT NULL
        );
    """
    
def down() -> str:
    return """
        DROP TABLE token;
    """