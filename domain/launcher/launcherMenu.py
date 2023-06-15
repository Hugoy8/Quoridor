from tkinter import Label, CENTER, Canvas, NW
import os

class LauncherMenu:
    def __init__(self, launcher, window, db):
        self.launcher = launcher
        self.window = window
        self.db = db
    
    
    def leaveLauncher(self) -> None:
        def leaveAll(event=None) -> None:
            from infrastructure.services.deletePycache import deletePycache
            
            self.launcher.notifs.status = False
            self.window.destroy()
            deletePycache()
            os._exit(0)
            
        self.launcher.leave_button = Label(self.window, image=self.launcher.leave_game_network, cursor="hand2", bd=0, highlightthickness=0)
        self.launcher.leave_button.place(relx=0.95, rely=0.92, anchor=CENTER)
        self.launcher.leave_button.bind("<Button-1>", lambda event: leaveAll())
        
        
    def createMenu(self, statut : None or int, btnCliked : str) -> None:
        self.statut = statut
        
        if self.statut == 4 or self.statut == 5 or  self.statut == 6:
            self.statut = None
            
        self.launcher.menu = getattr(self.launcher, f"menu{self.statut}")
        canvas = Canvas(self.window, width=self.launcher.menu.width(), height=self.launcher.menu.height(), bd=0, highlightthickness=0, cursor="hand2")
        canvas.place(relx=0.023, y=self.window.winfo_screenheight() / 2 - self.launcher.menu.height() / 2)
        
        canvas.create_image(0, 0, anchor=NW, image=self.launcher.menu)
        canvas.bind("<Button-1>", lambda event: self.clickMenu(event, self.launcher.menuCreateGameSolo, self.launcher.menuJoinGameNetwork, self.launcher.menuCreateGameNetwork))
        
        if btnCliked == "settings":
            settingsPicture = self.launcher.parametersOn
        else:
            settingsPicture = self.launcher.parameters
        settings = Canvas(self.window, width=settingsPicture.width(), height=settingsPicture.height(), bd=0, highlightthickness=0, cursor="hand2")
        settings.place(x=(int(self.window.winfo_screenwidth() * 0.023) + 20), rely=0.85)
        settings.create_image(0, 0, anchor=NW, image=settingsPicture)
        settings.bind("<Button-1>", self.launcher.displayParameters)

        if btnCliked == "shop":
            shopPicture = self.launcher.shopOn
        else:
            shopPicture = self.launcher.shop
        shops = Canvas(self.window, width=shopPicture.width(), height=shopPicture.height(), bd=0, highlightthickness=0, cursor="hand2")
        shops.place(x=(int(self.window.winfo_screenwidth() * 0.023) + 20), rely=0.72)
        shops.create_image(0, 0, anchor=NW, image=shopPicture)
        shops.bind("<Button-1>", lambda event: self.launcher.displayShop())
        
        self.createAccountMenu()

        
        ''' Zone de création des menu pour compte, deconnexion, amis '''
    def createAccountMenu(self) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        from infrastructure.services.configPictures import ConfigPictures
        
        __configPictures = ConfigPictures(self.launcher)
        
        if GetSetInformation().isConnected("serverPseudo.txt") == False:
            self.addLogoFriends(self.window, 80, 20, __configPictures)
            self.addLogoDeconnexion(self.window, 15, 20, __configPictures)
            self.addSectionPseudo(self.window, 0, 80, GetSetInformation().get_username("serverPseudo.txt"), __configPictures)
        else:
            self.addLogoAccount(self.window, 20, 20, __configPictures)
    
    
    def addSectionPseudo(self, label : Label, decalageX : int, decalageY : int, username : str, __configPictures : object) -> None:
        self.launcher.profile_account_label = Label(label, image=self.launcher.profile_account, bd=0, highlightthickness=0)
        
        __configPictures.labelPlaceXandYTopRight(self.launcher.profile_account_label, decalageX, decalageY, self)
        
        username = username[:10] + ".." if len(username) > 10 else username
        pseudo = Label(self.launcher.profile_account_label, text=f"{username}", font=("Arial", 13), bg="#062037", fg="white")
        pseudo.place(relx=0.2, rely=0.15, anchor=NW)
        
        statut = Label(self.launcher.profile_account_label, text=f"En ligne", font=("Arial", 9), bg="#062037", fg="#00FF38")
        statut.place(relx=0.2, rely=0.5, anchor=NW)
        
        money = self.db.getMoney(username)
        money_label = Label(self.launcher.profile_account_label, text=f"{money} Crédit(s)", font=("Arial", 13), bg="#062037", fg="#EAB308")
        money_label.place(relx=0.78, rely=0.5, anchor=CENTER)
        
        letter = username[0].upper()
        letter_logo = Label(self.launcher.profile_account_label, text=letter, bd=0, highlightthickness=0, font=("Arial", 20, "bold"), bg="#2DA6FF", fg="white")
        letter_logo.place(relx=0.09, rely=0.5, anchor=CENTER)

    
    def addLogoDeconnexion(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        def deconnexionAccount(event=None) -> None:
            from infrastructure.services.getSetInformation import GetSetInformation
            GetSetInformation().deleteFile("serverPseudo.txt")
            
            self.launcher.profile_account_label.destroy()
            self.launcher.deconnexion_user.destroy()
            self.launcher.friends_canvas.destroy()
            
            self.createAccountMenu()

        self.launcher.deconnexion_user = Label(label, image=self.launcher.deconnexion, bd=0, highlightthickness=0, cursor="hand2")
        self.launcher.deconnexion_user.bind("<Button-1>", lambda event: deconnexionAccount())
        
        __configPictures.labelConfigWidthHeight(self.launcher.deconnexion_user, 45, 43)
        __configPictures.labelPlaceXandYTopRight(self.launcher.deconnexion_user, decalageX, decalageY, self)
        
        
    def addLogoFriends(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        self.launcher.friends_canvas = Label(label, image=self.launcher.friends, bd=0, highlightthickness=0, cursor="hand2")
        self.launcher.friends_canvas.bind("<Button-1>", lambda event: self.launcher.launcherFriends.displayFriends())
        
        __configPictures.labelConfigWidthHeight(self.launcher.friends_canvas, 51, 43)
        __configPictures.labelPlaceXandYTopRight(self.launcher.friends_canvas, decalageX, decalageY, self)
        
        
    def addLogoAccount(self, label : Label, decalageX : int, decalageY : int, __configPictures : object) -> None:
        self.launcher.account_button = Label(label, image=self.launcher.account_image, bd=0, highlightthickness=0, cursor="hand2")
        self.launcher.account_button.bind("<Button-1>", lambda event: self.launcher.authentification.displayAccount())
        
        __configPictures.labelConfigWidthHeight(self.launcher.account_button, 39, 43)
        __configPictures.labelPlaceXandYTopRight(self.launcher.account_button, decalageX, decalageY, self)


    def clickMenu(self, event, callback_zone1, callback_zone2, callback_zone3) -> None:
        canvas = event.widget
        x = canvas.canvasx(event.x)
        y = canvas.canvasy(event.y)
        
        width = self.launcher.menu.width()
        height = self.launcher.menu.height()
        
        
        if 0 <= x <= width and 0 <= y <= height / 3:
            callback_zone1(event)
        elif 0 <= x <= width and height / 3 <= y <= height * 2 / 3:
            callback_zone2(event)
        elif 0 <= x <= width and height * 2 / 3 <= y <= height:
            callback_zone3(event)
    
    def changeMode(self) -> None:
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
        
    
    def leaveLauncher(self) -> None:
        def leaveAll(event=None) -> None:
            from infrastructure.services.deletePycache import deletePycache
            
            self.launcher.notifs.status = False
            self.window.destroy()
            deletePycache()
            os._exit(0)
            
        self.launcher.leave_button = Label(self.window, image=self.launcher.leave_game_network, cursor="hand2", bd=0, highlightthickness=0)
        self.launcher.leave_button.place(relx=0.95, rely=0.92, anchor=CENTER)
        self.launcher.leave_button.bind("<Button-1>", lambda event: leaveAll())

