from tkinter import Label, CENTER
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
        
        # Lancement de la vérification des notifications.
        from infrastructure.services.verifNotifs import VerifNotifs
        self.notifs = VerifNotifs(self.db)
        self.notifs.start()
        
        if os.name == "nt":
            launchScreen.status = False
            
            if launchScreen.is_alive():
                launchScreen.join()
        
        if errorStyle == "errorClientOfServer" or errorStyle == "errorServerOfClient" or errorStyle == "errorConnectClientOfServer" or errorStyle == "errorServerFull" or errorStyle == "errorLaunchServer":
            self.errorClientNetwork(errorStyle)
        elif hasattr(self, 'networkStatus'):
            if self.networkStatus == "noNetwork":
                self.errorClientNetwork(self.networkStatus)
                
        self.window.mainloop()

    
    def background(self, statut) -> None:
        self.statut = statut
        from domain.launcher.authentification import Authentification
        self.authentification = Authentification(self, self.window, self.statut, self.db, self.launcherMenu)
        img_bg = getattr(self, f"bg_photo{statut}")
        self.bg_label = Label(self.window, image=img_bg)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)


    def displayParameters(self, event):
        from infrastructure.services.settings import Settings
        
        __settingsClass = Settings(self)
        
        self.launcherMenu.changeMode()
        self.statut = 6
        self.background(self.statut)
        self.launcherMenu.createMenu(None, "settings")
        self.settingsLauncher.settingsActiveNotificationsSond()
        self.settingsLauncher.settingsSoundMap(__settingsClass)
        self.settingsLauncher.settingsSoundVictory(__settingsClass)
        self.settingsLauncher.settingsPionVolume(__settingsClass)
        self.settingsLauncher.settingsFenceVolume(__settingsClass)
        self.settingsLauncher.settingsNoFenceVolume(__settingsClass)
        self.settingsLauncher.choiceFavoriteMap()
        self.settingsLauncher.displayButtonChangeBind()
        self.settingsLauncher.settingsNotificationVolume(__settingsClass)
        self.launcherMenu.leaveLauncher()
        
        
    def displayShop(self) -> None:
        self.launcherMenu.changeMode()
        self.statut = 5
        self.is_shop = True
        self.background(self.statut)
        self.launcherMenu.createMenu(None, "shop")
        self.launcherShop.createButtonShop()
        self.launcherMenu.leaveLauncher()
        
        
    def menuCreateGameSolo(self, event):
        self.launcherMenu.changeMode()
        self.is_shop = False
        self.statut = 0
        self.background(self.statut)
        self.launcherMenu.createMenu(self.statut, "")
        self.paramsGame.numberIA(self.statut)
        self.paramsGame.getIaDifficulty(self.statut)
        self.paramsGame.numberPlayer(self.statut)
        self.paramsGame.sizeBoard(self.statut)
        self.paramsGame.numberFence(self.statut)
        self.paramsGame.choiceMap(self.statut)
        self.paramsGame.buttonStart()
        self.launcherMenu.leaveLauncher()
        
        
    def menuJoinGameNetwork(self, event):
        self.launcherMenu.changeMode()
        self.is_shop = False
        if self.statut != 3:
            self.statut = 1
        self.background(self.statut)
        self.launcherMenu.createMenu(self.statut, "")
        self.launcherJoinServer.create_entries()
        self.paramsGame.choiceMap(self.statut)
        self.launcherMenu.leaveLauncher()
        
        
    def menuCreateGameNetwork(self, event):
        self.launcherMenu.changeMode()
        self.is_shop = False
        self.statut = 2
        self.background(self.statut)
        self.launcherMenu.createMenu(self.statut, "")
        self.paramsGame.choiceMap(self.statut)
        self.paramsGame.numberPlayer(self.statut)
        self.paramsGame.sizeBoard(self.statut)
        self.paramsGame.numberFence(self.statut)
        self.launcherCreateServer.entryPortGame(self.statut)
        self.launcherCreateServer.startButtonNetwork()
        self.launcherMenu.leaveLauncher()
        
        
    def errorClientNetwork(self, errorStyle : str) -> None: 
        def destroyErrorClientNetwork(event=None) -> None:
            self.errorClientNetworkPopup.destroy()

        def contactSupport(event=None) -> None:
            import webbrowser
            
            self.window.attributes("-topmost", False)
            
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