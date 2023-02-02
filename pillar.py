class Pillar:
    
    def __init__(self, build):
        self.__build = build
    
    
    def get_build(self):
        return self.__build 
    
    
    def set_build(self, build):
        self.__build = build
    
        
    def buildPillar(self):
        self.__build = 1
    
        
    def displayPillar(self):
        if self.__build == 0:
            return "⚪️"
        else : 
            return "⚫️"