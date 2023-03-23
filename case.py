class Case:
    
    def __init__(self, player, possibleMove):
        self.__player = player


    def get_player(self):
        return self.__player
    
    
    def set_player(self, player):
        self.__player = player
    
    def get_possibleMove(self):
        return self.__possibleMove
    
    
    def set_possibleMove(self, possibleMove):
        self.__possibleMove = possibleMove
        
    def displayPlayer(self):
        if self.__player == 1:
            return 'P1'
        elif self.__player == 2:
            return 'P2'
        elif self.__player == 3:
            return 'P3'
        elif self.__player == 4:
            return 'P4'
        elif self.__player == 0:
            return 'P0'