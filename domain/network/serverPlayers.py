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
        # Variable qui contient le socket du joueur qui doit jouer.
        self.ClientToPlay = 0
        # Le dictionnaire qui contient les joueurs déconnectés à remplacer par des IA.
        self.diconnectPlayers = {}
        # Variable qui contient l'état de la boucle de jeu.
        self.status = True
        
        
    def setCheckClass(self, checkClass : object) -> None:
        self.checkClass = checkClass
        
        
    def sendInfosToClients(self, dataRecvClient : list) -> None:
        for player, socketClient in self.server.listClients.items():
            print("Player send : " + str(player) + "\n")
            time.sleep(0.1)
            # On vérifie si le joueur est bien connecté et prêt à recevoir les donnnées, et on vérifie de ne pas envoyé au serveur et au client déconnectée.
            if player != dataRecvClient[4]-1 and socketClient.fileno() != -1 and player != 0 and player not in self.diconnectPlayers:
                try:
                    messagePlayertoPlay = self.server.verifPlayertoPlay(player-1)
                    DataMove = ([dataRecvClient[0], dataRecvClient[1], dataRecvClient[2], dataRecvClient[3], str(messagePlayertoPlay)])
                    
                    dataSendtable = pickle.dumps(DataMove)
                    socketClient.send(dataSendtable)
                except OSError:
                    print(f"Erreur lors de l'envoi du message à Joueur {player}")
                                
                                
    def run(self):
        iaToPlay = False
        while self.status:
            # Je récupére le socket du client qui doit jouer.
            try:
                self.numClientActive = None
                
                if self.serverToPlay.getPlayerToPlay() < 3:
                    self.ClientToPlay = self.server.listClients[self.serverToPlay.getPlayerToPlay()+1]
                else:
                    self.ClientToPlay = self.server.listClients[self.board.current_player.get_player()]
                    self.serverToPlay.changePlayerToPlay()
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                    self.board.displayBoard(False)
                    
                for player, socket_client in self.server.listClients.items():
                    if socket_client == self.ClientToPlay:
                        self.numClientActive = player
                        break
                
                for player, type in self.diconnectPlayers.items():
                    if player == self.numClientActive and type == "Bot":
                        iaToPlay = True
                        
                        from domain.bot.bot import Bot
                        botClass = Bot()
                        botClass.setBoard(self.board)
                        resultChoice = botClass.currentBotPlaysBasedOnDifficulty(1)
                        
                        if resultChoice[0] == "move":
                            DataMoveBot = ([int(resultChoice[1][0]), int(resultChoice[1][1]), int(0), int(0), int(player)])
                        else:
                            DataMoveBot = ([int(resultChoice[1][0]), int(resultChoice[1][1]), int(1), int(resultChoice[1][2]), int(player)])
                        self.sendInfosToClients(DataMoveBot)
                        botClass.doAction(resultChoice)
                        
                        self.serverToPlay.changePlayerToPlay()
                        
                        self.board.resetPossibleCaseMovement() 
                        self.board.refreshCurrentPlayer()
                        
                        if not self.serverToPlay.getPlayerToPlay() < 3:
                            self.board.refreshPossibleCaseMovementForCurrentPlayer()
                            
                        self.board.displayBoard(False)
                        
                        break
                        
                if iaToPlay == False:
                    self.ClientToPlay.settimeout(None)
                    dataRecvArray = self.ClientToPlay.recv(4096)
                    dataRecvClient = pickle.loads(dataRecvArray)
                    
                    self.serverToPlay.changePlayerToPlay()
                
                    if dataRecvClient[2] == 0:
                        self.board.movement.move(int(dataRecvClient[0]),int(dataRecvClient[1]))
                        self.board.resetPossibleCaseMovement() 
                        self.board.refreshCurrentPlayer()
                        
                        if self.board.victory():
                            self.board.windowVictory()
                            break
                        else:
                            self.board.refreshCurrentPlayer()
                            if self.board.victory():
                                self.board.windowVictory()
                                break
                            else:
                                self.board.refreshCurrentPlayer()
                                if self.board.victory():
                                    self.board.windowVictory()
                                    break
                                else:
                                    self.board.refreshCurrentPlayer()
                                    if self.board.victory():
                                        self.board.windowVictory()
                                        break
                                    else:
                                        self.board.refreshCurrentPlayer()
                                        if self.serverToPlay.getPlayerToPlay() == 0:
                                            self.board.refreshPossibleCaseMovementForCurrentPlayer()
                                        self.board.displayBoard(False)
                        
                    elif dataRecvClient[2] == 1:
                        self.board.fenceStructure.buildFenceNetwork(int(dataRecvClient[0]),int(dataRecvClient[1]), int(dataRecvClient[3]))
                        if self.board.movement.fenceNotCloseAccesGoal() == False :
                            self.board.fenceStructure.deBuildFence(int(dataRecvClient[0]),int(dataRecvClient[1]))
                        else:
                            self.board.resetPossibleCaseMovement() 
                            self.board.refreshCurrentPlayer()
                            if self.serverToPlay.getPlayerToPlay() == 0:
                                self.board.refreshPossibleCaseMovementForCurrentPlayer()
                            self.board.displayBoard(False)
                            
                    self.sendInfosToClients(dataRecvClient)
                iaToPlay = False
                
            except Exception as e:
                if not None in self.diconnectPlayers:
                    self.diconnectPlayers[self.numClientActive] = "Bot"