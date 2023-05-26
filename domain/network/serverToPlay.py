class ServerToPlay():
    def __init__(self, typeGame : int):
        # Variable qui stocke le joueur qui doit jouer.
        self.PlayerToPlay = 0
        # Variable qui contient le mode de jeu.
        self.typeGame = typeGame
    
    def getPlayerToPlay(self):
        return self.PlayerToPlay
    
    def changePlayerToPlay(self):
        self.PlayerToPlay = (self.PlayerToPlay + 1) % self.typeGame