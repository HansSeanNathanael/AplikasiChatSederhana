from sqlite3 import Connection

class ChatsDB():
  
    def read_db(self, conn:Connection):
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM chats")
        chat = cursor.fetchall()
        if chat:
            return chat
        return None
    
  
    def write_db(self, user_email:str, message:str, conn:Connection):
        cursor = conn.cursor() 
        cursor.execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, email TEXT, message TEXT)")
        cursor.execute(f"INSERT INTO chats (email, message) VALUES ('{user_email}', '{message}')")
        conn.commit()
        return True

