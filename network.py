import socket
import threading
import pickle
import time
from tkinter import *
import tkinter as tk
from main import Board


def MainThread(callback : tk) -> None:
    root = tk.Tk()
    root.withdraw()
    root.after(0, callback)
    root.mainloop()
    
    
class Server:
    def __init__(self, host : str, port : int, typeGame : str) -> None:
        if typeGame == 2 or typeGame == 4:
            # Variable de l'adresse ip de connexion.
            self.host = host
            # Variable du port de connexion.
            self.port = port
            # Variable du contient le nombre de joueur du type de partie, soit 2 ou 4.
            self.typeGame = typeGame
            # Liste qui stocke tous les joueurs qui ont rejoins le serveur. A l'index 0, on stocke le nombre de joueur connectée au serveur.
            self.players = [1, 'Server_1']
            # Variable qui stocke le joueur en train de jouer (Un nombre qui correspond à l'index de la liste de joueurs).
            self.playerPlayed = 1
            
            # Liste qui stocke les sockets des clients sur le serveur dans l'ordre de leur connection.
            self.socketClients = []
            
            # Variable du socket du serveur.
            self.socketServer = ""
            
        else:
            print('Nombre de joueur de la partie non valide')
            exit()
        
    def server_config(self, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
        # Variable du socket du client.
        self.socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socketServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
        if self.host == "":
            # Recupération de l'ip du pc qui souhaite héberger un serveur.
            ip = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0])
            print("Voici l'ip d'hébergement du serveur de jeu : "+str(ip))
        else: 
            ip = self.host
        
        print(ip)
        # Attribution du port et de l'adresse ip.
        try: 
            self.socketServer.bind((ip,self.port))
        except socket.error:
            print("[-] Erreur pendant le lancement du serveur.")
            exit()

        while self.players[0] < self.typeGame:
            # Ecoute du serveur sur le réseau.
            try:
                self.socketServer.listen(10)
                print("Le serveur est démarée et sur écoute ...")
                self.statusServer = True
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                self.statusServer = False
                exit()
            
            (socket_client, (ip, self.port)) = self.socketServer.accept()
            
            if self.typeGame == 4:
                self.socketClients.append(socket_client)
                print(self.socketClients)
            
            treading_server = ServerThread(ip, self.port, socket_client, self.typeGame, self.players, self.playerPlayed, self.socketServer, self.statusServer)
            
            # Variable qui stocke la class du jeu.
            Network = True
            self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, treading_server, "instance", 1)

            treading_server.startThread(self.board)
            self.players[0] += 1
        
        threading_graphique = Graphique(self.board, "server")
        threading_graphique.start()

class ServerThread(threading.Thread):
    def __init__(self, host : str, port : int, socket_client : socket, typeGame : str, playersList : list, playerPlayed : int, socketServer : socket, statusServer : bool) -> None:
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
        
        # Variable qui stocke la class de jeu.
        self.board = None
        
        print("[+] Nouveau thread crée pour le client sur "+str(self.host)+":"+str(self.port))
        
    def startThread(self, boardInfos : Board) -> None:
        self.board = boardInfos
        self.start()
        
    def run(self) -> None: 
        
        print("Connexion du client %s:%s" % (self.host, self.port))
        
        try:
            # Attribution d'un numéro au Client, et enregistrement dans une variable.
            if self.typeGameThread == 2:
                self.playersThread = [2, 'Server_1', 'Client_2']
            else:
                numTemp = self.playersThread[0]
                self.playersThread[0] += 1
                textTemp = 'Client_' + str(numTemp+1)
                self.playersThread.append(textTemp)
                
            
            # Envoie des informations d'enregistrement au client.
            infoList = ([self.typeGameThread, self.playersThread, self.playerPlayedThread])
            dataSendInfos = pickle.dumps(infoList)
            try:
                self.socket_client.send(dataSendInfos)
            except socket.error:
                print("Erreur d'envoie des informations d'enregistrement ...")
                print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                self.socket_client.close()
                self.serverStopCrash()
                    
            
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
                        

            else:
                pass
                # Zone 4 joueurs.
        except:
            print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
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
        
        DataMove = (
            [int(x), int(y), int(typeClick), int(orientation)])
        dataSendtable = pickle.dumps(DataMove)
        
        try:
            self.socket_client.send(dataSendtable)
            time.sleep(0.1)
        except socket.error:
            print("Erreur d'envoie du tableau ...")
            print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
            self.socket_client.close()
            self.serverStopCrash()
    
    def serverStopCrash(self) -> None:
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


