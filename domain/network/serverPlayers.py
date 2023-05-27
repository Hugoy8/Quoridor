from domain.network.serverToPlay import ServerToPlay
from infrastructure.services.services import Board
import threading
import pickle
import time

class ServerPlayers(threading.Thread):
    def __init__(self, server : object, serverToPlay : ServerToPlay, board: Board):
        threading.Thread.__init__(self)
        # Variable qui contient l'object de la class Server.
        self.server = server
        # Variable qui cotient l'object de la class ServerToPlay.
        self.serverToPlay = serverToPlay
        # Variable qui contient l'object de la class Board.
        self.board = board
        
    def run(self):
        while True:
            # Je récupére le socket du client qui doit jouer.
            try:
                if self.serverToPlay.getPlayerToPlay() < 3:
                    ClientToPlay = self.server.listClients[self.serverToPlay.getPlayerToPlay()+1]
                else:
                    ClientToPlay = self.server.listClients[self.board.current_player.get_player()]
                    self.serverToPlay.changePlayerToPlay()
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                    self.board.displayBoard(False)

                dataRecvArray = ClientToPlay.recv(4096)
                dataRecvClient = pickle.loads(dataRecvArray)

                self.serverToPlay.changePlayerToPlay()
                if dataRecvClient[2] == 0:
                    self.board.move(int(dataRecvClient[0]),int(dataRecvClient[1]))
                    self.board.resetPossibleCaseMovement() 
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
                                if self.board.victory():
                                    self.board.windowVictory()
                                else:
                                    self.board.refreshCurrentPlayer()
                                    if self.serverToPlay.getPlayerToPlay() == 0:
                                        self.board.refreshPossibleCaseMovementForCurrentPlayer()
                                    self.board.displayBoard(False)
                    
                elif dataRecvClient[2] == 1:
                    self.board.buildFenceNetwork(int(dataRecvClient[0]),int(dataRecvClient[1]), int(dataRecvClient[3]))
                    if self.board.fenceNotCloseAccesGoal() == False :
                        self.board.deBuildFence(int(dataRecvClient[0]),int(dataRecvClient[1]))
                    else :
                        self.board.resetPossibleCaseMovement() 
                        self.board.refreshCurrentPlayer()
                        if self.serverToPlay.getPlayerToPlay() == 0:
                            self.board.refreshPossibleCaseMovementForCurrentPlayer()
                        self.board.displayBoard(False)

                
                for player, socketClient in self.server.listClients.items():
                    time.sleep(0.1)
                    # On vérifie si le joueur est bien connecté et prêt à recevoir les donnnées, et on vérifie de ne pas envoyé au serveur.
                    if player != dataRecvClient[4]-1 and socketClient.fileno() != -1 and player != 0:
                        try:
                            messagePlayertoPlay = self.server.verifPlayertoPlay(player-1)
                            DataMove = ([dataRecvClient[0], dataRecvClient[1], dataRecvClient[2], dataRecvClient[3], str(messagePlayertoPlay)])
                            dataSendtable = pickle.dumps(DataMove)
                            socketClient.send(dataSendtable)
                        except OSError:
                            print(f"Erreur lors de l'envoi du message à Joueur {player}")
            except:
                import main
                main()