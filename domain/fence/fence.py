class Fence:
    
    def __init__(self, build : int) -> None:
        self.__build = build
        self.neighbors = []
    
    
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
        
    def updateNeighborsPillars(self, board, i, j, size) -> None:
        self.neighbors = []
        if i%2 == 0:
            if i < (size-1)*2 :
                self.neighbors.append(board.board[i + 1][j])
            if i > 0:
                self.neighbors.append(board.board[i - 1][j])
        else :
            if j < (size-1)*2 :
                self.neighbors.append(board.board[i][j + 1])
            if j > 0:
                self.neighbors.append(board.board[i][j - 1])
                
    def get_neighborsPillar(self):
        return self.neighbors