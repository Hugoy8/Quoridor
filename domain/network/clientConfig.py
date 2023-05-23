import socket
import pickle
from infrastructure.services.services import Board
from graphique import Graphique
from client import Client

class ClientConfig:
    def __init__(self, host : str, port : int, mapID : int) -> None:
        # Variable de l'adresse ip de connexion.
        self.host = host
        # Variable du port de connexion.
        self.port = port
        # Liste qui stocke tous les messages reçu de la part du serveur.
        self.total_message = []
        # Liste qui contient toutes les informations d'enregistrement reçu par le serveur.
        self.Infos = []
        
        self.client_config(mapID)
    
    def client_config(self, mapID : int) -> None:
        # scanNetwork = ScanNetwork(8000, 8005)
        # scanNetwork.scan()
        # listIp = scanNetwork.getIp()
        # print(listIp)
        
        # Variable du socket du client.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((self.host, self.port))
        except socket.error:
            print("\nErreur de connexion au serveur "+str(self.host)+":"+str(self.port))
            print("\n\nTentaive de reconnection ...\n")
            ClientConfig(self.host, self.port).client_config()
        
        print("\nConnexion reussie au serveur "+str(self.host)+":"+str(self.port))
        
        # Réception des informations d'enregistrement côté serveur.
        dataRecvInfos = client.recv(4096)
        self.Infos = pickle.loads(dataRecvInfos)
        
        # Variable qui stocke la class du jeu.
        Network = True
        if self.Infos[3][1] == 2:
            self.board = Board(self.Infos[3][0], self.Infos[3][1] , self.Infos[3][2], self.Infos[3][3], mapID, Network, client, "socket", 2)
        elif self.Infos[3][1] == 4:
            pass
        
        threading_client = Client(client, self.board, self.Infos)
        threading_client.start()
        
        threading_graphique = Graphique(self.board, "client")
        threading_graphique.start()
        