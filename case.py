class Case:
    
    def __init__(self, player):
        self.__player = player


    def get_player(self):
        return self.__player
    
    
    def set_player(self, player):
        self.__player = player
    
    
    def displayPlayer(self):
        if self.__player == 1:
            return '🔵'
        elif self.__player == 2:
            return '🔴'
        elif self.__player == 3:
            return '🟢'
        elif self.__player == 4:
            return '🟡'
        elif self.__player == 0:
            return '⬜️'