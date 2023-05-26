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


# INSERT
# db = Database()
# insert_query = db.insert()
# query = "INSERT INTO users (username, password) VALUES (%s, %s)"
# params = ("Hugo", "1234")
# insert_query.execute(query, params)
# insert_query.close()
# db.close()

# DELETE
# db = Database()
# delete_query = db.delete()
# query = "DELETE FROM users WHERE id = %s"
# params = (1,)
# delete_query.execute(query, params)
# delete_query.close()
# db.close()

# UPDATE
# db = Database()
# update_query = db.update()
# query = "UPDATE users SET username = %s WHERE id = %s"
# params = ("Jane Doe", 2)
# update_query.execute(query, params)
# update_query.close()
# db.close()

# SELECT
# db = Database()
# select_query = db.select()
# query = "SELECT * FROM users"
# result = select_query.execute(query)

# for row in result:
#     print(row)

# select_query.close()
# db.close()

class Graphique:
    def __init__(self, db: Database):
        self.loginPassword = None
        self.loginButton = None
        self.winButton = None
        self.loginUsername = None
        self.login = None
        self.registerButton = None
        self.register = None
        self.registerUsername = None
        self.registerPassword = None
        self.db = db
        self.root = Tk()
        self.root.title("Quoridor")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        self.insert_query = None
        self.addRegister()
        self.addLogin()
        self.buttonWin("adrien")
        self.root.mainloop()

    def addRegister(self):
        self.register = Frame(self.root)
        self.register.pack()

        self.registerUsername = Entry(self.register)
        self.registerUsername.pack()

        self.registerPassword = Entry(self.register)
        self.registerPassword.pack()

        self.registerButton = Button(self.register, text="Register", command=self.createAccount)
        self.registerButton.pack()

    def createAccount(self):
        self.db.connectDb()
        username = self.registerUsername.get()
        password = self.registerPassword.get()
        if not username or not password:
            text = Label(self.root, text="Please complete all mandatory fields.")
            text.pack()
        else:
            # Check if the username already exists
            select_query = self.db.select()
            select_query.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = select_query.fetchone()
            select_query.close()

            if existing_user:
                text = Label(self.root,
                             text=f"This username '{username}' already exist. Please choose another.")
                text.pack()
            else:
                # Username is unique, register
                insert_query = self.db.insert()
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                params = (username, hashed_password)
                insert_query.execute(query, params)
                insert_query.close()
                text = Label(self.root, text=f"{username} you have successfully subscribed !")
                text.pack()

    def addLogin(self):
        self.login = Frame(self.root)
        self.login.pack()

        self.loginUsername = Entry(self.login)
        self.loginUsername.pack()

        self.loginPassword = Entry(self.login)
        self.loginPassword.pack()

        self.loginButton = Button(self.login, text="Login", command=self.loginUser)
        self.loginButton.pack()

    def loginUser(self):
        self.db.connectDb()
        select_query = self.db.select()
        query = "SELECT * FROM users WHERE username = %s"
        username = self.loginUsername.get()
        password = self.loginPassword.get()

        select_query.execute(query, (username,))
        result = select_query.fetchone()
        select_query.close()

        if result is not None:
            stored_password = result[2]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if stored_password == hashed_password:
                text = Label(self.root, text="you are logged")
                text.pack()
            else:
                text = Label(self.root, text="password incorrect")
                text.pack()
        else:
            text = Label(self.root, text="User not found")
            text.pack()

    def buttonWin(self, username):
        self.winButton = Button(self.root, text="WIN", command=lambda: self.addWin(username))
        self.winButton.pack(side=RIGHT)

    def addWin(self, username):
        self.db.connectDb()
        select_query = self.db.select()
        select_query.queries.execute("SELECT win FROM users WHERE username = %s", (username,))
        result = select_query.queries.fetchone()
        select_query.close()

        if result is not None:
            current_wins = result[0]
            new_wins = current_wins + 1

            update_query = self.db.update()
            update_query.execute("UPDATE users SET win = %s WHERE username = %s", (new_wins, username))
            update_query.close()
        else:
            print("User not found.")



