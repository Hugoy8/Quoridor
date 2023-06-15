from tkinter import CENTER, Label, Button
from tkinter import ttk
from infrastructure.services.services import restartGame

class ParamsGame:
    def __init__(self, launcher, window, db):
        self.launcher = launcher
        self.window = window
        self.db = db
    
    def numberIA(self, statut) -> None:
        def action(event) -> None:
            self.launcher.selectIA = int(listIA.get())
            
        listIAs=[0, 1, 2, 3]
        listIA = ttk.Combobox(self.window, values=listIAs, state="readonly")
        listIA.current(0)
        listIA.place(relx=0.45, rely=0.73, anchor=CENTER)
        listIA.bind("<<ComboboxSelected>>", action)
        if statut == 0:
            nbrIA = Label(self.window, text="Nombre d'IA", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
            nbrIA.place(relx=0.45, rely=0.7, anchor=CENTER)
            
            
    def getIaDifficulty(self, statut) -> None:
        def action(event) -> None:
            self.launcher.selectIaDifficulty = listIAdifficulty.get()
            try:
                if self.launcher.selectIaDifficulty == "Facile":
                    self.launcher.selectIaDifficulty = 1
                elif self.launcher.selectIaDifficulty == "Moyenne":
                    self.launcher.selectIaDifficulty = 2
                elif self.launcher.selectIaDifficulty == "Difficile":
                    self.launcher.selectIaDifficulty = 3
            except ValueError:
                print(f"Error: '{self.launcher.selectIaDifficulty}' is not a valid level")
                
        listIAdifficultys=["Facile", "Moyenne", "Difficile"]
        listIAdifficulty = ttk.Combobox(self.window, values=listIAdifficultys, state="readonly")
        listIAdifficulty.current(0)
        listIAdifficulty.place(relx=0.55, rely=0.73, anchor=CENTER)
        listIAdifficulty.bind("<<ComboboxSelected>>", action)
        if statut == 0:
            nbrIA = Label(self.window, text="Difficulté des bots", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
            nbrIA.place(relx=0.55, rely=0.7, anchor=CENTER)
            
            
    def numberPlayer(self, statut) -> None:
        def action(event) -> None:
            self.launcher.selectPlayer = int(listPlayer.get())
            
        if statut == 0:
            listPlayers = [1, 2, 3, 4]
            currentSelection = 1
        else:
            listPlayers = [2, 4]
            currentSelection = 0
            
        listPlayer = ttk.Combobox(self.window, values=listPlayers, state="readonly")
        listPlayer.current(currentSelection)
        listPlayer.place(relx=0.35, rely=0.73, anchor=CENTER)
        listPlayer.bind("<<ComboboxSelected>>", action)
        if statut == 0 or statut == 2:
            nbrPlayer = Label(self.window, text="Nombre de Joueur(s)", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
            nbrPlayer.place(relx=0.35, rely=0.7, anchor=CENTER)
            
            
    def sizeBoard(self, statut) -> None:
        def action(event) -> None:
            self.launcher.selectSize = int(listSize.get())
            
        listSizes=[5, 7, 9, 11]
        listSize = ttk.Combobox(self.window, values=listSizes, state="readonly")
        listSize.current(0)
        if statut == 0:
            x = 0.65
            y = 0.73
            x2 = 0.65
            y2 = 0.7
        elif statut == 2:
            x = 0.55
            y = 0.73
            x2 = 0.55
            y2 = 0.7
        listSize.place(relx=x, rely=y, anchor=CENTER)
        listSize.bind("<<ComboboxSelected>>", action)
        
        nbrIA = Label(self.window, text="Taille du plateau", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        nbrIA.place(relx=x2, rely=y2, anchor=CENTER)
        
        
    def numberFence(self, statut) -> None:
        def action(event) -> None:
            self.launcher.selectFence = int(listFence.get())
            
        listFences = []
        for i in range(4, 41):
            if i % 4 == 0:
                listFences.append(i)
                
        listFence = ttk.Combobox(self.window, values=listFences, state="readonly")
        listFence.current(0)
        if statut == 0:
            x = 0.75
            y = 0.73
            x2 = 0.75
            y2 = 0.7
        elif statut == 2:
            x = 0.45
            y = 0.73
            x2 = 0.45
            y2 = 0.7
        listFence.place(relx=x, rely=y, anchor=CENTER)
        listFence.bind("<<ComboboxSelected>>", action)
        nbrFence = Label(self.window, text="Nombre de barrières", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
        nbrFence.place(relx=x2, rely=y2, anchor=CENTER)
        
        
    def choiceMap(self, statut) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        def action(event) -> None:
            selected_value = listMap.get()
            try:
                if selected_value == "Jungle":
                    self.launcher.selectMap = 1
                elif selected_value == "Space":
                    self.launcher.selectMap = 2
                elif selected_value == "Hell":
                    self.launcher.selectMap = 3
                elif selected_value == "Ice":
                    self.launcher.selectMap = 4
                elif selected_value == "Electricity":
                    self.launcher.selectMap = 5
                elif selected_value == "Sugar":
                    self.launcher.selectMap = 6
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
        if statut == 1 or statut == 3:
            X = 0.45
        listMap.place(relx=X, rely=Y, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        if statut == 0 or statut == 2:
            nameMap = Label(self.window, text="Thème de la carte", font=("Arial", 10), bg="#0F2234", fg="#E3F8FF")
            nameMap.place(relx=0.25, rely=0.7, anchor=CENTER)
    
    def buttonStart(self) -> None:
        def start_game() -> None:
            if hasattr(self.launcher, 'error_label'):
                self.error_label.destroy()
            grid_size = self.launcher.selectSize
            nbr_fences = self.launcher.selectFence
            nb_ia = self.launcher.selectIA
            nb_player = self.launcher.selectPlayer + self.launcher.selectIA
            
            if nb_player > 4 or nb_player < 2 or nb_player == 3:
                self.error_label = Label(self.window, text=f"Le nombre de joueurs ({nb_player}) est incorrect (2 ou 4).", font=("Arial", 13), bg="#0F2234", fg="red")
                self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            elif grid_size == 5 and nbr_fences > 20:
                    self.error_label = Label(self.window, text=f"Le nombre de barrières({nbr_fences}) pour une taille de 5x5 est incorrect (20 max).", font=("Arial", 13), bg="#0F2234", fg="red")
                    self.error_label.place(relx=0.5, rely=0.9, anchor=CENTER)
            else:
                map = self.launcher.selectMap
                self.window.destroy()
                self.launcher.notifs.status = False
                restartGame(grid_size, nb_player, nb_ia, nbr_fences, map, self.launcher.selectIaDifficulty)
                
        start = Button(self.window, image=self.launcher.start_game, command=start_game, cursor="hand2", bd=0, highlightthickness=0, activebackground="#035388",  activeforeground="white")
        start.place(relx=0.25, rely=0.8, anchor=CENTER)