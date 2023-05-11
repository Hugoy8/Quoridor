class Case:
    
    def __init__(self, player : str, possibleMove : list) -> None:
        self.__player = player
        self.__possibleMove = possibleMove


    def get_player(self) -> str:
        return self.__player
    
    
    def set_player(self, player) -> None:
        self.__player = player
    
    def get_possibleMove(self) -> list:
        return self.__possibleMove
    
    
    def set_possibleMove(self, possibleMove) -> None:
        self.__possibleMove = possibleMove
        
    def displayPlayer(self) -> str:
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