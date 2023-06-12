import mysql.connector
from infrastructure.repositories.repositoryUsers.update import Update
from infrastructure.repositories.repositoryUsers.create import Create
from infrastructure.repositories.repositoryUsers.read import Read
from infrastructure.repositories.repositoryUsers.delete import Delete
from tkinter import *
import threading


class Database(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.db = None
        self.numUser = None
        self.port = None
        self.ip = None
    
    
    def addMoney(self, username :str) -> None:
        if username == " ":
            return None
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT money FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        if result is not None:
            new_Moneys = result[0] + 50
            update_query = self.update()
            update_query.execute("UPDATE users SET money = %s WHERE username = %s", (new_Moneys, username))
            update_query.close()
            self.db.close()
        else:
            print("User not found.")
        
        
    def setIP(self, newIP: str) -> None:
        self.ip = newIP
        
    
    def setPort(self, newPort: int) -> None:
        self.port = newPort
        
        
    def setNumPerso(self, newNumUser : int) -> None:
        self.numUser = newNumUser
        
        
    def connectDb(self):
        self.db = mysql.connector.connect(
            host="sql859.main-hosting.eu",
            user="u338035582_hugo",
            password="123456789Quoridor",
            database="u338035582_Quoridor"
        )


    def selectPassword(self, username : str) -> str:
        self.connectDb()
        select_queryPeoples = self.select()
        select_queryPeoples.execute(f"SELECT password FROM users WHERE username = '{username}'")
        resultPeoples = select_queryPeoples.queries.fetchall()
        select_queryPeoples.close()
        self.db.close()
        return resultPeoples
    
    
    def sendInviting(self, usernamePlayer : str, usernameUseradd : str) -> None:
        self.connectDb()
        cursor = self.db.cursor()
        
        insert_query = f"INSERT INTO invitingFriends (nameUser_1, toNameUser_2) VALUES (%s, %s)"
        values = (usernamePlayer,usernameUseradd,)

        cursor.execute(insert_query, values)
        self.db.commit()

        cursor.close()
        self.db.close()
        
        
    def acceptInviting(self, usernamePlayer : str, usernameUseradd : str) -> None:
        self.addFriends(usernamePlayer, usernameUseradd)
        self.addFriends(usernameUseradd, usernamePlayer)
        
        self.deleteInviting(usernameUseradd, usernamePlayer)
        
        
    def deleteInviting(self, usernamePlayer : str, usernameUseradd : str) -> None:
        self.connectDb()
        delete_query = self.delete()
        delete_query.execute(f"DELETE FROM invitingFriends WHERE nameUser_1 = '{usernamePlayer}' AND toNameUser_2 = '{usernameUseradd}'")
        
        self.db.commit()
        delete_query.close()
        self.db.close()
        
        
    def selectAllInviting(self, username : str, typeUser : bool) -> list:
        self.connectDb()
        select_queryFriends = self.select()
        
        if typeUser:
            select_queryFriends.execute(f"SELECT toNameUser_2 FROM invitingFriends WHERE nameUser_1 = '{username}'")
        else:
            select_queryFriends.execute(f"SELECT nameUser_1 FROM invitingFriends WHERE toNameUser_2 = '{username}'")
        
        resultInviting = select_queryFriends.queries.fetchall()
        select_queryFriends.close()
        self.db.close()
        return resultInviting
    
    
    def selectStatusFriends(self, username : str) -> list:
        self.connectDb()
        select_queryFriends = self.select()
        select_queryFriends.execute(f"SELECT status FROM users WHERE username = '{username}'")
        resultStatus = select_queryFriends.queries.fetchall()
        select_queryFriends.close()
        self.db.close()
        return resultStatus
        
    
    def selectAllPeoplesGame(self, ip : str, port : int) -> list:
        self.connectDb()
        select_queryPeoples = self.select()
        select_queryPeoples.execute(f"SELECT username FROM Game{ip.replace('.', '_')}{port}")
        resultPeoples = select_queryPeoples.queries.fetchall()
        select_queryPeoples.close()
        self.db.close()
        return resultPeoples
        
        
    def setStatusUser(self, username : str, status : int) -> None:
        self.connectDb()
        update_query = self.update()
        update_query.execute(f"UPDATE users SET status = {status} WHERE username = '{username}'")
        update_query.close()
        self.db.close()
        
        
    def selectAllFriends(self, username : str) -> list:
        resultStatus = self.selectStatusFriends(username)
        
        self.connectDb()
        select_queryFriends = self.select()
        select_queryFriends.execute(f"SELECT toNameUser_2 FROM friends WHERE nameUser_1 = '{username}'")
        resultFriends = select_queryFriends.queries.fetchall()
        select_queryFriends.close()
        self.db.close()
        return resultStatus[0][0], resultFriends
        
    
    def selectAllInvitingGames(self, username : str) -> list:
        self.connectDb()
        select_queryFriends = self.select()
        
        select_queryFriends.execute(f"SELECT nameUser_1 FROM invitingGames WHERE toNameUser_2 = '{username}'")
        
        resultInviting = select_queryFriends.queries.fetchall()
        select_queryFriends.close()
        self.db.close()
        return resultInviting
    
    
    def acceptInvitingGames(self, usernamePlayer : str, usernameUseradd : str) -> list:
        self.connectDb()
        select_queryFriends = self.select()
        
        select_queryFriends.execute(f"SELECT infoGame FROM invitingGames WHERE toNameUser_2 = '{usernamePlayer}' AND nameUser_1 = '{usernameUseradd}'")
        
        resultGame = select_queryFriends.queries.fetchall()
        select_queryFriends.close()
        self.db.close()
        
        self.deleteInvitingGames(usernameUseradd, usernamePlayer)
        
        return resultGame
    
    
    def sendInvitingGames(self, usernamePlayer : str, usernameUseradd : str, ip : str, port : int) -> None:
        self.connectDb()
        cursor = self.db.cursor()
        
        insert_query = f"INSERT INTO invitingGames (nameUser_1, toNameUser_2, infoGame) VALUES (%s, %s, %s)"
        values = (usernamePlayer,usernameUseradd,(str(ip) + ":" + str(port)))

        cursor.execute(insert_query, values)
        self.db.commit()

        cursor.close()
        self.db.close()
        
        
    def deleteInvitingGames(self, usernamePlayer : str, usernameUseradd :str) -> None:
        self.connectDb()
        delete_query = self.delete()
        delete_query.execute(f"DELETE FROM invitingGames WHERE nameUser_1 = '{usernamePlayer}' AND toNameUser_2 = '{usernameUseradd}'")
        
        self.db.commit()
        delete_query.close()
        self.db.close()
        
        
    def deleteFriends(self, usernamePlayer : str, usernameUseradd : str) -> None:
        self.connectDb()
        delete_query = self.delete()
        delete_query.execute(f"DELETE FROM friends WHERE nameUser_1 = '{usernamePlayer}' AND toNameUser_2 = '{usernameUseradd}'")
        
        self.db.commit()
        delete_query.close()
        self.db.close()
        
        
    def addFriends(self, usernamePlayer : str, usernameUseradd :str) -> None:
        self.connectDb()
        cursor = self.db.cursor()
        
        insert_query = f"INSERT INTO friends (nameUser_1, toNameUser_2) VALUES (%s, %s)"
        values = (usernamePlayer,usernameUseradd,)

        cursor.execute(insert_query, values)
        self.db.commit()

        cursor.close()
        self.db.close()
        
        
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
        self.dropTableIfExists(ip, port)
        self.connectDb()
        cursor = self.db.cursor()
        table_name = f"Game{ip.replace('.', '_')}{port}"
        create_table_query = f"""
        CREATE TABLE {table_name} (
            ID INT,
            username VARCHAR(255)
        )
        """
        cursor.execute(create_table_query)
        cursor.close()
        self.db.close()
        
        
    def dropTableIfExists(self, ip : str, port : int):
        self.connectDb()
        cursor = self.db.cursor()
        table_name = f"Game{ip.replace('.', '_')}{port}"
        check_table_query = f"SHOW TABLES LIKE '{table_name}'"
        cursor.execute(check_table_query)
        table_exists = cursor.fetchone()
        if table_exists:
            drop_table_query = f"DROP TABLE {table_name}"
            cursor.execute(drop_table_query)
        cursor.close()
        self.db.close()
        
        
    def insertUsername(self, ip: str, port: int, username: str) -> None:
        self.connectDb()
        cursor = self.db.cursor()

        table_name = f"Game{ip.replace('.', '_')}{port}"
        
        insert_query = f"INSERT INTO {table_name} (ID, username) VALUES (%s, %s)"
        values = (self.numUser, username)

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
        self.db.close()
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
            self.db.close()
        else:
            print("User not found.")


    # def deconnexionUser(self, ip: str, port: int, id: int):
    #     self.connectDb()
    #     delete_query = self.delete()
    #     delete_query.execute(f"DELETE FROM Game{ip.replace('.', '_')}{port} WHERE ID = {id}")

    #     self.db.commit()
    #     delete_query.close()
    #     self.db.close()
    
    
    def refreshTabel(self, ip: str, port: int):
        self.connectDb()
        select_query = self.select()
        select_query.execute(f"SELECT ID FROM Game{ip.replace('.', '_')}{port} ORDER BY ID ASC")
        rows = select_query.queries.fetchall()

        for index, row in enumerate(rows, start=1):
            new_id = index
            existing_id = row[0]

            if new_id != existing_id:
                update_query = self.update()
                update_query.execute(f"UPDATE Game{ip.replace('.', '_')}{port} SET ID = {new_id} WHERE ID = {existing_id}")
                self.db.commit()

        select_query.close()
        self.db.close()


    def addGame(self, username):
        if username == " ":
            return None
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT games FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        if result is not None:
            current_games = result[0]
            new_nbrgames = current_games + 1
            update_query = self.update()
            update_query.execute("UPDATE users SET games = %s WHERE username = %s", (new_nbrgames, username))
            update_query.close()
            self.db.close()
        else:
            print("User not found.")
            
            
    def getMoney(self, username):
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT money FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        self.db.close()
        
        if result is not None:
            return result[0]
        else:
            return 0


    def removeMoney(self, username, money):
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT money FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        if result is not None:
            current_money = result[0]
            new_Moneys = current_money - money
            update_query = self.update()
            update_query.execute("UPDATE users SET money = %s WHERE username = %s", (new_Moneys, username))
            update_query.close()
            self.db.close()
        else:
            print("User not found.")
    
    
    def addMap(self, username, map_name):
        if username == " ":
            return None
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT maps FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        if result is not None:
            current_maps = result[0]
            if current_maps:
                current_maps += ", "
            new_maps = current_maps + map_name
            update_query = self.update()
            update_query.execute("UPDATE users SET maps = %s WHERE username = %s", (new_maps, username))
            update_query.close()
            self.db.close()
        else:
            print("User not found.")
    
    
    def getUserIdByUsername(self, username):
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT id FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        self.db.close()

        if result is not None:
            return result[0]
        else:
            return None
    
    
    def addPurchase(self, user_id, map):
        self.connectDb()
        insert_query = self.insert()
        insert_query.execute("INSERT INTO purchases (user_id, map_name) VALUES (%s, %s)", (user_id, map))
        insert_query.close()
        self.db.close()
        
        
    def getMapByUsername(self, username):
        self.connectDb()
        select_query = self.select()
        select_query.execute("SELECT maps FROM users WHERE username = %s", (username,))
        result = select_query.fetchone()
        select_query.close()
        self.db.close()

        if result is not None:
            maps = result[0]
            map_list = maps.split(", ")
            return map_list
        else:
            return []