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
        self.window.geometry("1400x700")
        self.window.title("Quoridor")
        self.window.maxsize(1400, 700)
        self.window.minsize(1400, 700)
        self.window.iconbitmap('./assets/logo.ico')
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
        
        fence_horizontal_width = 80
        fence_horizontal_height = 20
        fence_width = Image.open("./assets/fence_width.png")
        fence_width = fence_width.resize((fence_horizontal_width, fence_horizontal_height))
        self.fence_width = ImageTk.PhotoImage(fence_width)
        
        # IMAGE DES PILLIERS
        pillar = Image.open("./assets/pillier.png")
        pillar = pillar.resize((20, 20))
        self.pillar = ImageTk.PhotoImage(pillar)

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
            return 1
        elif tags[0] == "move_case2":
            print("droite")
            return 2
        elif tags[0] == "move_case3":
            print("bas")
            return 3
        elif tags[0] == "move_case4":
            print("gauche")
            return 4

    
    def displayBoard(self): 
        self.canvas = Canvas(self.window, width=1000, height=700, bg="gray")
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        tab =[]
        for i in range(self.__size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.__size*2-1):
                    x1 = i * 50
                    y1 = j * 50
                    x2 = x1 + 50
                    y2 = y1 + 50
                    if j%2 == 0 :
                        case = self.board[i][j]
                        tab2.append(case.displayPlayer())
                        if case.displayPlayer() == "P0" :
                            if case.get_possibleMove() != 0 :
                                position = self.current_player.displayPlace()
                                # si position de la case cliquable est en haut de la position du joueur
                                if i < position[0]:
                                    self.move_case = self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.moove_possible, anchor="nw", tags="move_case1")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # Si la position de la case cliquable est en bas de la position du joueur
                                elif i > position[0]:
                                    self.move_case = self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.moove_possible, anchor="nw", tags="move_case3")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # si la case cliquable est à droite du joueur
                                elif j > position[1]:
                                    self.move_case = self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.moove_possible, anchor="nw", tags=f"move_case2")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                                # si la case cliquable est à gauche du joueur
                                elif j < position[1]:
                                    self.move_case = self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.moove_possible, anchor="nw", tags=f"move_case4")
                                    self.canvas.tag_bind(self.move_case, "<Button-1>", self.caseClicked)
                            else :
                                self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.no_player, anchor="nw")
                        elif case.displayPlayer() == "P1" :
                            self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.image_player_1, anchor="nw")
                        elif case.displayPlayer() == "P2" :
                            self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.image_player_2, anchor="nw")
                        elif case.displayPlayer() == "P3" :
                            self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.image_player_3, anchor="nw")
                        elif case.displayPlayer() == "P4" :
                            self.canvas.create_image(((j*20)+(j*5))*2, ((i*20)+(i*5))*2, image=self.image_player_4, anchor="nw")
                    else :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(((j*20)+(j*5)+15)*2, ((i*20)+(i*5))*2, image=self.fence_height, anchor="nw")
                tab.append(tab2)
            else :
                tab2 = []
                for j in range(self.__size*2-1):
                    x1 = i * 50
                    y1 = j * 50
                    x2 = x1 + 50
                    y2 = y1 + 50
                    if j%2 == 0 :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(((j*20)+(j*5))*2 ,((i*20)+(i*5)+15)*2, image=self.fence_width, anchor="nw")
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        if pillar.displayPillar() == "B1" :
                            self.canvas.create_image(((j*20)+(j*5)+15)*2, ((i*20)+(i*5)+15)*2, image=self.pillar, anchor="nw")
                tab.append(tab2)
        for x in tab :
            print(x)


    def decideIALevel(self, player):
        if int(input(f"Entrez 1 pour mettre le joueur {player} en IA ")) == 1 :
            return 1
        return False

    
    
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
                    
    
    def changeFenceOrientation(self):
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
            if jeu.seachPossibleWayForPlayer(i+1) == False :
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
                    
        
    def game(self) :
        jeu.start()
        while self.victory() == False :
            self.refreshPossibleCaseMovementForCurrentPlayer()
            jeu.displayBoard()
            if self.current_player.get_IALevel() == 1 :
                list = [0,1]
                value= random.choice(list)
            else :
                value = int(input("tape 1 pour placer barriere sinon 0 pour déplacement:"))
            if value == 1  and self.playerHasFence() == True and self.allPossibleBuildFence() !=[]:
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
                        print(self.fence_orientation)
                        self.buildFence(x_co_fence,y_co_fence)
                        if self.fenceNotCloseAccesGoal()==False :
                            self.deBuildFence(x_co_fence,y_co_fence)
                        else : 
                            can_build = True
                    else:
                        x_co_fence = int(input("x du pillier"))
                        x_co_fence = int(input("y du pillier"))
                        orientation = int(input("orientation barriere 0= vertical sinon placer en horizontal:"))
                        if orientation == 0 :
                            self.fence_orientation = "vertical"
                        else :
                            self.fence_orientation = "horizontal"
                        if self.isPossibleFence(x_co_fence,y_co_fence) == True :
                            self.buildFence(x_co_fence,y_co_fence)
                        else :
                            x_co_fence = int(input("x du pillier"))
                            y_co_fence = int(input("y du pillier"))
                            orientation = int(input("orientation barriere 0=vertical sinon horizontal"))
                            if orientation == 0 :
                                self.fence_orientation = "vertical"
                            else :
                                self.fence_orientation = "horizontal"
                        if self.fenceNotCloseAccesGoal()==False :
                            self.deBuildFence(x_co_fence,y_co_fence)
                            print("tu bloques le chemin idiot")
                        else : 
                            can_build = True
            else :
                if value == 1  and self.playerHasFence() == False:
                    print("ta plus de barriere chacal")
                    if self.current_player.get_IALevel() == 1 :
                        movement = random.choice(self.allPossibleMoveForPlayer())
                        print(movement,self.current_player.get_player())
                        self.move(movement[0],movement[1])
                else : 
                    # partie IA
                    if self.current_player.get_IALevel() == 1 :
                        movement = random.choice(self.allPossibleMoveForPlayer())
                        print(movement,self.current_player.get_player())
                        self.move(movement[0],movement[1])
                        
                    else :
                        can_move = False
                        position = self.current_player.displayPlace()
                        while can_move == False :
                            move = int(input("haut = 1, droite = 2, bas = 3, gauche = 4 :"))
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
                jeu.displayBoard()
                break 
            self.resetPossibleCaseMovement()   
            jeu.displayBoard()
            print()
            self.refreshCurrentPlayer()    
        print("EH JOUEUR", self.current_player.get_player(), " BRAVO SAL BATARD !!! ")            
            

    #partie IA
    
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
            
            # Si taille plateau = 5 : max barriere = 20
# taille = int(input("Choisi la taille de la grille fdp (5, 7, 9 ou 11) :"))
# nb_joueur = int(input("Choisi le nombre de joueur enculé (2 ou 4) :"))
# nb_barriere = int(input("Choisi le nombre de barrière batard (multiple de 4 entre 4 et 40) :"))
jeu = Board(7, 2, 20)
# print(jeu.allPossibleBuildFence())
jeu.game()
mainloop()