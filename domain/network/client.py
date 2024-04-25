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
        # Variable qui stocke l'état de l'écoute.
        self.statusListenClient = True
        
        
    def runClient(self, client : socket) -> None:
        # Boucle en de jeu en 2 joueurs.
        if self.Infos[0] == 2:
            while self.statusListenClient:
                # Réception des informations du serveur.
                try:
                    dataRecvArray = client.recv(4096)
                    dataRecvServer = pickle.loads(dataRecvArray)
                    
                    print(dataRecvServer)
                    self.fonctionBoard(dataRecvServer)
                except socket.error:
                    from domain.launcher.launcher import QuoridorLauncher
                    
                    self.statusListenClient = False
                    self.board.window.destroy()
                    runError = QuoridorLauncher("errorClientOfServer")
                    break
                    
        elif self.Infos[0] == 4:
            while self.statusListenClient:
                # Réception des informations du serveur.
                try:
                    dataRecvArray = client.recv(4096)
                    dataRecvServer = pickle.loads(dataRecvArray)
                    
                    self.fonctionBoard(dataRecvServer)
                except socket.error:
                    from domain.launcher.launcher import QuoridorLauncher
                    
                    self.statusListenClient = False
                    self.board.window.destroy()
                    runError = QuoridorLauncher("errorClientOfServer")
                    break
        
        
    def fonctionBoard(self, dataRecvServer : list) -> None:
        # Affichage graphique des changements du serveur.
        if dataRecvServer[2] == 0:
            self.board.movement.move(int(dataRecvServer[0]),int(dataRecvServer[1]))
            self.board.resetPossibleCaseMovement() 
            self.board.refreshCurrentPlayer()
            
            if self.Infos[0] == 4:
                if self.board.victory():
                    self.board.windowVictory()
                else:
                    self.board.refreshCurrentPlayer()
                    if self.board.victory():
                        self.board.windowVictory()
                    else:
                        self.board.refreshCurrentPlayer()
                        if self.board.victory():
                            self.board.windowVictory()
                        else:
                            self.board.refreshCurrentPlayer()
                            if self.board.victory():
                                self.board.windowVictory()
                            else:
                                self.board.refreshCurrentPlayer()
                                if dataRecvServer[4] == "You":
                                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                                self.board.displayBoard(False)
            
            elif self.Infos[0] == 2:
                if self.board.victory():
                    self.board.windowVictory()
                else:
                    self.board.refreshCurrentPlayer()
                    if self.board.victory():
                        self.board.windowVictory()
                    else:
                        self.board.refreshCurrentPlayer()
                        self.board.refreshPossibleCaseMovementForCurrentPlayer()
                        self.board.displayBoard(False)
                        
            
            
        elif dataRecvServer[2] == 1:
            self.board.fenceStructure.buildFenceNetwork(int(dataRecvServer[0]),int(dataRecvServer[1]), int(dataRecvServer[3]))
            if self.board.movement.fenceNotCloseAccesGoal() == False :
                self.board.fenceStructure.deBuildFence(int(dataRecvServer[0]),int(dataRecvServer[1]))
            else:
                self.board.resetPossibleCaseMovement() 
                self.board.refreshCurrentPlayer()
                if self.Infos[0] == 4:
                    if dataRecvServer[4] == "You":
                        self.board.refreshPossibleCaseMovementForCurrentPlayer()
                elif self.Infos[0] == 2:
                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                self.board.displayBoard(False)