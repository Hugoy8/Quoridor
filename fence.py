class Fence:
    
    def __init__(self, build : int) -> None:
        self.__build = build
    
    
    def get_build(self) -> None:
        return self.__build 
    
    
    def set_build(self, build : int) -> None:
        self.__build = build
    
    
    def buildFence(self) -> None:
        self.__build = 1    
    
    
    def displayFence(self) -> str:
        if self.__build == 0:
            return "F0"
        else : 
            return "F1"