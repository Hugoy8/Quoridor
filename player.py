class Player:
    
    def __init__(self, x, y, player, nb_fence, IA_level):
        self.__player = player
        self.__nb_fence = nb_fence
        self.__x = x
        self.__y = y
        self.__IA_level = IA_level
    
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
    
    
    def get_IALevel(self):
        return self.__IA_level
    
    
    def set_IALevel(self, IA_level):
        self.__IA_level = IA_level