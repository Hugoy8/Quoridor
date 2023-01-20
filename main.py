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
        
        
class Board:
    
    def __init__(self, size):
        tab = []
        for i in range(size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(size*2-1):
                    if j%2 == 0 :
                        tab2.append("C")
                    else :
                        tab2.append("F")
                tab.append(tab2)
            else :
                tab2 = []
                for j in range(size*2-1):
                    if j%2 == 0 :
                        tab2.append("F")
                    else :
                        tab2.append("P")
                tab.append(tab2)
        for x in tab:
            print(x)
        
Board(9)