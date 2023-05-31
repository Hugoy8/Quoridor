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
            build = self.botBuildRandomFence(self.board.allPossibleBuildFence())
            if build != False :
                return ["build", build]
        return ["move",self.randomChoice(self.board.allPossibleMoveForPlayer())]
            
            
    def currentBotPlaysBasedOnDifficulty(self, difficulty):
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
            
    