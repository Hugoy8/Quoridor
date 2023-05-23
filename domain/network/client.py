import threading
import socket
import pickle
from infrastructure.services.services import Board

class Client(threading.Thread):
    def __init__(self, client : socket, boardInfos : Board, Infos : list) -> None:
        threading.Thread.__init__(self, group=None, target=self.runClient, args=(client,))
        
        # Variable qui stocke la class de jeu.
        self.board = boardInfos
        # Liste qui contient tous les paramètres reçu par le serveur.
        self.Infos = Infos
        
    def runClient(self, client : socket) -> None:
        # Boucle en de jeu en 2 joueurs.
        if self.Infos[0] == 2:
            while True:
                # Réception des informations du serveur.
                dataRecvArray = client.recv(4096)
                dataRecvServer = pickle.loads(dataRecvArray)
                
                # Affichage graphique des changements du serveur.
                if dataRecvServer[2] == 0:
                    self.board.move(int(dataRecvServer[0]),int(dataRecvServer[1]))
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshCurrentPlayer()
                    
                    victory = self.board.victory()
                    if victory == True:
                        self.board.windowVictory()
                    else:
                        self.board.refreshCurrentPlayer()
                        victory = self.board.victory()
                        if victory == True:
                            self.board.windowVictory()
                        else:
                            self.board.refreshCurrentPlayer()
                            self.board.refreshPossibleCaseMovementForCurrentPlayer()
                            self.board.displayBoard(False)
                    
                    
                elif dataRecvServer[2] == 1:
                    self.board.buildFenceNetwork(int(dataRecvServer[0]),int(dataRecvServer[1]), int(dataRecvServer[3]))
                    if self.board.fenceNotCloseAccesGoal() == False :
                        self.board.deBuildFence(int(dataRecvServer[0]),int(dataRecvServer[1]))
                    else :
                        self.board.resetPossibleCaseMovement() 
                        self.board.refreshCurrentPlayer()
                        self.board.refreshPossibleCaseMovementForCurrentPlayer()
                        self.board.displayBoard(False)
                else:
                    print("Erreur de type de click")
        else:
            pass
            # Zone 4 joueurs.
