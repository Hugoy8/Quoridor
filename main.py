from tkinter import*
from case import *
from fence import*
from pillar import*
from player import*
import random
from PIL import Image, ImageTk


class Board:
    
    def __init__(self, size, nb_players, nb_fence):
        self.window = Tk()
        self.window.geometry("1500x700")
        self.window.title("Quoridor")
        self.window.maxsize(1500, 700)
        self.window.minsize(1500, 700)
        self.window.iconbitmap('./assets/logo.ico')
        self.window_game = True
        self.center_window()
        self.__size = size
        self.__nb_players = nb_players
        self.__nb_fence = nb_fence
        self.players = []
        self.board = []
        self.fence_orientation = "horizontal"    
        self.id_possible_move = 0 
        # Création des images du plateau
        # IMAGE DES CASES
        width = 80
        height = 80
        no_player = Image.open("./assets/case.png")
        no_player = no_player.resize((width, height))
        self.no_player = ImageTk.PhotoImage(no_player)
        
        moove_possible = Image.open("./assets/moove_possible.png")
        moove_possible = moove_possible.resize((width, height))
        self.moove_possible = ImageTk.PhotoImage(moove_possible)
        
        image_player_1 = Image.open("./assets/player_1.png")
        image_player_1 = image_player_1.resize((width, height))
        self.image_player_1 = ImageTk.PhotoImage(image_player_1)
        
        image_player_2 = Image.open("./assets/player_2.png")
        image_player_2 = image_player_2.resize((width, height))
        self.image_player_2 = ImageTk.PhotoImage(image_player_2)
        
        image_player_3 = Image.open("./assets/player_3.png")
        image_player_3 = image_player_3.resize((width, height))
        self.image_player_3 = ImageTk.PhotoImage(image_player_3)
        
        image_player_4 = Image.open("./assets/player_4.png")
        image_player_4 = image_player_4.resize((width, height))
        self.image_player_4 = ImageTk.PhotoImage(image_player_4)
        
        #IMAGES DES FENCES
        fence_vertical_width = 20
        fence_vertical_height = 80
        fence_height = Image.open("./assets/fence_height.png")
        fence_height = fence_height.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height = ImageTk.PhotoImage(fence_height)
        
        fence_height_vide = Image.open("./assets/fence_height_vide.png")
        fence_height_vide = fence_height_vide.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height_vide = ImageTk.PhotoImage(fence_height_vide)
        
        fence_horizontal_width = 80
        fence_horizontal_height = 20
        fence_width = Image.open("./assets/fence_width.png")
        fence_width = fence_width.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width = ImageTk.PhotoImage(fence_width)
        
        fence_width_vide = Image.open("./assets/fence_width_vide.png")
        fence_width_vide = fence_width_vide.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width_vide = ImageTk.PhotoImage(fence_width_vide)
        
        # IMAGE DES PILLIERS
        pillar = Image.open("./assets/pillier.png")
        pillar = pillar.resize((20, 20))
        self.pillar = ImageTk.PhotoImage(pillar)
        
        pillar_vide = Image.open("./assets/pillier_vide.png")
        pillar_vide = pillar_vide.resize((20, 20))
        self.pillar_vide = ImageTk.PhotoImage(pillar_vide)
        
        # IMAGE DES OBJETS HOVERED
        fence_width_hover = Image.open("./assets/fence_width_hover.png")
        fence_width_hover = fence_width_hover.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width_hover = ImageTk.PhotoImage(fence_width_hover)
        
        fence_height_hover = Image.open("./assets/fence_height_hover.png")
        fence_height_hover = fence_height_hover.resize((fence_vertical_width, fence_vertical_height))
        self.fence_height_hover = ImageTk.PhotoImage(fence_height_hover)

        pillar_hover = Image.open("./assets/pillier_hover.png")
        pillar_hover = pillar_hover.resize((20, 20))
        self.pillar_hover = ImageTk.PhotoImage(pillar_hover)
        
        # Image de victoire
        img_win_p1 = Image.open("./assets/victory_p1.png")
        img_win_p1 = img_win_p1.resize((600, 500))
        self.img_win_p1 = ImageTk.PhotoImage(img_win_p1)
        
        img_win_p2 = Image.open("./assets/victory_p2.png")
        img_win_p2 = img_win_p2.resize((600, 500))
        self.img_win_p2 = ImageTk.PhotoImage(img_win_p2)
        
        img_win_p3 = Image.open("./assets/victory_p3.png")
        img_win_p3 = img_win_p3.resize((600, 500))
        self.img_win_p3 = ImageTk.PhotoImage(img_win_p3)       
        
        img_win_p4 = Image.open("./assets/victory_p4.png")
        img_win_p4 = img_win_p4.resize((600, 500))
        self.img_win_p4 = ImageTk.PhotoImage(img_win_p4) 
        
        if size == 5:
            self.canvas_game_width = 478
            self.canvas_game_height = 478
        elif size == 7:
            self.canvas_game_width = 678
            self.canvas_game_height = 678

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
        
    
    def caseClicked(self, event):
        item_id = event.widget.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        if tags[0] == "move_case1":
            print("haut")
            move = 1
        elif tags[0] == "move_case2":
            print("droite")
            move = 2
        elif tags[0] == "move_case3":
            print("bas")
            move = 3
        elif tags[0] == "move_case4":
            print("gauche")
            move = 4
        position = self.current_player.displayPlace()
        if move == 1:
            if self.isPossibleMove(-2,0) == True :
                if self.board[position[0]-2][position[1]].get_player() !=0:
                    if position[0] == 2 :
                        print("case occupée")
                    else:
                        self.move(-4,0)
                        can_move = True
                else:
                    self.move(-2,0)
                    can_move = True
        elif move == 2:
            if self.isPossibleMove(0,2) == True :
                if self.board[position[0]][position[1]+2].get_player() !=0:
                    if position[1] == (self.__size-1)*2-2 :
                        print("case occupée")
                    else:
                        self.move(0,4)
                        can_move = True
                else :
                    self.move(0,2)
                    can_move = True
        elif move == 3:
            if self.isPossibleMove(2,0) == True :
                if self.board[position[0]+2][position[1]].get_player() !=0:
                    if position[0] == (self.__size-1)*2-2 :
                        print("case occupée")
                    else:
                        self.move(4,0)
                        can_move = True
                else :
                    self.move(2,0)
                    can_move = True
        elif move == 4:
            if self.isPossibleMove(0,-2) == True :
                if self.board[position[0]][position[1]-2].get_player() !=0:
                    if position[1] == 2 :
                            print("case occupée")
                    else:
                        self.move(0,-4)
                        can_move = True
                else :
                    self.move(0,-2)
                    can_move = True
        if self.victory() == True :
            self.displayBoard()
            self.canvas.unbind_all("<Button-1>")
            print("EH JOUEUR", self.current_player.get_player(), " BRAVO SAL BATARD !!! ") 
            for child in self.window.winfo_children():
                if child.winfo_exists():
                    child.destroy()
            self.windowVictory()
        else:
            self.resetPossibleCaseMovement() 
            self.refreshCurrentPlayer()
            self.refreshPossibleCaseMovementForCurrentPlayer()
            self.displayBoard()

    def center_window(self):
        # Récupération de la résolution de l'écran
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        # Calcul de la position x et y pour centrer la fenêtre
        if self.window_game == True:
            x = (screen_width - 1500) // 2
            y = (screen_height - 700) // 2
        else:
            x = (screen_width - 600) // 2
            y = (screen_height - 650) // 2

        # Configuration de la fenêtre
        if self.window_game == True:
            self.window.geometry(f"1500x700+{x}+{y}")
            self.window_game = False
        else:
            self.window.geometry(f"600x650+{x}+{y}")
        
        
    def windowVictory(self):
        self.window.geometry("600x650")
        self.window.title("Quoridor")
        self.window.maxsize(600, 650)
        self.window.minsize(600, 650)
        self.center_window()
        # Affichage de l'image de fond
        victory_canvas = Canvas(self.window, width=600, height=500, bg="green", bd=0, highlightthickness=0)
        if self.current_player.get_player() == 1:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p1)
        elif self.current_player.get_player() == 2:
            victory_canvas.create_image(0, 20, anchor="nw", image=self.img_win_p2)
        elif self.current_player.get_player() == 3:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p3)
        elif self.current_player.get_player() == 4:
            victory_canvas.create_image(0, 0, anchor="nw", image=self.img_win_p4)
        victory_canvas.pack()

        # Ajout des boutons
        button_frame = Frame(self.window, bg="green")
        button_frame.pack(side="top", expand=True, fill="both")

        quit_button = Button(button_frame, text="Quitter", font=("Arial", 14), fg="white", bg="#DB0000", bd=2, highlightthickness=0, command=self.window.destroy)
        quit_button.pack(side=LEFT, padx=110)

        replay_button = Button(button_frame, text="Rejouer", font=("Arial", 14), fg="white", bg="#78B000", bd=2, highlightthickness=0)
        replay_button.pack(side=LEFT, padx=100)

    def displayBoard(self): 
        self.canvas = Canvas(self.window, width=self.canvas_game_width, height=self.canvas_game_height, bg="gray")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        Label(self.window, text=" Tour : Joueur "+str(self.current_player.get_player()), font=("Arial", 14), fg="gray").place(x=10, y=10)
        Label(self.window, text=f"Nombre de barrières restantes : ", font=("Arial", 14) ).place(x=10, y=50)
        for index, nbr_fence_player in enumerate(self.players):
            print(nbr_fence_player.get_player(), nbr_fence_player.get_nb_fence())
            a = nbr_fence_player.get_player()
            b = nbr_fence_player.get_nb_fence()
            if b == 0:
                b = "Plus de "
            Label(self.window, text=f"Joueur {a} : {b} barrières", font=("Arial", 14), fg="brown").place(x=10, y=80 + (index * 30))
            
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
                                # si position de la case cliquable est en haut de la position du joueur
                                if i < position[0]:
                                    self.move_case = self.canvas.create_image(j*50, i*50, image=self.moove_possible, anchor="nw", tags="move_case1")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # Si la position de la case cliquable est en bas de la position du joueur
                                elif i > position[0]:
                                    self.move_case = self.canvas.create_image(j*50, i*50, image=self.moove_possible, anchor="nw", tags="move_case3")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # si la case cliquable est à droite du joueur
                                elif j > position[1]:
                                    self.move_case = self.canvas.create_image(j*50, i*50, image=self.moove_possible, anchor="nw", tags=f"move_case2")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # si la case cliquable est à gauche du joueur
                                elif j < position[1]:
                                    self.move_case = self.canvas.create_image(j*50, i*50, image=self.moove_possible, anchor="nw", tags=f"move_case4")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                            else :
                                self.canvas.create_image(j*50, i*50, image=self.no_player, anchor="nw")
                        elif case.displayPlayer() == "P1" :
                            self.canvas.create_image(j*50, i*50, image=self.image_player_1, anchor="nw")
                        elif case.displayPlayer() == "P2" :
                            self.canvas.create_image(j*50, i*50, image=self.image_player_2, anchor="nw")
                        elif case.displayPlayer() == "P3" :
                            self.canvas.create_image(j*50, i*50, image=self.image_player_3, anchor="nw")
                        elif case.displayPlayer() == "P4" :
                            self.canvas.create_image(j*50, i*50, image=self.image_player_4, anchor="nw")
                    else :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*50+30, i*50, image=self.fence_height, anchor="nw", tags=str(i) + "_" + str(j))
                        else :
                            self.canvas.create_image(j*50+30, i*50, image=self.fence_height_vide, anchor="nw", tags=str(i) + "_" + str(j))

                tab.append(tab2)
            else :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*50 ,i*50+30, image=self.fence_width, anchor="nw", tags=str(i) + "_" + str(j))
                        else:
                            self.canvas.create_image(j*50 ,i*50+30, image=self.fence_width_vide, anchor="nw", tags=str(i) + "_" + str(j))
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        if pillar.displayPillar() == "B1" :
                            self.pillar_rects.append(self.canvas.create_image(j*50+30, i*50+30, image=self.pillar, anchor="nw", tags=[i,j]))
                        else :
                            self.pillar_rects.append(self.canvas.create_image(j*50+30, i*50+30, image=self.pillar_vide, anchor="nw", tags=[i,j]))
                        self.canvas.tag_bind(self.pillar_rects[-1], "<Button-1>", self.buildFenceOnClick)
                        if self.victory() == False:
                            self.canvas.tag_bind(self.pillar_rects[-1], "<Enter>", self.on_hover)
                            self.canvas.tag_bind(self.pillar_rects[-1], "<Leave>", self.on_leave)
                            
                tab.append(tab2)
        for x in tab :
            print(x)
            
    def buildFenceOnClick(self,event):
        if self.playerHasFence() == False :
            print("Tu n'as plus de barrière :/")
        else :
            item_id = event.widget.find_withtag("current")[0], 
            tags = self.canvas.gettags(item_id)
            print(tags)
            if len(tags) >= 2 :
                x = int(tags[0])
                y = int(tags[1])
                print(x,y)
                if self.isPossibleFence(x,y) == True :
                    self.buildFence(x,y)
                    if self.fenceNotCloseAccesGoal()==False :
                        self.deBuildFence(x,y)
                    else :
                        self.resetPossibleCaseMovement() 
                        self.refreshCurrentPlayer()
                        self.refreshPossibleCaseMovementForCurrentPlayer()
                        self.displayBoard()
        
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


    def decideIALevel(self, player):
        # if int(input(f"Entrez 1 pour mettre le joueur {player} en IA ")) == 1 :
        #     return 1
        # return False
        return 0

    
    
    def start(self):
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
    
    
    def refreshCurrentPlayer(self) :
        if self.current_player.get_player() == self.__nb_players :
            self.current_player = self.players[0]
        else :
            self.current_player = self.players[self.current_player.get_player()]
    
            
    def move(self,x,y) :
        position = self.current_player.displayPlace()
        case = self.board[position[0]][position[1]]
        case.set_player(0)
        case = self.board[position[0]+x][position[1]+y]
        case.set_player(self.current_player.get_player())
        self.current_player.move(position[0]+x,position[1]+y)
                    
    
    def changeFenceOrientation(self, event=None):
        if self.fence_orientation == "vertical":
            self.fence_orientation = "horizontal"
        else :
            self.fence_orientation = "vertical"
        
    
    
    def playerHasFence(self):
        nb_fence_current_player  = self.current_player.get_nb_fence()
        if nb_fence_current_player <= 0 :
            return False
        return True
    
    def isPossibleFence(self,x,y):
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
    
    
    def buildFence(self,x,y):
        print("buildFence")
        pillar = self.board[x][y]
        pillar.buildPillar()
        if self.fence_orientation == "vertical":
            fence = self.board[x-1][y]
            fence.buildFence()
            fence = self.board[x+1][y]
            fence.buildFence()
        else :
            fence = self.board[x][y-1]
            fence.buildFence()
            fence = self.board[x][y+1]
            fence.buildFence()
        nb_fence_current_player  = self.current_player.get_nb_fence()
        self.current_player.set_fence(nb_fence_current_player-1)
        self.displayBoard()
        
    def deBuildFence(self,x,y):
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
    
    def victory(self):
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
        
    
    def alreadyChecked(self, x, y):
        for i in self.list_case_check:
                    if i[0] == x and i[1] == y:
                        return True
        return False
    
    def thereIsFence(self, x, y):
        fence = self.board[x][y]
        if fence.get_build() == 1:
            return True
        return False
        
    def isPossibleWay(self, x, y, player):
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
                        
        
    
    def seachPossibleWayForPlayer(self, player):
        self.list_case_check = []
        position = self.players[player-1].displayPlace()
        if self.isPossibleWay(position[0], position[1], player) !=True :
            return False
        return True
        
    def fenceNotCloseAccesGoal(self):
        for i in range(self.__nb_players):
            if self.seachPossibleWayForPlayer(i+1) == False :
                return False
        return True
    
    def isPossibleMove(self, x, y):
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
    
    def refreshPossibleCaseMovementForCurrentPlayer(self):
        position = self.current_player.displayPlace()
        list_possible_move = self.allPossibleMoveForPlayer()
        for coord in list_possible_move :
            case = self.board[position[0]+coord[0]][position[1]+coord[1]]
            case.set_possibleMove([coord[0],coord[1]])
            
    def resetPossibleCaseMovement(self):
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
    #     jeu.displayBoard()
        
    def allPossibleMoveForPlayer(self):
        list = []
        position = self.current_player.displayPlace()
        if self.isPossibleMove(-2,0) == True :
            if self.board[position[0]-2][position[1]].get_player() !=0:
                if position[0] != 2 :
                    list.append([-4,0])
            else:
                list.append([-2,0])
        if self.isPossibleMove(2,0) == True :
            if self.board[position[0]+2][position[1]].get_player() !=0:
                if position[0] != (self.__size-1)*2-2 :
                    list.append([4,0])
            else:
                list.append([2,0])
        if self.isPossibleMove(0,-2) == True :
            if self.board[position[0]][position[1]-2].get_player() !=0:
                if position[1] != 2 :
                    list.append([0,-4])
            else:
                list.append([0,-2])
        if self.isPossibleMove(0,2) == True :
            if self.board[position[0]][position[1]+2].get_player() !=0:
                if position[1] != (self.__size-1)*2-2 :
                    list.append([0,4])
            else:
                list.append([0,2])
        return list
    
    def allPossibleBuildFence(self):
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
            
            
        
        
def restartGame(size, nb_players, nb_fences):
    jeu = Board(size, nb_players , nb_fences)
    jeu.start()
    jeu.refreshPossibleCaseMovementForCurrentPlayer()
    jeu.displayBoard()
            # Si taille plateau = 5 : max barriere = 20
# taille = int(input("Choisi la taille de la grille fdp (5, 7, 9 ou 11) :"))
# nb_joueur = int(input("Choisi le nombre de joueur enculé (2 ou 4) :"))
# nb_barriere = int(input("Choisi le nombre de barrière batard (multiple de 4 entre 4 et 50) :"))
# print(jeu.allPossibleBuildFence())
restartGame(7,2,4)
mainloop()