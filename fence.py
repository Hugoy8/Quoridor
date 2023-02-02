class Fence:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
    
    def buildFence(self):
        self.__build = 1    
    
    def displayFence(self):
        if self.__build == 0:
            return "--"
        else : 
            return "🚧"