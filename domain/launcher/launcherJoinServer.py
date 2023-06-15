from tkinter import Label, Button, CENTER, Entry, FLAT
from domain.network.network import joinSession
from domain.network.scanNetwork import ScanNetwork


class launcherJoinServer:
    def __init__(self, launcher, window, launcherCreateServer: object):
        self.launcher = launcher
        self.window = window
        self.launcherCreateServer = launcherCreateServer
        
    def create_entries(self) -> None:
        def clickButtonVerifConnection(typeButton : str, event=None) -> None:
            from infrastructure.services.verifConnection import VerifConnection
            if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
                if typeButton == "JoinGame":
                    self.launcher.notifs.status = False
                    self.joinGameNetwork()
                elif typeButton == "ScanGames":
                    self.displayIp()
            else:
                self.launcher.errorClientNetwork("noNetwork")
            
        ip = Label(self.window, text="Adresse IP :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        ip.place(relx=0.25, rely=0.7, anchor=CENTER)
        self.entryIp = Entry(self.window, bd=3, width=15, font=("Arial", 13), background="#102A43", foreground="white", insertbackground="white", highlightbackground="#2BB0ED", highlightcolor="#2BB0ED", highlightthickness=1, relief=FLAT)
        self.entryIp.place(relx=0.25, rely=0.73, anchor=CENTER)

        self.launcherCreateServer.entryPortGame(self.launcher.statut)
        
        map = Label(self.window, text="Thème de la carte :", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        map.place(relx=0.45, rely=0.7, anchor=CENTER)
        
        start = Button(self.window, image=self.launcher.join_game, cursor="hand2", activebackground="#035388", bd=0, highlightthickness=0, activeforeground="white", command=lambda: clickButtonVerifConnection("JoinGame"))
        search_game_button = Button(self.window, image=self.launcher.search_game,  cursor="hand2", bd=0, highlightthickness=0, command=lambda: clickButtonVerifConnection("ScanGames"), activebackground="#486581",  activeforeground="white")
        
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

        portstr = self.launcherCreateServer.entry_port.get()
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
        joinSession(ip, port, self.launcher.selectMap)
        
    
    def displayIp(self) -> None:
        scanNetwork = ScanNetwork(8000, 8003)
        scanNetwork.scan()
        listip = scanNetwork.getIp()
        if len(listip) == 0:
            self.launcher.statut = 3
            self.launcher.menuJoinGameNetwork(event=None)
        else:
            relyDisplay = 0.4
            relyLabel = 0.51
            for i, address in enumerate(listip):
                if i > 2:
                    break
                
                ip, port = address.split(":")
                
                ip_port_display = Label(self.window, image=self.launcher.display_ip_port, bd=0, highlightthickness=0)
                
                if i == 0:
                    ip_port_display.place(relx=0.83, rely=relyDisplay, anchor=CENTER)
                elif i == 1:
                    ip_port_display.place(relx=0.83, rely=(relyDisplay + (((140 * 100) / self.window.winfo_screenheight())/100) + (((31 * 100) / self.window.winfo_screenheight())/100) + 0.05), anchor=CENTER)
                    
                ip_text = Label(ip_port_display, text=ip, bd=0, highlightthickness=0, bg="#101D2C", fg="white", font=("Arial", 10))
                ip_text.place(relx=0.5, rely=0.33, anchor=CENTER)
                port_text = Label(ip_port_display, text=port, bd=0, highlightthickness=0, bg="#101D2C", fg="white", font=("Arial", 10))
                port_text.place(relx=0.5, rely=0.88, anchor=CENTER)
                
                join_game_label = Label(self.window, image=self.launcher.join_game_button, bd=0, highlightthickness=0, cursor="hand2")
                
                if i == 0:
                    join_game_label.place(relx=0.83, rely=relyLabel, anchor=CENTER)
                elif i == 1:
                    join_game_label.place(relx=0.83, rely=(relyDisplay + (((140 * 100) / self.window.winfo_screenheight())/100) + (((31 * 100) / self.window.winfo_screenheight())/100) + 0.05 + 0.11), anchor=CENTER)
                    
                join_game_label.bind("<Button-1>", lambda event: self.onIpClick(ip, port))


    def onIpClick(self, ip: str, port: int, event=None) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation

        ip = str(ip)
        port = int(port)
        self.window.destroy()
        joinSession(ip, port, self.launcher.selectMap)