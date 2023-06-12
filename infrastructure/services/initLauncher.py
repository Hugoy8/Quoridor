from infrastructure.database.config import Database
from domain.launcher.launchScreen import LaunchScreen
from PIL import Image, ImageTk
import os
from tkinter import Tk

class InitLauncher():
    def __init__(self, launcher : object, launcherScreen : LaunchScreen, db : Database) -> None:
        self.launcher = launcher
        self.launchScreen = launcherScreen
        self.db = db
    
    
    def addProgressLaunchScreen(self) -> None:
        if os.name == "nt":
            self.launchScreen.addProgress()
        
        
    def startInit(self) -> None:
        from infrastructure.services.verifConnection import VerifConnection
        from infrastructure.services.getSetInformation import GetSetInformation
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            from infrastructure.database.userDb import UserDb
            userDbVerif = UserDb().verifUserPassword(GetSetInformation().get_username('serverPseudo.txt'))
            
            if userDbVerif[0] == False:
                GetSetInformation().deleteFile("serverPseudo.txt")
        else:
            GetSetInformation().deleteFile("serverPseudo.txt")
            
        self.addProgressLaunchScreen()
                
        self.launcher.window = Tk()
        
        (self.widthWindow, self.heightWindow) = (self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight())
        
        # self.launcher.window.attributes("-topmost", True)
        
        self.launcher.window.title("Mon Launcher")
        
        self.addProgressLaunchScreen()
        
        if os.name == "nt":
            self.launcher.window.attributes("-fullscreen", True)
        
        self.addProgressLaunchScreen()
        
        self.launcher.window.geometry(f"{self.widthWindow}x{self.heightWindow}")
        
        self.launcher.widthWindowLauncher = self.widthWindow
        self.launcher.heightWindowLauncher = self.heightWindow
        
        self.addProgressLaunchScreen()
        
        self.launcher.selectPlayer = 2
        self.launcher.selectIA = 0
        self.launcher.selectSize = 5
        self.launcher.selectFence = 4
        self.launcher.selectMap = 1
        self.launcher.selectIaDifficulty = 1
        self.launcher.statut = 0
        self.launcher.db = self.db
        self.launcher.selectFavoriteMap = self.launcher.loadFavoriteMap()
        
        self.addProgressLaunchScreen()
        
        from infrastructure.services.getSetInformation import GetSetInformation
        self.launcher.getInformation = GetSetInformation()
        
        self.addProgressLaunchScreen()
        
        self.launcher.ip = None
        self.launcher.port = None
        self.launcher.loginPassword = None
        self.launcher.loginButton = None
        self.launcher.winButton = None
        self.launcher.loginUsername = None
        self.launcher.login = None
        self.launcher.registerButton = None
        self.launcher.register = None
        
        self.addProgressLaunchScreen()
        
        self.launcher.registerUsername = None
        self.launcher.registerPassword = None
        self.launcher.insert_query = None
        self.launcher.login_created = None
        self.launcher.register_created = None
        self.launcher.is_shop = False
        self.launcher.widget_register = []
        self.launcher.widget_login = []
        self.launcher.widget_label = []
        self.launcher.pseudo = " "
        self.launcher.bg_not_connected = None
        self.launcher.delete_friend_popup_label = None
        
        self.addProgressLaunchScreen()
        
        self.launcher.owned = Image.open(f"./assets/images/launcher/buy.png")
        self.launcher.owned = self.launcher.owned.resize((385, 66))
        self.launcher.owned = ImageTk.PhotoImage(self.launcher.owned)
        
        self.addProgressLaunchScreen()
        
        self.launcher.buying_fail = Image.open(f"./assets/images/launcher/buying_fail.png")
        self.launcher.buying_fail = self.launcher.buying_fail.resize((385, 66))
        self.launcher.buying_fail = ImageTk.PhotoImage(self.launcher.buying_fail)
        
        
        leave_friend = Image.open(f"./assets/images/launcher/leave_friend.png")
        leave_friend = leave_friend.resize((29, 29))
        self.launcher.leave_friends = ImageTk.PhotoImage(leave_friend)
        
        self.addProgressLaunchScreen()
        
        list_friend = Image.open(f"./assets/images/launcher/list_friends.png")
        menu_height = self.heightWindow
        self.launcher.list_friend = list_friend.resize((int(self.widthWindow / 5), menu_height))
        self.launcher.list_friends = ImageTk.PhotoImage(self.launcher.list_friend)
        
        
        list_notification = Image.open(f"./assets/images/launcher/list_notifications.png")
        menu_height = self.heightWindow
        self.launcher.list_notification = list_notification.resize((int(self.widthWindow / 5), menu_height))
        self.launcher.list_notifications = ImageTk.PhotoImage(self.launcher.list_notification)
        
        self.addProgressLaunchScreen()
        
        delete_friend = Image.open(f"./assets/images/launcher/delete_friends.png")
        delete_friend = delete_friend.resize((25, 29))
        self.launcher.delete_friends = ImageTk.PhotoImage(delete_friend)
        
        valid_friend = Image.open(f"./assets/images/launcher/check.png")
        valid_friend = valid_friend.resize((29, 29))
        self.launcher.valid_friends = ImageTk.PhotoImage(valid_friend)
        
        
        invite_friend = Image.open(f"./assets/images/launcher/invite_friends.png")
        invite_friend = invite_friend.resize((40, 29))
        self.launcher.invite_friends = ImageTk.PhotoImage(invite_friend)
        
        search_friend = Image.open(f"./assets/images/launcher/search_friends.png")
        search_friend = search_friend.resize((29, 29))
        self.launcher.search_friends = ImageTk.PhotoImage(search_friend)
        
        self.addProgressLaunchScreen()
        
        no_notification = Image.open(f"./assets/images/launcher/no_notification.png")
        no_notification = no_notification.resize((26, 26))
        self.launcher.no_notification = ImageTk.PhotoImage(no_notification)
        
        notifications = Image.open(f"./assets/images/launcher/notifications.png")
        notifications = notifications.resize((26, 26))
        self.launcher.notifications = ImageTk.PhotoImage(notifications)
        
        
        back_list_friends = Image.open(f"./assets/images/launcher/back_list_friends.png")
        back_list_friends = back_list_friends.resize((29, 29))
        self.launcher.back_list_friends = ImageTk.PhotoImage(back_list_friends)
        
        friend_online = Image.open(f"./assets/images/launcher/friend_online.png")
        friend_online = friend_online.resize((12, 13))
        self.launcher.statut_online = ImageTk.PhotoImage(friend_online)
        
        self.addProgressLaunchScreen()
        
        friend_offlive = Image.open(f"./assets/images/launcher/friend_offline.png")
        friend_offlive = friend_offlive.resize((12, 13))
        self.launcher.statut_offline = ImageTk.PhotoImage(friend_offlive)
        
        background_not_connect = Image.open(f"./assets/images/launcher/background_not_connect.png")
        background_not_connect = background_not_connect.resize((203, 93))
        self.launcher.background_not_connect = ImageTk.PhotoImage(background_not_connect)
        
        
        account_image = Image.open(f"./assets/images/launcher/account.png")
        account_image = account_image.resize((39, 43))
        self.launcher.account_image = ImageTk.PhotoImage(account_image)
        
        profile_account = Image.open(f"./assets/images/launcher/background_connect.png")
        profile_account = profile_account.resize((350, 60))
        self.launcher.profile_account = ImageTk.PhotoImage(profile_account)
        
        self.addProgressLaunchScreen()
        
        friend = Image.open(f"./assets/images/launcher/friend.png")
        friend = friend.resize((51, 43))
        self.launcher.friends = ImageTk.PhotoImage(friend)
        
        deconnexion = Image.open(f"./assets/images/launcher/deconnexion.png")
        deconnexion = deconnexion.resize((45, 43))
        self.launcher.deconnexion = ImageTk.PhotoImage(deconnexion)
        
        shop = Image.open(f"./assets/images/launcher/shop.png")
        shop = shop.resize((90, 90))
        self.launcher.shop = ImageTk.PhotoImage(shop)
        
        shopOn = Image.open(f"./assets/images/launcher/shopOn.png")
        shopOn = shopOn.resize((90, 90))
        self.launcher.shopOn = ImageTk.PhotoImage(shopOn)
        
        bg_image0 = Image.open(f"./assets/images/launcher/launcher0.png")
        bg_image0 = bg_image0.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo0 = ImageTk.PhotoImage(bg_image0)
        
        self.addProgressLaunchScreen()
        
        bg_image1 = Image.open(f"./assets/images/launcher/launcher1.png")
        bg_image1 = bg_image1.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo1 = ImageTk.PhotoImage(bg_image1)
        
        bg_image2 = Image.open(f"./assets/images/launcher/launcher2.png")
        bg_image2 = bg_image2.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo2 = ImageTk.PhotoImage(bg_image2)
        
        bg_image3 = Image.open(f"./assets/images/launcher/launcher3.png")
        bg_image3 = bg_image3.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo3 = ImageTk.PhotoImage(bg_image3)
        
        bg_image4 = Image.open(f"./assets/images/launcher/launcher4.png")
        bg_image4 = bg_image4.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo4 = ImageTk.PhotoImage(bg_image4)
        
        self.addProgressLaunchScreen()
        
        bg_image5 = Image.open(f"./assets/images/launcher/launcher5.png")
        bg_image5 = bg_image5.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo5 = ImageTk.PhotoImage(bg_image5)
        
        bg_image6 = Image.open(f"./assets/images/launcher/launcher6.png")
        bg_image6 = bg_image6.resize((self.widthWindow, self.heightWindow))
        self.launcher.bg_photo6 = ImageTk.PhotoImage(bg_image6)
        
        parameters = Image.open(f"./assets/images/launcher/parameters.png")
        parameters = parameters.resize((90, 90))
        self.launcher.parameters = ImageTk.PhotoImage(parameters)
        
        parametersOn = Image.open(f"./assets/images/launcher/parametersOn.png")
        parametersOn = parametersOn.resize((90, 90))
        self.launcher.parametersOn = ImageTk.PhotoImage(parametersOn)
        
        menu_image0 = Image.open(f"./assets/images/launcher/menu0.png")
        menu_image0 = menu_image0.resize((130, 360))
        self.launcher.menu0 = ImageTk.PhotoImage(menu_image0)
        
        menu_image1 = Image.open(f"./assets/images/launcher/menu1.png")
        menu_image1 = menu_image1.resize((130, 360))
        self.launcher.menu1 = ImageTk.PhotoImage(menu_image1)
        
        self.addProgressLaunchScreen()
        
        menu_image2 = Image.open(f"./assets/images/launcher/menu2.png")
        menu_image2 = menu_image2.resize((130, 360))
        self.launcher.menu2 = ImageTk.PhotoImage(menu_image2)
        
        menu_image3 = Image.open(f"./assets/images/launcher/menu3.png")
        menu_image3 = menu_image3.resize((130, 360))
        self.launcher.menu3 = ImageTk.PhotoImage(menu_image3)
        
        menu_image_None = Image.open(f"./assets/images/launcher/menuNone.png")
        menu_image_None = menu_image_None.resize((130, 360))
        self.launcher.menuNone = ImageTk.PhotoImage(menu_image_None)
        
        login_image = Image.open(f"./assets/images/launcher/connexion.png")
        login_image = login_image.resize((300, 300))
        self.launcher.login_image = ImageTk.PhotoImage(login_image)
        
        register_image = Image.open(f"./assets/images/launcher/inscription.png")
        register_image = register_image.resize((300, 300))
        self.launcher.register_image = ImageTk.PhotoImage(register_image)
        
        
        
        self.addProgressLaunchScreen()
        
        start_game = Image.open(f"./assets/images/launcher/start_game.png")
        start_game = start_game.resize((165, 50))
        self.launcher.start_game = ImageTk.PhotoImage(start_game)
        
        join_game = Image.open(f"./assets/images/launcher/join_game.png")
        join_game = join_game.resize((205, 50))
        self.launcher.join_game = ImageTk.PhotoImage(join_game)
        
        search_game = Image.open(f"./assets/images/launcher/search_game.png")
        search_game = search_game.resize((235, 50))
        self.launcher.search_game = ImageTk.PhotoImage(search_game)
        
        create_game = Image.open(f"./assets/images/launcher/create_game.png")
        create_game = create_game.resize((205, 50))
        self.launcher.create_game = ImageTk.PhotoImage(create_game)
        
        error_client_network = Image.open(f"./assets/images/errorNetwork/lostConnectOfServer.png")
        error_client_network = error_client_network.resize((550, 320))
        self.launcher.error_client_network = ImageTk.PhotoImage(error_client_network)
        
        error_server_network = Image.open(f"./assets/images/errorNetwork/lostConnectOfClient.png")
        error_server_network = error_server_network.resize((550, 320))
        self.launcher.error_server_network = ImageTk.PhotoImage(error_server_network)
        
        error_connect_server_network = Image.open(f"./assets/images/errorNetwork/ConnectNotOfServer.png")
        error_connect_server_network = error_connect_server_network.resize((550, 320))
        self.launcher.error_connect_server_network = ImageTk.PhotoImage(error_connect_server_network)
        
        errorServerFull = Image.open(f"./assets/images/errorNetwork/ServerFull.png")
        errorServerFull = errorServerFull.resize((550, 320))
        self.launcher.errorServerFull = ImageTk.PhotoImage(errorServerFull)
        
        errorLaunchServer = Image.open(f"./assets/images/errorNetwork/launchServer.png")
        errorLaunchServer = errorLaunchServer.resize((550, 320))
        self.launcher.errorLaunchServer = ImageTk.PhotoImage(errorLaunchServer)
        
        no_network = Image.open(f"./assets/images/errorNetwork/NoNetwork.png")
        no_network = no_network.resize((550, 320))
        self.launcher.no_network = ImageTk.PhotoImage(no_network)

        error_client_network_btn = Image.open(f"./assets/images/errorNetwork/lostConnectOfServerBtn.png")
        error_client_network_btn = error_client_network_btn.resize((157, 42))
        self.launcher.error_client_network_btn = ImageTk.PhotoImage(error_client_network_btn)
        
        error_client_network_btn_link = Image.open(f"./assets/images/errorNetwork/lostConnectOfServerBtnLink.png")
        error_client_network_btn_link = error_client_network_btn_link.resize((177, 42))
        self.launcher.error_client_network_btn_link = ImageTk.PhotoImage(error_client_network_btn_link)
        
        self.addProgressLaunchScreen()
        
        buy1 = Image.open(f"./assets/images/launcher/buy1.png")
        buy1 = buy1.resize((400, 60))
        self.launcher.buy1 = ImageTk.PhotoImage(buy1)
        
        buy2 = Image.open(f"./assets/images/launcher/buy2.png")
        buy2 = buy2.resize((400, 60))
        self.launcher.buy2 = ImageTk.PhotoImage(buy2)
        
        buy3 = Image.open(f"./assets/images/launcher/buy3.png")
        buy3 = buy3.resize((400, 60))
        self.launcher.buy3 = ImageTk.PhotoImage(buy3)
        
        image_money = Image.open(f"./assets/images/launcher/money.png")
        image_money = image_money.resize((48, 48))
        self.launcher.image_money = ImageTk.PhotoImage(image_money)
        
        no_sound_notifications = Image.open(f"./assets/images/launcher/no_notifications_sound.png")
        no_sound_notifications = no_sound_notifications.resize((48, 48))
        self.launcher.no_sound_notifications_image = ImageTk.PhotoImage(no_sound_notifications)

        yes_sound_notifications = Image.open(f"./assets/images/launcher/yes_notifications_sound.png")
        yes_sound_notifications = yes_sound_notifications.resize((48, 48))
        self.launcher.yes_sound_notifications_image = ImageTk.PhotoImage(yes_sound_notifications)

        bind_changing = Image.open(f"./assets/images/launcher/bind_changing.png")
        bind_changing = bind_changing.resize((48, 48))
        self.launcher.bind_changing = ImageTk.PhotoImage(bind_changing)

        bind = Image.open(f"./assets/images/launcher/bind.png")
        bind = bind.resize((48, 48))
        self.launcher.bind = ImageTk.PhotoImage(bind)

        leave_game_network = Image.open(f"./assets/images/launcher/leaveGameNetwork.png")
        leave_game_network = leave_game_network.resize((90, 90))
        self.launcher.leave_game_network = ImageTk.PhotoImage(leave_game_network)
        
        no_notification_text = Image.open(f"./assets/images/launcher/no_notification_text.png")
        no_notification_text = no_notification_text.resize((242, 29))
        self.launcher.no_notification_text = ImageTk.PhotoImage(no_notification_text)
        
        delete_friend_pop = Image.open(f"./assets/images/launcher/delete_friends_popup.png")
        delete_friend_pop = delete_friend_pop.resize((554, 322))
        self.launcher.delete_friend_popup = ImageTk.PhotoImage(delete_friend_pop)
        
        delete_friend_button = Image.open(f"./assets/images/launcher/delete_friend_button.png")
        delete_friend_button = delete_friend_button.resize((155, 40))
        self.launcher.delete_friend_button = ImageTk.PhotoImage(delete_friend_button)
        
        no_delete_friend_button = Image.open(f"./assets/images/launcher/no_delete_friend_button.png")
        no_delete_friend_button = no_delete_friend_button.resize((155, 40))
        self.launcher.no_delete_friend_button = ImageTk.PhotoImage(no_delete_friend_button)
        
        self.addProgressLaunchScreen()
        
        self.launchScreen.status = False