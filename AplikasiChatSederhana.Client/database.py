import sqlite3
from sqlite3 import Connection

class Database():
    def __init__(self):
        self.con = sqlite3.connect("database.db", check_same_thread=False)
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS rooms (id INTEGER PRIMARY KEY, sender TEXT, receiver TEXT)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS chats (id INTEGER PRIMARY KEY, room_id TEXT, content TEXT, file_path TEXT, is_user TEXT)")
        self.con.cursor().execute("CREATE TABLE IF NOT EXISTS token (id INTEGER PRIMARY KEY, email TEXT, token TEXT, password TEXT)")

    
    # def read_db(self, user_email:str, password:str):
    #     cursor = self.con.cursor()  
    #     cursor.execute("SELECT * FROM users")
    #     user = cursor.fetchall()
    #     #print("Iniciando sesion.... ")
    #     for i in user:
    #         # print(user)
    #         if (i[2]==user_email and i[3]==password):
    #             return True
    #     return False
    
    def get_user_token(self, email:str):
        cursor = self.con.cursor()  
        cursor.execute(f"SELECT token FROM token WHERE email='{email}'")
        token = cursor.fetchone()
        print(f"Get Token: {token[0]}")
        return token[0]
    
    def delete_user_token(self, token:str):
        cursor = self.con.cursor()  
        cursor.execute(f"DELETE FROM token WHERE token='{token}'")
        row_count = cursor.rowcount
        self.con.commit()
        if row_count > 0:
            print(f"Deletion successful. {row_count} row(s) deleted.")
            return True
        else:
            print("No rows deleted.")
            return False
    
    # def add_user(self, user_email:str, password:str, user_name:str):
    #     cursor = self.con.cursor() 
    #     cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user TEXT, email TEXT, password TEXT)")
    #     cursor.execute(f"INSERT INTO users (user, email, password) VALUES ('{user_name}', '{user_email}', '{password}')")
    #     self.con.commit()
    #     return True
    
    def write_token_to_db(self, user_email:str, token:str, password:str):
        cursor = self.con.cursor() 
        cursor.execute(f"INSERT INTO token (email, token, password) VALUES ('{user_email}', '{token}', '{password}')")
        print("Write Token...")
        self.con.commit()
        return True
    
    def get_chat(self, room_id:int):
        cursor = self.con.cursor()  
        cursor.execute(f"SELECT * FROM chats WHERE room_id='{room_id}'")
        chat = cursor.fetchall()
        if chat:
            return chat
        return None
    
    def write_chat(self, room_id:str, content:str, file_path:str, is_user:str = "0"):
        cursor = self.con.cursor() 
        cursor.execute(f"INSERT INTO chats (room_id, content, file_path, is_user) VALUES ('{room_id}', '{content}', '{file_path}', '{is_user}')")
        self.con.commit()
        return True
    
    def write_room(self, sender:str, rec:str):
        cursor = self.con.cursor() 
        cursor.execute(f"INSERT INTO rooms (sender, receiver) VALUES ('{sender}', '{rec}')")
        self.con.commit()
        return True

    def is_room_exist(self, id:str, type:str):
        cursor = self.con.cursor() 
        if type == "GROUP" :
            cursor.execute(f"SELECT * FROM rooms WHERE receiver='{id}'")
            data = cursor.fetchone()
        else :
            cursor.execute(f"SELECT * FROM rooms WHERE sender='{id}'")
            data = cursor.fetchone()
        if data:
            return True
        return False
    
    def get_room(self, id:str, type:str):
        cursor = self.con.cursor() 
        if type == "GROUP" :
            cursor.execute(f"SELECT * FROM rooms WHERE receiver='{id}'")
            data = cursor.fetchone()
        else :
            cursor.execute(f"SELECT * FROM rooms WHERE sender='{id}'")
            data = cursor.fetchone()
        return data[0]
    
    def get_rooms(self):
        cursor = self.con.cursor() 
        cursor.execute(f"SELECT * FROM rooms")
        data = cursor.fetchall()
        return data
    
    def get_user_from_private_room(self, id:int):
        cursor = self.con.cursor() 
        cursor.execute(f"SELECT * FROM rooms WHERE id='{id}'")
        data = cursor.fetchone()
        if data:
            return data[1]
        return None
    
    def get_group_room_name(self, id:int):
        cursor = self.con.cursor() 
        cursor.execute(f"SELECT * FROM rooms WHERE id='{id}'")
        data = cursor.fetchone()
        if data:
            return data[2]
        return None
    
    def is_group_room(self, id:str):
        cursor = self.con.cursor() 
        cursor.execute(f"SELECT * FROM rooms WHERE receiver='{id}'")
        data = cursor.fetchone()
        if data:
            return True
        return False

