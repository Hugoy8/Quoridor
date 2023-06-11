class Pillar:
    
    def __init__(self, build : int, position :list) -> None:
        self.__build = build
        self.__position = position
    
    
    def get_build(self) -> int:
        return self.__build 
    
    
    def set_build(self, build : int) -> None:
        self.__build = build
    
        
    def buildPillar(self) -> None:
        self.__build = 1
    
        
    def displayPillar(self) -> str:
        if self.__build == 0:
            return "B0"
        else : 
            return "B1"
        
    def get_position(self) -> list:
        return self.__position