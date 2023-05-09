from tkinter import *
from PIL import Image, ImageTk
from main import restartGame
from network import *
import platform

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
        self.text.place(x=290, y=570)
        self.text = Label(self.window, text="Nombre de barrière : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=530, y=570)
    
        
        # Nombre d'IA
    def toggle_checkbox_ia(self):
        if self.nbr_ia.get() == 1:
            self.ia_3.configure(state="disabled")
            self.ia_2.configure(state="disabled")
            self.ia_1.configure(state="disabled")
        elif self.nbr_ia_2.get() == 1:
            self.ia_0.configure(state="disabled")
            self.ia_3.configure(state="disabled")
            self.ia_1.configure(state="disabled")
        elif self.nbr_ia_0.get() == 1:
            self.ia_3.configure(state="disabled")
            self.ia_2.configure(state="disabled")
            self.ia_1.configure(state="disabled")
        elif self.nbr_ia_3.get() == 1:
            self.ia_0.configure(state="disabled")
            self.ia_2.configure(state="disabled")
            self.ia_1.configure(state="disabled")
        else:
            self.ia_1.configure(state="normal")
            self.ia_3.configure(state="normal")
            self.ia_0.configure(state="normal")
            self.ia_2.configure(state="normal")
            
            
    def numberIA(self):
        # Boutons de nombre d'IA
        self.nbr_ia = IntVar()
        self.nbr_ia_2 = IntVar()
        self.nbr_ia_0 = IntVar()
        self.nbr_ia_3 = IntVar()
        self.ia_0 = Checkbutton(self.window, text="0", bg="#0D2338", fg="#FFF", variable=self.nbr_ia_0, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_0.place(x=440, y=520)
        self.ia_1 = Checkbutton(self.window, text="1", bg="#0D2338", fg="#FFF", variable=self.nbr_ia, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_1.place(x=480, y=520)
        self.ia_2 = Checkbutton(self.window, text="2", bg="#0D2338", fg="#FFF", variable=self.nbr_ia_2, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_2.place(x=520, y=520)
        self.ia_3 = Checkbutton(self.window, text="3", bg="#0D2338", fg="#FFF", variable=self.nbr_ia_3, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_3.place(x=560, y=520)
    
    def get_selected_ia(self):
        selected_value = 0
        if self.nbr_ia.get() == 1:
            selected_value = 1
        elif self.nbr_ia_2.get() == 1:
            selected_value = 2
        elif self.nbr_ia_3.get() == 1:
            selected_value = 3
        return selected_value
        
    def update_ia_state(self):
        if self.nbr_player.get() == 1:
            self.ia_1.configure(state="normal")
            self.ia_2.configure(state="disabled")
            self.ia_0.configure(state="disabled")
            self.ia_3.configure(state="normal")
            self.p2.configure(state="disabled")
            self.p3.configure(state="disabled")
            self.p4.configure(state="disabled")
        elif self.nbr_player2.get() == 1:
            self.ia_0.configure(state="normal")
            self.ia_1.configure(state="disabled")
            self.ia_2.configure(state="normal")
            self.ia_3.configure(state="disabled")
            self.p1.configure(state="disabled")
            self.p3.configure(state="disabled")
            self.p4.configure(state="disabled")
        elif self.nbr_player3.get() == 1:
            self.ia_1.configure(state="normal")
            self.ia_0.configure(state="disabled")
            self.ia_2.configure(state="disabled")
            self.ia_3.configure(state="disabled")
            self.p2.configure(state="disabled")
            self.p1.configure(state="disabled")
            self.p4.configure(state="disabled")
        elif self.nbr_player4.get() == 1:
            self.ia_0.configure(state="disabled")
            self.ia_1.configure(state="disabled")
            self.ia_2.configure(state="disabled")
            self.ia_3.configure(state="disabled")
            self.p2.configure(state="disabled")
            self.p3.configure(state="disabled")
            self.p1.configure(state="disabled")
        else:  
            self.p1.configure(state="normal")
            self.p2.configure(state="normal")
            self.p3.configure(state="normal")
            self.p4.configure(state="normal")
            
            self.ia_0.configure(state="normal")
            self.ia_1.configure(state="normal")
            self.ia_2.configure(state="normal")
            self.ia_3.configure(state="normal")


    def numberPlayer(self):
        self.nbr_player = IntVar()
        self.nbr_player2 = IntVar()
        self.nbr_player3 = IntVar()
        self.nbr_player4 = IntVar()
        self.p1 = Checkbutton(self.window, text="1", bg="#0D2338", fg="#FFF", variable=self.nbr_player, cursor="hand2", command=self.update_ia_state)
        self.p1.place(x=290, y=520)
        self.p2 = Checkbutton(self.window, text="2", bg="#0D2338", fg="#FFF", variable=self.nbr_player2, cursor="hand2", command=self.update_ia_state)
        self.p2.place(x=320, y=520)
        self.p3 = Checkbutton(self.window, text="3", bg="#0D2338", fg="#FFF", variable=self.nbr_player3, cursor="hand2", command=self.update_ia_state)
        self.p3.place(x=350, y=520)
        self.p4 = Checkbutton(self.window, text="4", bg="#0D2338", fg="#FFF", variable=self.nbr_player4, cursor="hand2", command=self.update_ia_state)
        self.p4.place(x=380, y=520)
        
    def get_selected_player(self):
        if self.nbr_player.get() == 1:
            return 1
        elif self.nbr_player2.get() == 1:
            return 2
        elif self.nbr_player3.get() == 1:
            return 3
        elif self.nbr_player4.get() == 1:
            return 4
    
    # Nombres de barrieres par joueur
    def validate_integer(value_if_allowed):
        if value_if_allowed == "":
            return True
        try:
            int(value_if_allowed)
            return True
        except ValueError:
            return False
        
    def numberFence(self):
        self.entry_grid_size = Entry(self.window, width=10)
        self.entry_grid_size.place(x=400, y=570)
        
        self.entry_nbr_fence = Entry(self.window, width=10)
        self.entry_nbr_fence.place(x=655, y=570)
        
    def get_grid_size(self):
        return int(self.entry_grid_size.get())

    def get_nbr_fence(self):
        return int(self.entry_nbr_fence.get())

    def buttonStart(self):
        def start_game():
            grid_size = self.get_grid_size()
            nbr_fences = self.get_nbr_fence()
            nb_ia = self.get_selected_ia()
            nb_player = self.get_selected_player() + self.get_selected_ia()
            self.window.destroy()
            if not (nbr_fences % 4 == 0 and 4 <= nbr_fences <= 40):
                nbr_fences = 20
            if grid_size not in (5, 7, 9, 11):
                grid_size = 9
            if grid_size == 5 and nbr_fences > 20:
                nbr_fences = 20
            restartGame(grid_size, nb_player, nb_ia, nbr_fences)

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
        if platform.system() == "Windows":
            self.window.destroy()
        else:
            self.window.quit()
        joinSession(ip, port)
        
    def startGame(self):
        port = int(self.entry_port.get())
        nbr_player = int(self.nbr_player_network.get())
        if platform.system() == "Windows":
            self.window.destroy()
        else:
            self.window.quit()
        startSession(port, nbr_player)

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