class ClientConfig:
    def __init__(self, host : str, port : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
        # Variable de l'adresse ip de connexion.
        self.host = host
        # Variable du port de connexion.
        self.port = port
        # Liste qui stocke tous les messages reçu de la part du serveur.
        self.total_message = []
        # Liste qui contient toutes les informations d'enregistrement reçu par le serveur.
        self.Infos = []
        
        self.client_config(size, nb_players, nb_IA, nb_fences, mapID)
    
    def client_config(self, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
        # Variable du socket du client.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((self.host, self.port))
        except socket.error:
            print("\nErreur de connexion au serveur "+str(self.host)+":"+str(self.port))
            print("\n\nTentaive de reconnection ...\n")
            ClientConfig(self.host, self.port).client_config()
        
        print("\nConnexion reussie au serveur "+str(self.host)+":"+str(self.port))
            
        # Variable qui stocke la class du jeu.
        Network = True
        if nb_players == 2:
            self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, client, "socket", 2)
        elif nb_players == 4:
            pass

        threading_client = Client(client, self.board)
        threading_client.start()
        
        threading_graphique = Graphique(self.board, "client")
        threading_graphique.start()
        

class Client(threading.Thread):
    def __init__(self, client : socket, boardInfos : Board) -> None:
        threading.Thread.__init__(self, group=None, target=self.runClient, args=(client,))
        
        # Variable qui stocke la class de jeu.
        self.board = boardInfos
        
    def runClient(self, client : socket) -> None:
        # Réception des informations d'enregistrement côté serveur.
        dataRecvInfos = client.recv(4096)
        self.Infos = pickle.loads(dataRecvInfos)
        print('\nVoici les informations d\'enregistrement reçu par le serveur : ', self.Infos)

        if self.Infos[0] == 2:
            # Boucle de jeu
            while not self.board.victory():
                # Réception des informations du serveur.
                dataRecvArray = client.recv(4096)
                dataRecvServer = pickle.loads(dataRecvArray)
                
                # Affichage graphique des changements du serveur.
                if dataRecvServer[2] == 0:
                    self.board.move(int(dataRecvServer[0]),int(dataRecvServer[1]))
                    self.board.resetPossibleCaseMovement() 
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
            
            # Deconnexion du client du serveur.
            client.close()
            exit()
        else:
            pass
            # Zone 4 joueurs.

class Graphique(threading.Thread):
    def __init__(self, boardInfo : Board, playerUser : str) -> None:
        threading.Thread.__init__(self)
        #Variable qui stocke la class de jeu.
        self.board = boardInfo
        # Variable qui contient le numéro de l'utilisateur.
        self.playerUser = playerUser
        
        MainThread(self.runGraphique())
    
    def runGraphique(self) -> None:
        self.board.start()
        if self.playerUser == "server":
            self.board.refreshPossibleCaseMovementForCurrentPlayer()
        elif self.playerUser == "client":
            pass
        else:
            self.board.refreshPossibleCaseMovementForCurrentPlayer()
        self.board.displayBoard(False)
        mainloop()
        

def joinSession(ip : str, port : int) -> None:
    ClientConfig(ip, port, 5, 2, 0, 8, 1)


def startSession(port : int, nbr_player : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
    Server("", port, nbr_player).server_config(size, nb_players, nb_IA, nb_fences, mapID)
    
    
startSession(8000, 2, 5, 2, 0, 8, 2)

# ClientConfig("10.128.173.190", 8000, 5, 2, 0, 8, 2)