class Case:
    
    def __init__(self, player : str, possibleMove : list, position :list) -> None:
        self.__player = player
        self.__possibleMove = possibleMove
        self.neighbors = []
        self.position = position


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
        
    def updateNeighbors(self, board, i, j, size):
        self.neighbors = []
        if i < (size-1)*2 and board.board[i + 1][j].get_build() == 0: # DOWN
            self.neighbors.append(board.board[i + 2][j])

        if i > 0 and board.board[i - 1][j].get_build() == 0: # UP
            self.neighbors.append(board.board[i - 2][j])

        if j < (size-1)*2 and board.board[i][j + 1].get_build() == 0: # RIGHT
            self.neighbors.append(board.board[i][j + 2])

        if j > 0 and board.board[i][j - 1].get_build() == 0: # LEFT
            self.neighbors.append(board.board[i][j - 2])
        # print(board.board[i][j].displayPlayer())
        
    def get_neighbors(self):
        return self.neighbors
    
    def get_position(self):
        return self.position