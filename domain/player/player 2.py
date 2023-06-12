class Player:
    
    def __init__(self, x : int, y : int, player, nb_fence, IA_level) -> None:
        self.__player = player
        self.__nb_fence = nb_fence
        self.__x = x
        self.__y = y
        self.__IA_level = IA_level
    
    def get_player(self) -> str:
        return self.__player
    
    
    def set_player(self, player : str) -> None:
        self.__player = player
    
    
    def get_nb_fence(self) -> int:
        return self.__nb_fence
    
    
    def set_fence(self, nb_fence : int) -> None:
        self.__nb_fence = nb_fence
    
    def move(self, x : int, y : int) -> None:
        self.__x = x
        self.__y = y
        
    def displayPlace(self) -> list:
        return [self.__x, self.__y]
    
    
    def get_IALevel(self) -> int:
        return self.__IA_level
    
    
    def set_IALevel(self, IA_level : int) -> None:
        self.__IA_level = IA_level