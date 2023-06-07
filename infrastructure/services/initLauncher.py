from infrastructure.database.config import Database
from domain.launcher.launchScreen import LaunchScreen
from PIL import Image, ImageTk
import os
from tkinter import Tk

class InitLauncher:
    def __init__(self, launcher : object, launcherScreen : LaunchScreen) -> None:
        self.launcher = launcher
        self.launchScreen = launcherScreen
        
        
    def startInit(self, db : Database) -> None:
        self.launcher.window = Tk()
        self.launcher.window.title("Mon Launcher")
        
        self.launchScreen.addProgress()
        
        if os.name == "nt":
            self.launcher.window.attributes("-fullscreen", True)
        
        self.launchScreen.addProgress()
        
        self.launcher.window.geometry(f"{self.launcher.window.winfo_screenwidth()}x{self.launcher.window.winfo_screenheight()}")
        
        self.launchScreen.addProgress()
        
        self.launcher.selectPlayer = 2
        self.launcher.selectIA = 0
        self.launcher.selectSize = 5
        self.launcher.selectFence = 4
        self.launcher.selectMap = 1
        self.launcher.selectIaDifficulty = 0
        self.launcher.statut = 0
        self.launcher.db = db
        
        self.launchScreen.addProgress()
        
        self.launcher.selectFavoriteMap = self.launcher.loadFavoriteMap()
        
        self.launchScreen.addProgress()
        
        # Zone de changement de status 
        self.launcher.db.setStatusUser(self.launcher.get_username("serverPseudo.txt"), 1)
        
        self.launchScreen.addProgress()
        
        self.launcher.ip = None
        self.launcher.port = None
        self.launcher.loginPassword = None
        self.launcher.loginButton = None
        self.launcher.winButton = None
        self.launcher.loginUsername = None
        self.launcher.login = None
        self.launcher.registerButton = None
        self.launcher.register = None
        
        self.launchScreen.addProgress()
        
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
        
        self.launchScreen.addProgress()
        
        self.launcher.owned = Image.open(f"./assets/images/launcher/buy.png")
        self.launcher.owned = self.launcher.owned.resize((385, 66))
        self.launcher.owned = ImageTk.PhotoImage(self.launcher.owned)
        
        self.launchScreen.addProgress()
        
        self.launcher.buying_fail = Image.open(f"./assets/images/launcher/buying_fail.png")
        self.launcher.buying_fail = self.launcher.buying_fail.resize((385, 66))
        self.launcher.buying_fail = ImageTk.PhotoImage(self.launcher.buying_fail)
        
        
        leave_friend = Image.open(f"./assets/images/launcher/leave_friend.png")
        leave_friend = leave_friend.resize((29, 29))
        self.launcher.leave_friends = ImageTk.PhotoImage(leave_friend)
        
        self.launchScreen.addProgress()
        
        list_friend = Image.open(f"./assets/images/launcher/list_friends.png")
        menu_height = self.launcher.window.winfo_screenheight()
        self.launcher.list_friend = list_friend.resize((int(self.launcher.window.winfo_screenwidth() / 5), menu_height))
        self.launcher.list_friends = ImageTk.PhotoImage(self.launcher.list_friend)
        
        
        list_notification = Image.open(f"./assets/images/launcher/list_notifications.png")
        menu_height = self.launcher.window.winfo_screenheight()
        self.launcher.list_notification = list_notification.resize((int(self.launcher.window.winfo_screenwidth() / 5), menu_height))
        self.launcher.list_notifications = ImageTk.PhotoImage(self.launcher.list_notification)
        
        self.launchScreen.addProgress()
        
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
        
        self.launchScreen.addProgress()
        
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
        
        self.launchScreen.addProgress()
        
        friend_offlive = Image.open(f"./assets/images/launcher/friend_offline.png")
        friend_offlive = friend_offlive.resize((12, 13))
        self.launcher.statut_offline = ImageTk.PhotoImage(friend_offlive)
        
        background_not_connect = Image.open(f"./assets/images/launcher/background_not_connect.png")
        background_not_connect = background_not_connect.resize((203, 93))
        self.launcher.background_not_connect = ImageTk.PhotoImage(background_not_connect)
        
        
        account_image = Image.open(f"./assets/images/launcher/account.png")
        account_image = account_image.resize((39, 43))
        self.launcher.account_image = ImageTk.PhotoImage(account_image)
        
        background_connect = Image.open(f"./assets/images/launcher/background_connect.png")
        background_connect = background_connect.resize((203, 183))
        self.launcher.background_connect = ImageTk.PhotoImage(background_connect)
        
        self.launchScreen.addProgress()
        
        friend = Image.open(f"./assets/images/launcher/friend.png")
        friend = friend.resize((51, 43))
        self.launcher.friends = ImageTk.PhotoImage(friend)
        
        deconnexion = Image.open(f"./assets/images/launcher/deconnexion.png")
        deconnexion = deconnexion.resize((45, 43))
        self.launcher.deconnexion = ImageTk.PhotoImage(deconnexion)
        
        shop = Image.open(f"./assets/images/launcher/shop.png")
        shop = shop.resize((90, 90))
        self.launcher.shop = ImageTk.PhotoImage(shop)
        
        bg_image0 = Image.open(f"./assets/images/launcher/launcher0.png")
        bg_image0 = bg_image0.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo0 = ImageTk.PhotoImage(bg_image0)
        
        self.launchScreen.addProgress()
        
        bg_image1 = Image.open(f"./assets/images/launcher/launcher1.png")
        bg_image1 = bg_image1.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo1 = ImageTk.PhotoImage(bg_image1)
        
        bg_image2 = Image.open(f"./assets/images/launcher/launcher2.png")
        bg_image2 = bg_image2.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo2 = ImageTk.PhotoImage(bg_image2)
        
        bg_image3 = Image.open(f"./assets/images/launcher/launcher3.png")
        bg_image3 = bg_image3.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo3 = ImageTk.PhotoImage(bg_image3)
        
        bg_image4 = Image.open(f"./assets/images/launcher/launcher4.png")
        bg_image4 = bg_image4.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo4 = ImageTk.PhotoImage(bg_image4)
        
        self.launchScreen.addProgress()
        
        bg_image5 = Image.open(f"./assets/images/launcher/launcher5.png")
        bg_image5 = bg_image5.resize((self.launcher.window.winfo_screenwidth(), self.launcher.window.winfo_screenheight()))
        self.launcher.bg_photo5 = ImageTk.PhotoImage(bg_image5)
        
        parameters = Image.open(f"./assets/images/launcher/parameters.png")
        parameters = parameters.resize((90, 90))
        self.launcher.parameters = ImageTk.PhotoImage(parameters)
        
        menu_image0 = Image.open(f"./assets/images/launcher/menu0.png")
        menu_image0 = menu_image0.resize((115, 320))
        self.launcher.menu0 = ImageTk.PhotoImage(menu_image0)
        
        menu_image1 = Image.open(f"./assets/images/launcher/menu1.png")
        menu_image1 = menu_image1.resize((115, 320))
        self.launcher.menu1 = ImageTk.PhotoImage(menu_image1)
        
        self.launchScreen.addProgress()
        
        menu_image2 = Image.open(f"./assets/images/launcher/menu2.png")
        menu_image2 = menu_image2.resize((115, 320))
        self.launcher.menu2 = ImageTk.PhotoImage(menu_image2)
        
        menu_image3 = Image.open(f"./assets/images/launcher/menu3.png")
        menu_image3 = menu_image3.resize((115, 320))
        self.launcher.menu3 = ImageTk.PhotoImage(menu_image3)
        
        login_image = Image.open(f"./assets/images/launcher/connexion.png")
        login_image = login_image.resize((300, 300))
        self.launcher.login_image = ImageTk.PhotoImage(login_image)
        
        register_image = Image.open(f"./assets/images/launcher/inscription.png")
        register_image = register_image.resize((300, 300))
        self.launcher.register_image = ImageTk.PhotoImage(register_image)
        
        self.launchScreen.addProgress()
        
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
        
        self.launchScreen.addProgress()
        
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
        
        self.launchScreen.addProgress()