from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class QuoridorLauncher:
    def __init__(self):
        self.window = Tk()
        self.window.title("Mon Launcher")
        self.window.attributes("-fullscreen", True)
        self.window.geometry(f"{self.window.winfo_screenwidth()}x{self.window.winfo_screenheight()}")
        self.background(0)
        self.createMenu(self.statut)
        self.selectPlayer = 2
        self.selectIA = 0
        self.selectSize = 5
        self.selectFence = 4
        self.selectMap = 1
        
    def background(self, statut) -> None:
        # Image de fond
        self.statut = statut
        self.bg_image = Image.open(f"./assets/launcher{self.statut}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def changeMode(self) -> None:
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
        
    def createMenu(self, statut) -> None:
        self.statut = statut
        # Chargement de l'image
        menu_image = Image.open(f"./assets/menu{self.statut}.png")
        menu_image = menu_image.resize((115, 320))
        self.menu = ImageTk.PhotoImage(menu_image)
        
        # Création d'un canvas pour afficher l'image
        canvas = Canvas(self.window, width=self.menu.width(), height=self.menu.height(), bd=0, highlightthickness=0)
        canvas.place(x=42, y=self.window.winfo_screenheight() / 2 - self.menu.height() / 2)
        
        # Affichage de l'image sur le canvas
        canvas.create_image(0, 0, anchor=NW, image=self.menu)
        
        # Ajout des événements de clic pour tout le canvas
        canvas.bind("<Button-1>", lambda event: self.clickMenu(event, self.menuCreateGameSolo, self.menuJoinGameNetwork, self.menuCreateGameNetwork))
        

        # Chargement de la nouvelle image
        parameters = Image.open(f"./assets/parameters.png")
        parameters = parameters.resize((90, 90))
        self.parameters = ImageTk.PhotoImage(parameters)
        
        # Calcul des coordonnées pour aligner la nouvelle image en bas de l'écran
        parameters_x = 50
        parameters_y = self.window.winfo_screenheight() - self.parameters.height() - 55  
        
        # Création d'un canvas pour afficher la nouvelle image
        new_canvas = Canvas(self.window, width=self.parameters.width(), height=self.parameters.height(), bd=0, highlightthickness=0)
        new_canvas.place(x=parameters_x, y=parameters_y)
        
        # Affichage de la nouvelle image sur le canvas
        new_canvas.create_image(0, 0, anchor=NW, image=self.parameters)
        
        # Définition de la fonction de rappel pour la nouvelle zone cliquable
        def callback_parameters(event):
            print("Nouvelle image cliquée")
        
        # Ajout de l'événement de clic pour la nouvelle zone cliquable
        new_canvas.bind("<Button-1>", callback_parameters)
    
    def clickMenu(self, event, callback_zone1, callback_zone2, callback_zone3):
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
            
    def numberIA(self) -> None:
        def action(event) -> None:
            self.selectIA = int(listIA.get())
            print("IA : ", self.selectIA)
            
        listIAs=[0, 1, 2, 3]
        listIA = ttk.Combobox(self, values=listIAs, state="readonly")
        listIA.current(0)
        listIA.grid(row=0, column=0)
        listIA.bind("<<ComboboxSelected>>", action)

    def numberPlayer(self) -> None:
        def action(event) -> None:
            self.selectPlayer = int(listPlayer.get())
            print("Player : ", self.selectPlayer)

        listPlayers=[1, 2, 3, 4]
        listPlayer = ttk.Combobox(self, values=listPlayers, state="readonly")
        listPlayer.current(1)
        listPlayer.grid(row=0, column=1)
        listPlayer.bind("<<ComboboxSelected>>", action)
        
    def sizeBoard(self) -> None:
        def action(event) -> None:
            self.selectSize = int(listSize.get())
            print("Board : ", self.selectSize)

        listSizes=[5, 7, 9, 11]
        listSize = ttk.Combobox(self, values=listSizes, state="readonly")
        listSize.current(0)
        listSize.grid(row=0, column=2)
        listSize.bind("<<ComboboxSelected>>", action)
        
    def numberFence(self) -> None:
        def action(event) -> None:
            self.selectFence = int(listFence.get())
            print("Fence : ", self.selectFence)

        listFences = []
        for i in range(4, 41):
            if i % 4 == 0:
                listFences.append(i)

        listFence = ttk.Combobox(self, values=listFences, state="readonly")
        listFence.current(0)
        listFence.grid(row=0, column=3)
        listFence.bind("<<ComboboxSelected>>", action)

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
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")

        listMaps=["Jungle", "Space", "Hell"]
        listMap = ttk.Combobox(self, values=listMaps, state="readonly")
        listMap.current(0)
        listMap.grid(row=0, column=4)
        listMap.bind("<<ComboboxSelected>>", action)
    
    def menuCreateGameSolo(self, event):
        self.changeMode()
        print("Create Game Solo")
        self.statut = 0
        self.background(self.statut)
        self.createMenu(self.statut)
        # self.numberIA()
        # self.numberPlayer()
        # self.sizeBoard()
        # self.numberFence()
        self.choiceMap()
        
        
    def menuJoinGameNetwork(self, event):
        self.changeMode()
        print("Join Game Network")
        self.statut = 1
        self.background(self.statut)
        self.createMenu(self.statut)
        
    def menuCreateGameNetwork(self, event):
        self.changeMode()
        print("Create Game Network")
        self.statut = 2
        self.background(self.statut)
        self.createMenu(self.statut)


run_launcher = QuoridorLauncher()
run_launcher.window.mainloop()