from tkinter import *
from domain.case.case import Case
from domain.fence.fence import Fence
from domain.pillar.pillar import Pillar
from PIL import Image, ImageTk
from pygame import mixer
from infrastructure.database.config import Database
from domain.bot.bot import Bot
import os
from infrastructure.services.services import Board


class InitGame:
    def __init__(self, board : Board) -> None:
        self.board = board
        
        
    def startInit(self, size : int, nb_players : int, nb_IA : int, nb_fence : int, select_map : int, Network : bool, InstanceNetwork : object, typeNetwork : str, playerUser : int, db : Database) -> None:
        if Network == True:
            # Variable bool qui autorise le multijoueur.
            self.board.networkStatus = True
            
            # Variable qui contient l'instance de la class en ligne.
            self.board.InstanceNetwork = InstanceNetwork
            
            # Variable qui enregistre si l'instance est en est une ou un socket.
            self.board.typeNetwork = typeNetwork

            # Variable qui enregistre le numéro de l'utilisateur sur le pc.
            self.board.playerUser = playerUser
            
            # Espace base de données.
            self.board.db = db
            
            from infrastructure.services.getSetInformation import GetSetInformation
            self.board.pseudo = GetSetInformation().get_username("serverPseudo.txt")
            
            self.board.db.insertUsername(self.board.db.ip, self.board.db.port, self.board.pseudo)
        else:
            # Variable bool qui autorise le multijoueur.
            self.board.networkStatus = False
            
        self.board.bot = Bot()
        self.board.bot.setBoard(self.board)
            
        self.board.window = Tk()
        self.board.window.title("Quoridor")
        self.board.window.minsize(self.board.window.winfo_screenwidth(), self.board.window.winfo_screenheight())
        
        if os.name == "nt":
            self.board.window.attributes("-fullscreen", True)
            self.board.window.state('zoomed')

        self.board.window.iconbitmap('./assets/images/logo.ico')
        self.board.window.configure(bg="#F0B169")
        self.board.window_game = True
        self.board.size = size
        self.board.nb_players = nb_players
        self.board.nb_IA = nb_IA
        self.board.nb_fence = nb_fence
        self.board.players = []
        self.board.board = []
        self.board.fence_orientation = "horizontal"    
        self.board.id_possible_move = 0 
        self.board.leavepopup =  None
        self.board.waiting_room1 = None
        self.board.waiting_room2 = None
        self.board.pop_up_no_fence = []
        self.board.popup_settings = None
        
        mixer.init()
        
        # Tailles des éléments
        if size == 5:
            self.board.canvas_game_width = 478
            self.board.canvas_game_height = 478
            self.board.epaisseur_barriere = 25
        elif size == 7 or size == 9 or size == 11:
            self.board.canvas_game_width = 628
            self.board.canvas_game_height = 628
            if size == 7:
                self.board.epaisseur_barriere = 20
            elif size == 9:
                self.board.epaisseur_barriere = 18
            elif size == 11:
                self.board.canvas_game_width = 622
                self.board.canvas_game_height = 622
                self.board.epaisseur_barriere = 15

        self.board.longueur_element = round(((self.board.canvas_game_width - (self.board.epaisseur_barriere * (size - 1))) / size))
        
        width = self.board.longueur_element
        height = self.board.longueur_element
        fence_vertical_width = self.board.epaisseur_barriere
        fence_vertical_height = self.board.longueur_element
        fence_horizontal_width = self.board.longueur_element
        fence_horizontal_height = self.board.epaisseur_barriere
        pillar_taille = self.board.epaisseur_barriere
        self.board.widget_space = (self.board.longueur_element + self.board.epaisseur_barriere) / 2
        
        if select_map == 1:
            self.board.map = "jungle"
        elif select_map == 2:
            self.board.map = "space"
        elif select_map == 3:
            self.board.map = "hell"
        elif select_map == 4:
            self.board.map = "ice"
        elif select_map == 5:
            self.board.map = "electricity"
        elif select_map == 6:
            self.board.map = "sugar"
            
        self.board.volume_map = 0.1
        self.board.volume_victory = 0.3
        self.board.volume_pion = 0.4
        self.board.volume_fence = 1
        self.board.volume_nofence = 1
        self.button_fence = ""
        
        
        self.board.name_bg = size
        if self.board.name_bg == 11 or self.board.name_bg == 9 or self.board.name_bg == 7:
            self.board.name_bg = 7
        
        self.board.bg_image = Image.open(f"./assets/images/{self.board.map}/background{nb_players}{self.board.name_bg}.png")
        self.board.bg_image = self.board.bg_image.resize((self.board.window.winfo_screenwidth(), self.board.window.winfo_screenheight()))
        self.board.bg_photo = ImageTk.PhotoImage(self.board.bg_image)
        self.board.bg_label = Label(self.board.window, image=self.board.bg_photo)
        self.board.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        no_player = Image.open(f"./assets/images/{self.board.map}/case.png")
        no_player = no_player.resize((width, height))
        self.board.no_player = ImageTk.PhotoImage(no_player)
        
        moove_possible = Image.open(f"./assets/images/{self.board.map}/moove_possible.png")
        moove_possible = moove_possible.resize((width, height))
        self.board.moove_possible = ImageTk.PhotoImage(moove_possible)
        
        image_player_1 = Image.open(f"./assets/images/{self.board.map}/player_1.png")
        image_player_1 = image_player_1.resize((width, height))
        self.board.image_player_1 = ImageTk.PhotoImage(image_player_1)
        
        image_player_2 = Image.open(f"./assets/images/{self.board.map}/player_2.png")
        image_player_2 = image_player_2.resize((width, height))
        self.board.image_player_2 = ImageTk.PhotoImage(image_player_2)
        
        image_player_3 = Image.open(f"./assets/images/{self.board.map}/player_3.png")
        image_player_3 = image_player_3.resize((width, height))
        self.board.image_player_3 = ImageTk.PhotoImage(image_player_3)
        
        image_player_4 = Image.open(f"./assets/images/{self.board.map}/player_4.png")
        image_player_4 = image_player_4.resize((width, height))
        self.board.image_player_4 = ImageTk.PhotoImage(image_player_4)
        
        #IMAGES DES FENCES
        fence_height = Image.open(f"./assets/images/{self.board.map}/fence_height.png")
        fence_height = fence_height.resize((fence_vertical_width, fence_vertical_height))
        self.board.fence_height = ImageTk.PhotoImage(fence_height)
        
        fence_height_vide = Image.open(f"./assets/images/{self.board.map}/fence_height_vide.png")
        fence_height_vide = fence_height_vide.resize((fence_vertical_width, fence_vertical_height))
        self.board.fence_height_vide = ImageTk.PhotoImage(fence_height_vide)
        
        fence_width = Image.open(f"./assets/images/{self.board.map}/fence_width.png")
        fence_width = fence_width.resize((fence_horizontal_width, fence_horizontal_height))
        self.board.fence_width = ImageTk.PhotoImage(fence_width)
        
        fence_width_vide = Image.open(f"./assets/images/{self.board.map}/fence_width_vide.png")
        fence_width_vide = fence_width_vide.resize((fence_horizontal_width, fence_horizontal_height))
        self.board.fence_width_vide = ImageTk.PhotoImage(fence_width_vide)
        
        # IMAGE DES PILLIERS
        pillar = Image.open(f"./assets/images/{self.board.map}/pillier.png")
        pillar = pillar.resize((pillar_taille, pillar_taille))
        self.board.pillar = ImageTk.PhotoImage(pillar)
        
        pillar_vide = Image.open(f"./assets/images/{self.board.map}/pillier_vide.png")
        pillar_vide = pillar_vide.resize((pillar_taille, pillar_taille))
        self.board.pillar_vide = ImageTk.PhotoImage(pillar_vide)
        
        # IMAGE DES OBJETS HOVERED
        fence_width_hover = Image.open(f"./assets/images/{self.board.map}/fence_width_hover.png")
        fence_width_hover = fence_width_hover.resize((fence_horizontal_width, fence_horizontal_height))
        self.board.fence_width_hover = ImageTk.PhotoImage(fence_width_hover)
        
        fence_height_hover = Image.open(f"./assets/images/{self.board.map}/fence_height_hover.png")
        fence_height_hover = fence_height_hover.resize((fence_vertical_width, fence_vertical_height))
        self.board.fence_height_hover = ImageTk.PhotoImage(fence_height_hover)

        pillar_hover = Image.open(f"./assets/images/{self.board.map}/pillier_hover.png")
        pillar_hover = pillar_hover.resize((pillar_taille, pillar_taille))
        self.board.pillar_hover = ImageTk.PhotoImage(pillar_hover)
        
        # IMAGE CURRENT PLAYER
        current_player1_image = Image.open(f"./assets/images/{self.board.map}/current_player1.png")
        current_player1_image = current_player1_image.resize((40, 43))
        self.board.current_player1_image = ImageTk.PhotoImage(current_player1_image)
        
        current_player2_image = Image.open(f"./assets/images/{self.board.map}/current_player2.png")
        current_player2_image = current_player2_image.resize((40, 43))
        self.board.current_player2_image = ImageTk.PhotoImage(current_player2_image)
        
        current_player3_image = Image.open(f"./assets/images/{self.board.map}/current_player3.png")
        current_player3_image = current_player3_image.resize((40, 43))
        self.board.current_player3_image = ImageTk.PhotoImage(current_player3_image)
        
        current_player4_image = Image.open(f"./assets/images/{self.board.map}/current_player4.png")
        current_player4_image = current_player4_image.resize((40, 43))
        self.board.current_player4_image = ImageTk.PhotoImage(current_player4_image)
        
        leave_game_victory = Image.open(f"./assets/images/{self.board.map}/leave_game_victory.png")
        leave_game_victory = leave_game_victory.resize((157, 42))
        self.board.leave_game_victory = ImageTk.PhotoImage(leave_game_victory)
        
        restart_game_victory = Image.open(f"./assets/images/{self.board.map}/restart_game_victory.png")
        restart_game_victory = restart_game_victory.resize((157, 42))
        self.board.restart_game_victory = ImageTk.PhotoImage(restart_game_victory)
        
        popup_escape_game = Image.open(f"./assets/images/pauseMenu/popup_escape_game.png")
        popup_escape_game = popup_escape_game.resize((662, 670))
        self.board.popup_escape_game = ImageTk.PhotoImage(popup_escape_game)
        
        button_popup_resumegame = Image.open(f"./assets/images/pauseMenu/button_popup_resume_game.png")
        button_popup_resumegame = button_popup_resumegame.resize((155, 40))
        self.board.button_popup_resumegame = ImageTk.PhotoImage(button_popup_resumegame)
        
        button_popup_quitgame = Image.open(f"./assets/images/pauseMenu/button_popup_quitgame.png")
        button_popup_quitgame = button_popup_quitgame.resize((155, 40))
        self.board.button_popup_quitgame = ImageTk.PhotoImage(button_popup_quitgame)
        
        bind_changing = Image.open(f"./assets/images/launcher/bind_changing.png")
        bind_changing = bind_changing.resize((48, 48))
        self.board.bind_changing = ImageTk.PhotoImage(bind_changing)

        bind = Image.open(f"./assets/images/launcher/bind.png")
        bind = bind.resize((48, 48))
        self.board.bind = ImageTk.PhotoImage(bind)
        
        self.board.display_current_player = None
        
        from infrastructure.services.settingsGame import SettingsGame
        self.board.settings = SettingsGame(self.board.window, self.board.popup_escape_game, self.board.button_popup_resumegame, self.board.button_popup_quitgame, self.board.bind, self.board.bind_changing, self.board)
        
        self.board.loadVolumeSettings()
        self.board.window.bind("<KeyPress-Escape>", lambda event: self.board.settings.displayBreakGame(event))

        for i in range(self.board.size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.board.size*2-1):
                    if j%2 == 0 : 
                        tab2.append(Case(0,0,[i,j]))
                        
                    else :
                        tab2.append(Fence(0))
                self.board.board.append(tab2)
            else :
                tab2 = []
                for j in range(self.board.size*2-1):
                    if j%2 == 0 :
                        tab2.append(Fence(0))
                    else :
                        tab2.append(Pillar(0,[i,j]))
                self.board.board.append(tab2)
        