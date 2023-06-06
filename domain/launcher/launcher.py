from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from infrastructure.services.services import restartGame
from domain.network.network import joinSession, startSession
from domain.network.scanNetwork import ScanNetwork
from infrastructure.database.config import Database
import hashlib
import os
import time

class QuoridorLauncher:
    def __init__(self, db: Database) -> None:
        self.window = Tk()
        self.window.title("Mon Launcher")
        
        if os.name == "nt":
            self.window.attributes("-fullscreen", True)
            
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}")
        self.selectPlayer = 2
        self.selectIA = 0
        self.selectSize = 5
        self.selectFence = 4
        self.selectMap = 1
        self.selectIaDifficulty = 0
        self.statut = 0
        self.db = db
        self.ip = None
        self.port = None
        self.loginPassword = None
        self.loginButton = None
        self.winButton = None
        self.loginUsername = None
        self.login = None
        self.registerButton = None
        self.register = None
        self.registerUsername = None
        self.registerPassword = None
        self.insert_query = None
        self.login_created = None
        self.register_created = None
        self.widget_register = []
        self.widget_login = []
        self.widget_label = []
        self.pseudo = " "
        self.owned = Image.open(f"./assets/images/launcher/buy.png")
        self.owned = self.owned.resize((385, 66))
        self.owned = ImageTk.PhotoImage(self.owned)
        
        self.buying_fail = Image.open(f"./assets/images/launcher/buying_fail.png")
        self.buying_fail = self.buying_fail.resize((385, 66))
        self.buying_fail = ImageTk.PhotoImage(self.buying_fail)
        
            
        leave_friend = Image.open(f"./assets/images/launcher/leave_friend.png")
        leave_friend = leave_friend.resize((34, 32))
        self.leave_friends = ImageTk.PhotoImage(leave_friend)
        
        list_friend = Image.open(f"./assets/images/launcher/list_friends.png")
        menu_height = self.window.winfo_screenheight()
        self.list_friend = list_friend.resize((int(self.window.winfo_screenwidth() / 5), menu_height))
        self.list_friends = ImageTk.PhotoImage(self.list_friend)
        
        list_notification = Image.open(f"./assets/images/launcher/list_notifications.png")
        menu_height = self.window.winfo_screenheight()
        self.list_notification = list_notification.resize((int(self.window.winfo_screenwidth() / 5), menu_height))
        self.list_notifications = ImageTk.PhotoImage(self.list_notification)
        
        delete_friend = Image.open(f"./assets/images/launcher/delete_friends.png")
        delete_friend = delete_friend.resize((25, 29))
        self.delete_friends = ImageTk.PhotoImage(delete_friend)
        
        valid_friend = Image.open(f"./assets/images/launcher/check.png")
        valid_friend = valid_friend.resize((25, 29))
        self.valid_friends = ImageTk.PhotoImage(valid_friend)
        
        invite_friend = Image.open(f"./assets/images/launcher/invite_friends.png")
        invite_friend = invite_friend.resize((40, 29))
        self.invite_friends = ImageTk.PhotoImage(invite_friend)
        
        search_friend = Image.open(f"./assets/images/launcher/search_friends.png")
        search_friend = search_friend.resize((29, 29))
        self.search_friends = ImageTk.PhotoImage(search_friend)
        
        no_notification = Image.open(f"./assets/images/launcher/no_notification.png")
        no_notification = no_notification.resize((28, 29))
        self.no_notification = ImageTk.PhotoImage(no_notification)
        
        notifications = Image.open(f"./assets/images/launcher/notifications.png")
        notifications = notifications.resize((28, 29))
        self.notifications = ImageTk.PhotoImage(notifications)
        
        back_list_friends = Image.open(f"./assets/images/launcher/back_list_friends.png")
        back_list_friends = back_list_friends.resize((35, 35))
        self.back_list_friends = ImageTk.PhotoImage(back_list_friends)
        
        self.menuCreateGameSolo(event=None)
        
        
    def background(self, statut) -> None:
        self.statut = statut
        self.bg_image = Image.open(f"./assets/images/launcher/launcher{self.statut}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    def changeMode(self) -> None:
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
        
        
    def createMenu(self, statut) -> None:
        self.statut = statut
        menu_image = Image.open(f"./assets/images/launcher/menu{self.statut}.png")
        menu_image = menu_image.resize((115, 320))
        self.menu = ImageTk.PhotoImage(menu_image)
        
        canvas = Canvas(self.window, width=self.menu.width(), height=self.menu.height(), bd=0, highlightthickness=0)
        canvas.place(relx=0.023, y=self.window.winfo_screenheight() / 2 - self.menu.height() / 2)
        
        canvas.create_image(0, 0, anchor=NW, image=self.menu)
        canvas.bind("<Button-1>", lambda event: self.clickMenu(event, self.menuCreateGameSolo, self.menuJoinGameNetwork, self.menuCreateGameNetwork))
        
        parameters = Image.open(f"./assets/images/launcher/parameters.png")
        parameters = parameters.resize((90, 90))
        self.parameters = ImageTk.PhotoImage(parameters)

        parameters_x = 52
        
        settings = Canvas(self.window, width=self.parameters.width(), height=self.parameters.height(), bd=0, highlightthickness=0)
        settings.place(x=parameters_x, rely=0.85)
        settings.create_image(0, 0, anchor=NW, image=self.parameters)
        
        def parameter(event):
            print("Section parametres")
        
        settings.bind("<Button-1>", parameter)
        
        shop = Image.open(f"./assets/images/launcher/shop.png")
        shop = shop.resize((90, 90))
        self.shop = ImageTk.PhotoImage(shop)

        shop_x = 52 
        
        shops = Canvas(self.window, width=self.shop.width(), height=self.shop.height(), bd=0, highlightthickness=0)
        shops.place(x=shop_x, rely=0.72)
        shops.create_image(0, 0, anchor=NW, image=self.shop)
        
        shops.bind("<Button-1>", lambda event: self.displayShop())
        
        self.addLogoAccount()
        self.displayPseudo()
        
        
    def addLogoAccount(self) -> None:
        account_image = Image.open(f"./assets/images/launcher/account.png")
        account_image = account_image.resize((34, 32))
        self.account_image = ImageTk.PhotoImage(account_image)

        self.account_button = Button(self.window, image=self.account_image, bd=0, highlightthickness=0, cursor="hand2", command=self.displayAccount)
        self.account_button.place(relx=0.99, rely=0.02, anchor=CENTER)

    
    def clickMenu(self, event, callback_zone1, callback_zone2, callback_zone3) -> None:
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        
        width = self.menu.width()
        height = self.menu.height()
        
        
        if 0 <= x <= width and 0 <= y <= height / 3:
            callback_zone1(event)
        elif 0 <= x <= width and height / 3 <= y <= height * 2 / 3:
            callback_zone2(event)
        elif 0 <= x <= width and height * 2 / 3 <= y <= height:
            callback_zone3(event)
    
    def createButtonShop(self) -> None:
        username = self.get_username("serverPseudo.txt")
        listMap = self.db.getMapByUsername(username)
        money = self.db.getMoney(username)

        map_info = [
            ("Ice", 1000, 0.29),
            ("Electricity", 2500, 0.55),
            ("Sugar", 5000, 0.81)
        ]

        for i, (map_name, map_price, relx) in enumerate(map_info, start=1):
            if map_name not in listMap:
                button = Button(self.window, text=f"Acheter {map_price}$", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=18, cursor="hand2", activebackground="#035388", activeforeground="white", command=lambda price=map_price, map=map_name: self.buy(price, map))
                button.place(relx=relx, rely=0.75, anchor=CENTER)
                if money < map_price:
                    # button.config(state="disabled")
                    pass
            else:
                label_owned = Label(self.window, image=self.owned, bd=0, highlightthickness=0)
                label_owned.place(relx=relx, rely=0.5, anchor=CENTER)


    def buy(self, price, map) -> None:
        if self.isConnected("serverPseudo.txt"):
            self.displayAccount()
        else:
            if map == "Ice":
                x = 0.29
            elif map == "Electricity":
                x = 0.55
            elif map == "Sugar":
                x = 0.81
            pseudo = self.get_username("serverPseudo.txt")
            money = self.db.getMoney(pseudo)
            if money >= price:
                self.db.removeMoney(pseudo, price)
                self.db.addMap(pseudo, map)
                id = self.db.getUserIdByUsername(pseudo)
                self.db.addPurchase(id, map)
                self.displayShop()
            else:
                label_buying_fail = Label(self.window, image=self.buying_fail, bd=0, highlightthickness=0)
                label_buying_fail.place(relx=x, rely=0.5, anchor=CENTER)
            self.displayPseudo()
    
    
    def displayPseudo(self) -> None:
        if self.isConnected("serverPseudo.txt"):
            login = Label(self.window, text="Vous n'êtes pas connecté", font=("Arial", 13), bg="#0F283F", fg="red")
            login.place(relx=0.85, rely=0.02, anchor=CENTER)
        else:
            username = self.get_username("serverPseudo.txt")
            money = self.db.getMoney(username)
            login = Label(self.window, text=f"Vous êtes connecté en tant que {username} : {money}$", font=("Arial", 13), bg="#0F283F", fg="green")
            login.place(relx=0.5, rely=0.02, anchor=CENTER)
            
            
    def addLogoFriends(self) -> None:
        if self.isConnected:
            friend = Image.open(f"./assets/images/launcher/friend.png")
            friend = friend.resize((34, 32))
            self.friends = ImageTk.PhotoImage(friend)
            
            self.friends_canvas = Button(self.window, image=self.friends, bd=0, highlightthickness=0, cursor="hand2", command=self.displayFriends)
            self.friends_canvas.place(relx=0.95, rely=0.02, anchor=CENTER)
            
            
    def displayFriends(self) -> None:
        self.friends_canvas.destroy()
        self.account_button.destroy()
        friends_panel = Label(self.window, image=self.list_friends, bd=0, highlightthickness=0)
        friends_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayListFriends(friends_panel)
        
        
    def quit_friends_list(self, panel) -> None:
        panel.destroy()
        self.addLogoFriends()
        self.addLogoAccount()
            
        
    def display_notifications(self, friends_panel : Label) -> None:
        def destroy_friends_list():
            friends_panel.destroy()
            
        destroy_friends_list()
        notifications_panel = Label(self.window, image=self.list_notifications, bd=0, highlightthickness=0)
        notifications_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayInvitatins(notifications_panel, True)
        
        self.displayGameInvitations(notifications_panel, False)
        
        self.notifications_panel = notifications_panel
        
        
    def quit_notifications(self, notifications_panel) -> None:
        notifications_panel.destroy()
        self.addLogoFriends()
        self.addLogoAccount()


    def back_friends_list(self, notifications_panel) -> None:
        notifications_panel.destroy()
        self.displayFriends()
            
            
    def displayGameInvitations(self, notifications_panel : Label, btnDisplay : bool) -> None:
        def blink_text(label):
            current_color = label.cget("fg")
            new_color = "#D7D03A" if current_color == "#93904D" else "#93904D"
            label.config(fg=new_color)
            label.after(500, blink_text, label)
        
        if btnDisplay:
            button_leave_friends = Label(notifications_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
            button_leave_friends.place(relx=0.92, rely=0.02, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.8, rely=0.02, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
                
        friend_game_demands = self.db.selectAllInvitingGames(self.get_username("serverPseudo.txt")) # demande de partie via la bdd
        for index, friend in enumerate(friend_game_demands):
            friend = friend[:19] + ".." if len(friend) > 21 else friend
            label_game_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="#D7D03A", bg="#102A43")
            label_game_demand.place(relx=0.1, rely=0.52 + index * 0.05, anchor=NW)
            blink_text(label_game_demand)

            accept_game_demand = Label(notifications_panel, image=self.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
            accept_game_demand.place(relx=0.75, rely=0.53 + index * 0.05, anchor=CENTER)
            accept_game_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptGameDemand(friend))
            
            refuse_game_demand = Label(notifications_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2",)
            refuse_game_demand.place(relx=0.9, rely=0.53 + index * 0.05, anchor=CENTER)
            refuse_game_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseGameDemand(friend))


    def displayInvitatins(self, notifications_panel : Label, btnDisplay: bool) -> None:
        if btnDisplay:
            button_leave_friends = Label(notifications_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
            button_leave_friends.place(relx=0.92, rely=0.02, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.8, rely=0.02, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
        
        friend_demands = self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)  # demande d'amis à récupérer depuis la bdd
        for index, friend in enumerate(friend_demands):
            friend = friend[:19] + ".." if len(friend) > 21 else friend
            label_friend_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            label_friend_demand.place(relx=0.1, rely=0.23 + index * 0.05, anchor=NW)

            valid_friend_demand = Label(notifications_panel, image=self.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
            valid_friend_demand.place(relx=0.75, rely=0.24 + index * 0.05, anchor=CENTER)
            valid_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptFriendDemand(friend))

            delete_friend_demand = Label(notifications_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
            delete_friend_demand.place(relx=0.9, rely=0.24 + index * 0.05, anchor=CENTER)
            delete_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseFriendDemand(friend))


    def displayListFriends(self, friends_panel : Label) -> None:
        if len(self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)) != 0 or len(self.db.selectAllInvitingGames(self.get_username("serverPseudo.txt"))) != 0:
            image_notifications = self.notifications
        else:
            image_notifications = self.no_notification
        button_notifications = Label(friends_panel, image=image_notifications, bd=0, highlightthickness=0, cursor="hand2")
        button_notifications.place(relx=0.75, rely=0.045, anchor=CENTER)
        button_notifications.bind("<Button-1>", lambda event: self.display_notifications(friends_panel))

        button_leave_friends = Button(friends_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
        button_leave_friends.place(relx=0.92, rely=0.02, anchor=CENTER)
        button_leave_friends.bind("<Button-1>", lambda event: self.quit_friends_list(friends_panel))


        friends = self.db.selectAllFriends(self.get_username("serverPseudo.txt"))  # liste des amis à récupérer depuis la bdd
        for index, friend in enumerate(friends):
            friend = friend[:19] + ".." if len(friend) > 21 else friend
            label_friend = Label(friends_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            label_friend.place(relx=0.1, rely=0.2 + index * 0.05, anchor=NW)

            invite_friend = Label(friends_panel, image=self.invite_friends, bd=0, highlightthickness=0, cursor="hand2")
            invite_friend.place(relx=0.75, rely=0.21 + index * 0.05, anchor=CENTER)
            invite_friend.bind("<Button-1>", lambda event, friend=friend: self.invitFriend(friend))

            delete_friend = Label(friends_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
            delete_friend.place(relx=0.9, rely=0.21 + index * 0.05, anchor=CENTER)
            delete_friend.bind("<Button-1>", lambda event, friend=friend: self.deleteFriends(friend))

        entry_friend = Entry(friends_panel, bd=0, font=("Arial", 13))
        entry_friend.place(relx=0.45, rely=0.115, anchor=CENTER)

        search_button = Button(friends_panel, image=self.search_friends, bd=0, highlightthickness=0, cursor="hand2", command=lambda: self.searchFriend(entry_friend.get()))
        search_button.place(relx=0.85, rely=0.115, anchor=CENTER)
        
        self.friends_panel = friends_panel
        
        
    def invitFriend(self, friend : tuple) -> None:
        self.db.sendInvitingGames(str(self.get_username("serverPseudo.txt")), friend[0], "127.0.0.1", 8000)

    
    def acceptFriendDemand(self, friend : tuple) -> None:
        self.db.acceptInviting(str(self.get_username("serverPseudo.txt")), friend[0])
        self.notifications_panel.config(text="")
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseFriendDemand(self, friend : tuple) -> None:
        self.db.deleteInviting(friend[0], str(self.get_username("serverPseudo.txt")))
        self.notifications_panel.config(text="")
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def acceptGameDemand(self, friend : tuple) -> None:
        resultGameInfo = self.db.acceptInvitingGames(str(self.get_username("serverPseudo.txt")), friend[0])
        (ip, port) = resultGameInfo[0][0].split(":")
        print(ip, port)
        # joinSession(ip, int(port), 1)
        
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseGameDemand(self, friend : tuple) -> None:
        self.db.deleteInvitingGames(friend[0], str(self.get_username("serverPseudo.txt")))

        time.sleep(1)
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def searchFriend(self, friend : str) -> None:
        friend = friend.replace(" ", "")
        invList = self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)
        friendsList = self.db.selectAllFriends(self.get_username("serverPseudo.txt"))
            
        if friend != "" and friend != self.get_username("serverPseudo.txt") and not any(friend in tupleInfos for tupleInfos in friendsList) and not any(friend in tupleInfosInv for tupleInfosInv in invList):
            self.db.sendInviting(self.get_username("serverPseudo.txt"), friend)
        
        
    def deleteFriends(self, friend):
        delete = Tk()
        delete.title("Confirmation de suppression")
        delete.geometry("500x200")
        delete.resizable(False, False)
        delete.config(bg="#0F283F")
        delete.iconbitmap("./assets/images/launcher/delete_friends.ico")

        def on_yes_click():
            delete.destroy()
            self.db.deleteFriends(self.get_username("serverPseudo.txt"), friend[0])
            self.db.deleteFriends(friend[0], self.get_username("serverPseudo.txt"))
            self.displayListFriends(self.friends_panel)

        def on_no_click():
            delete.destroy()


        if len(friend) > 15:
                friend = friend[:15] + ".."
        label = Label(delete, text=f"Êtes-vous sûr de vouloir supprimer l'ami '{friend}' ?", padx=20, pady=10, bd=0,
                    highlightthickness=0, font=("Arial", 13), fg="white", bg="#0F283F")
        label.place(relx=0.5, rely=0.4, anchor=CENTER)

        button_frame = Frame(delete, bg="#0F283F")
        button_frame.pack(pady=10)

        yes_button = Button(button_frame, text="Oui", bg="green", fg="#FFF", font=("Arial", 13), width=18, cursor="hand2", activebackground="green", command=on_yes_click)
        yes_button.pack(side="left", padx=20)

        no_button = Button(button_frame, text="Non", bg="red", fg="#FFF", font=("Arial", 13), width=18, cursor="hand2", activebackground="red", command=on_no_click)
        no_button.pack(side="left", padx=20)

        delete.update_idletasks() 
        width = delete.winfo_width()
        height = delete.winfo_height()
        x = (delete.winfo_screenwidth() // 2) - (width // 2)
        y = (delete.winfo_screenheight() // 2) - (height // 2)
        delete.geometry(f"{width}x{height}+{x}+{y}")

        button_frame.place(relx=0.5, rely=0.8, anchor="center")

        delete.mainloop()


    def displayShop(self) -> None:
        self.changeMode()
        statut = self.getStatut()
        self.statut = 5
        self.background(self.statut)
        self.createMenu(statut)
        self.createButtonShop()
        self.addLogoFriends()
            
            
    def numberIA(self) -> None:
        def action(event) -> None:
            self.selectIA = int(listIA.get())
            print("IA : ", self.selectIA)
            
        listIAs=[0, 1, 2, 3]
        listIA = ttk.Combobox(self.window, values=listIAs, state="readonly")
        listIA.current(0)
        listIA.place(relx=0.45, rely=0.73, anchor=CENTER)
        listIA.bind("<<ComboboxSelected>>", action)
        if self.statut == 0:
            nbrIA = Label(self.window, text="Nombre d'IA", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
            nbrIA.place(relx=0.45, rely=0.7, anchor=CENTER)
    
    
    def getIaDifficulty(self) -> None:
        def action(event) -> None:
            self.selectIaDifficulty = listIAdifficulty.get()
            print("IA difficulty : ", self.selectIaDifficulty)
            try:
                if self.selectIaDifficulty == "Facile":
                    self.selectIaDifficulty = 1
                elif self.selectIaDifficulty == "Moyenne":
                    self.selectIaDifficulty = 2
                elif self.selectIaDifficulty == "Difficile":
                    self.selectIaDifficulty = 3
            except ValueError:
                print(f"Error: '{self.selectIaDifficulty}' is not a valid level")

        listIAdifficultys=["Facile", "Moyenne", "Difficile"]
        listIAdifficulty = ttk.Combobox(self.window, values=listIAdifficultys, state="readonly")
        listIAdifficulty.current(0)
        listIAdifficulty.place(relx=0.55, rely=0.73, anchor=CENTER)
        listIAdifficulty.bind("<<ComboboxSelected>>", action)
        if self.statut == 0:
            nbrIA = Label(self.window, text="Difficulté des bots", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
            nbrIA.place(relx=0.55, rely=0.7, anchor=CENTER)


    def numberPlayer(self) -> None:
        def action(event) -> None:
            self.selectPlayer = int(listPlayer.get())
            print("Player : ", self.selectPlayer)

        if self.statut == 0:
            listPlayers = [1, 2, 3, 4]
            currentSelection = 1
        else:
            listPlayers = [2, 4]
            currentSelection = 0
            
        listPlayer = ttk.Combobox(self.window, values=listPlayers, state="readonly")
        listPlayer.current(currentSelection)
        listPlayer.place(relx=0.35, rely=0.73, anchor=CENTER)
        listPlayer.bind("<<ComboboxSelected>>", action)
        if self.statut == 0 or self.statut == 2:
            nbrPlayer = Label(self.window, text="Nombre de Joueur(s)", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
            nbrPlayer.place(relx=0.35, rely=0.7, anchor=CENTER)


    def sizeBoard(self) -> None:
        def action(event) -> None:
            self.selectSize = int(listSize.get())
            print("Board : ", self.selectSize)

        listSizes=[5, 7, 9, 11]
        listSize = ttk.Combobox(self.window, values=listSizes, state="readonly")
        listSize.current(0)
        if self.statut == 0:
            x = 0.65
            y = 0.73
            x2 = 0.65
            y2 = 0.7
        elif self.statut == 2:
            x = 0.55
            y = 0.73
            x2 = 0.55
            y2 = 0.7
        listSize.place(relx=x, rely=y, anchor=CENTER)
        listSize.bind("<<ComboboxSelected>>", action)

        nbrIA = Label(self.window, text="Taille du plateau", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
        nbrIA.place(relx=x2, rely=y2, anchor=CENTER)


    def numberFence(self) -> None:
        def action(event) -> None:
            self.selectFence = int(listFence.get())
            print("Fence : ", self.selectFence)

        listFences = []
        for i in range(4, 41):
            if i % 4 == 0:
                listFences.append(i)

        listFence = ttk.Combobox(self.window, values=listFences, state="readonly")
        listFence.current(0)
        if self.statut == 0:
            x = 0.75
            y = 0.73
            x2 = 0.75
            y2 = 0.7
        elif self.statut == 2:
            x = 0.45
            y = 0.73
            x2 = 0.45
            y2 = 0.7
        listFence.place(relx=x, rely=y, anchor=CENTER)
        listFence.bind("<<ComboboxSelected>>", action)
        nbrFence = Label(self.window, text="Nombre de barrières", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
        nbrFence.place(relx=x2, rely=y2, anchor=CENTER)


    def choiceMap(self) -> None:
        def action(event) -> None:
            selected_value = listMap.get()
            print("Value : ", selected_value)
            try:
                if selected_value == "Jungle":
                    self.selectMap = 1
                elif selected_value == "Space":
                    self.selectMap = 2
                elif selected_value == "Hell":
                    self.selectMap = 3
                elif selected_value == "Ice":
                    self.selectMap = 4
                elif selected_value == "Electricity":
                    self.selectMap = 5
                elif selected_value == "Sugar":
                    self.selectMap = 6
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")
                
        username = self.get_username("serverPseudo.txt")
        listMaps=self.db.getMapByUsername(username)
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(0)
        X = 0.25
        Y = 0.73
        if self.statut == 1 or self.statut == 3:
            X = 0.45
        listMap.place(relx=X, rely=Y, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        if self.statut == 0 or self.statut == 2:
            nameMap = Label(self.window, text="Thème de la carte", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
            nameMap.place(relx=0.25, rely=0.7, anchor=CENTER)
        
        
    def buttonStart(self) -> None:
        def start_game() -> None:
            if hasattr(self, 'error_label'):
                self.error_label.destroy()
            grid_size = self.selectSize
            nbr_fences = self.selectFence
            nb_ia = self.selectIA
            nb_player = self.selectPlayer + self.selectIA
            if nb_player > 4 or nb_player < 2 or nb_player == 3:
                self.error_label = Label(self.window, text=f"Le nombre de joueurs ({nb_player}) est incorrect (2 ou 4).", font=("Arial", 13), bg="#0F283F", fg="red")
                self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            elif grid_size == 5 and nbr_fences > 20:
                    self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F283F", fg="red")
                    self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            else:
                map = self.selectMap
                self.window.destroy()
                restartGame(grid_size, nb_player, nb_ia, nbr_fences, map)

        start = Button(self.window, text="Lancer la partie", command=start_game, bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=18, cursor="hand2",  activebackground="#035388",  activeforeground="white")
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
    
    
    def menuCreateGameSolo(self, event):
        self.changeMode()
        self.statut = 0
        self.background(self.statut)
        self.createMenu(self.statut)
        self.numberIA()
        self.getIaDifficulty()
        self.numberPlayer()
        self.sizeBoard()
        self.numberFence()
        self.choiceMap()
        self.buttonStart()
        self.addLogoFriends()
        
    """REJOINDRE UNE PARTIE EN RESEAU"""
    def menuJoinGameNetwork(self, event):
        self.changeMode()
        if self.statut != 3:
            self.statut = 1
        self.background(self.statut)
        self.createMenu(self.statut)
        self.create_entries()
        self.choiceMap()
        self.addLogoFriends()
        
    def create_entries(self) -> None:
        ip = Label(self.window, text="Adresse IP :", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
        ip.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.entryIp = Entry(self.window, width=20)
        self.entryIp.place(relx=0.25, rely=0.73, anchor=CENTER)

        self.entryPortGame()
        
        map = Label(self.window, text="Thème de la carte :", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
        map.place(relx=0.45, rely=0.7, anchor=CENTER)
        
        start = Button(self.window, text="Rejoindre la partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.joinGameNetwork)
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
        
        reset_button = Button(self.window, text="Rechercher une partie", font=("Arial", 13),  cursor="hand2", fg="#FFF",  bg="#486581", command=self.displayIp, width=25, activebackground="#486581",  activeforeground="white")
        reset_button.place(relx=0.4, rely=0.8, anchor=CENTER)
        
    def joinGameNetwork(self) -> None:
        ip = self.entryIp.get()
        if hasattr(self, 'error_label'):
            self.error_label.destroy()
        parts = ip.split('.')
        if len(parts) != 4:
            self.error_label = Label(self.window, text=f"IP: {ip} invalide", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        for part in parts:
            if not part.isdigit() or int(part) > 255:
                self.error_label = Label(self.window, text=f"IP: {ip} invalide", font=("Arial", 13), bg="#0F283F", fg="red")
                self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
                return

        portstr = self.entry_port.get()
        if portstr == "":
            self.error_label = Label(self.window, text="Veuillez renseigner un port", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        if not portstr.isdigit() or int(portstr) > 65535:
            self.error_label = Label(self.window, text=f"Port: {portstr} invalide", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        port = int(portstr)
        self.window.destroy()
        self.setUsername(self.pseudo)
        joinSession(ip, port, self.selectMap)
        
    
    def displayIp(self) -> None:
        scanNetwork = ScanNetwork(8000, 8005)
        scanNetwork.scan()
        listip = scanNetwork.getIp()
        print(listip)
        if len(listip) == 0:
            self.statut = 3
            self.menuJoinGameNetwork(event=None)
        for i, address in enumerate(listip):
            ip, port = address.split(":")
            frame = tk.LabelFrame(self.window, text=ip, fg="white", bg="blue", width=200)
            x = self.window.winfo_screenwidth() - 200 - 10  
            y = (i+1)/(len(listip)+1) * self.window.winfo_screenheight()
            frame.place(x=x, y=y, anchor='ne')
            label = tk.Label(frame, text="Port: " + port, fg="white", bg="blue")
            label.pack(padx=5, pady=5)
            frame.bind("<Button-1>", lambda event, ip=ip, port=port: self.onIpClick(event, port))
            
    def onIpClick(self, event, port):
        ip = event.widget['text']
        port = int(port)
        self.window.destroy()
        # self.db.insertUsername(ip, port, self.pseudo)
        self.setUsername(self.pseudo)
        joinSession(ip, port, self.selectMap)
        
    """CREER UNE GAME EN LOCAL"""
        
    def menuCreateGameNetwork(self, event):
        self.changeMode()
        print("Create Game Network")
        self.statut = 2
        self.background(self.statut)
        self.createMenu(self.statut)
        self.choiceMap()
        self.numberPlayer()
        self.sizeBoard()
        self.numberFence()
        self.entryPortGame()
        self.startButtonNetwork()
        self.addLogoFriends()
        
    def entryPortGame(self) -> None:
        if self.statut ==2:
            x = 0.65
            y = 0.7
            x2 = 0.65
            y2 = 0.73
        else:
            x = 0.35
            y = 0.7
            x2 = 0.35
            y2 = 0.73
        port = Label(self.window, text="Port :", font=("Arial", 10), bg="#0F283F", fg="#E3F8FF")
        port.place(relx=x, rely=y, anchor=CENTER)
        self.entry_port = Entry(self.window, width=20)
        self.entry_port.place(relx=x2, rely=y2, anchor=CENTER)
    
    def startButtonNetwork(self) -> None:
        start = Button(self.window, text="Créer une partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2,  cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.startGame)
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
    
    def startGame(self) -> None:
        portstr = self.entry_port.get()
        
        if hasattr(self, 'error_label'):
            self.error_label.destroy()

        if portstr == "":
            self.error_label = Label(self.window, text="Veuillez renseigner un port", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        if not portstr.isdigit() or int(portstr) > 65535:
            self.error_label = Label(self.window, text=f"Port: {portstr} invalide", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return
        
        port = int(portstr)
        nbr_player = int(self.selectPlayer)
        grid_size = self.selectSize
        nbr_fences = self.selectFence
        map = self.selectMap

        if grid_size == 5 and nbr_fences > 20:
            self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F283F", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        else:
            self.window.destroy()
            self.setUsername(self.pseudo)
            startSession(port, nbr_player, grid_size, nbr_player, 0, nbr_fences, map)
    
    """SE CONNECTER OU S'INSCRIRE"""
    
    def getStatut(self) -> int:
        return self.statut
    
    def displayAccount(self) -> None:
        self.changeMode()
        statut = self.getStatut()
        self.statut = 4
        self.background(self.statut)
        self.createMenu(statut)
        self.connexion()
        self.inscription()
        self.addLogoFriends()
    
    def connexion(self) -> None:
        login_image = Image.open(f"./assets/images/launcher/connexion.png")
        login_image = login_image.resize((300, 300))
        self.login_image = ImageTk.PhotoImage(login_image)

        self.login_button = Button(self.window, image=self.login_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addLogin)
        self.login_button.place(relx=0.35, rely=0.8, anchor=CENTER)
        
    def addLogin(self):
        self.login_button.configure(state=DISABLED)
        self.register_button.configure(state=NORMAL)
        if len(self.widget_register) > 0:
            for widget in self.widget_register:
                widget.destroy()
                
        username = Label(self.window, text="Pseudo :", font=("Arial", 13), bg="#0F283F", fg="#E3F8FF")
        username.place(relx=0.54, rely=0.68, anchor=CENTER)
        self.loginUsername = Entry(self.login)
        self.loginUsername.place(relx=0.54, rely=0.71, anchor=CENTER)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 13), bg="#0F283F", fg="#E3F8FF")
        password.place(relx=0.54, rely=0.76, anchor=CENTER)
        self.loginPassword = Entry(self.login, show="*")
        self.loginPassword.place(relx=0.54, rely=0.79, anchor=CENTER)

        self.loginButton =  Button(self.login, text="Se connecter", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2, cursor="hand2", activebackground="#035388", activeforeground="white", command=self.loginUser)
        self.loginButton.place(relx=0.54, rely=0.85, anchor=CENTER)
        
        self.widget_login = [username, self.loginUsername, password, self.loginPassword, self.loginButton]
    
    def loginUser(self):
        self.db.connectDb()
        select_query = self.db.select()
        query = "SELECT * FROM users WHERE username = %s"
        username = self.loginUsername.get().rstrip()
        password = self.loginPassword.get().replace(" ", "")

        select_query.execute(query, (username,))
        result = select_query.fetchone()
        select_query.close()

        if result is not None:
            stored_password = result[2]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if stored_password == hashed_password:
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text="Vous êtes bien connecté.")
                    self.pseudo = username
                    self.setUsername(username)
                    return self.pseudo
                else:
                    self.infoLabel = Label(self.window, text="Vous êtes bien connecté.", fg="green", font=("Arial", 13), bg="#0F283F")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
                    self.pseudo = username
                    self.setUsername(username)
                    return self.pseudo
            else:
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text="Mot de passe incorrect.")
                else:
                    self.infoLabel = Label(self.window, text="Mot de passe incorrect.", fg="red", font=("Arial", 13), bg="#0F283F")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        else:
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Cet utilisateur n'existe pas.")
            else:
                self.infoLabel = Label(self.window, text="Cet utilisateur n'existe pas.", fg="red", font=("Arial", 13), bg="#0F283F")
                self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        self.widget_label = [self.infoLabel]


    def inscription(self) -> None:
        register_image = Image.open(f"./assets/images/launcher/inscription.png")
        register_image = register_image.resize((300, 300))
        self.register_image = ImageTk.PhotoImage(register_image)
        self.register_button = Button(self.window, image=self.register_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addRegister)
        self.register_button.place(relx=0.73, rely=0.8, anchor=CENTER)
        
        
    def addRegister(self):
        self.register_button.configure(state=DISABLED)
        self.login_button.configure(state=NORMAL)
        if len(self.widget_login) > 0:
            for widget in self.widget_login:
                widget.destroy()
            
        username = Label(self.window, text="Pseudo :", font=("Arial", 13), bg="#0F283F", fg="#E3F8FF")
        username.place(relx=0.54, rely=0.6, anchor=CENTER)
        self.registerUsername = Entry(self.register)
        self.registerUsername.place(relx=0.54, rely=0.63, anchor=CENTER)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 13), bg="#0F283F", fg="#E3F8FF")
        password.place(relx=0.54, rely=0.68, anchor=CENTER)
        self.registerPassword = Entry(self.register, show="*")
        self.registerPassword.place(relx=0.54, rely=0.71, anchor=CENTER)

        passwordConfirm = Label(self.window, text="Confirmer le mot de passe :", font=("Arial", 13), bg="#0F283F", fg="#E3F8FF")
        passwordConfirm.place(relx=0.54, rely=0.76, anchor=CENTER)
        self.registerPasswordConfirm = Entry(self.register, show="*")
        self.registerPasswordConfirm.place(relx=0.54, rely=0.79, anchor=CENTER)

        self.registerButton = Button(self.register, text="S'inscrire", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2, cursor="hand2", activebackground="#035388", activeforeground="white", command=self.createAccount)
        self.registerButton.place(relx=0.54, rely=0.85, anchor=CENTER)
        self.widget_register = [username, self.registerUsername, password, self.registerPassword, passwordConfirm, self.registerPasswordConfirm, self.registerButton]
        
    def createAccount(self):
        self.db.connectDb()
        username = self.registerUsername.get().rstrip()
        password = self.registerPassword.get().replace(" ", "")
        confirm_password = self.registerPasswordConfirm.get()

        if not username or not password or not confirm_password:
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Veuillez remplir tous les champs")
            else:
                self.infoLabel = Label(self.window, text="Veuillez remplir tous les champs", fg="red", font=("Arial", 13), bg="#0F283F")
                self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        elif password != confirm_password:
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Les mots de passe ne correspondent pas")
            else:
                self.infoLabel = Label(self.window, text="Les mots de passe ne correspondent pas", fg="red", font=("Arial", 13), bg="#0F283F")
                self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        else:
            # Check si le username existe deja 
            select_query = self.db.select()
            select_query.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = select_query.fetchone()
            select_query.close()

            if existing_user:
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text=f"Ce pseudo '{username}' est déjà utilisé.")
                else:
                    self.infoLabel = Label(self.window, text=f"Ce pseudo '{username}' est déjà utilisé.", fg="red", font=("Arial", 13), bg="#0F283F")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
            else:
                # Si le pseudo est unique on l'insère dans la base de données
                insert_query = self.db.insert()
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                params = (username, hashed_password)
                insert_query.execute(query, params)
                insert_query.close()
                # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text=f"Bravo {username} ! Votre compte à bien été créé.")
                    self.pseudo = username
                    self.setUsername(username)
                    return self.pseudo
                else:
                    self.infoLabel = Label(self.window, text=f"Bravo {username} ! Vous êtes bien inscrit.", fg="green", font=("Arial", 13), bg="#0F283F")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
                    self.pseudo = username
                    self.setUsername(username)
                    return self.pseudo
        self.widget_label = [self.infoLabel]
        
        
    def setUsername(self, username):
        try:
            with open('serverPseudo.txt', 'a') as fichier:
                fichier.write(username)
        except IOError:
            print("Erreur : impossible d'écrire dans le fichier.")
            
            
    """ Vérifie si l'utilisateur est connecté"""
    def isConnected(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()
                return len(content) == 0
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False


    def get_username(self, file_path):
        try:
            with open(file_path, 'r') as file:
                username = file.read().strip()
                return username
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False

run_launcher = QuoridorLauncher(Database())
run_launcher.window.mainloop()