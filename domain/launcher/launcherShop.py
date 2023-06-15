from tkinter import *

class LauncherShop:
    def __init__(self, launcher, window, db, authentification : object):
        self.launcher = launcher
        self.db = db
        self.window = window
        self.authentification = authentification
    
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
                image_buy = getattr(self.launcher, f"buy{i}")
                button = Button(self.window, image=image_buy, cursor="hand2", bd=0, highlightthickness=0, activebackground="#035388", activeforeground="white", command=lambda price=map_price, map=map_name: self.buy(price, map))
                button.place(relx=relx, rely=0.8, anchor=CENTER)
                if money < map_price:
                    # button.config(state="disabled")
                    pass
            else:
                label_owned = Label(self.window, image=self.launcher.owned, bd=0, highlightthickness=0)
                label_owned.place(relx=relx, rely=0.5, anchor=CENTER)
    
    def buy(self, price, map) -> None:
        from infrastructure.services.verifConnection import VerifConnection
        if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
            from infrastructure.services.getSetInformation import GetSetInformation
            
            if GetSetInformation().isConnected("serverPseudo.txt"):
                self.authentification.displayAccount()
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
                    self.launcher.displayShop()
                else:
                    label_buying_fail = Label(self.window, image=self.launcher.buying_fail, bd=0, highlightthickness=0)
                    label_buying_fail.place(relx=x, rely=0.5, anchor=CENTER)
        else:
            self.launcher.errorClientNetwork("noNetwork")