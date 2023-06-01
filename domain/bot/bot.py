import random
import math
from queue import PriorityQueue

class Bot :
    def __init__(self):
        self.board = None
        
        
    def setBoard(self, newBoard : object):
        self.board = newBoard
        
        
    def randomChoice(self, allPossibleChoice : list ):
        return random.choice(allPossibleChoice)
    
    def botPlaysRandom(self):
        action = self.randomChoice(["move","build"])
        if action == "build"  and self.board.playerHasFence() == True and self.board.allPossibleBuildFence() !=[]:
            build = self.botBuildRandomFence(self.board.allPossibleBuildFence())
            if build != False :
                return ["build", build]
        return ["move",self.randomChoice(self.board.allPossibleMoveForPlayer())]
            
            
    def currentBotPlaysBasedOnDifficulty(self, difficulty):
        print(self.main(self.board.board[8][4], self.board.board[0][2]))
        if difficulty ==  1 :
            action = self.botPlaysRandom()
        self.doAction(action)
            
            
    def botBuildRandomFence(self, allPossibleBuildFence):
        possibleBuildFence = allPossibleBuildFence
        while possibleBuildFence !=[]:
            build = self.randomChoice(possibleBuildFence)
            x_co_fence = build[0]
            y_co_fence = build[1]
            orientation = build[2]
            if orientation == 0 :
                self.fence_orientation = "vertical"
            else :
                self.fence_orientation = "horizontal"
            self.board.buildFence(x_co_fence,y_co_fence)
            if self.board.fenceNotCloseAccesGoal()==False :
                possibleBuildFence.remove(build)
                self.board.deBuildFence(x_co_fence,y_co_fence)
            else : 
                self.board.deBuildFence(x_co_fence,y_co_fence)
                return [x_co_fence, y_co_fence, orientation]
        return False
    
    
    def doAction(self, action):
        if action[0] == "move":
            self.board.move(action[1][0],action[1][1])
        else :
            if action[1][2] == "vertical":
                self.fence_orientation = "vertical"
            else :
                self.fence_orientation = "horizontal"
            self.board.buildFence(action[1][0],action[1][1])
            
    
    def updateNeighborsForEachCase(self):
        for i in range(self.board.get_size()*2-1):
            if i%2 == 0 :
                for j in range(self.board.get_size()*2-1):
                    if j%2 == 0 : 
                        self.board.board[i][j].updateNeighbors(self.board, i, j, self.board.get_size())
                        
    def h(self, coordinates1 : list, coordinates2 : list):  #calculer distance
        x1 = int(coordinates1[0])
        y1 = int(coordinates1[1])
        x2 = int(coordinates2[0])
        y2 = int(coordinates2[1])
        return abs(x1 - x2) + abs(y1 - y2)   #abs = distance absolue
    
    def algorithm(self, board, startCase, endCase):
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, startCase))
        came_from = {}
        g_score = {}
        for row in board:
            for case in row:
                g_score[case] = float("inf")
        g_score[startCase] = 0
        f_score = {}
        for row in board:
            for case in row:
                f_score[case] = float("inf")
        f_score[startCase] = self.h(startCase.get_position(), endCase.get_position())

        open_set_hash = {startCase}
        
        
        while not open_set.empty():
            print("dans boucle")
            currentCase = open_set.get()[2]
            open_set_hash.remove(currentCase)

            if currentCase == endCase:
                # reconstruct_path(came_from, end, draw)
                # end.make_end()
                # return True
                print("win")
                return came_from

            for neighbor in currentCase.get_neighbors():
                temp_g_score = g_score[currentCase] + 1

                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = currentCase
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + self.h(neighbor.get_position(), endCase.get_position())
                    if neighbor not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor], count, neighbor))
                        open_set_hash.add(neighbor)
                        # neighbor.make_open()

            # if currentCase != start:
            #     currentCase.make_closed()

        return False
    
    
    def main(self, startCase, endCase):
        self.updateNeighborsForEachCase()  #mets a jour les voisins de chaque case
        self.algorithm(self.board.board, startCase, endCase)