import socket
from domain.network.graphique import Graphique
from infrastructure.services.services import Board
from domain.network.serverThread import ServerThread
from domain.network.serverPlayers import ServerPlayers
from domain.network.serverToPlay import ServerToPlay
import time
import pickle

class Server:
    def __init__(self, host : str, port : int, typeGame : str) -> None:
        # Variable de l'adresse ip de connexion.
        self.host = host
        # Variable du port de connexion.
        self.port = port
        
        if typeGame == 2 or typeGame == 4:
            # Variable du contient le nombre de joueur du type de partie, soit 2 ou 4.
            self.typeGame = typeGame
        else: 
            self.typeGame = 2
            
        # Liste qui stocke tous les joueurs qui ont rejoins le serveur. A l'index 0, on stocke le nombre de joueur connectée au serveur.
        self.players = [1, 'Server_1']
        # Variable qui stocke le joueur en train de jouer (Un nombre qui correspond à l'index de la liste de joueurs).
        self.playerPlayed = 1
        
        # Variable qui contient l'object de la class qui permet de faire le changement de tour.
        self.serverToPlay = ServerToPlay(self.typeGame)
        
        # Dictionnaire qui stocke les sockets des clients sur le serveur dans l'ordre de leur connection.
        self.listClients = {}
        
        # Variable du socket du serveur.
        self.socketServer = ""

        
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
        
        # Attribution du port et de l'adresse ip.
        try: 
            self.socketServer.bind((ip,self.port))
        except socket.error:
            print("[-] Erreur pendant le lancement du serveur.")
            exit()

        if self.typeGame == 2:
            while self.players[0] < self.typeGame:
                # Ecoute du serveur sur le réseau.
                try:
                    self.socketServer.listen(self.typeGame)
                    print("Le serveur est démarée et sur écoute ...")
                    self.statusServer = True
                except socket.error:
                    print("[-] Erreur pendant le lancement du serveur.")
                    self.statusServer = False
                    exit()
                
                (socket_client, (ip, port)) = self.socketServer.accept()
                
                listInfosBoard = [size, nb_players , nb_IA, nb_fences, mapID]
                treading_server = ServerThread(ip, self.port, socket_client, self.typeGame, self.players, self.playerPlayed, self.socketServer, self.statusServer, listInfosBoard, "")
                
                # Variable qui stocke la class du jeu.
                Network = True
                self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, treading_server, "instance", 1)

                treading_server.startThread(self.board)
                self.players[0] += 1

        elif self.typeGame == 4:
            # Ecoute du serveur sur le réseau.
            try:
                self.socketServer.listen(self.typeGame)
                print("Le serveur est démarée et sur écoute ...")
                self.statusServer = True
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                self.statusServer = False
                exit()
                
            print("En attente des connexions des joueurs...")
            while len(self.listClients) < (self.typeGame - 1):
                (clientSocket, (ip, port))= self.socketServer.accept()
                
                print(f"Joueur connecté : {ip}:{port}")
                numClient = len(self.listClients) + 1
                self.listClients[numClient] = clientSocket
                
                # Attribution d'un numéro au Client, et enregistrement dans une variable.
                numTemp = self.players[0]
                self.players[0] += 1
                textTemp = 'Client_' + str(numTemp+1)
                self.players.append(textTemp)
                
            # Socket Server pour le tour de rôle.
            self.listClients[0] = self.socketServer
            print("Tous les joueurs sont connectés.")

            listInfosBoard = [size, nb_players , nb_IA, nb_fences, mapID]
                
            # Envoie des informations d'enregistrement au client.
            for player, socketClient in self.listClients.items():
                if player != 0:
                    self.players[0] = player+1
                    infoList = ([4, self.players, self.playerPlayed, listInfosBoard])
                    dataSendInfos = pickle.dumps(infoList)
                    try:
                        socketClient.send(dataSendInfos)
                    except socket.error:
                        print("Erreur d'envoie des informations d'enregistrement ...")
                        print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                        socketClient.close()
                        self.socketServer.close()
                    
            # Variable qui stocke la class du jeu.
            Network = True
            self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, self, "instance", 1)

            self.serverPlayers = ServerPlayers(self, self.serverToPlay, self.board)
            self.serverPlayers.start()

        threading_graphique = Graphique(self.board, "server")
        threading_graphique.start()
            
            
    def SendBoard(self, x : int, y : int, typeClick : int, orientation : str) -> None:
        # typeClick = 0 (caseClicked)
        # typeClick = 1 (fenceClicked)
        
        # orientation = 0 (vertical)
        # orientation = 1 (horizontal)
        
        if orientation == "vertical":
            orientation = 0
        else: 
            orientation = 1
        
        for player, socketClient in self.listClients.items():
            if player != 0 and socketClient.fileno() != -1:
                if self.serverToPlay.getPlayerToPlay()+1 == player:
                    messagePlayertoPlay = "You"
                else:
                    messagePlayertoPlay = "NotYou"
                DataMove = ([int(x), int(y), int(typeClick), int(orientation), str(messagePlayertoPlay)])
                dataSendtable = pickle.dumps(DataMove)
                try:
                    socketClient.send(dataSendtable)
                    time.sleep(0.1)
                except socket.error:
                    print("Erreur d'envoie des informations d'enregistrement ...")
                    print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                    socketClient.close()
                    self.socketServer.close()
    
    
    def verifPlayertoPlay(self, player : int) -> str:
        if self.serverToPlay.getPlayerToPlay() == player:
            return "You"
        else:
            return "NotYou"
