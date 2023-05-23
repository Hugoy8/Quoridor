from tkinter import *
import socket
import pickle
from domain.case.case import Case
from domain.fence.fence import Fence
from domain.pillar.pillar import Pillar
from domain.player.player import Player
import random
from PIL import Image, ImageTk
import time

class Board:
    def __init__(self, size : int, nb_players : int, nb_IA : int, nb_fence : int, select_map : int, Network : bool, InstanceNetwork : object, typeNetwork : str, playerUser : int) -> None:
        if Network == True:
            # Variable bool qui autorise le multijoueur.
            self.networkStatus = True
            
            # Variable qui contient l'instance de la class en ligne.
            self.InstanceNetwork = InstanceNetwork
            
            # Variable qui enregistre si l'instance est en est une ou un socket.
            self.typeNetwork = typeNetwork

            # Variable qui enregistre le numéro de l'utilisateur sur le pc.
            self.playerUser = playerUser
        else:
            # Variable bool qui autorise le multijoueur.
            self.networkStatus = False
            
        self.window = Tk()
        self.window.title("Quoridor")
        self.window.state('zoomed')
        self.window.minsize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.iconbitmap('./assets/logo.ico')
        self.window.configure(bg="#F0B169")
        self.window_game = True
        self.__size = size
        self.__nb_players = nb_players
        self.__nb_IA = nb_IA
        self.__nb_fence = nb_fence
        self.players = []
        self.board = []
        self.fence_orientation = "horizontal"    
        self.id_possible_move = 0 
        self.leavepopup =  None
        self.waiting_room1 = None
        self.waiting_room2 = None
        # CrÃ©ation des images du plateau
        
        # IMAGE DES CASES
        width = 80
        height = 80
        fence_vertical_width = 20
        fence_vertical_height = 80
        fence_horizontal_width = 80
        fence_horizontal_height = 20
        pillar_taille = 20
        self.widget_space = 50
        
        if size == 5:
            self.canvas_game_width = 478
            self.canvas_game_height = 478
        elif size == 7:
            self.canvas_game_width = 678
            self.canvas_game_height = 678
        elif size == 9:
            self.canvas_game_width = 878
            self.canvas_game_height = 878
        elif size == 11:
            self.canvas_game_width = 890
            self.canvas_game_height = 878
            width = 70
            height = 70
            fence_vertical_width = 10
            fence_vertical_height = 73
            fence_horizontal_width = 73
            fence_horizontal_height = 10
            pillar_taille = 11
            self.widget_space = 41
        
        if select_map == 1:
            self.map = "jungle"
        elif select_map == 2:
            self.map = "space"
        elif select_map == 3:
            self.map = "hell"
        
        self.bg_image = Image.open(f"./assets/{self.map}/background.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        no_player = Image.open(f"./assets/{self.map}/case.png")
        no_player = no_player.resize((width, height))
        self.no_player = ImageTk.PhotoImage(no_player)
        
        moove_possible = Image.open(f"./assets/{self.map}/moove_possible.png")
        moove_possible = moove_possible.resize((width, height))
        self.moove_possible = ImageTk.PhotoImage(moove_possible)
        
        image_player_1 = Image.open(f"./assets/{self.map}/player_1.png")
        image_player_1 = image_player_1.resize((width, height))
        self.image_player_1 = ImageTk.PhotoImage(image_player_1)
        
        image_player_2 = Image.open(f"./assets/{self.map}/player_2.png")
        image_player_2 = image_player_2.resize((width, height))
        self.image_player_2 = ImageTk.PhotoImage(image_player_2)
        
        image_player_3 = Image.open(f"./assets/{self.map}/player_3.png")
        image_player_3 = image_player_3.resize((width, height))
        self.image_player_3 = ImageTk.PhotoImage(image_player_3)
        
        image_player_4 = Image.open(f"./assets/{self.map}/player_4.png")
        image_player_4 = image_player_4.resize((width, height))
        self.image_player_4 = ImageTk.PhotoImage(image_player_4)
        
        #IMAGES DES FENCES
        fence_height = Image.open(f"./assets/{self.map}/fence_height.png")
        fence_height = fence_height.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height = ImageTk.PhotoImage(fence_height)
        
        fence_height_vide = Image.open(f"./assets/{self.map}/fence_height_vide.png")
        fence_height_vide = fence_height_vide.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height_vide = ImageTk.PhotoImage(fence_height_vide)
        
        fence_width = Image.open(f"./assets/{self.map}/fence_width.png")
        fence_width = fence_width.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width = ImageTk.PhotoImage(fence_width)
        
        fence_width_vide = Image.open(f"./assets/{self.map}/fence_width_vide.png")
        fence_width_vide = fence_width_vide.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width_vide = ImageTk.PhotoImage(fence_width_vide)
        
        # IMAGE DES PILLIERS
        pillar = Image.open(f"./assets/{self.map}/pillier.png")
        pillar = pillar.resize((pillar_taille, pillar_taille))
        self.pillar = ImageTk.PhotoImage(pillar)
        
        pillar_vide = Image.open(f"./assets/{self.map}/pillier_vide.png")
        pillar_vide = pillar_vide.resize((pillar_taille, pillar_taille))
        self.pillar_vide = ImageTk.PhotoImage(pillar_vide)
        
        # IMAGE DES OBJETS HOVERED
        fence_width_hover = Image.open(f"./assets/{self.map}/fence_width_hover.png")
        fence_width_hover = fence_width_hover.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width_hover = ImageTk.PhotoImage(fence_width_hover)
        
        fence_height_hover = Image.open(f"./assets/{self.map}/fence_height_hover.png")
        fence_height_hover = fence_height_hover.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height_hover = ImageTk.PhotoImage(fence_height_hover)

        pillar_hover = Image.open(f"./assets/{self.map}/pillier_hover.png")
        pillar_hover = pillar_hover.resize((pillar_taille, pillar_taille))
        self.pillar_hover = ImageTk.PhotoImage(pillar_hover)
        
        # Image de victoire
        img_win_p1 = Image.open("./assets/jungle/victory_p1.png")
        img_win_p1 = img_win_p1.resize((600, 500))
        self.img_win_p1 = ImageTk.PhotoImage(img_win_p1)
        
        img_win_p2 = Image.open("./assets/jungle/victory_p2.png")
        img_win_p2 = img_win_p2.resize((600, 500))
        self.img_win_p2 = ImageTk.PhotoImage(img_win_p2)
        
        img_win_p3 = Image.open("./assets/jungle/victory_p3.png")
        img_win_p3 = img_win_p3.resize((600, 500))
        self.img_win_p3 = ImageTk.PhotoImage(img_win_p3)       
        
        img_win_p4 = Image.open("./assets/jungle/victory_p4.png")
        img_win_p4 = img_win_p4.resize((600, 500))
        self.img_win_p4 = ImageTk.PhotoImage(img_win_p4) 
        

        for i in range(self.__size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 : 
                        tab2.append(Case(0,0))
                        
                    else :
                        tab2.append(Fence(0))
                self.board.append(tab2)
            else :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 :
                        tab2.append(Fence(0))
                    else :
                        tab2.append(Pillar(0))
                self.board.append(tab2)
        
    
    def caseClicked(self, event : int) -> None:
        item_id = event.widget.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        x = int(tags[0])
        y = int(tags[1])
        
        if self.networkStatus == True:
            if self.typeNetwork == "instance":
                self.InstanceNetwork.SendBoard(x, y, 0, self.fence_orientation)
            elif self.typeNetwork == "socket":
                SendBoardClient(x, y, 0, self.InstanceNetwork, self.fence_orientation)

        self.move(x,y)
        if self.victory() == True :
            self.displayBoard(False)
            self.canvas.unbind_all("<Button-1>")
            for child in self.window.winfo_children():
                if child.winfo_exists():
                    child.destroy()
            self.windowVictory()
        else:
            self.resetPossibleCaseMovement() 
            self.refreshCurrentPlayer()

            if self.networkStatus == True:
                if self.current_player.get_player() == self.playerUser:
                    self.refreshPossibleCaseMovementForCurrentPlayer()
                else:
                    pass
            else:
                self.refreshPossibleCaseMovementForCurrentPlayer()

            self.displayBoard(False)
        while self.current_player.get_IALevel() != 0 :
            if self.current_player.get_IALevel() == 1 :
                list = [0,1]
                action = random.choice(list)
                if action == 1  and self.playerHasFence() == True and self.allPossibleBuildFence() !=[]:
                    can_build = False
                    while can_build == False :
                        if self.current_player.get_IALevel() == 1:
                            build = random.choice(self.allPossibleBuildFence())
                            x_co_fence = build[0]
                            y_co_fence = build[1]
                            orientation = build[2]
                            if orientation == 0 :
                                self.fence_orientation = "vertical"
                            else :
                                self.fence_orientation = "horizontal"
                            self.buildFence(x_co_fence,y_co_fence)
                            if self.fenceNotCloseAccesGoal()==False :
                                self.deBuildFence(x_co_fence,y_co_fence)
                                self.displayBoard(False)
                            else : 
                                can_build = True
                else :
                    if self.current_player.get_IALevel() == 1 :
                        movement = random.choice(self.allPossibleMoveForPlayer())
                        self.move(movement[0],movement[1])
            if self.victory() == True :
                self.displayBoard(False)
                self.canvas.unbind_all("<Button-1>")
                for child in self.window.winfo_children():
                    if child.winfo_exists():
                        child.destroy()
                self.windowVictory()
                break
            else:
                self.resetPossibleCaseMovement() 
                self.refreshCurrentPlayer()
                self.refreshPossibleCaseMovementForCurrentPlayer()
                self.displayBoard(False)                        
        
        
    def windowVictory(self) -> None:
        self.bg_image = Image.open(f"./assets/{self.map}/background.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.displayBoard(False)
        
        # Affichage de l'image de fond
        victory_canvas = Canvas(self.window, width=600, height=500, bd=0, highlightthickness=0)
        if self.current_player.get_player() == 1:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p1)
        elif self.current_player.get_player() == 2:
            victory_canvas.create_image(0, 20, anchor="nw", image=self.img_win_p2)
        elif self.current_player.get_player() == 3:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p3)
        elif self.current_player.get_player() == 4:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p4)
        victory_canvas.place(relx=0.5, rely=0.5, anchor="center")

        # Ajout des boutons
        button_frame = Frame(self.window, bg="blue")
        button_frame.pack(side="bottom", pady=100)

        quit_button = Button(button_frame, text="Quitter", font=("Arial", 14), fg="white", bg="#DB0000", bd=2, highlightthickness=0, command=self.window.destroy)
        quit_button.pack(side="left", padx=110)
        def rejouer():
            self.window.destroy()
            from domain.launcher.launcher import QuoridorLauncher
            QuoridorLauncher()
        replay_button = Button(button_frame, text="Rejouer", font=("Arial", 14), fg="white", bg="#78B000", bd=2, highlightthickness=0, command=rejouer)
        replay_button.pack(side="left", padx=100)

    def displayBoard(self, leave: bool) -> None: 
        player_colors = {
            1: "red",
            2: "green",
            3: "blue",
            4: "#C137BC"
        }
        self.canvas = Canvas(self.window, width=self.canvas_game_width, height=self.canvas_game_height, bg="#F0B169", bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Widget d'informations
        current_player_number = self.current_player.get_player()
        current_player_color = player_colors.get(current_player_number, "gray")
        if self.map == "jungle":
            color_frame_info = "#FFC593"
            color_font = "black"
        elif self.map == "space":
            color_frame_info = "#371761"
            color_font = "white"
        elif self.map == "hell":
            color_frame_info = "#AF3500"
            color_font = "black"
        info_frame = Frame(self.window, bg=color_frame_info, bd=30)
        info_frame.place(x=self.window.winfo_screenheight()-self.window.winfo_screenheight()+50, y=self.window.winfo_screenheight()/2, anchor="sw")

        current_player_number = self.current_player.get_player()
        current_player_color = player_colors.get(current_player_number, "gray")
        Label(info_frame, text="Tour : ", font=("Arial", 14), bg=color_frame_info, fg=color_font).grid(row=0, column=0, padx=(0, 0))
        Label(info_frame, text="Joueur " + str(current_player_number), font=("Arial", 14), foreground=current_player_color, bg=color_frame_info).grid(row=0, column=1, padx=(0, 10))

        barrier_icon = PhotoImage(file=f"./assets/{self.map}/fence_nbr.png") 
        barrier_icon = barrier_icon.subsample(3, 3)  

        for index, nbr_fence_player in enumerate(self.players):
            a = nbr_fence_player.get_player()
            b = nbr_fence_player.get_nb_fence()
            if b == 0:
                b = "0"
            player_color = player_colors.get(a, "red")
            Label(info_frame, text=f"Joueur {a} : {b}", font=("Arial", 14), foreground=player_color, bg=color_frame_info).grid(row=index + 2, column=0, padx=(0, 5), pady=(5, 0))

            # Affichez l'icÃ´ne de barriÃ¨re Ã  cÃ´tÃ© du nombre de barriÃ¨res
            barrier_label = Label(info_frame, image=barrier_icon, bg=color_frame_info)
            barrier_label.image = barrier_icon 
            barrier_label.grid(row=index + 2, column=1, padx=(0, 5), pady=(5, 0))
        
        if leave == True:
            #PopUp de leave d'un joueur
            leavepopup = Image.open(f"./assets/leavepopup.png")
            leavepopup = leavepopup.resize((self.window.winfo_screenwidth() // 2, 100))
            self.leavepopup = ImageTk.PhotoImage(leavepopup)
            
                # Créer un label pour l'image et l'ajouter à la fenêtre avec la méthode grid()
            label = Label(self.window, image=self.leavepopup)
            label.place(relx=0.5, rely=0.05, anchor='center')
            
        
        self.window.bind("<space>", self.changeFenceOrientation)
        tab =[]
        self.pillar_rects = []
        for i in range(self.__size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 :
                        case = self.board[i][j]
                        tab2.append(case.displayPlayer())
                        if case.displayPlayer() == "P0" :
                            if case.get_possibleMove() != 0 and self.victory() == False:
                                position = self.current_player.displayPlace()
                                self.move_case = self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.moove_possible, anchor="nw", tags=case.get_possibleMove())
                                self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                            else :
                                self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.no_player, anchor="nw")
                        elif case.displayPlayer() == "P1" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_1, anchor="nw")
                        elif case.displayPlayer() == "P2" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_2, anchor="nw")
                        elif case.displayPlayer() == "P3" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_3, anchor="nw")
                        elif case.displayPlayer() == "P4" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_4, anchor="nw")
                    else :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*self.widget_space+30, i*self.widget_space, image=self.fence_height, anchor="nw", tags=str(i) + "_" + str(j))
                        else :
                            self.canvas.create_image(j*self.widget_space+30, i*self.widget_space, image=self.fence_height_vide, anchor="nw", tags=str(i) + "_" + str(j))

                tab.append(tab2)
            else :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*self.widget_space ,i*self.widget_space+30, image=self.fence_width, anchor="nw", tags=str(i) + "_" + str(j))
                        else:
                            self.canvas.create_image(j*self.widget_space ,i*self.widget_space+30, image=self.fence_width_vide, anchor="nw", tags=str(i) + "_" + str(j))
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        if pillar.displayPillar() == "B1" :
                            self.pillar_rects.append(self.canvas.create_image(j*self.widget_space+30, i*self.widget_space+30, image=self.pillar, anchor="nw", tags=[i,j]))
                        else :
                            self.pillar_rects.append(self.canvas.create_image(j*self.widget_space+30, i*self.widget_space+30, image=self.pillar_vide, anchor="nw", tags=[i,j]))
                        
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Button-1>", self.buildFenceOnClick)
                            else:
                                pass
                        else:
                            self.canvas.tag_bind(self.pillar_rects[-1], "<Button-1>", self.buildFenceOnClick)
                            
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                if self.victory() == False:
                                    self.canvas.tag_bind(self.pillar_rects[-1], "<Enter>", self.on_hover)
                                    self.canvas.tag_bind(self.pillar_rects[-1], "<Leave>", self.on_leave)
                            else:
                                pass
                        else:
                            if self.victory() == False:
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Enter>", self.on_hover)
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Leave>", self.on_leave)
                        
                            
                tab.append(tab2)
            
    def buildFenceOnClick(self,event):
        if self.playerHasFence() == False :
            print(" ")
        else :
            item_id = event.widget.find_withtag("current")[0], 
            tags = self.canvas.gettags(item_id)
            if len(tags) >= 2 :
                x = int(tags[0])
                y = int(tags[1])
                if self.isPossibleFence(x,y) == True :
                    self.buildFence(x,y)
                    if self.fenceNotCloseAccesGoal()==False :
                        self.deBuildFence(x,y)
                        self.displayBoard(False)
                    else :
                        if self.networkStatus == True:
                            if self.typeNetwork == "instance":
                                self.InstanceNetwork.SendBoard(x, y, 1, self.fence_orientation)
                            elif self.typeNetwork == "socket":
                                SendBoardClient(x, y, 1, self.InstanceNetwork, self.fence_orientation)
                        
                        self.resetPossibleCaseMovement() 
                        self.refreshCurrentPlayer()
                        
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                self.refreshPossibleCaseMovementForCurrentPlayer()
                            else:
                                pass
                        else:
                            self.refreshPossibleCaseMovementForCurrentPlayer()
                            
                        self.displayBoard(False)
                        while self.current_player.get_IALevel() != 0 :
                            if self.current_player.get_IALevel() == 1 :
                                list = [0,1]
                                action = random.choice(list)
                                if action == 1  and self.playerHasFence() == True and self.allPossibleBuildFence() !=[]:
                                    can_build = False
                                    while can_build == False :
                                        if self.current_player.get_IALevel() == 1:
                                            build = random.choice(self.allPossibleBuildFence())
                                            x_co_fence = build[0]
                                            y_co_fence = build[1]
                                            orientation = build[2]
                                            if orientation == 0 :
                                                self.fence_orientation = "vertical"
                                            else :
                                                self.fence_orientation = "horizontal"
                                            self.buildFence(x_co_fence,y_co_fence)
                                            if self.fenceNotCloseAccesGoal()==False :
                                                self.deBuildFence(x_co_fence,y_co_fence)
                                                self.displayBoard(False)
                                            else : 
                                                can_build = True
                                else :
                                    if self.current_player.get_IALevel() == 1 :
                                        movement = random.choice(self.allPossibleMoveForPlayer())
                                        self.move(movement[0],movement[1])
                            if self.victory() == True :
                                self.displayBoard(False)
                                self.canvas.unbind_all("<Button-1>")
                                # for child in self.window.winfo_children():
                                #     if child.winfo_exists():
                                #         child.destroy()
                                self.windowVictory()
                                break
                            else:
                                self.resetPossibleCaseMovement() 
                                self.refreshCurrentPlayer()
                                self.refreshPossibleCaseMovementForCurrentPlayer()
                                self.displayBoard(False)         
                        
    def on_hover(self, event):
        if self.playerHasFence() == True :
            item_id = event.widget.find_withtag("current")[0]
            tags = self.canvas.gettags(item_id)
            if len(tags) >= 2 and item_id in self.pillar_rects:
                x = int(tags[0])
                y = int(tags[1])
                if self.isPossibleFence(x,y) == True :
                    self.canvas.itemconfig(item_id, image=self.pillar_hover)
                    if self.fence_orientation == "vertical":
                        fence = self.canvas.find_withtag(str(x-1) + "_" + str(y))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_height_hover)
                        fence = self.canvas.find_withtag(str(x+1) + "_" + str(y))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_height_hover)
                    else :
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y-1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_hover)
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y+1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_hover)
    
    def on_leave(self, event):
        item_id = event.widget.find_withtag("current")[0]
        tags = self.canvas.gettags(item_id)
        if item_id in self.pillar_rects:
            x = int(tags[0])
            y = int(tags[1])
            if self.isPossibleFence(x,y) == True :
                pillar = self.board[x][y]
                if pillar.get_build() != 1:
                    self.canvas.itemconfig(item_id, image=self.pillar_vide)
                if self.fence_orientation == "vertical":
                    fence = self.canvas.find_withtag(str(x-1) + "_" + str(y))
                    item_id = fence[0]
                    self.canvas.itemconfig(item_id, image=self.fence_height_vide)
                    fence = self.canvas.find_withtag(str(x+1) + "_" + str(y))
                    item_id = fence[0]
                    self.canvas.itemconfig(item_id, image=self.fence_height_vide)
                else :
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y-1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_vide)
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y+1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_vide)


    def decideIALevel(self, player : int) -> bool:
        if player > self.__nb_players - self.__nb_IA:
            return 1
        return False


    def start(self) -> None:
        nb_fence_each_player = int(self.__nb_fence / self.__nb_players)
        case = self.board[0][self.__size-1]
        case.set_player(1)
        self.players.append(Player(0,self.__size-1,1,nb_fence_each_player,self.decideIALevel(1)))
        case = self.board[-1][self.__size-1]
        case.set_player(2)
        self.players.append(Player((self.__size-1)*2,self.__size-1,2,nb_fence_each_player,self.decideIALevel(2)))
        if self.__nb_players == 4 :
            case = self.board[self.__size-1][0]
            case.set_player(3)
            self.players.append(Player(self.__size-1,0,3,nb_fence_each_player,self.decideIALevel(3)))
            case = self.board[self.__size-1][-1]
            case.set_player(4)
            self.players.append(Player(self.__size-1,(self.__size-1)*2,4,nb_fence_each_player,self.decideIALevel(4)))
        self.current_player = self.players[0]
        
    
    
    def refreshCurrentPlayer(self) -> None:
        if self.current_player.get_player() == self.__nb_players :
            self.current_player = self.players[0]
        else :
            self.current_player = self.players[self.current_player.get_player()]
    
            
    def move(self, x : int, y : int) -> None:
        position = self.current_player.displayPlace()
        case = self.board[position[0]][position[1]]
        case.set_player(0)
        case = self.board[position[0]+x][position[1]+y]
        case.set_player(self.current_player.get_player())
        self.current_player.move(position[0]+x,position[1]+y)
                    
    
    def changeFenceOrientation(self, event=None) -> None:
        self.displayBoard(False)
        if self.fence_orientation == "vertical":
            self.fence_orientation = "horizontal"
        else :
            self.fence_orientation = "vertical"
        
    
    
    def playerHasFence(self) -> bool:
        nb_fence_current_player  = self.current_player.get_nb_fence()
        if nb_fence_current_player <= 0 :
            return False
        return True
    
    def isPossibleFence(self, x : int, y : int) -> bool:
        if self.fence_orientation == "vertical":
            fence = self.board[x-1][y]
            if fence.get_build() == 1:
                return False
            fence = self.board[x+1][y]
            if fence.get_build() == 1:
                return False
        else :
            fence = self.board[x][y-1]
            if fence.get_build() == 1:
                return False
            fence = self.board[x][y+1]
            if fence.get_build() == 1:
                return False
        return True
    
    
    def buildFence(self, x : int, y : int) -> None:
        pillar = self.board[x][y]
        pillar.buildPillar()
        if self.fence_orientation == "vertical":
            fence = self.board[x-1][y]
            fence.buildFence()
            fence = self.board[x+1][y]
            fence.buildFence()
        else:
            fence = self.board[x][y-1]
            fence.buildFence()
            fence = self.board[x][y+1]
            fence.buildFence()
        nb_fence_current_player  = self.current_player.get_nb_fence()
        self.current_player.set_fence(nb_fence_current_player-1)
        self.displayBoard(False)
        
        
    def buildFenceNetwork(self, x : int, y : int, orientation : int) -> None:
        pillar = self.board[x][y]
        pillar.buildPillar()
        if orientation == 0:
            fence = self.board[x-1][y]
            fence.buildFence()
            fence = self.board[x+1][y]
            fence.buildFence()
        else:
            fence = self.board[x][y-1]
            fence.buildFence()
            fence = self.board[x][y+1]
            fence.buildFence()
        nb_fence_current_player  = self.current_player.get_nb_fence()
        self.current_player.set_fence(nb_fence_current_player-1)
        self.displayBoard(False)
        
        
    def deBuildFence(self, x : int, y : int) -> None:
        pillar = self.board[x][y]
        pillar.set_build(0)
        if self.fence_orientation == "vertical":
            fence = self.board[x-1][y]
            fence.set_build(0)
            fence = self.board[x+1][y]
            fence.set_build(0)
        else :
            fence = self.board[x][y-1]
            fence.set_build(0)
            fence = self.board[x][y+1]
            fence.set_build(0)
        nb_fence_current_player  = self.current_player.get_nb_fence()
        self.current_player.set_fence(nb_fence_current_player+1)
    
    def victory(self) -> bool:
        position = self.current_player.displayPlace()
        if self.current_player.get_player() == 1 :
            if position[0] == (self.__size-1)*2 :
                return True
        elif self.current_player.get_player() == 2 : 
            if position[0] == 0 :
                return True
        elif self.current_player.get_player() == 3 : 
            if position[1] == (self.__size-1)*2 :
                return True
        elif self.current_player.get_player() == 4 : 
            if position[1] == 0 :
                return True
        return False
        
    
    def alreadyChecked(self, x : int, y : int) -> bool:
        for i in self.list_case_check:
                    if i[0] == x and i[1] == y:
                        return True
        return False
    
    def thereIsFence(self, x : int, y : int) -> bool:
        fence = self.board[x][y]
        if fence.get_build() == 1:
            return True
        return False
        
    def isPossibleWay(self, x : int, y : int, player : str) -> bool:
        self.list_case_check.append([x, y])
        if x == (self.__size-1)*2 and player == 1:
            return True
        elif x == 0 and player == 2:
            return True
        elif y == (self.__size-1)*2 and player == 3:
            return True
        elif y == 0 and player == 4:
            return True
        if x == 0:
            if y == 0: #coin haut gauche
                if self.alreadyChecked(0, 2) == False and self.thereIsFence(0, 1) == False:
                    if self.isPossibleWay(0, 2, player) == True :
                        return True
                        
                if self.alreadyChecked(2, 0) == False and self.thereIsFence(1, 0) == False:
                    if self.isPossibleWay(2, 0, player) == True :
                        return True
                        
            elif y==(self.__size-1)*2: #coin haut droite
                if self.alreadyChecked(0, y-2) == False and self.thereIsFence(0, y-1) == False:
                    if self.isPossibleWay(0, y-2, player) == True :
                        return True
                        
                if self.alreadyChecked(2, y) == False and self.thereIsFence(1, y) == False:
                    if self.isPossibleWay(2, y, player) == True :
                        return True
                        
            else: #ligne haut
                if self.alreadyChecked(x, y-2) == False and self.thereIsFence(x, y-1) == False:
                    if self.isPossibleWay(x, y-2, player) == True :
                        return True 
                        
                if self.alreadyChecked(x, y+2) == False and self.thereIsFence(x, y+1) == False:
                    if self.isPossibleWay(x, y+2, player) == True :
                        return True 
                        
                if self.alreadyChecked(x+2, y) == False and self.thereIsFence(x+1, y) == False:
                    if self.isPossibleWay(x+2, y, player) == True :
                        return True 
                        
        elif y==0: 
            if x == (self.__size-1)*2: #coin bas gauche
                if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                    if self.isPossibleWay(x-2, y, player) == True :
                        return True
                        
                if self.alreadyChecked(x, y+2) == False and self.thereIsFence(x,y+1) == False:
                    if self.isPossibleWay(x, y+2, player) == True :
                        return True 
                        
            else : #colonne gauche
                if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                    if self.isPossibleWay(x-2, y, player) == True :
                        return True 
                        
                if self.alreadyChecked(x+2, y) == False and self.thereIsFence(x+1, y) == False:
                    if self.isPossibleWay(x+2, y, player) == True :
                        return True 
                        
                if self.alreadyChecked(x, y+2) == False and self.thereIsFence(x, y+1) == False:
                    if self.isPossibleWay(x, y+2, player) == True :
                        return True 
                        
        elif y==(self.__size-1)*2: 
            if x == (self.__size-1)*2: #coin bas droite
                if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                    if self.isPossibleWay(x-2, y, player) == True :
                        return True 
                        
                if self.alreadyChecked(x, y-2) == False and self.thereIsFence(x, y-1) == False:
                    if self.isPossibleWay(x, y-2, player) == True :
                        return True 
                        
            else: #colonne droite
                if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                    if self.isPossibleWay(x-2, y, player) == True :
                        return True 
                        
                if self.alreadyChecked(x+2, y) == False and self.thereIsFence(x+1, y) == False:
                    if self.isPossibleWay(x+2, y, player) == True :
                        return True 
                        
                if self.alreadyChecked(x, y-2) == False  and self.thereIsFence(x, y-1) == False:
                    if self.isPossibleWay(x, y-2, player) == True :
                        return True 
                    
        elif x == (self.__size-1)*2: #ligne bas 
            if self.alreadyChecked(x, y-2) == False and self.thereIsFence(x, y-1) == False:
                if self.isPossibleWay(x, y-2, player) == True :
                    return True 
            if self.alreadyChecked(x, y+2) == False and self.thereIsFence(x, y+1) == False:
                if self.isPossibleWay(x, y+2, player) == True :
                    return True 
                    
            if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                if self.isPossibleWay(x-2, y, player) == True :
                    return True
                
        else: #middle
            if self.alreadyChecked(x-2, y) == False and self.thereIsFence(x-1, y) == False:
                if self.isPossibleWay(x-2, y, player) == True :
                    return True 
                        
            if self.alreadyChecked(x+2, y) == False and self.thereIsFence(x+1, y) == False:
                if self.isPossibleWay(x+2, y, player) == True :
                    return True 
                        
            if self.alreadyChecked(x, y-2) == False and self.thereIsFence(x, y-1) == False:
                if self.isPossibleWay(x, y-2, player) == True :
                    return True 
                        
            if self.alreadyChecked(x, y+2) == False and self.thereIsFence(x, y+1) == False:
                if self.isPossibleWay(x, y+2, player) == True :
                    return True 
                        
        
    
    def seachPossibleWayForPlayer(self, player : str) -> bool:
        self.list_case_check = []
        position = self.players[player-1].displayPlace()
        if self.isPossibleWay(position[0], position[1], player) !=True :
            return False
        return True
        
    def fenceNotCloseAccesGoal(self) -> bool:
        for i in range(self.__nb_players):
            if self.seachPossibleWayForPlayer(i+1) == False :
                return False
        return True
    
    def isPossibleMove(self, x : int, y : int) -> bool:
        position = self.current_player.displayPlace()
        if position[0]==0:
            if x ==-2:
                return False
        if position[1]==0:
            if y==-2:
                return False
        if position[0]==(self.__size-1)*2:
            if x==2:
                return False
        if position[1]==(self.__size-1)*2:
            if y==2:
                return False
        if self.thereIsFence(position[0]+int(x/2), position[1]+int(y/2)) == True :
            return False        
        return True   
    
    def refreshPossibleCaseMovementForCurrentPlayer(self) -> None:
        position = self.current_player.displayPlace()
        list_possible_move = self.allPossibleMoveForPlayer()
        for coord in list_possible_move :
            case = self.board[position[0]+coord[0]][position[1]+coord[1]]
            case.set_possibleMove([coord[0],coord[1]])
            
    def resetPossibleCaseMovement(self) -> None:
        for i in range(self.__size*2-1):
            if i%2 == 0 :
                for j in range(self.__size*2-1):
                    if j%2 == 0 :
                        case = self.board[i][j]
                        case.set_possibleMove(0)
                    

    #partie IA
    # def game(self) :
    #     jeu.start()
    #     self.refreshPossibleCaseMovementForCurrentPlayer()
    #     jeu.displayBoard(False)
    def isPossibleMoveOnLeftSizePlayer(self, position : list, x : int, y : int) -> bool:
        if x != 0 :
            if position[0] != 0 :
                if self.board[position[0]+int(x*1.5)][position[1]].get_build() != 0 or self.board[position[0]+x*2][position[1]].get_player() !=0 :
                    if self.board[position[0]+x][position[1]-1].get_build() == 0 and self.board[position[0]+x][position[1]-2].get_player() ==0 :
                        return True
                
        else :
            if position[1] != 0 :
                if self.board[position[0]][position[1]+int(y*1.5)].get_build() != 0 or self.board[position[0]][position[1]+y*2].get_player() !=0 :
                        if self.board[position[0]-1][position[1]+y].get_build() == 0 and self.board[position[0]-2][position[1]+y].get_player() ==0 :
                            return True
        return False
    
    def isPossibleMoveOnRightSizePlayer(self,position : list, x : int, y : int) -> bool:
        if x != 0 :
            if position[0] != (self.__size-1)*2 :
                if self.board[position[0]+int(x*1.5)][position[1]].get_build() != 0 or self.board[position[0]+x*2][position[1]].get_player() !=0 :
                    if self.board[position[0]+x][position[1]+1].get_build() == 0 and self.board[position[0]+x][position[1]+2].get_player() ==0 :
                        return True
                
        else :
            if position[1] != (self.__size-1)*2 :
                if self.board[position[0]][position[1]+int(y*1.5)].get_build() != 0 or self.board[position[0]][position[1]+y*2].get_player() !=0 :
                        if self.board[position[0]+1][position[1]+y].get_build() == 0 and self.board[position[0]+2][position[1]+y].get_player() ==0 :
                            return True
        return False

            
    def allPossibleMoveForPlayer(self) -> list:
        list = []
        position = self.current_player.displayPlace()
        if self.isPossibleMove(-2,0) == True :
            if self.board[position[0]-2][position[1]].get_player() !=0:
                if position[0] != 2 :
                    if self.board[position[0]-3][position[1]].get_build() == 0 and self.board[position[0]-4][position[1]].get_player() == 0:
                        list.append([-4,0])
                    if self.isPossibleMoveOnLeftSizePlayer(position,-2,0) == True :
                        list.append([-2,-2])
                    if self.isPossibleMoveOnRightSizePlayer(position,-2,0) == True :
                        list.append([-2,2])
            else:
                list.append([-2,0])
        if self.isPossibleMove(2,0) == True :
            if self.board[position[0]+2][position[1]].get_player() !=0:
                if position[0] != (self.__size-1)*2-2 :
                    if self.board[position[0]+3][position[1]].get_build() ==0:
                        list.append([4,0])
                    if self.isPossibleMoveOnLeftSizePlayer(position,2,0) == True :
                        list.append([2,-2])
                    if self.isPossibleMoveOnRightSizePlayer(position,2,0) == True :
                        list.append([2,2])
            else:
                list.append([2,0])
        if self.isPossibleMove(0,-2) == True :
            if self.board[position[0]][position[1]-2].get_player() !=0:
                if position[1] != 2 :
                    if self.board[position[0]][position[1]-3].get_build() ==0:
                        list.append([0,-4])
                    if self.isPossibleMoveOnLeftSizePlayer(position,0,-2) == True :
                        list.append([-2,-2])
                    if self.isPossibleMoveOnRightSizePlayer(position,0,-2) == True :
                        list.append([2,-2])
            else:
                list.append([0,-2])
        if self.isPossibleMove(0,2) == True :
            if self.board[position[0]][position[1]+2].get_player() !=0:
                if position[1] != (self.__size-1)*2-2 :
                    if self.board[position[0]][position[1]+3].get_build() ==0:
                        list.append([0,4])
                    if self.isPossibleMoveOnLeftSizePlayer(position,0,2) == True :
                        list.append([-2,2])
                    if self.isPossibleMoveOnRightSizePlayer(position,0,2) == True :
                        list.append([2,2])
            else:
                list.append([0,2])
        return list
    
    def allPossibleBuildFence(self) -> list:
        list = [] 
        for i in range(1,self.__size*2-1,2):
            for j in range(1,self.__size*2-1,2):
                self.fence_orientation == "vertical"
                if self.isPossibleFence(i, j) == True :
                    list.append([i,j,0])
                self.fence_orientation == "horizontal"
                if self.isPossibleFence(i, j) == True :
                    list.append([i,j,1])
        return list

def SendBoardClient(x : int, y : int, typeClick : int, client : socket, orientation : str) -> None:
    # typeClick = 0 (caseClicked)
    # typeClick = 1 (fenceClicked)
    
    # orientation = 0 (vertical)
    # orientation = 1 (horizontal)
    
    if orientation == "vertical":
        orientation = 0
    else: 
        orientation = 1
        
    DataMove = (
        [int(x), int(y), int(typeClick), int(orientation)])
    dataSendArray = pickle.dumps(DataMove)
    
    try:
        client.send(dataSendArray)
        time.sleep(0.1)
    except socket.error:
        print("Erreur d'envoie du tableau ...")
        exit()
    
    
        


def restartGame(size : int, nb_players : int, nb_IA : int, nb_fences : int, select_map : int) -> None:
    jeu = Board(size, nb_players , nb_IA, nb_fences, select_map, False, "", "", 0)
    jeu.start()
    jeu.refreshPossibleCaseMovementForCurrentPlayer()
    jeu.displayBoard(False)


if __name__ == "__main__":
    restartGame(5, 2, 0, 8, 2)
    mainloop()