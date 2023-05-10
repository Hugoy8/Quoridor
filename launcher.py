from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from main import restartGame
from network import *

class QuoridorLauncher:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1400x700")
        self.window.title("Quoridor")
        self.window.maxsize(1400, 700)
        self.window.minsize(1400, 700)
        self.window.iconbitmap('./assets/logo.ico')
        self.statut = 0
        self.modeToSolo()
        self.selectPlayer = 2
        self.selectIA = 0
        self.selectSize = 5
        self.selectFence = 4
        self.selectMap = 1

    def background(self):
        # Image de fond
        self.bg_image = Image.open(f"./assets/launcher{self.statut}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth()-300, self.window.winfo_screenheight()-200))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def addText(self):
        # Ajout du texte
        self.text = Label(self.window, text="Nombre de joueurs", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=290, y=490)
        self.text = Label(self.window, text="bientôt disponible", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=640, y=520)
        
        
        self.text = Label(self.window, text="Taille du tableau : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=290, y=545)
        self.text = Label(self.window, text="Nombre de barrière : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=450, y=545)
        self.text = Label(self.window, text="Choix de la map : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=620, y=545)
    
    def numberIA(self):
        def action(event):
            self.selectIA = int(listIA.get())
            print("IA : ", self.selectIA)
            
        listIAs=[0, 1, 2, 3]
        listIA = ttk.Combobox(self.window, values=listIAs, state="readonly")
        listIA.current(0)
        listIA.place(x=440, y=520)
        listIA.bind("<<ComboboxSelected>>", action)

    def numberPlayer(self):
        def action(event):
            self.selectPlayer = int(listPlayer.get())
            print("Player : ", self.selectPlayer)

        listPlayers=[1, 2, 3, 4]
        listPlayer = ttk.Combobox(self.window, values=listPlayers, state="readonly")
        listPlayer.current(1)
        listPlayer.place(x=280, y=520)
        listPlayer.bind("<<ComboboxSelected>>", action)
        
    def sizeBoard(self):
        def action(event):
            self.selectSize = int(listSize.get())
            print("Board : ", self.selectSize)

        listSizes=[5, 7, 9, 11]
        listSize = ttk.Combobox(self.window, values=listSizes, state="readonly")
        listSize.current(0)
        listSize.place(x=280, y=570)
        listSize.bind("<<ComboboxSelected>>", action)
        
    def numberFence(self):
        def action(event):
            self.selectFence = int(listFence.get())
            print("Fence : ", self.selectFence)

        listFences = []
        for i in range(4, 41):
            if i % 4 == 0:
                listFences.append(i)

        listFence = ttk.Combobox(self.window, values=listFences, state="readonly")
        listFence.current(0)
        listFence.place(x=440, y=570)
        listFence.bind("<<ComboboxSelected>>", action)

    def choiceMap(self):
        def action(event):
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
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(0)
        listMap.place(x=610, y=570)
        listMap.bind("<<ComboboxSelected>>", action)
        
    def buttonStart(self):
        def start_game():
            grid_size = self.selectSize
            nbr_fences = self.selectFence
            nb_ia = self.selectIA
            nb_player = self.selectPlayer + self.selectIA
            map = self.selectMap
            self.window.destroy()
            if grid_size == 5 and nbr_fences > 20:
                nbr_fences = 20
            restartGame(grid_size, nb_player, nb_ia, nbr_fences, map)

        start = Button(self.window, text="START", command=start_game, bg="#0D2338", fg="#FFF", font=("Arial", 15), width=10, cursor="hand2",  activebackground="#035388",  activeforeground="white")
        start.place(x=775, y=550)
        
    def changeMode(self):
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
                
    def choiceMode(self):
        image_path = "./assets/fond_menu.png"
        img = Image.open(image_path)
        img = img.resize((95, 255))
        fond_menu = ImageTk.PhotoImage(img)

        menu_label = Label(self.window, image=fond_menu, bg="#035388")
        menu_label.image = fond_menu
        menu_label.place(x=30, y=220)

        image_path = "./assets/solo_mode.png"
        img = Image.open(image_path)
        img = img.resize((80, 80))
        solo_mode = ImageTk.PhotoImage(img)

        image_path = "./assets/rejoindre.png"
        img2 = Image.open(image_path)
        img2 = img2.resize((65, 65))
        rejoindre = ImageTk.PhotoImage(img2)

        image_path = "./assets/host.png"
        img3 = Image.open(image_path)
        img3 = img3.resize((65, 65))
        host = ImageTk.PhotoImage(img3)

        solo = Button(menu_label, image=solo_mode, command=self.modeToSolo, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        solo.image = solo_mode  
        solo.place(x=8, y=10)

        rejoindre_mode = Button(menu_label, image=rejoindre, command=self.modeToSelectGame, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        rejoindre_mode.image = rejoindre
        rejoindre_mode.place(x=16, y=90)

        host_mode = Button(menu_label, image=host, command=self.modeToCreateGame, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        host_mode.image = host 
        host_mode.place(x=16, y=170)
        
    def modeToSolo(self):
        self.changeMode()
        self.statut = 0
        self.background()
        self.numberIA()
        self.center_window()
        self.choiceMode()
        self.addText()
        self.numberFence()
        self.numberPlayer()
        self.sizeBoard()
        self.choiceMap()
        self.buttonStart()
        
        
    def create_entries(self):
        self.entry1 = Entry(self.window, width=20)
        self.entry1.place(x=296, y=508)

        self.entry2 = Entry(self.window, width=20)
        self.entry2.place(x=481, y=508)

        self.entry3 = Entry(self.window, width=20)
        self.entry3.place(x=665, y=508)
        
        start = Button(self.window, text="Rejoindre la partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.joinGameNewtork)
        start.place(x=290, y=563)
        
        reset_button = Button(self.window, text="Réinitialiser", font=("Arial", 13),  cursor="hand2", fg="#FFF",  bg="#486581", command=self.resetEntries, width=10, activebackground="#486581",  activeforeground="white")
        reset_button.place(x=500, y=563)
    
    def joinGameNewtork(self):
        ip = self.entry1.get()
        port = int(self.entry2.get())
        self.window.destroy()
        joinSession(ip, port)
        
    def startGame(self):
        port = int(self.entry_port.get())
        nbr_player = int(self.nbr_player_network.get())
        self.window.destroy()
        startSession(port, nbr_player, 5, 2, 0, 8)

    def entriesNetwork(self):
        self.nbr_player_network = Entry(self.window, width=20)
        self.nbr_player_network.place(x=296, y=508)
        
        self.entry_port = Entry(self.window, width=20)
        self.entry_port.place(x=1201, y=508)

    def startButtonNetwork(self):
        start = Button(self.window, text="Créer une partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.startGame)
        start.place(x=290, y=563)

    def resetEntries(self):
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        self.entry3.delete(0, END)

    def modeToSelectGame(self):
        self.changeMode()
        self.statut = 1
        self.background()
        self.center_window()
        self.choiceMode()
        self.create_entries()
        
    def modeToCreateGame(self):
        self.changeMode()
        self.statut = 2
        self.background()
        self.center_window()
        self.choiceMode()
        self.entriesNetwork()
        self.startButtonNetwork()
                
    def center_window(self):
        # Récupération de la résolution de l'écran
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        x = (screen_width - 1400) // 2
        y = (screen_height - 700) // 2
        # Configuration de la fenêtre
        self.window.geometry(f"1400x700+{x}+{y}")
        
run_launcher = QuoridorLauncher()
run_launcher.window.mainloop()


