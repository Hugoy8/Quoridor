from tkinter import *
from PIL import Image, ImageTk

class QuoridorLauncher:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("1400x700")
        self.window.title("Quoridor")
        self.window.maxsize(1400, 700)
        self.window.minsize(1400, 700)
        self.window.iconbitmap('./assets/logo.ico')
        self.statut = 0
        self.background()
        self.choiceMapButton()
        self.numberIA()
        self.difficultyIA()
        self.buttonStart()
        self.menuLauncher()

    def background(self):
        # Image de fond
        self.bg_image = Image.open(f"./assets/launcher{self.statut}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth()-300, self.window.winfo_screenheight()-200))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def toggle_checkbox_map(self):
        # Désactive les autres cases à cocher
        if self.map.get() == 1:
            self.theme_button_space.configure(state="disabled")
            self.theme_button_forest.configure(state="disabled")
        elif self.map2.get() == 1:
            self.theme_button_evil.configure(state="disabled")
            self.theme_button_forest.configure(state="disabled")
        elif self.map3.get() == 1:
            self.theme_button_evil.configure(state="disabled")
            self.theme_button_space.configure(state="disabled")
        # Réactive toutes les cases à cocher si aucune n'est cochée
        else:
            self.theme_button_evil.configure(state="normal")
            self.theme_button_space.configure(state="normal")
            self.theme_button_forest.configure(state="normal")
            
    def choiceMapButton(self):
        # Boutons de thème
        self.theme_buttons_frame = Frame(self.window, bg="#0D2338")
        self.theme_buttons_frame.place(x=273, y=520)
        self.map = IntVar()
        self.map2 = IntVar()
        self.map3 = IntVar()
        self.theme_button_evil = Checkbutton(self.theme_buttons_frame, text="Evil", bg="#0D2338", fg="#FFF", variable=self.map, cursor="hand2", command=self.toggle_checkbox_map)
        self.theme_button_evil.pack(side="left")

        self.theme_button_space = Checkbutton(self.theme_buttons_frame, text="Space", bg="#0D2338", fg="#FFF", variable=self.map2, cursor="hand2", command=self.toggle_checkbox_map)
        self.theme_button_space.pack(side="left")

        self.theme_button_forest = Checkbutton(self.theme_buttons_frame, text="Forest", bg="#0D2338", fg="#FFF", variable=self.map3, cursor="hand2", command=self.toggle_checkbox_map)
        self.theme_button_forest.pack(side="left")

        # Nombre d'IA
    def toggle_checkbox_ia(self):
        if self.nbr_ia.get() == 1:
            self.ia_3.configure(state="disabled")
        elif self.nbr_ia_2.get() == 1:
            self.ia_1.configure(state="disabled")
        else:
            self.ia_1.configure(state="normal")
            self.ia_3.configure(state="normal")
            
    def numberIA(self):
        # Boutons de nombre d'IA
        self.nbr_ia = IntVar()
        self.nbr_ia_2 = IntVar()
        self.ia_1 = Checkbutton(self.window, text="1", bg="#0D2338", fg="#FFF", variable=self.nbr_ia, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_1.place(x=470, y=520)
        self.ia_3 = Checkbutton(self.window, text="3", bg="#0D2338", fg="#FFF", variable=self.nbr_ia_2, cursor="hand2", command=self.toggle_checkbox_ia)
        self.ia_3.place(x=520, y=520)

    # Difficulté d'IA...
    def toggle_checkbox_difficulty_ia(self):
        # Désactive les autres cases à cocher
        if self.level1.get() == 1:
            self.difficulty2.configure(state="disabled")
            self.difficulty3.configure(state="disabled")
            self.difficulty4.configure(state="disabled")
        elif self.level2.get() == 1:
            self.difficulty1.configure(state="disabled")
            self.difficulty3.configure(state="disabled")
            self.difficulty4.configure(state="disabled")
        elif self.level3.get() == 1:
            self.difficulty2.configure(state="disabled")
            self.difficulty1.configure(state="disabled")
            self.difficulty4.configure(state="disabled")
        elif self.level4.get() == 1:
            self.difficulty2.configure(state="disabled")
            self.difficulty3.configure(state="disabled")
            self.difficulty1.configure(state="disabled")
        # Réactive toutes les cases à cocher si aucune n'est cochée
        else:
            self.difficulty1.configure(state="normal")
            self.difficulty2.configure(state="normal")
            self.difficulty3.configure(state="normal")
            self.difficulty4.configure(state="normal")
        
    def difficultyIA(self):
        # Button de difficulté d'IA
        self.level1 = IntVar()
        self.level2 = IntVar()
        self.level3 = IntVar()
        self.level4 = IntVar()
        self.difficulty1 = Checkbutton(self.window, text="Niveau 1", bg="#0D2338", fg="#FFF", variable=self.level1, cursor="hand2", command=self.toggle_checkbox_difficulty_ia)
        self.difficulty1.place(x=660, y=510)

        self.difficulty2 = Checkbutton(self.window, text="Niveau 2", bg="#0D2338", fg="#FFF", variable=self.level2, cursor="hand2", command=self.toggle_checkbox_difficulty_ia)
        self.difficulty2.place(x=660, y=530)

        self.difficulty3 = Checkbutton(self.window, text="Niveau 3", bg="#0D2338", fg="#FFF", variable=self.level3, cursor="hand2", command=self.toggle_checkbox_difficulty_ia)
        self.difficulty3.place(x=660, y=550)

        self.difficulty4 = Checkbutton(self.window, text="Niveau 4", bg="#0D2338", fg="#FFF", variable=self.level4, cursor="hand2", command=self.toggle_checkbox_difficulty_ia)
        self.difficulty4.place(x=660, y=570)

    def buttonStart(self):
    # Ajout un bouton pour start l'application
        start = Button(self.window, text="START", command=self.window.destroy, bg="#0D2338", fg="#FFF", font=("Arial", 15), width=10, cursor="hand2")
        start.place(x=775, y=550)

    def changeBgSolo(self):
        self.statut = 0
        self.background()
        self.choiceMapButton()
        self.numberIA()
        self.difficultyIA()
        self.buttonStart()
        self.menuLauncher()
        
    def changeBgJoinGame(self):
        self.statut = 1
        self.background()
        self.menuLauncher()
        
    def changeBgCreateGame(self):
        self.statut = 2
        self.background()
        self.menuLauncher()

    def menuLauncher(self):
        # Création de la frame
        # Destruction de la frame existante (s'il y en a une)
        if hasattr(self, 'menu_frame'):
            self.menu_frame.destroy()

        # Création de la frame
        self.menu_frame = Frame(self.window)
        self.menu_frame.pack(side="left")

        # Menu de l'application
        self.solo_mode = Button(self.menu_frame, command=self.changeBgSolo, bg="#0B69A3", fg="#FFF", font=("Arial", 15), width=6, height=2, cursor="hand2")
        self.solo_mode.pack(side="top", padx=43, pady=10)
        self.solo_mode.configure(state="normal", relief="flat", highlightthickness=0)
        
        self.join_game = Button(self.menu_frame, command=self.changeBgJoinGame, bg="#0B69A3", fg="#FFF", font=("Arial", 15), width=6, height=2, cursor="hand2")
        self.join_game.pack(side="top", padx=43, pady=10)
        self.join_game.configure(state="normal", relief="flat", highlightthickness=0)

        self.create_game = Button(self.menu_frame, command=self.changeBgCreateGame, bg="#0B69A3", fg="#FFF", font=("Arial", 15), width=6, height=2, cursor="hand2")
        self.create_game.pack(side="top", padx=43, pady=10)
        self.create_game.configure(state="normal", relief="flat", highlightthickness=0)

run_launcher = QuoridorLauncher()
run_launcher.window.mainloop()


