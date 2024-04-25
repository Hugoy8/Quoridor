class Movement :
    def __init__(self, board) -> None:
        self.board = board

    def move(self, x : int, y : int) -> None:
            position = self.board.current_player.displayPlace()
            case = self.board.board[position[0]][position[1]]
            case.set_player(0)
            case = self.board.board[position[0]+x][position[1]+y]
            case.set_player(self.board.current_player.get_player())
            self.board.current_player.move(position[0]+x,position[1]+y)
            
    def isPossibleWay2(self, case : object, player : object):
            self.board.list_case_check.append(case.get_position())
            if case.get_position()[0] == (self.board.size-1)*2 and player == 1:
                return True
            elif case.get_position()[0] == 0 and player == 2:
                return True
            elif case.get_position()[1] == (self.board.size-1)*2 and player == 3:
                return True
            elif case.get_position()[1] == 0 and player == 4:
                return True
            for neighbor in case.get_neighbors() :
                if self.board.alreadyChecked(neighbor.get_position()[0], neighbor.get_position()[1]) == False and self.isPossibleWay2(neighbor, player) == True :
                    return True
                
    def seachPossibleWayForPlayer(self, player : str) -> bool:
        self.board.list_case_check = []
        if self.isPossibleWay2(self.board.board[self.board.players[player-1].displayPlace()[0]][self.board.players[player-1].displayPlace()[1]], player) !=True :
            return False
        else :
            return True
        
        
    def fenceNotCloseAccesGoal(self) -> bool:
        self.board.bot.updateNeighborsForEachCase()
        for i in range(self.board.nb_players):
            if self.seachPossibleWayForPlayer(i+1) == False :
                return False
        return True
    
    def isPossibleMove(self, x : int, y : int) -> bool:
        position = self.board.current_player.displayPlace()
        if position[0]==0:
            if x ==-2:
                return False
        if position[1]==0:
            if y==-2:
                return False
        if position[0]==(self.board.size-1)*2:
            if x==2:
                return False
        if position[1]==(self.board.size-1)*2:
            if y==2:
                return False
        if self.board.thereIsFence(position[0]+int(x/2), position[1]+int(y/2)) == True :
            return False        
        return True   
    
    def allPossibleMoveForPlayer(self, player : object) -> list:
        list2 = []
        position = player.displayPlace()
        self.board.bot.updateNeighborsForEachCase()
        for neighbor in self.board.board[position[0]][position[1]].get_neighbors():
            if neighbor.get_player() == 0 :
                list2.append([neighbor.get_position()[0] - position[0], neighbor.get_position()[1] - position[1]])
            else :
                can_jump = False
                for neighbor2 in neighbor.get_neighbors():
                    if neighbor2.get_player() == 0 and neighbor2.get_position()[0] == position[0] + (neighbor.get_position()[0] - position[0])*2 and neighbor2.get_position()[1] == position[1] + (neighbor.get_position()[1] - position[1])*2 :
                        list2.append([(neighbor.get_position()[0] - position[0])*2, (neighbor.get_position()[1] - position[1])*2])
                        can_jump = True
                if can_jump == False :
                    for neighbor2 in neighbor.get_neighbors():
                        if neighbor2.get_player() == 0 :
                            list2.append([neighbor2.get_position()[0] - position[0], neighbor2.get_position()[1] - position[1]])
        return list2