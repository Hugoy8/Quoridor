class Pillar:
    
    def __init__(self, build : int) -> None:
        self.__build = build
    
    
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