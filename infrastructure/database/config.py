import mysql.connector
from infrastructure.repositories.repositoryUsers.update import Update
from infrastructure.repositories.repositoryUsers.create import Create
from infrastructure.repositories.repositoryUsers.read import Read
from infrastructure.repositories.repositoryUsers.delete import Delete
from tkinter import *
import hashlib


class Database:
    def __init__(self):
        self.db = None

    def connectDb(self):
        self.db = mysql.connector.connect(
            host="sql859.main-hosting.eu",
            user="u338035582_hugo",
            password="HJJYHJALh12",
            database="u338035582_quoridor"
        )

    def insert(self):
        return Create(self.db)

    def select(self):
        return Read(self.db)

    def update(self):
        return Update(self.db)

    def delete(self):
        return Delete(self.db)

    def close(self):
        self.db.close()
    
    def createTableGame(self, ip, port: int) -> None:
        self.connectDb()
        cursor = self.db.cursor()
        table_name = f"Game{ip.replace('.', '_')}{port}"
        create_table_query = f"""
        CREATE TABLE {table_name} (
            ID INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        self.db.close()
        
    def dropTableIfExists(self, ip, port):
        self.connectDb()
        cursor = self.db.cursor()
        table_name = f"Game{ip.replace('.', '_')}{port}"
        check_table_query = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(check_table_query)
        table_exists = cursor.fetchone()
        if table_exists:
            drop_table_query = f"DROP TABLE {table_name}"
            cursor.execute(drop_table_query)
            print(f"Table {table_name} dropped.")
        cursor.close()
        self.db.close()
        
    def insertUsername(self, ip: str, port: int, username: str) -> None:
        self.connectDb()
        cursor = self.db.cursor()

        table_name = f"Game{ip.replace('.', '_')}{port}"
        insert_query = f"INSERT INTO {table_name} (username) VALUES (%s)"
        values = (username,)

        cursor.execute(insert_query, values)
        self.db.commit()

        cursor.close()
        self.db.close()
    
    def selectUsername(self, ip:str, port: int, id: int):
        self.connectDb()
        select_query = self.select()
        select_query.execute(f"SELECT username FROM Game{ip.replace('.', '_')}{port} WHERE ID = {id}")
        result = select_query.fetchone()
        select_query.close()
        return result[0]
    
    def addWin(self, username):
        if username == " ":
            return None
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT win FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        if result is not None:
            current_wins = result[0]
            new_wins = current_wins + 1
            update_query = self.update()
            update_query.execute("UPDATE users SET win = %s WHERE username = %s", (new_wins, username))
            update_query.close()
        else:
            print("User not found.")
