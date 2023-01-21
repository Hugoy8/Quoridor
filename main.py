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
            return 'Player1'
        elif self.__player == 2:
            return 'Player2'
        elif self.__player == 3:
            return 'Player3'
        elif self.__player == 4:
            return 'Player4'
        else:
            return 'NoPlayer'


class Fence:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
        
    
    def displayFence(self):
        if self.__build == 0:
            return False
        else : 
            return True

        
class Pillar:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
        
    
    def displayPillar(self):
        if self.__build == 0:
            return False
        else : 
            return True

        
class Player:
    
    def __init__(self, x, y, player):
        self.__player = player
        self.__x = x
        self.__y = y
    
    def get_player(self):
        return self.__player
    
    
    def set_player(self, player):
        self.__player = player
    
    def move(self, x, y):
        self.__x = x
        self.__y = y
        
    def displayPlace(self):
        return [self.__x, self.__y]
        
class Board:
    
    def __init__(self, size):
        
        self.display = Tk()
        largeur_ecran= self.display.winfo_screenwidth()
        hauteur_ecran = self.display.winfo_screenheight()
        self.display.geometry(f"+{(largeur_ecran - 900) // 2}+{(hauteur_ecran - 510) // 2}")
        self.display.geometry("900x510")
        
        self.__size = size
        self.board = []
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
        self.c = Canvas(self.display, width=900, height=510)
        self.c.grid(row=self.__size, column=self.__size, padx=5, pady=5)
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
                        
                        self.c.create_rectangle(x1, y1, x2, y2, fill='white', outline="black", width=1)
                    else :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        self.c.create_rectangle(x1+10, y1, x2+5, y2-20, fill='brown', outline="black", width=1)
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
                        self.c.create_rectangle(x1+10, y1, x2-10, y2, fill='brown', outline="black", width=1)
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        self.c.create_rectangle(x1+15, y1+10, x2-15, y2-15, fill='gray', outline="black", width=1)
                tab.append(tab2)
        for x in tab :
            print(x)
        self.display.mainloop()
    
    
    def start(self):
        case = self.board[0][self.__size-1]
        case.set_player(1)
        self.player1 = Player(0,self.__size-1,1)
        print(self.player1.displayPlace())
        case = self.board[-1][self.__size-1]
        case.set_player(2)
        self.player2 = Player((self.__size-1)*2,self.__size-1,2)
        print(self.player2.displayPlace())
        
    def moveUp(self,x,y,joueur):
        case = self.board[x][y]
        case.set_player(0)
        case = self.board[x-2][y]
        case.set_player(joueur)
        
        
    def moveDown(self):
        position = self.player1.displayPlace()
        case = self.board[position[0]][position[1]]
        case.set_player(0)
        case = self.board[position[0]+2][position[1]]
        case.set_player(1)
        self.player1.move(position[0]+2,position[1])
        
        

    def moveLeft(self,x,y,joueur):
        case = self.board[x][y]
        case.set_player(0)
        case = self.board[x][y-2]
        case.set_player(joueur)
        
        
    def moveRight(self,x,y,joueur):
        case = self.board[x][y]
        case.set_player(0)
        case = self.board[x][y+2]
        case.set_player(joueur)
        
        
        
        
        
        







jeu = Board(7)
jeu.start()
jeu.moveDown()
jeu.displayBoard()
