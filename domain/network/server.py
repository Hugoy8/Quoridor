import socket
from domain.network.graphique import Graphique
from infrastructure.services.services import Board
from domain.network.serverThread import ServerThread

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
        
        # Attribution du port et de l'adresse ip.
        try: 
            self.socketServer.bind((ip,self.port))
        except socket.error:
            print("[-] Erreur pendant le lancement du serveur.")
            exit()

        # self.waitingRoom = WaitingRoomNetwork("server", 1)
        # self.waitingRoom.start()
        
        while self.players[0] < self.typeGame:
            # Ecoute du serveur sur le réseau.
            try:
                self.socketServer.listen(10)
                print("Le serveur est démarée et sur écoute ...")
                self.statusServer = True
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                # self.waitingRoom.destroyWindow()
                self.statusServer = False
                exit()
            
            (socket_client, (ip, self.port)) = self.socketServer.accept()
            
            if self.typeGame == 4:
                self.socketClients.append(socket_client)
                print(self.socketClients)
            
            
            listInfosBoard = [size, nb_players , nb_IA, nb_fences, mapID]
            treading_server = ServerThread(ip, self.port, socket_client, self.typeGame, self.players, self.playerPlayed, self.socketServer, self.statusServer, listInfosBoard, "")
            
            # Variable qui stocke la class du jeu.
            Network = True
            self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, treading_server, "instance", 1)

            treading_server.startThread(self.board)
            self.players[0] += 1
            # self.waitingRoom.add()
        
        threading_graphique = Graphique(self.board, "server")
        threading_graphique.start()