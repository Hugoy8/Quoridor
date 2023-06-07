from tkinter import *
import tkinter as tk
from tkinter import ttk
from infrastructure.services.services import restartGame
from domain.network.network import joinSession, startSession
from domain.network.scanNetwork import ScanNetwork
import hashlib

class QuoridorLauncher:
    def __init__(self) -> None:
        # Page de lancement.
        from domain.launcher.launchScreen import LaunchScreen
        launchScreen = LaunchScreen()
        
        # Lancement de la class d'initialisation des variables, images, sons...
        from infrastructure.services.initLauncher import InitLauncher
        from infrastructure.database.config import Database
        initGame = InitLauncher(self, launchScreen)
        
        # Lancement de l'affichage du chargement.
        launchScreen.start()
        
        initGame.startInit(Database())
            
        # Lancement de l'affichage du launcher.
        self.menuCreateGameSolo(event=None)
        
        launchScreen.status = False
        
        if launchScreen.is_alive():
            launchScreen.join()
        
        self.window.mainloop()
        
        
    def loadFavoriteMap(self):
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 7:
                try:
                    return int(lines[6].strip())
                except ValueError:
                    print("Error: Invalid value for favorite map")
        return 1
    
    def background(self, statut) -> None:
        self.statut = statut
        img_bg = getattr(self, f"bg_photo{statut}")
        self.bg_label = Label(self.window, image=img_bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    
    def changeMode(self) -> None:
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
        
        
    def createMenu(self, statut) -> None:
        self.statut = statut
        
        self.menu = getattr(self, f"menu{self.statut}")
        canvas = Canvas(self.window, width=self.menu.width(), height=self.menu.height(), bd=0, highlightthickness=0, cursor="hand2")
        canvas.place(relx=0.023, y=self.window.winfo_screenheight() / 2 - self.menu.height() / 2)
        
        canvas.create_image(0, 0, anchor=NW, image=self.menu)
        canvas.bind("<Button-1>", lambda event: self.clickMenu(event, self.menuCreateGameSolo, self.menuJoinGameNetwork, self.menuCreateGameNetwork))
        
        parameters_x = 52
        
        settings = Canvas(self.window, width=self.parameters.width(), height=self.parameters.height(), bd=0, highlightthickness=0, cursor="hand2")
        settings.place(x=parameters_x, rely=0.85)
        settings.create_image(0, 0, anchor=NW, image=self.parameters)
        
        
        settings.bind("<Button-1>", self.displayParameters)

        shop_x = 52 
        
        shops = Canvas(self.window, width=self.shop.width(), height=self.shop.height(), bd=0, highlightthickness=0, cursor="hand2")
        shops.place(x=shop_x, rely=0.72)
        shops.create_image(0, 0, anchor=NW, image=self.shop)
        
        shops.bind("<Button-1>", lambda event: self.displayShop())
        self.createAccountMenu()
    
    
    def displayParameters(self, event):
        self.changeMode()
        statut = self.getStatut()
        self.statut = 2
        self.background(self.statut)
        self.createMenu(statut)
        self.settingsActiveNotificationsSond()
        self.settingsSoundMap()
        self.settingsSoundVictory()
        self.settingsPionVolume()
        self.settingsFenceVolume()
        self.settingsNoFenceVolume()
        self.choiceFavoriteMap()
        
        
    def choiceFavoriteMap(self) -> None:
        def action(event) -> None:
            selected_value = listMap.get()
            print("Value : ", selected_value)
            try:
                if selected_value == "Jungle":
                    self.selectFavoriteMap = 1
                elif selected_value == "Space":
                    self.selectFavoriteMap = 2
                elif selected_value == "Hell":
                    self.selectFavoriteMap = 3
                elif selected_value == "Ice":
                    self.selectFavoriteMap = 4
                elif selected_value == "Electricity":
                    self.selectFavoriteMap = 5
                elif selected_value == "Sugar":
                    self.selectFavoriteMap = 6
                # Ajouter la valeur de self.selectFavoriteMap à la 7e ligne de settings.txt
                with open("settings.txt", "r") as file:
                    lines = file.readlines()
                if len(lines) >= 7:
                    lines[6] = str(self.selectFavoriteMap) + "\n"
                with open("settings.txt", "w") as file:
                    file.writelines(lines)
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")

        if self.isConnected("serverPseudo.txt") == False:
            username = self.get_username("serverPseudo.txt")
            listMaps = self.db.getMapByUsername(username)
        else:
            listMaps = ["Jungle", "Space", "Hell"]
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(self.selectFavoriteMap - 1)
        X = 0.25
        Y = 0.73
        if self.statut == 1 or self.statut == 3:
            X = 0.45
        listMap.place(relx=X, rely=Y, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        if self.statut == 0 or self.statut == 2:
            nameMap = Label(self.window, text="Votre carte favorite:", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
            nameMap.place(relx=0.25, rely=0.7, anchor=CENTER)

    
    # Activer ou désactiver le son des notifications de demande d'amis
    def settingsActiveNotificationsSond(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 1:
                self.active_sound_notification = lines[0].strip() == "True"

        def changeStatutSoundNotification(event):
            if self.active_sound_notification:
                self.active_sound_notification = False
            else:
                self.active_sound_notification = True
            update_statut()
            lines[0] = str(self.active_sound_notification) + "\n"  # Mettre à jour la première ligne

            with open("settings.txt", "w") as file:
                file.writelines(lines)  # Réécrire toutes les lignes dans le fichier

        def update_statut():
            if self.active_sound_notification:
                value = "Activé"
            else:
                value = "Désactivé"
            statut_sound_notification.config(text=value)

        sound_notification = Label(self.window, text="Son des notifications", bd=0, highlightthickness=0, cursor="hand2")
        sound_notification.place(relx=0.5, rely=0.5, anchor=CENTER)

        statut_sound_notification = Label(self.window, text="", bd=0, highlightthickness=0, cursor="hand2")
        statut_sound_notification.place(relx=0.5, rely=0.55, anchor=CENTER)
        update_statut()
        statut_sound_notification.bind("<Button-1>", changeStatutSoundNotification)
    
    
    # Modifier le son de la map
    def settingsSoundMap(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                self.sound_map = float(lines[1].strip())

        sound_map_texte = Label(self.window, text="Son de la map", bd=0, highlightthickness=0, cursor="hand2")
        sound_map_texte.place(relx=0.7, rely=0.75, anchor=CENTER)
        self.slider = Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, bg="#2C2F33", fg="#FFFFFF", troughcolor="#99AAB5", highlightthickness=0, cursor="hand2")
        self.slider.set(self.sound_map)  # Valeur initiale du slider
        self.slider.place(relx=0.7, rely=0.8, anchor=CENTER)
        self.slider.config(command=self.updateValue)

    def updateValue(self, value):
        value = float(value)
        self.saveValueToFile(value)

    def saveValueToFile(self, value):
        # Modifier la deuxième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()
        
        if len(lines) >= 2:
            lines[1] = str(value) + "\n"
        
        with open("settings.txt", "w") as file:
            file.writelines(lines)
    
    # modifier le son de la victoire 
    def settingsSoundVictory(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                self.sound_victory = float(lines[2].strip())

        sound_victory_texte = Label(self.window, text="Son de la victoire", bd=0, highlightthickness=0, cursor="hand2")
        sound_victory_texte.place(relx=0.5, rely=0.75, anchor=CENTER)
        self.slider_victory = Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, bg="#2C2F33", fg="#FFFFFF", troughcolor="#99AAB5", highlightthickness=0, cursor="hand2")
        self.slider_victory.set(self.sound_victory)  # Valeur initiale du slider
        self.slider_victory.place(relx=0.5, rely=0.8, anchor=CENTER)
        self.slider_victory.config(command=self.updateVictoryValue)

    def updateVictoryValue(self, value):
        value = float(value)
        self.saveVictoryValueToFile(value)

    def saveVictoryValueToFile(self, value):
        # Modifier la troisième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()

        if len(lines) >= 3:
            lines[2] = str(value) + "\n"

        with open("settings.txt", "w") as file:
            file.writelines(lines)

    # Modifier le volume du pion
    def settingsPionVolume(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 4:
                self.pion_volume = float(lines[3].strip())

        pion_volume_texte = Label(self.window, text="Volume du pion", bd=0, highlightthickness=0, cursor="hand2")
        pion_volume_texte.place(relx=0.5, rely=0.9, anchor=CENTER)
        self.slider_pion_volume = Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, bg="#2C2F33", fg="#FFFFFF", troughcolor="#99AAB5", highlightthickness=0, cursor="hand2")
        self.slider_pion_volume.set(self.pion_volume)  # Valeur initiale du slider
        self.slider_pion_volume.place(relx=0.5, rely=0.95, anchor=CENTER)
        self.slider_pion_volume.config(command=self.updatePionVolume)

    def updatePionVolume(self, value):
        value = float(value)
        self.savePionVolumeToFile(value)

    def savePionVolumeToFile(self, value):
        # Modifier la quatrième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()

        if len(lines) >= 4:
            lines[3] = str(value) + "\n"

        with open("settings.txt", "w") as file:
            file.writelines(lines)
            
            
    # Modifier le volume des clôtures
    def settingsFenceVolume(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 5:
                self.fence_volume = float(lines[4].strip())

        fence_volume_texte = Label(self.window, text="Volume des clôtures", bd=0, highlightthickness=0, cursor="hand2")
        fence_volume_texte.place(relx=0.3, rely=0.8, anchor=CENTER)
        self.slider_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, bg="#2C2F33", fg="#FFFFFF", troughcolor="#99AAB5", highlightthickness=0, cursor="hand2")
        self.slider_fence_volume.set(self.fence_volume)  # Valeur initiale du slider
        self.slider_fence_volume.place(relx=0.3, rely=0.85, anchor=CENTER)
        self.slider_fence_volume.config(command=self.updateFenceVolume)

    def updateFenceVolume(self, value):
        value = float(value)
        self.saveFenceVolumeToFile(value)

    def saveFenceVolumeToFile(self, value):
        # Modifier la cinquième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()

        if len(lines) >= 5:
            lines[4] = str(value) + "\n"

        with open("settings.txt", "w") as file:
            file.writelines(lines)
    
        
    # Modifier le volume du son "no fence"
    def settingsNoFenceVolume(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 6:
                self.no_fence_volume = float(lines[5].strip())

        no_fence_volume_texte = Label(self.window, text="Volume du son 'No Fence'", bd=0, highlightthickness=0, cursor="hand2")
        no_fence_volume_texte.place(relx=0.4, rely=0.45, anchor=CENTER)
        self.slider_no_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, length=200, bg="#2C2F33", fg="#FFFFFF", troughcolor="#99AAB5", highlightthickness=0, cursor="hand2")
        self.slider_no_fence_volume.set(self.no_fence_volume)  # Valeur initiale du slider
        self.slider_no_fence_volume.place(relx=0.4, rely=0.5, anchor=CENTER)
        self.slider_no_fence_volume.config(command=self.updateNoFenceVolume)

    def updateNoFenceVolume(self, value):
        value = float(value)
        self.saveNoFenceVolumeToFile(value)

    def saveNoFenceVolumeToFile(self, value):
        # Modifier la sixième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()

        if len(lines) >= 6:
            lines[5] = str(value) + "\n"

        with open("settings.txt", "w") as file:
            file.writelines(lines)
        
    def createAccountMenu(self) -> None:
        if self.isConnected("serverPseudo.txt") == False:
            self.bg_connect = Label(self.window, image=self.background_connect, bd=0, highlightthickness=0, cursor="hand2")
            self.bg_connect.place(relx=1, rely=0, anchor=NE)
            self.addLogoFriends(self.bg_connect)
            self.addLogoDeconnexion(self.bg_connect)
            self.displayPseudo(self.bg_connect)
        else:
            self.bg_not_connected = Label(self.window, image=self.background_not_connect, bd=0, highlightthickness=0, cursor="hand2")
            self.bg_not_connected.bind("<Button-1>", lambda event: self.displayAccount())
            self.bg_not_connected.place(relx=1, rely=0, anchor=NE)
            self.addLogoAccount(self.bg_not_connected)
    
    def displayPseudo(self, label) -> None:
        username = self.get_username("serverPseudo.txt")
        username = username[:7] + ".." if len(username) > 7 else username
        pseudo = Label(label, text=f"{username}", font=("Arial", 15), bg="#00172D", fg="white")
        pseudo.place(relx=0.53, rely=0.62, anchor=NW)
        
        statut = Label(label, text=f"Online", font=("Arial", 11), bg="#00172D", fg="#0D860A")
        statut.place(relx=0.53, rely=0.76, anchor=NW)
    
    def addLogoDeconnexion(self, label) -> None:
        self.deconnexion_user = Label(label, image=self.deconnexion, bd=0, highlightthickness=0, cursor="hand2")
        self.deconnexion_user.place(relx=0.8, rely=0.3, anchor=CENTER)
        self.deconnexion_user.bind("<Button-1>", lambda event: self.deconnexionUser("serverPseudo.txt"))
        
    def addLogoFriends(self, label) -> None:
        self.friends_canvas = Label(label, image=self.friends, bd=0, highlightthickness=0, cursor="hand2")
        self.friends_canvas.place(relx=0.3, rely=0.3, anchor=CENTER)
        self.friends_canvas.bind("<Button-1>", lambda event: self.displayFriends())
        
    def addLogoAccount(self, label) -> None:
        self.account_button = Label(label, image=self.account_image, bd=0, highlightthickness=0, cursor="hand2")
        self.account_button.bind("<Button-1>", lambda event: self.displayAccount())
        self.account_button.place(relx=0.5, rely=0.5, anchor=CENTER)

    
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
                image_buy = getattr(self, f"buy{i}")
                button = Button(self.window, image=image_buy, cursor="hand2", bd=0, highlightthickness=0, activebackground="#035388", activeforeground="white", command=lambda price=map_price, map=map_name: self.buy(price, map))
                button.place(relx=relx, rely=0.8, anchor=CENTER)
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
    
    
    def displayMoney(self) -> None:
        username = self.get_username("serverPseudo.txt")
        money = self.db.getMoney(username)
        login = Label(self.window, text=f"Vous avez : {money}", font=("Arial", 20), bg="#10283D", fg="white")
        login.place(relx=0.55, rely=0.95, anchor=CENTER)
        money_image = Label(self.window, image=self.image_money, bd=0, highlightthickness=0, cursor="hand2")
        money_image.place(relx=0.63, rely=0.945, anchor=CENTER)
            
            
    def displayFriends(self) -> None:
        self.bg_connect.destroy()
        friends_panel = Label(self.window, image=self.list_friends, bd=0, highlightthickness=0)
        friends_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayListFriends(friends_panel)
        
        
    def quit_friends_list(self, panel) -> None:
        panel.destroy()
        self.createAccountMenu()
            
        
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
        self.createAccountMenu()


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
            button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.1, rely=0.045, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
        
        text_invitation = Label(notifications_panel, text="Invitation à des parties :", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
        text_invitation.place(relx=0.09, rely=0.5, anchor=NW)
        friend_game_demands = self.db.selectAllInvitingGames(self.get_username("serverPseudo.txt")) # demande de partie via la bdd
        if len(friend_game_demands) == 0:
            no_friend_demand = Label(notifications_panel, text="Aucune notifications ...", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            no_friend_demand.place(relx=0.5, rely=0.55, anchor=CENTER)
        else:
            for index, friend in enumerate(friend_game_demands):
                friend = friend[:19] + ".." if len(friend) > 21 else friend
                label_game_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="#D7D03A", bg="#102A43")
                label_game_demand.place(relx=0.1, rely=0.54 + index * 0.05, anchor=NW)
                blink_text(label_game_demand)

                accept_game_demand = Label(notifications_panel, image=self.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
                accept_game_demand.place(relx=0.75, rely=0.55 + index * 0.05, anchor=CENTER)
                accept_game_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptGameDemand(friend))
                
                refuse_game_demand = Label(notifications_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2",)
                refuse_game_demand.place(relx=0.9, rely=0.55 + index * 0.05, anchor=CENTER)
                refuse_game_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseGameDemand(friend))


    def displayInvitatins(self, notifications_panel : Label, btnDisplay: bool) -> None:
        if btnDisplay:
            button_leave_friends = Label(notifications_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
            button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.1, rely=0.045, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
        
        text_friend_demand = Label(notifications_panel, text="Demande d'amis :", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
        text_friend_demand.place(relx=0.09, rely=0.1, anchor=NW)
        
        friend_demands = self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)  # demande d'amis à récupérer depuis la bdd
        if len(friend_demands) == 0:
            no_friend_demand = Label(notifications_panel, text="Aucune notifications...", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            no_friend_demand.place(relx=0.5, rely=0.15, anchor=CENTER)
        else:
            for index, friend in enumerate(friend_demands):
                friend = friend[:19] + ".." if len(friend) > 21 else friend
                label_friend_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
                label_friend_demand.place(relx=0.09, rely=0.14 + index * 0.05, anchor=NW)

                valid_friend_demand = Label(notifications_panel, image=self.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
                valid_friend_demand.place(relx=0.75, rely=0.15 + index * 0.05, anchor=CENTER)
                valid_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptFriendDemand(friend))

                delete_friend_demand = Label(notifications_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
                delete_friend_demand.place(relx=0.9, rely=0.15 + index * 0.05, anchor=CENTER)
                delete_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseFriendDemand(friend))


    def displayListFriends(self, friends_panel : Label) -> None:
        if len(self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)) != 0 or len(self.db.selectAllInvitingGames(self.get_username("serverPseudo.txt"))) != 0:
            image_notifications = self.notifications
        else:
            image_notifications = self.no_notification
        button_notifications = Label(friends_panel, image=image_notifications, bd=0, highlightthickness=0, cursor="hand2")
        button_notifications.place(relx=0.1, rely=0.045, anchor=CENTER)
        button_notifications.bind("<Button-1>", lambda event: self.display_notifications(friends_panel))

        button_leave_friends = Button(friends_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
        button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
        button_leave_friends.bind("<Button-1>", lambda event: self.quit_friends_list(friends_panel))


        ResultFriends = self.db.selectAllFriends(self.get_username("serverPseudo.txt"))  # liste des amis à récupérer depuis la bdd
        friends = ResultFriends[1]
        for index, friend in enumerate(friends):
            result_statut = self.db.selectStatusFriends(friend[0])
            if result_statut[0][0] == 1:
                friend_statut_image = self.statut_online 
            else:
                friend_statut_image = self.statut_offline
                
            friend = friend[:19] + ".." if len(friend) > 21 else friend
            friend_statut = Label(friends_panel, image=friend_statut_image, bd=0, highlightthickness=0)
            friend_statut.place(relx=0.08, rely=0.205 + index * 0.05, anchor=NW)
            
            label_friend = Label(friends_panel, text=friend, bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            label_friend.place(relx=0.13, rely=0.2 + index * 0.05, anchor=NW)

            invite_friend = Label(friends_panel, image=self.invite_friends, bd=0, highlightthickness=0, cursor="hand2")
            invite_friend.place(relx=0.75, rely=0.21 + index * 0.05, anchor=CENTER)
            invite_friend.bind("<Button-1>", lambda event, friend=friend: self.invitFriend(friend))

            delete_friend = Label(friends_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
            delete_friend.place(relx=0.9, rely=0.21 + index * 0.05, anchor=CENTER)
            delete_friend.bind("<Button-1>", lambda event, friend=friend: self.deleteFriends(friend))

        entry_friend = Entry(friends_panel, bd=3, width=25, font=("Arial", 13), background="#102A43", foreground="white", insertbackground="white", highlightbackground="#2BB0ED", highlightcolor="#2BB0ED", highlightthickness=1, relief=FLAT)
        entry_friend.place(relx=0.42, rely=0.13, anchor=CENTER)

        search_button = Button(friends_panel, image=self.search_friends, bd=0, highlightthickness=0, cursor="hand2", command=lambda: self.searchFriend(entry_friend.get()))
        search_button.place(relx=0.9, rely=0.13, anchor=CENTER)
        
        self.friends_panel = friends_panel
        
        
    def invitFriend(self, friend : tuple) -> None:
        self.db.sendInvitingGames(str(self.get_username("serverPseudo.txt")), friend[0], "127.0.0.1", 8000)

    
    def acceptFriendDemand(self, friend : tuple) -> None:
        self.db.acceptInviting(str(self.get_username("serverPseudo.txt")), friend[0])
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseFriendDemand(self, friend : tuple) -> None:
        self.db.deleteInviting(friend[0], str(self.get_username("serverPseudo.txt")))
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def acceptGameDemand(self, friend : tuple) -> None:
        resultGameInfo = self.db.acceptInvitingGames(str(self.get_username("serverPseudo.txt")), friend[0])
        (ip, port) = resultGameInfo[0][0].split(":")
        print(ip, port)
        # joinSession(ip, int(port), 1)
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseGameDemand(self, friend : tuple) -> None:
        self.db.deleteInvitingGames(friend[0], str(self.get_username("serverPseudo.txt")))
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def searchFriend(self, friend : str) -> None:
        friend = friend.replace(" ", "")
        invList = self.db.selectAllInviting(self.get_username("serverPseudo.txt"), False)
        ResultFriends = self.db.selectAllFriends(self.get_username("serverPseudo.txt"))
        friendsList = ResultFriends[1]
        
        if friend != "" and friend != self.get_username("serverPseudo.txt") and not any(friend in tupleInfos for tupleInfos in friendsList) and not any(friend in tupleInfosInv for tupleInfosInv in invList):
            self.db.sendInviting(self.get_username("serverPseudo.txt"), friend)
        
        
    def deleteFriends(self, friend):
        delete = Tk()
        delete.title("Confirmation de suppression")
        delete.geometry("500x200")
        delete.resizable(False, False)
        delete.config(bg="#0F2234")
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
                    highlightthickness=0, font=("Arial", 13), fg="white", bg="#0F2234")
        label.place(relx=0.5, rely=0.4, anchor=CENTER)

        button_frame = Frame(delete, bg="#0F2234")
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
        self.is_shop = True
        self.background(self.statut)
        self.createMenu(statut)
        self.createButtonShop()
        if not self.isConnected("serverPseudo.txt"):
            self.displayMoney()
            
            
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
            nbrIA = Label(self.window, text="Nombre d'IA", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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
            nbrIA = Label(self.window, text="Difficulté des bots", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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
            nbrPlayer = Label(self.window, text="Nombre de Joueur(s)", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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

        nbrIA = Label(self.window, text="Taille du plateau", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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
        nbrFence = Label(self.window, text="Nombre de barrières", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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
                
        
        if self.isConnected("serverPseudo.txt") == False:
            username = self.get_username("serverPseudo.txt")
            listMaps=self.db.getMapByUsername(username)
        else:
            listMaps=["Jungle", "Space", "Hell"]
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(0)
        X = 0.25
        Y = 0.73
        if self.statut == 1 or self.statut == 3:
            X = 0.45
        listMap.place(relx=X, rely=Y, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        if self.statut == 0 or self.statut == 2:
            nameMap = Label(self.window, text="Thème de la carte", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
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
                self.error_label = Label(self.window, text=f"Le nombre de joueurs ({nb_player}) est incorrect (2 ou 4).", font=("Arial", 13), bg="#0F2234", fg="red")
                self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            elif grid_size == 5 and nbr_fences > 20:
                    self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F2234", fg="red")
                    self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            else:
                map = self.selectMap
                self.window.destroy()
                restartGame(grid_size, nb_player, nb_ia, nbr_fences, map)

        start = Button(self.window, image=self.start_game, command=start_game, cursor="hand2", bd=0, highlightthickness=0, activebackground="#035388",  activeforeground="white")
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
    
    
    def menuCreateGameSolo(self, event):
        self.changeMode()
        self.is_shop = False
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
        
    """REJOINDRE UNE PARTIE EN RESEAU"""
    def menuJoinGameNetwork(self, event):
        self.changeMode()
        self.is_shop = False
        if self.statut != 3:
            self.statut = 1
        self.background(self.statut)
        self.createMenu(self.statut)
        self.create_entries()
        self.choiceMap()
        
    def create_entries(self) -> None:
        ip = Label(self.window, text="Adresse IP :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        ip.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.entryIp = Entry(self.window, width=20)
        self.entryIp.place(relx=0.25, rely=0.73, anchor=CENTER)

        self.entryPortGame()
        
        map = Label(self.window, text="Thème de la carte :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        map.place(relx=0.45, rely=0.7, anchor=CENTER)
        
        start = Button(self.window, image=self.join_game, cursor="hand2", activebackground="#035388", bd=0, highlightthickness=0, activeforeground="white", command=self.joinGameNetwork)
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
        
        reset_button = Button(self.window, image=self.search_game,  cursor="hand2", bd=0, highlightthickness=0, command=self.displayIp, activebackground="#486581",  activeforeground="white")
        reset_button.place(relx=0.4, rely=0.8, anchor=CENTER)
        
    def joinGameNetwork(self) -> None:
        ip = self.entryIp.get()
        if hasattr(self, 'error_label'):
            self.error_label.destroy()
        parts = ip.split('.')
        if len(parts) != 4:
            self.error_label = Label(self.window, text=f"IP: {ip} invalide", font=("Arial", 13), bg="#0F2234", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        for part in parts:
            if not part.isdigit() or int(part) > 255:
                self.error_label = Label(self.window, text=f"IP: {ip} invalide", font=("Arial", 13), bg="#0F2234", fg="red")
                self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
                return

        portstr = self.entry_port.get()
        if portstr == "":
            self.error_label = Label(self.window, text="Veuillez renseigner un port", font=("Arial", 13), bg="#0F2234", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        if not portstr.isdigit() or int(portstr) > 65535:
            self.error_label = Label(self.window, text=f"Port: {portstr} invalide", font=("Arial", 13), bg="#0F2234", fg="red")
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
        self.is_shop = False
        self.statut = 2
        self.background(self.statut)
        self.createMenu(self.statut)
        self.choiceMap()
        self.numberPlayer()
        self.sizeBoard()
        self.numberFence()
        self.entryPortGame()
        self.startButtonNetwork()
        
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
        port = Label(self.window, text="Port :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        port.place(relx=x, rely=y, anchor=CENTER)
        self.entry_port = Entry(self.window, width=20)
        self.entry_port.place(relx=x2, rely=y2, anchor=CENTER)
    
    def startButtonNetwork(self) -> None:
        start = Button(self.window, image=self.create_game, bd=0, highlightthickness=0, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.startGame)
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
    
    def startGame(self) -> None:
        portstr = self.entry_port.get()
        
        if hasattr(self, 'error_label'):
            self.error_label.destroy()

        if portstr == "":
            self.error_label = Label(self.window, text="Veuillez renseigner un port", font=("Arial", 13), bg="#0F2234", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return

        if not portstr.isdigit() or int(portstr) > 65535:
            self.error_label = Label(self.window, text=f"Port: {portstr} invalide", font=("Arial", 13), bg="#0F2234", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            return
        
        port = int(portstr)
        nbr_player = int(self.selectPlayer)
        grid_size = self.selectSize
        nbr_fences = self.selectFence
        map = self.selectMap

        if grid_size == 5 and nbr_fences > 20:
            self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F2234", fg="red")
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
        self.is_shop = False
        statut = self.getStatut()
        self.statut = 4
        self.background(self.statut)
        self.createMenu(statut)
        self.connexion()
        self.inscription()
    
    
    def connexion(self) -> None:
        self.login_button = Button(self.window, image=self.login_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addLogin)
        self.login_button.place(relx=0.35, rely=0.8, anchor=CENTER)
        
        
    def addLogin(self):
        self.login_button.configure(state=DISABLED)
        self.register_button.configure(state=NORMAL)
        if len(self.widget_register) > 0:
            for widget in self.widget_register:
                widget.destroy()
                
        username = Label(self.window, text="Pseudo :", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
        username.place(relx=0.54, rely=0.68, anchor=CENTER)
        self.loginUsername = Entry(self.login)
        self.loginUsername.place(relx=0.54, rely=0.71, anchor=CENTER)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
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
                    self.bg_not_connected.destroy()
                    self.menuCreateGameSolo(event=None)
                    return self.pseudo
                else:
                    self.infoLabel = Label(self.window, text="Vous êtes bien connecté.", fg="green", font=("Arial", 13), bg="#0F2234")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
                    self.pseudo = username
                    self.setUsername(username)
                    self.bg_not_connected.destroy()
                    self.menuCreateGameSolo(event=None)
                    return self.pseudo
            else:
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text="Mot de passe incorrect.")
                else:
                    self.infoLabel = Label(self.window, text="Mot de passe incorrect.", fg="red", font=("Arial", 13), bg="#0F2234")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        else:
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Cet utilisateur n'existe pas.")
            else:
                self.infoLabel = Label(self.window, text="Cet utilisateur n'existe pas.", fg="red", font=("Arial", 13), bg="#0F2234")
                self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        self.widget_label = [self.infoLabel]


    def inscription(self) -> None:
        self.register_button = Button(self.window, image=self.register_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addRegister)
        self.register_button.place(relx=0.73, rely=0.8, anchor=CENTER)
        
        
    def addRegister(self):
        self.register_button.configure(state=DISABLED)
        self.login_button.configure(state=NORMAL)
        if len(self.widget_login) > 0:
            for widget in self.widget_login:
                widget.destroy()
            
        username = Label(self.window, text="Pseudo :", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
        username.place(relx=0.54, rely=0.6, anchor=CENTER)
        self.registerUsername = Entry(self.register)
        self.registerUsername.place(relx=0.54, rely=0.63, anchor=CENTER)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
        password.place(relx=0.54, rely=0.68, anchor=CENTER)
        self.registerPassword = Entry(self.register, show="*")
        self.registerPassword.place(relx=0.54, rely=0.71, anchor=CENTER)

        passwordConfirm = Label(self.window, text="Confirmer le mot de passe :", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
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
                self.infoLabel = Label(self.window, text="Veuillez remplir tous les champs", fg="red", font=("Arial", 13), bg="#0F2234")
                self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
        elif password != confirm_password:
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Les mots de passe ne correspondent pas")
            else:
                self.infoLabel = Label(self.window, text="Les mots de passe ne correspondent pas", fg="red", font=("Arial", 13), bg="#0F2234")
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
                    self.infoLabel = Label(self.window, text=f"Ce pseudo '{username}' est déjà utilisé.", fg="red", font=("Arial", 13), bg="#0F2234")
                    self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
            else:
                try:
                    # Si le pseudo est unique on l'insère dans la base de données
                    insert_query = self.db.insert()
                    query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    params = (username, hashed_password)
                    insert_query.execute(query, params)
                    
                    # Fermeture de la requête d'insertion
                    insert_query.close()

                    # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                    if hasattr(self, "infoLabel"):
                        self.infoLabel.config(text=f"Bravo {username} ! Votre compte à bien été créé.")
                        self.pseudo = username
                        self.setUsername(username)
                        self.bg_not_connected.destroy()
                        self.menuCreateGameSolo(event=None)
                        return self.pseudo
                    else:
                        self.infoLabel = Label(self.window, text=f"Bravo {username} ! Vous êtes bien inscrit.", fg="green", font=("Arial", 13), bg="#0F2234")
                        self.infoLabel.place(relx=0.54, rely=0.9, anchor=CENTER)
                        self.pseudo = username
                        self.setUsername(username)
                        self.bg_not_connected.destroy()
                        self.menuCreateGameSolo(event=None)
                        return self.pseudo
                finally:
                    # Fermeture de la connexion à la base de données
                    self.db.close()

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

    def deconnexionUser(self, file_path):
        try:
            with open(file_path, 'w') as file:
                file.write("")
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False
        self.bg_connect.destroy()
        self.createMenu(self.getStatut())
        if self.is_shop == True:
            self.displayShop()