from tkinter import Label, CENTER, Button
from tkinter import ttk
from domain.network.network import startSession

class LauncherCreateServer:
    def __init__(self, launcher, window):
        self.launcher = launcher
        self.window = window
    
    
    def entryPortGame(self, statut) -> None:
        if statut == 2:
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
        def clickButtonVerifConnection(typeButton : str, event=None) -> None:
            from infrastructure.services.verifConnection import VerifConnection
            if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
                if typeButton == "startGame":
                    self.launcher.notifs.status = False
                    self.startGame()
            else:
                self.launcher.errorClientNetwork("noNetwork")
                
        start = Button(self.window, image=self.launcher.create_game, bd=0, highlightthickness=0, cursor="hand2", activebackground="#035388",  activeforeground="white", command=lambda: clickButtonVerifConnection("startGame"))
            
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
        nbr_player = int(self.launcher.selectPlayer)
        grid_size = self.launcher.selectSize
        nbr_fences = self.launcher.selectFence
        map = self.launcher.selectMap

        if grid_size == 5 and nbr_fences > 20:
            self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F2234", fg="red")
            self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
        else:
            self.window.destroy()
            startSession(port, nbr_player, grid_size, nbr_player, 0, nbr_fences, map, "", False)