import sqlite3
from sqlite3 import Connection

class UsersDB():
    def __init__(self):
        self.con = sqlite3.connect("database.db", check_same_thread=False)
    
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
    
    def write_token_to_db(self, user_email:str, token:str):
        cursor = self.con.cursor() 
        cursor.execute("CREATE TABLE IF NOT EXISTS token (id INTEGER PRIMARY KEY, email TEXT, token TEXT)")
        cursor.execute(f"INSERT INTO token (email, token) VALUES ('{user_email}', '{token}')")
        print("Write Token...")
        self.con.commit()
        return True
