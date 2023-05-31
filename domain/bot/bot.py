import random

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
            self.botBuildRandomFence(self.board.allPossibleBuildFence())
        else :
            movement = self.randomChoice(self.board.allPossibleMoveForPlayer())
            self.board.move(movement[0],movement[1])
        
    
    def currentBotPlaysBasedOnDifficulty(self, difficulty):
        if difficulty ==  1 :
            self.botPlaysRandom()
            
    
    def botBuildRandomFence(self, allPossibleBuildFence):
        can_build = False
        possibleBuildFence = allPossibleBuildFence
        while can_build == False and possibleBuildFence !=[]:
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
                self.board.displayBoard(False) 
            else : 
                can_build = True
    