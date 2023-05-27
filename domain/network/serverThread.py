import threading
import socket
import pickle
from infrastructure.services.services import Board
import time

class ServerThread(threading.Thread):
    def __init__(self, host : str, port : int, socket_client : socket, typeGame : str, playersList : list, playerPlayed : int, socketServer : socket, statusServer : bool, instanceRoomWaiting : object) -> None:
        threading.Thread.__init__(self)
        # Variable de l'adresse ip de connexion.
        self.host = host
        # Variable du port de connexion.
        self.port = port 
        
        # Variable du socket du client.
        self.socket_client = socket_client
        # Liste qui stocke tous les messages reçu de la part du serveur.
        self.total_message = []
        
        # Variable du contient le nombre de joueur du type de partie, soit 2 ou 4.
        self.typeGameThread = typeGame
        # Liste qui stocke tous les joueurs qui ont rejoins le serveur. A l'index 0, on stocke le nombre de joueur connectée au serveur.
        self.playersThread = playersList
        # Variable qui stocke le joueur en train de jouer (Un nombre qui correspond à l'index de la liste de joueurs).
        self.playerPlayedThread = playerPlayed
        
        # Varaible du socket du serveur.
        self.socketServer = socketServer
        # Variable booléenne qui sauvegarde l'état du serveur.
        self.statusServer = statusServer
        # L'instance de la class WaitingRoomNetwork.
        self.instanceRoomWaiting = instanceRoomWaiting
        
        # Variable qui stocke la class de jeu.
        self.board = None
        
        print("[+] Nouveau thread crée pour le client sur "+str(self.host)+":"+str(self.port))
        
    def startThread(self, boardInfos : Board) -> None:
        self.board = boardInfos
        self.start()
        
    def run(self) -> None: 
        
        print("Connexion du client %s:%s" % (self.host, self.port))
        
        try:
            if self.typeGameThread == 2:
                # Boucle de jeu
                while self.statusServer == True:
                    # Réception des informations du client.
                    dataRecvArray = self.socket_client.recv(4096)
                    dataRecvClient = pickle.loads(dataRecvArray)
                    
                    # Affichage graphique des changements du client.
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
                                self.board.refreshPossibleCaseMovementForCurrentPlayer()
                                self.board.displayBoard(False)
                            
                    elif dataRecvClient[2] == 1:
                        self.board.buildFenceNetwork(int(dataRecvClient[0]),int(dataRecvClient[1]), int(dataRecvClient[3]))
                        if self.board.fenceNotCloseAccesGoal() == False :
                            self.board.deBuildFence(int(dataRecvClient[0]),int(dataRecvClient[1]))
                        else :
                            self.board.resetPossibleCaseMovement() 
                            self.board.refreshCurrentPlayer()
                            self.board.refreshPossibleCaseMovementForCurrentPlayer()
                            self.board.displayBoard(False)
                    else:
                        print("Erreur de type de click")
        except:
            if self.typeGameThread == 2:
                print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                # self.instanceRoomWaiting.add()
                self.socket_client.close()
                self.serverStopCrash()
        
    def SendBoard(self, x : int, y : int, typeClick : int, orientation : str) -> None:
        # typeClick = 0 (caseClicked)
        # typeClick = 1 (fenceClicked)
        
        # orientation = 0 (vertical)
        # orientation = 1 (horizontal)
        
        
        if orientation == "vertical":
            orientation = 0
        else: 
            orientation = 1
        
        DataMove = ([int(x), int(y), int(typeClick), int(orientation)])
        dataSendtable = pickle.dumps(DataMove)
        
        if self.typeGameThread == 2:
            try:
                self.socket_client.send(dataSendtable)
                time.sleep(0.1)
            except socket.error:
                print("Erreur d'envoie du tableau ...")
                print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                self.socket_client.close()
                self.serverStopCrash()
    
    def serverStopCrash(self) -> None:
        self.statusServer = False
        print("Arrêt du serveur Crash...")
        self.board.displayBoard(True)
        time.sleep(1)
        self.socketServer.close()
        exit()
        
    def serverStop(self) -> None:
        # Deconnexion des clients et arrêt du serveur.
        self.statusServer = False
        print("Arrêt du serveur ...")
        self.socketServer.close()
        exit()
