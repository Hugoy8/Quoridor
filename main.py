from tkinter import*



class Case:
    
    def __init__(self, player):
        self.__player = player


    def get_player(self):
        return self.__player
    
    
    def set_player(self, player):
        self.__player = player
    
    
    def displayPlayer(self):
        if self.__player == 1:
            return 'P1'
        elif self.__player == 2:
            return 'P2'
        elif self.__player == 3:
            return 'P3'
        elif self.__player == 4:
            return 'P4'
        else:
            return 'NP'


class Fence:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
    
    def buildFence(self):
        self.__build = 1    
    
    def displayFence(self):
        if self.__build == 0:
            return "FF"
        else : 
            return "FT"

        
class Pillar:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
    
        
    def buildPillar(self):
        self.__build = 1
    
        
    def displayPillar(self):
        if self.__build == 0:
            return "PF"
        else : 
            return "PT"

        
class Player:
    
    def __init__(self, x, y, player, nb_fence):
        self.__player = player
        self.nb_fence = nb_fence
        self.__x = x
        self.__y = y
    
    def get_player(self):
        return self.__player
    
    
    def set_player(self, player):
        self.__player = player
    
    
    def get_nb_fence(self):
        return self.__nb_fence
    
    
    def set_fence(self, nb_fence):
        self.__nb_fence = nb_fence
    
    def move(self, x, y):
        self.__x = x
        self.__y = y
        
    def displayPlace(self):
        return [self.__x, self.__y]
        
class Board:
    
    def __init__(self, size, nb_players, nb_fence):
        
        # self.display = Tk()
        # largeur_ecran= self.display.winfo_screenwidth()
        # hauteur_ecran = self.display.winfo_screenheight()
        # self.display.geometry(f"+{(largeur_ecran - 900) // 2}+{(hauteur_ecran - 510) // 2}")
        # self.display.geometry("900x510")
        
        self.__size = size
        self.__nb_players = nb_players
        self.__nb_fence = nb_fence
        self.players = []
        self.board = []
        self.fence_orientation = "vertical"
        for i in range(self.__size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.__size*2-1):
                    if j%2 == 0 : 
                        tab2.append(Case(0))
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
    
    
    def displayBoard(self): 
        # self.c = Canvas(self.display, width=900, height=510)
        # self.c.grid(row=self.__size, column=self.__size, padx=5, pady=5)
        tab =[]
        coucou = 0
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
                        
                        # self.c.create_rectangle(x1, y1, x2, y2, fill='white', outline="black", width=1)
                    else :
                        coucou +=1
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        # self.c.create_rectangle(x1+10, y1, x2+5, y2-20, fill='brown', outline="black", width=1)
                tab.append(tab2)
            else :
                tab2 = []
                for j in range(self.__size*2-1):
                    x1 = i * 50
                    y1 = j * 50
                    x2 = x1 + 50
                    y2 = y1 + 50
                    if j%2 == 0 :
                        coucou +=1
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        # self.c.create_rectangle(x1+10, y1, x2-10, y2, fill='brown', outline="black", width=1)
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        # self.c.create_rectangle(x1+15, y1+10, x2-15, y2-15, fill='gray', outline="black", width=1)
                tab.append(tab2)
        for x in tab :
            print(x)
        # self.display.mainloop()
    
    
    def start(self):
        nb_fence_each_player = int(self.__nb_fence / self.__nb_players)
        case = self.board[0][self.__size-1]
        case.set_player(1)
        self.players.append(Player(0,self.__size-1,1,nb_fence_each_player))
        case = self.board[-1][self.__size-1]
        case.set_player(2)
        self.players.append(Player((self.__size-1)*2,self.__size-1,2,nb_fence_each_player))
        if self.__nb_players == 4 :
            case = self.board[self.__size-1][0]
            case.set_player(3)
            self.players.append(Player(self.__size-1,0,3,nb_fence_each_player))
            case = self.board[self.__size-1][-1]
            case.set_player(4)
            self.players.append(Player(self.__size-1,(self.__size-1)*2,4,nb_fence_each_player))
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
        nb_fence_current_player  = self.current_players.get_nb_fence()
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
        nb_fence_current_player  = self.current_players.get_nb_fence()
        self.current_players.set_nb_fence(nb_fence_current_player-1)
        
    
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
        if self.way_find == True :
            return False
        for i in self.list_case_check:
                    if i[0] == x and i[1] == y:
                        return True
        return False
        
    def isPossibleWay(self, x, y):
        self.list_case_check.append([x, y])
        if x == (self.__size-1)*2:
            return True
        if x == 0:
            if y == 0:
                if self.alreadyChecked(0, 2) == False:
                    return self.isPossibleWay(0, 2)
                        
                if self.alreadyChecked(2, 0) == False:
                    return self.isPossibleWay(2, 0)
                        
            elif y==(self.__size-1)*2:
                if self.alreadyChecked(0, y-2) == False:
                    return self.isPossibleWay(0, y-2)
                        
                if self.alreadyChecked(2, y) == False:
                    return self.isPossibleWay(2, y)
                        
            else:
                
                if self.alreadyChecked(x, y-2) == False:
                    return self.isPossibleWay(x, y-2) 
                        
                if self.alreadyChecked(x, y+2) == False:
                    return self.isPossibleWay(x, y+2) 
                        
                if self.alreadyChecked(x+2, y) == False:
                    return self.isPossibleWay(x+2, y) 
                        
        elif y==0:
            if x == (self.__size-1)*2:
                if self.alreadyChecked(x-2, y) == False:
                    return self.isPossibleWay(x-2, y)
                        
                if self.alreadyChecked(x, y+2) == False:
                    return self.isPossibleWay(x, y+2) 
                        
            else :
                if self.alreadyChecked(x-2, y) == False:
                    return self.isPossibleWay(x-2, y) 
                        
                if self.alreadyChecked(x+2, y) == False:
                    return self.isPossibleWay(x+2, y) 
                        
                if self.alreadyChecked(x, y+2) == False:
                    return self.isPossibleWay(x, y+2) 
                        
        elif y==(self.__size-1)*2:
            if x == (self.__size-1)*2:
                if self.alreadyChecked(x-2, y) == False:
                    return self.isPossibleWay(x-2, y) 
                        
                if self.alreadyChecked(x, y-2) == False:
                    return self.isPossibleWay(x, y-2) 
                        
            else:
                if self.alreadyChecked(x-2, y) == False:
                    return self.isPossibleWay(x-2, y) 
                        
                if self.alreadyChecked(x+2, y) == False:
                    return self.isPossibleWay(x+2, y) 
                        
                if self.alreadyChecked(x, y-2) == False:
                    return self.isPossibleWay(x, y-2) 
                        
        else:
            if self.alreadyChecked(x-2, y) == False:
                return self.isPossibleWay(x-2, y) 
                        
            if self.alreadyChecked(x+2, y) == False:
                return self.isPossibleWay(x+2, y) 
                        
            if self.alreadyChecked(x, y-2) == False:
                return self.isPossibleWay(x, y-2) 
                        
            if self.alreadyChecked(x, y+2) == False:
                return self.isPossibleWay(x, y+2) 
                        
        
    
    def seachWay(self):
        self.way_find = False
        self.list_case_check = []
        print(self.isPossibleWay(0,6)) 
        
        
            
# Si taille plateau = 5 : max barriere = 20
# Si taille plateau = 7 : max barriere = 40
taille = 7
nb_joueur = 2
nb_barriere = 20
jeu = Board(taille, nb_joueur, nb_barriere)
jeu.start()
jeu.displayBoard()
jeu.seachWay()
