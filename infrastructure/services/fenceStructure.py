class FenceStructure:
    
    def __init__(self, board) -> None:
        self.board = board
        
    def buildFence(self, x : int, y : int) -> None:
            pillar = self.board.board[x][y]
            pillar.buildPillar()
            if self.board.fence_orientation == "vertical":
                fence = self.board.board[x-1][y]
                fence.buildFence()
                fence = self.board.board[x+1][y]
                fence.buildFence()
            else:
                fence = self.board.board[x][y-1]
                fence.buildFence()
                fence = self.board.board[x][y+1]
                fence.buildFence()
            nb_fence_current_player  = self.board.current_player.get_nb_fence()
            self.board.current_player.set_fence(nb_fence_current_player-1)
            self.board.displayBoard(False)
            
    def buildFenceNetwork(self, x : int, y : int, orientation : int) -> None:
            pillar = self.board.board[x][y]
            pillar.buildPillar()
            if orientation == 0:
                fence = self.board.board[x-1][y]
                fence.buildFence()
                fence = self.board.board[x+1][y]
                fence.buildFence()
            else:
                fence = self.board.board[x][y-1]
                fence.buildFence()
                fence = self.board.board[x][y+1]
                fence.buildFence()
            nb_fence_current_player  = self.board.current_player.get_nb_fence()
            self.board.current_player.set_fence(nb_fence_current_player-1)
            self.board.displayBoard(False)
            
    def deBuildFence(self, x : int, y : int) -> None:
        pillar = self.board.board[x][y]
        if self.board.fence_orientation == "vertical":
            fence = self.board.board[x-1][y]
            fence.set_build(0)
            fence = self.board.board[x+1][y]
            fence.set_build(0)
            if self.board.board[x][y-1].get_build() == 0 and self.board.board[x][y+1].get_build() == 0:
                pillar.set_build(0)
        else :
            fence = self.board.board[x][y-1]
            fence.set_build(0)
            fence = self.board.board[x][y+1]
            fence.set_build(0)
            if self.board.board[x-1][y].get_build() == 0 and self.board.board[x+1][y].get_build() == 0:
                pillar.set_build(0)
        nb_fence_current_player  = self.board.current_player.get_nb_fence()
        self.board.current_player.set_fence(nb_fence_current_player+1)
        
    def thereIsFence(self, x : int, y : int) -> bool:
        fence = self.board.board[x][y]
        if fence.get_build() == 1:
            return True
        return False