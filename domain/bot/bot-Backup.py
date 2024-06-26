import random

class Bot:
    def __init__(self) -> None:
        self.board = None
        
    
    def setBoard(self, newBoard : object) -> None:
        self.board = newBoard
        
        
    def randomChoice(self, allPossibleChoice : list ):
        return random.choice(allPossibleChoice)
    
    
    def botPlaysRandom(self) -> list:
        action = self.randomChoice(["move","build"])
        if action == "build"  and self.board.fenceStructure.playerHasFence() == True and self.board.fenceStructure.allPossibleBuildFence() !=[]:
            build = self.botBuildRandomFence(self.board.fenceStructure.allPossibleBuildFence())
            if build != False :
                return ["build", build]
        return ["move",self.randomChoice(self.board.movement.allPossibleMoveForPlayer())]


    def currentBotPlaysBasedOnDifficulty(self, difficulty : int) -> None:
        if difficulty ==  1 :
            action = self.botPlaysRandom()
            return action


    def botBuildRandomFence(self, allPossibleBuildFence : list) -> list:
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
            self.board.fenceStructure.buildFence(x_co_fence,y_co_fence)
            if self.board.movement.fenceNotCloseAccesGoal()==False :
                possibleBuildFence.remove(build)
                self.board.fenceStructure.deBuildFence(x_co_fence,y_co_fence)
            else : 
                self.board.fenceStructure.deBuildFence(x_co_fence,y_co_fence)
                return [x_co_fence, y_co_fence, orientation]
        return False
    
    
    def doAction(self, action : list) -> None:
        if action[0] == "move":
            self.board.movement.move(action[1][0],action[1][1])
        else :
            if action[1][2] == "vertical":
                self.fence_orientation = "vertical"
            else :
                self.fence_orientation = "horizontal"
            self.board.fenceStructure.buildFence(action[1][0],action[1][1])