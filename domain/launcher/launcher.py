from tkinter import *
import tkinter as tk
from tkinter import ttk
from infrastructure.services.services import restartGame
from domain.network.network import joinSession, startSession
from domain.network.scanNetwork import ScanNetwork
import os


class QuoridorLauncher:
    def __init__(self, errorStyle : str) -> None:
        # Page de lancement.
        from domain.launcher.launchScreen import LaunchScreen
        launchScreen = LaunchScreen()
        
        # Lancement de la class d'initialisation des variables, images, sons...
        from infrastructure.services.initLauncher import InitLauncher
        from infrastructure.database.config import Database
        initGame = InitLauncher(self, launchScreen, Database())
        
        # Lancement de l'affichage du chargement.
        if os.name == "nt":
            launchScreen.start()
        
        initGame.startInit()
            
        # Lancement de l'affichage du launcher.
        self.menuCreateGameSolo(event=None)
        
        if os.name == "nt":
            launchScreen.status = False
            
            if launchScreen.is_alive():
                launchScreen.join()
        
        if errorStyle == "errorClientOfServer" or errorStyle == "errorServerOfClient" or errorStyle == "errorConnectClientOfServer" or errorStyle == "errorServerFull" or errorStyle == "errorLaunchServer":
            self.errorClientNetwork(errorStyle)
        else:
            from infrastructure.services.verifConnection import VerifConnection
            if VerifConnection("").isConnectDatabase() == False or VerifConnection("https://google.com").isConnectInternet() == False:
                self.errorClientNetwork("noNetwork")
                
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
        
    
    def leaveLauncher(self) -> None:
        def leaveAll(event=None) -> None:
            from infrastructure.services.deletePycache import deletePycache
            
            self.window.destroy()
            deletePycache()
            exit()
            
        self.leave_button = Label(self.window, image=self.leave_game_network, cursor="hand2", bd=0, highlightthickness=0)
        self.leave_button.place(relx=0.95, rely=0.92, anchor=CENTER)
        self.leave_button.bind("<Button-1>", lambda event: leaveAll())
        
        
    def createMenu(self, statut : None or int, btnCliked : str) -> None:
        self.statut = statut
        
        self.menu = getattr(self, f"menu{self.statut}")
        canvas = Canvas(self.window, width=self.menu.width(), height=self.menu.height(), bd=0, highlightthickness=0, cursor="hand2")
        canvas.place(relx=0.023, y=self.window.winfo_screenheight() / 2 - self.menu.height() / 2)
        
        canvas.create_image(0, 0, anchor=NW, image=self.menu)
        canvas.bind("<Button-1>", lambda event: self.clickMenu(event, self.menuCreateGameSolo, self.menuJoinGameNetwork, self.menuCreateGameNetwork))
        
        if btnCliked == "settings":
            settingsPicture = self.parametersOn
        else:
            settingsPicture = self.parameters
        settings = Canvas(self.window, width=settingsPicture.width(), height=settingsPicture.height(), bd=0, highlightthickness=0, cursor="hand2")
        settings.place(x=(int(self.window.winfo_screenwidth() * 0.023) + 20), rely=0.85)
        settings.create_image(0, 0, anchor=NW, image=settingsPicture)
        settings.bind("<Button-1>", self.displayParameters)

        if btnCliked == "shop":
            shopPicture = self.shopOn
        else:
            shopPicture = self.shop
        shops = Canvas(self.window, width=shopPicture.width(), height=shopPicture.height(), bd=0, highlightthickness=0, cursor="hand2")
        shops.place(x=(int(self.window.winfo_screenwidth() * 0.023) + 20), rely=0.72)
        shops.create_image(0, 0, anchor=NW, image=shopPicture)
        shops.bind("<Button-1>", lambda event: self.displayShop())
        
        self.createAccountMenu()
    
    
    
    
    ''' Zone de création des menus de settings et gestion des changement en temps réel '''
    def displayParameters(self, event):
        from infrastructure.services.settings import Settings
        
        __settingsClass = Settings(self)
        
        self.changeMode()
        self.statut = 6
        self.background(self.statut)
        self.createMenu(None, "settings")
        self.settingsActiveNotificationsSond()
        self.settingsSoundMap(__settingsClass)
        self.settingsSoundVictory(__settingsClass)
        self.settingsPionVolume(__settingsClass)
        self.settingsFenceVolume(__settingsClass)
        self.settingsNoFenceVolume(__settingsClass)
        self.choiceFavoriteMap()
        self.displayButtonChangeBind()
        self.settingsNotificationVolume(__settingsClass)
        self.leaveLauncher()
        

    def setBind(self, event=None):
        if self.changeButton:
            touche = event.keysym
            if touche == "space":
                touche_affichee = "space"
            else:
                touche_affichee = touche[0]

            self.addBindToFile(touche_affichee)
            self.changeButton = False
            self.wait_bind.destroy()  # Détruire le label wait_bind


    def modifyBind(self):
        self.wait_bind = Label(image=self.bind_changing, bd=0, highlightthickness=0)
        self.wait_bind.place(relx=0.6, rely=0.8, anchor=CENTER)
        self.wait_bind.bind("<Button-1>", lambda event: self.setBind(event))
        self.changeButton = True
        self.window.unbind("<Key>")
        self.window.bind("<Key>", self.setBind)
        self.bindActual()
        self.label_touche.destroy()


    def displayButtonChangeBind(self):
        bind_actual = Label(self.window, image=self.bind, cursor="hand2", bd=0, highlightthickness=0)
        bind_actual.place(relx=0.6, rely=0.8, anchor=CENTER)
        bind_actual.bind("<Button-1>", lambda event: self.modifyBind())

        self.bindActual()
    
    
    def addBindToFile(self, touche):
        with open("settings.txt", "r") as file:
            lignes = file.readlines()

        if len(lignes) >= 8:
            lignes[7] = f"<{touche}>\n" 
            with open("settings.txt", "w") as file:
                file.writelines(lignes)
            
            self.bindActual()  
        else:
            print("Le fichier settings.txt ne contient pas suffisamment de lignes.")
    
    
    def bindActual(self):
        with open("settings.txt", "r") as file:
            lignes = file.readlines()

        if len(lignes) >= 8:
            touche = lignes[7].strip()
            texte = f"{touche.upper().replace('<', '').replace('>', '')}"
            if texte == "SPACE":
                texte = "ESPACE"
                size_font = 9
            else:
                size_font = 15

            if hasattr(self, "label_touche"): 
                self.label_touche.destroy()  

            text_bind_actual = Label(self.window, text="Direction des barrières :", background="#0F2234", bd=0, highlightthickness=0, fg="white", font=("Arial", 13))
            text_bind_actual.place(relx=0.6, rely=0.75, anchor=CENTER)
            self.label_touche = Label(self.window, text=texte, background="#102C42", bd=0, highlightthickness=0, fg="white", font=("Arial", size_font), cursor="hand2")
            self.label_touche.place(relx=0.6, rely=0.8, anchor=CENTER)
            self.label_touche.bind("<Button-1>", lambda event: self.modifyBind())
        else:
            print("Le fichier settings.txt ne contient pas suffisamment de lignes.")
            
            
    def choiceFavoriteMap(self) -> None:
        def action(event) -> None:
            selected_value = listMap.get()
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
        
                with open("settings.txt", "r") as file:
                    lines = file.readlines()
                if len(lines) >= 7:
                    lines[6] = str(self.selectFavoriteMap) + "\n"
                with open("settings.txt", "w") as file:
                    file.writelines(lines)
                    
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")

        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        if __getSetInformation.isConnected("serverPseudo.txt") == False:
            username = __getSetInformation.get_username("serverPseudo.txt")
            listMaps = self.db.getMapByUsername(username)
        else:
            listMaps = ["Jungle", "Space", "Hell"]
        
        self.selectFavoriteMap = min(self.selectFavoriteMap, len(listMaps))  
        
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(self.selectFavoriteMap - 1)
            
        listMap.place(relx=0.6, rely=0.68, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        
        nameMap = Label(self.window, text="Votre carte favorite:", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
        nameMap.place(relx=0.6, rely=0.65, anchor=CENTER)

    
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
            lines[0] = str(self.active_sound_notification) + "\n"  

            with open("settings.txt", "w") as file:
                file.writelines(lines)  

        def update_statut():
            if self.active_sound_notification:
                self.image_statut_notification = self.yes_sound_notifications_image
            else:
                self.image_statut_notification = self.no_sound_notifications_image
            statut_sound_notification.config(image=self.image_statut_notification)

        sound_notification = Label(self.window, text="Notifications", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_notification.place(relx=0.6, rely=0.5, anchor=CENTER)

        statut_sound_notification = Label(self.window, image=self.yes_sound_notifications_image, bd=0, highlightthickness=0, cursor="hand2")
        statut_sound_notification.place(relx=0.6, rely=0.54, anchor=CENTER)
        update_statut()
        statut_sound_notification.bind("<Button-1>", changeStatutSoundNotification)
    
    
    # Modifier le son de la map
    def settingsSoundMap(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                self.sound_map = float(lines[1].strip())
                
        sound_map_texte = Label(self.window, text="Volume du son d'ambiance", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_map_texte.place(relx=0.25, rely=0.5, anchor=CENTER)
        self.slider = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider.set(self.sound_map)  
        self.slider.place(relx=0.25, rely=0.54, anchor=CENTER)
        self.slider.config(command=settingClass.saveValueToFile)
        
        
    # Modifier le son de la victoire 
    def settingsSoundVictory(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                self.sound_victory = float(lines[2].strip())
                
        sound_victory_texte = Label(self.window, text="Son de la victoire", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_victory_texte.place(relx=0.43, rely=0.5, anchor=CENTER)
        self.slider_victory = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_victory.set(self.sound_victory) 
        self.slider_victory.place(relx=0.43, rely=0.54, anchor=CENTER)
        self.slider_victory.config(command=settingClass.saveVictoryValueToFile)
        
        
    # Modifier le volume du pion
    def settingsPionVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 4:
                self.pion_volume = float(lines[3].strip())
                
        pion_volume_texte = Label(self.window, text="Volume de la pose du pion", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        pion_volume_texte.place(relx=0.25, rely=0.65, anchor=CENTER)
        self.slider_pion_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_pion_volume.set(self.pion_volume)  
        self.slider_pion_volume.place(relx=0.25, rely=0.68, anchor=CENTER)
        self.slider_pion_volume.config(command=settingClass.savePionVolumeToFile)
        
        
    # Modifier le volume des clôtures
    def settingsFenceVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 5:
                self.fence_volume = float(lines[4].strip())
                
        fence_volume_texte = Label(self.window, text="Volume des barrières", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        fence_volume_texte.place(relx=0.25, rely=0.78, anchor=CENTER)
        self.slider_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_fence_volume.set(self.fence_volume)  
        self.slider_fence_volume.place(relx=0.25, rely=0.82, anchor=CENTER)
        self.slider_fence_volume.config(command=settingClass.saveFenceVolumeToFile)
        
        
    # Modifier le volume du son "no fence"
    def settingsNoFenceVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 6:
                self.no_fence_volume = float(lines[5].strip())
                
        no_fence_volume_texte = Label(self.window, text="Volume du son barrière incorrecte", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        no_fence_volume_texte.place(relx=0.43, rely=0.65, anchor=CENTER)
        self.slider_no_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_no_fence_volume.set(self.no_fence_volume) 
        self.slider_no_fence_volume.place(relx=0.43, rely=0.68, anchor=CENTER)
        self.slider_no_fence_volume.config(command=settingClass.saveNoFenceVolumeToFile)
        
        
    def settingsNotificationVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 9:
                self.notification_volume = float(lines[8].strip())

        notification_volume_texte = Label(self.window, text="Volume des notifications", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        notification_volume_texte.place(relx=0.43, rely=0.78, anchor=CENTER)
        self.slider_notification_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_notification_volume.set(self.notification_volume)
        self.slider_notification_volume.place(relx=0.43, rely=0.82, anchor=CENTER)
        self.slider_notification_volume.config(command=settingClass.saveNotificationVolumeToFile)
    
        
    ''' Zone de création des menu pour compte, deconnexion, amis '''
    def createAccountMenu(self) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        from infrastructure.services.configPictures import ConfigPictures
        
        __configPictures = ConfigPictures()
        
        if GetSetInformation().isConnected("serverPseudo.txt") == False:
            self.addLogoFriends(self.window, 80, 20, __configPictures)
            self.addLogoDeconnexion(self.window, 15, 20, __configPictures)
            self.addSectionPseudo(self.window, 0, 80, GetSetInformation().get_username("serverPseudo.txt"), __configPictures)
        else:
            self.addLogoAccount(self.window, 20, 20, __configPictures)
    
    
    def addSectionPseudo(self, label : Label, decalageX : int, decalageY : int, username : str, __configPictures : object) -> None:
        self.profile_account_label = Label(label, image=self.profile_account, bd=0, highlightthickness=0)
        
        __configPictures.labelPlaceXandYTopRight(self.profile_account_label, decalageX, decalageY, self)
        
        username = username[:10] + ".." if len(username) > 10 else username
        pseudo = Label(self.profile_account_label, text=f"{username}", font=("Arial", 13), bg="#062037", fg="white")
        pseudo.place(relx=0.2, rely=0.15, anchor=NW)
        
        statut = Label(self.profile_account_label, text=f"En ligne", font=("Arial", 9), bg="#062037", fg="#00FF38")
        statut.place(relx=0.2, rely=0.5, anchor=NW)
        
        money = self.db.getMoney(username)
        money_label = Label(self.profile_account_label, text=f"{money} Crédit(s)", font=("Arial", 13), bg="#062037", fg="#EAB308")
        money_label.place(relx=0.78, rely=0.5, anchor=CENTER)
        
        letter = username[0].upper()
        letter_logo = Label(self.profile_account_label, text=letter, bd=0, highlightthickness=0, font=("Arial", 20, "bold"), bg="#2DA6FF", fg="white")
        letter_logo.place(relx=0.09, rely=0.5, anchor=CENTER)

    
    def addLogoDeconnexion(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        def deconnexionAccount(event=None) -> None:
            from infrastructure.services.getSetInformation import GetSetInformation
            GetSetInformation().deleteFile("serverPseudo.txt")
            
            self.profile_account_label.destroy()
            self.deconnexion_user.destroy()
            self.friends_canvas.destroy()
            
            self.createAccountMenu()

        self.deconnexion_user = Label(label, image=self.deconnexion, bd=0, highlightthickness=0, cursor="hand2")
        self.deconnexion_user.bind("<Button-1>", lambda event: deconnexionAccount())
        
        __configPictures.labelConfigWidthHeight(self.deconnexion_user, 45, 43)
        __configPictures.labelPlaceXandYTopRight(self.deconnexion_user, decalageX, decalageY, self)
        
        
    def addLogoFriends(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        self.friends_canvas = Label(label, image=self.friends, bd=0, highlightthickness=0, cursor="hand2")
        self.friends_canvas.bind("<Button-1>", lambda event: self.displayFriends())
        
        __configPictures.labelConfigWidthHeight(self.friends_canvas, 51, 43)
        __configPictures.labelPlaceXandYTopRight(self.friends_canvas, decalageX, decalageY, self)
        
        
    def addLogoAccount(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        self.account_button = Label(label, image=self.account_image, bd=0, highlightthickness=0, cursor="hand2")
        self.account_button.bind("<Button-1>", lambda event: self.displayAccount())
        
        __configPictures.labelConfigWidthHeight(self.account_button, 39, 43)
        __configPictures.labelPlaceXandYTopRight(self.account_button, decalageX, decalageY, self)


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
        from infrastructure.services.getSetInformation import GetSetInformation
        
        username = GetSetInformation().get_username("serverPseudo.txt")
        listMap = self.db.getMapByUsername(username)
        money = self.db.getMoney(username)

        map_info = [
            ("Ice", 1000, 0.29),
            ("Electricity", 2500, 0.55),
            ("Sugar", 5000, 0.81)]

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
        from infrastructure.services.getSetInformation import GetSetInformation
        
        if GetSetInformation().isConnected("serverPseudo.txt"):
            self.displayAccount()
        else:
            if map == "Ice":
                x = 0.29
            elif map == "Electricity":
                x = 0.55
            elif map == "Sugar":
                x = 0.81
            pseudo = GetSetInformation().get_username("serverPseudo.txt")
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
            
            
    def displayFriends(self) -> None:
        friends_panel = Label(self.window, image=self.list_friends, bd=0, highlightthickness=0)
        friends_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayListFriends(friends_panel)
        
        
    def quit_friends_list(self, panel) -> None:
        panel.destroy()
        self.createAccountMenu()
        if self.delete_friend_popup_label is not None:
            self.delete_friend_popup_label.destroy()
            
        
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
        if self.delete_friend_popup_label is not None:
            self.delete_friend_popup_label.destroy()


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
        friend_game_demands = self.db.selectAllInvitingGames(self.getInformation.get_username("serverPseudo.txt")) # demande de partie via la bdd
        if len(friend_game_demands) == 0:
            no_friend_demand = Label(notifications_panel, image=self.no_notification_text, bd=0, highlightthickness=0)
            no_friend_demand.place(relx=0.09, rely=0.55, anchor=NW)
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
        
        friend_demands = self.db.selectAllInviting(self.getInformation.get_username("serverPseudo.txt"), False)  # demande d'amis à récupérer depuis la bdd
        if len(friend_demands) == 0:
            no_friend_demand = Label(notifications_panel, image=self.no_notification_text, bd=0, highlightthickness=0)
            no_friend_demand.place(relx=0.09, rely=0.145, anchor=NW)
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
        if len(self.db.selectAllInviting(self.getInformation.get_username("serverPseudo.txt"), False)) != 0 or len(self.db.selectAllInvitingGames(self.getInformation.get_username("serverPseudo.txt"))) != 0:
            image_notifications = self.notifications
        else:
            image_notifications = self.no_notification
        button_notifications = Label(friends_panel, image=image_notifications, bd=0, highlightthickness=0, cursor="hand2")
        button_notifications.place(relx=0.1, rely=0.045, anchor=CENTER)
        button_notifications.bind("<Button-1>", lambda event: self.display_notifications(friends_panel))

        button_leave_friends = Button(friends_panel, image=self.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
        button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
        button_leave_friends.bind("<Button-1>", lambda event: self.quit_friends_list(friends_panel))

        ResultFriends = self.db.selectAllFriends(self.getInformation.get_username("serverPseudo.txt"))  # liste des amis à récupérer depuis la bdd
        friends = ResultFriends[1]
        for index, friend in enumerate(friends):
            
            label_friend = Label(friends_panel, text=friend, bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            label_friend.place(relx=0.09, rely=0.2 + index * 0.05, anchor=NW)

            invite_friend = Label(friends_panel, image=self.invite_friends, bd=0, highlightthickness=0, cursor="hand2")
            invite_friend.place(relx=0.75, rely=0.21 + index * 0.05, anchor=CENTER)
            invite_friend.bind("<Button-1>", lambda event, friend=friend: self.invitFriend(friend))

            delete_friend = Label(friends_panel, image=self.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
            delete_friend.place(relx=0.9, rely=0.21 + index * 0.05, anchor=CENTER)
            delete_friend.bind("<Button-1>", lambda event, friend=friend: self.deleteFriends(friend))

        self.entry_friend = Entry(friends_panel, bd=3, width=25, font=("Arial", 13), background="#102A43", foreground="white", insertbackground="white", highlightbackground="#2BB0ED", highlightcolor="#2BB0ED", highlightthickness=1, relief=FLAT)
        self.entry_friend.place(relx=0.42, rely=0.13, anchor=CENTER)

        search_button = Button(friends_panel, image=self.search_friends, bd=0, highlightthickness=0, cursor="hand2", command=lambda: self.searchFriend(self.entry_friend.get()))
        search_button.place(relx=0.9, rely=0.13, anchor=CENTER)
        
        self.friends_panel = friends_panel
        
        
    def invitFriend(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.sendInvitingGames(str(GetSetInformation().get_username("serverPseudo.txt")), friend[0], "127.0.0.1", 8000)
        
        
    def acceptFriendDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.acceptInviting(str(GetSetInformation().get_username("serverPseudo.txt")), friend[0])
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseFriendDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.deleteInviting(friend[0], str(GetSetInformation().get_username("serverPseudo.txt")))
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def acceptGameDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        resultGameInfo = self.db.acceptInvitingGames(str(GetSetInformation().get_username("serverPseudo.txt")), friend[0])
        (ip, port) = resultGameInfo[0][0].split(":")
        print(ip, port)
        # joinSession(ip, int(port), 1)
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseGameDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.deleteInvitingGames(friend[0], str(GetSetInformation().get_username("serverPseudo.txt")))
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def searchFriend(self, friend : str) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        friend = friend.replace(" ", "")
        invList = self.db.selectAllInviting(__getSetInformation.get_username("serverPseudo.txt"), False)
        ResultFriends = self.db.selectAllFriends(__getSetInformation.get_username("serverPseudo.txt"))
        friendsList = ResultFriends[1]
        
        if friend != "" and friend != __getSetInformation.get_username("serverPseudo.txt") and not any(friend in tupleInfos for tupleInfos in friendsList) and not any(friend in tupleInfosInv for tupleInfosInv in invList):
            self.db.sendInviting(__getSetInformation.get_username("serverPseudo.txt"), friend)
        
        
    def deleteFriends(self, friend):
        self.delete_friend_popup_label = Label(self.window, image=self.delete_friend_popup, bd=0, highlightthickness=0, cursor="hand2")
        self.delete_friend_popup_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        

        def on_yes_click():
            from infrastructure.services.getSetInformation import GetSetInformation
            __getSetInformation = GetSetInformation()
        
            self.delete_friend_popup_label.destroy()
            self.db.deleteFriends(__getSetInformation.get_username("serverPseudo.txt"), friend[0])
            self.db.deleteFriends(friend[0], __getSetInformation.get_username("serverPseudo.txt"))
            self.displayListFriends(self.friends_panel)

        def on_no_click():
            self.delete_friend_popup_label.destroy()


        if len(friend) > 15:
                friend = friend[:15] + ".."
        label = Label(self.delete_friend_popup_label, text=f"Souhaitez-vous vraiment supprimer \n{friend[0]} de vos amis ?", bd=0,
                    highlightthickness=0, font=("Inter", 22), fg="#E3F8FF", bg="#102A43")
        label.place(relx=0.05, rely=0.35, anchor=NW)
        label.config(justify="left")


        yes_button = Label(self.delete_friend_popup_label, image=self.delete_friend_button,bd=0, highlightthickness=0, cursor="hand2")
        yes_button.place(relx=0.05, rely=0.78, anchor=NW)
        yes_button.bind("<Button-1>", lambda event: on_yes_click())

        no_button = Button(self.delete_friend_popup_label, image=self.no_delete_friend_button,bd=0, highlightthickness=0, cursor="hand2")
        no_button.place(relx=0.38, rely=0.78, anchor=NW)
        no_button.bind("<Button-1>", lambda event: on_no_click())


    def displayShop(self) -> None:
        from infrastructure.services.verifConnection import VerifConnection
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            self.changeMode()
            self.statut = 5
            self.is_shop = True
            self.background(self.statut)
            self.createMenu(None, "shop")
            self.createButtonShop()
            self.leaveLauncher()
        else:
            self.errorClientNetwork("noNetwork")
            
            
    def numberIA(self) -> None:
        def action(event) -> None:
            self.selectIA = int(listIA.get())
            
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
        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        def action(event) -> None:
            selected_value = listMap.get()
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
                
        
        if __getSetInformation.isConnected("serverPseudo.txt") == False:
            username = __getSetInformation.get_username("serverPseudo.txt")
            listMaps=self.db.getMapByUsername(username)
        else:
            listMaps=["Jungle", "Space", "Hell"]
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TCombobox",
                        fieldbackground="#10273C",
                        background="#10273C",
                        foreground="white",
                        arrowcolor="white",
                        bordercolor="#5ED0FA",
                        lightcolor="#5ED0FA",
                        darkcolor="#5ED0FA",
                        activebackground="#10273C")
        style.map("TCombobox", fieldbackground=[("readonly", "#10273C")])

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
                restartGame(grid_size, nb_player, nb_ia, nbr_fences, map, self.selectIaDifficulty)

        start = Button(self.window, image=self.start_game, command=start_game, cursor="hand2", bd=0, highlightthickness=0, activebackground="#035388",  activeforeground="white")
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
    
    
    def menuCreateGameSolo(self, event):
        self.changeMode()
        self.is_shop = False
        self.statut = 0
        self.background(self.statut)
        self.createMenu(self.statut, "")
        self.numberIA()
        self.getIaDifficulty()
        self.numberPlayer()
        self.sizeBoard()
        self.numberFence()
        self.choiceMap()
        self.buttonStart()
        self.leaveLauncher()
        
        
    """REJOINDRE UNE PARTIE EN RESEAU"""
    def menuJoinGameNetwork(self, event):
        self.changeMode()
        self.is_shop = False
        if self.statut != 3:
            self.statut = 1
        self.background(self.statut)
        self.createMenu(self.statut, "")
        self.create_entries()
        self.choiceMap()
        self.leaveLauncher()
        
        
    def create_entries(self) -> None:
        ip = Label(self.window, text="Adresse IP :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        ip.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.entryIp = Entry(self.window, bd=3, width=15, font=("Arial", 13), background="#102A43", foreground="white", insertbackground="white", highlightbackground="#2BB0ED", highlightcolor="#2BB0ED", highlightthickness=1, relief=FLAT)
        self.entryIp.place(relx=0.25, rely=0.73, anchor=CENTER)

        self.entryPortGame()
        
        map = Label(self.window, text="Thème de la carte :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        map.place(relx=0.45, rely=0.7, anchor=CENTER)
        
        from infrastructure.services.verifConnection import VerifConnection
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            start = Button(self.window, image=self.join_game, cursor="hand2", activebackground="#035388", bd=0, highlightthickness=0, activeforeground="white", command=self.joinGameNetwork)
            search_game_button = Button(self.window, image=self.search_game,  cursor="hand2", bd=0, highlightthickness=0, command=self.displayIp, activebackground="#486581",  activeforeground="white")
        else:
            start = Button(self.window, image=self.join_game, cursor="hand2", activebackground="#035388", bd=0, highlightthickness=0, activeforeground="white", command=lambda: self.errorClientNetwork("noNetwork"))
            search_game_button = Button(self.window, image=self.search_game,  cursor="hand2", bd=0, highlightthickness=0, command=lambda: self.errorClientNetwork("noNetwork"), activebackground="#486581",  activeforeground="white")
        
        start.place(relx=0.25, rely=0.8, anchor=CENTER)
        search_game_button.place(relx=0.4, rely=0.8, anchor=CENTER)
        
        
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

        from infrastructure.services.getSetInformation import GetSetInformation
        port = int(portstr)
        self.window.destroy()
        GetSetInformation().setUsername(self.pseudo)
        joinSession(ip, port, self.selectMap)
        
    
    def displayIp(self) -> None:
        scanNetwork = ScanNetwork(8000, 8003)
        scanNetwork.scan()
        listip = scanNetwork.getIp()
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
        from infrastructure.services.getSetInformation import GetSetInformation
        
        ip = event.widget['text']
        port = int(port)
        self.window.destroy()
        GetSetInformation().setUsername(self.pseudo)
        joinSession(ip, port, self.selectMap)
        
        
    """CREER UNE GAME EN LOCAL"""
        
    def menuCreateGameNetwork(self, event):
        self.changeMode()
        self.is_shop = False
        self.statut = 2
        self.background(self.statut)
        self.createMenu(self.statut, "")
        self.choiceMap()
        self.numberPlayer()
        self.sizeBoard()
        self.numberFence()
        self.entryPortGame()
        self.startButtonNetwork()
        self.leaveLauncher()
        
        
    def entryPortGame(self) -> None:
        if self.statut == 2:
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

        port_values = [8000, 8001, 8002, 8003]
        self.entry_port = ttk.Combobox(self.window, values=port_values, state="readonly")
        self.entry_port.current(0)
        self.entry_port.place(relx=x2, rely=y2, anchor=CENTER)
    
    
    def startButtonNetwork(self) -> None:
        from infrastructure.services.verifConnection import VerifConnection
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            start = Button(self.window, image=self.create_game, bd=0, highlightthickness=0, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.startGame)
        else:
            start = Button(self.window, image=self.create_game, bd=0, highlightthickness=0, cursor="hand2", activebackground="#035388",  activeforeground="white", command=lambda: self.errorClientNetwork("noNetwork"))
            
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
            from infrastructure.services.getSetInformation import GetSetInformation
            
            self.window.destroy()
            GetSetInformation().setUsername(self.pseudo)
            startSession(port, nbr_player, grid_size, nbr_player, 0, nbr_fences, map)
    
    
    def getStatut(self) -> int:
        return self.statut
    
    
    def displayAccount(self) -> None:
        from infrastructure.services.verifConnection import VerifConnection
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            self.changeMode()
            self.is_shop = False
            statut = self.getStatut()
            self.statut = 4
            self.background(self.statut)
            self.createMenu(statut, "")
            self.connexion()
            self.inscription()
            self.leaveLauncher()
        else:
            self.errorClientNetwork("noNetwork")
    
    
    def connexion(self) -> None:
        self.login_button = Button(self.window, image=self.login_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addLogin)
        self.login_button.place(relx=0.35, rely=0.8, anchor=CENTER)
        
        
    def addLogin(self):
        def addLoginUserFunc() -> None:
            from infrastructure.database.userDb import UserDb
            UserDb().loginUser(self)
            
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

        self.loginButton =  Button(self.login, text="Se connecter", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2, cursor="hand2", activebackground="#035388", activeforeground="white", command=addLoginUserFunc)
        self.loginButton.place(relx=0.54, rely=0.85, anchor=CENTER)
        
        self.widget_login = [username, self.loginUsername, password, self.loginPassword, self.loginButton]


    def inscription(self) -> None:
        self.register_button = Button(self.window, image=self.register_image, bd=0, highlightthickness=0, cursor="hand2", command=self.addRegister)
        self.register_button.place(relx=0.73, rely=0.8, anchor=CENTER)
        
        
    def addRegister(self):
        def addAccountFunc() -> None:
            from infrastructure.database.userDb import UserDb
            UserDb().createAccount(self)
            
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
        
        self.registerButton = Button(self.register, text="S'inscrire", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2, cursor="hand2", activebackground="#035388", activeforeground="white", command=addAccountFunc)
        self.registerButton.place(relx=0.54, rely=0.85, anchor=CENTER)
        self.widget_register = [username, self.registerUsername, password, self.registerPassword, passwordConfirm, self.registerPasswordConfirm, self.registerButton]
        
    
    def errorClientNetwork(self, errorStyle : str) -> None: 
        def destroyErrorClientNetwork(event=None) -> None:
            self.errorClientNetworkPopup.destroy()

        def contactSupport(event=None) -> None:
            import webbrowser
            webbrowser.open("https://quoridor.maxencebombeeck.fr/contact")

        if errorStyle == "errorClientOfServer":
            pictureError = self.error_client_network
        elif errorStyle == "errorServerOfClient":
            pictureError = self.error_server_network
        elif errorStyle == "errorConnectClientOfServer":
            pictureError = self.error_connect_server_network
        elif errorStyle == "errorServerFull":
            pictureError = self.errorServerFull
        elif errorStyle == "errorLaunchServer":
            pictureError = self.errorLaunchServer
        elif errorStyle == "noNetwork":
            pictureError = self.no_network
            
        self.errorClientNetworkPopup = Label(self.window, image=pictureError, bd=0, highlightthickness=0)
        self.errorClientNetworkPopup.place(relx=0.5, rely=0.5, anchor=CENTER)

        self.errorClientNetworkButton = Label(self.errorClientNetworkPopup, image=self.error_client_network_btn, bd=0, highlightthickness=0, cursor="hand2")
        self.errorClientNetworkButton.place(relx=0.3, rely=0.81, anchor=CENTER)
        self.errorClientNetworkButton.bind("<Button-1>", destroyErrorClientNetwork)
        
        self.errorClientNetworkButtonLink = Label(self.errorClientNetworkPopup, image=self.error_client_network_btn_link, bd=0, highlightthickness=0, cursor="hand2")
        self.errorClientNetworkButtonLink.place(relx=0.7, rely=0.81, anchor=CENTER)
        self.errorClientNetworkButtonLink.bind("<Button-1>", contactSupport)