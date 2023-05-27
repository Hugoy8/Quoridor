import socket
import pickle
from infrastructure.services.services import Board
from domain.network.graphique import Graphique
from domain.network.client import Client
from domain.network.waitingRoomNetwork import WaitingRoomNetwork
from domain.network.waitingRoomUi import WaitingRoomUi
import time

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
        # Variable du socket du client.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        try:
            client.connect((self.host, self.port))
        except socket.error:
            print("\nErreur de connexion au serveur "+str(self.host)+":"+str(self.port))
            print("\n\nTentaive de reconnection ...\n")
            ClientConfig(self.host, self.port).client_config()
        
        # Réception des informations d'enregistrement côté serveur et de salle d'attente.
        dataRecvServer = client.recv(4096)
        self.InfosAttente = pickle.loads(dataRecvServer)
        
        # Section salle d'attente.
        try:
            waitingRoomUI = WaitingRoomUi("Client", self.InfosAttente[0], self.InfosAttente[1], "")
            waitingRoomNetwork = WaitingRoomNetwork("Client", waitingRoomUI, self.InfosAttente[0], self.InfosAttente[1], client, "")
            waitingRoomUI.setWaitingRoomNetwork(waitingRoomNetwork)
            waitingRoomNetwork.start()
            waitingRoomUI.waitNetwork()
        except:
            import main
            main()
        
        while waitingRoomUI.status == True:
            time.sleep(0.5)
        
        # Réception des informations d'enregistrement côté serveur.
        dataRecvInfos = client.recv(4096)
        self.Infos = pickle.loads(dataRecvInfos)
        
        # Variable qui stocke la class du jeu.
        Network = True
        if self.Infos[3][1] == 2:
            self.board = Board(self.Infos[3][0], self.Infos[3][1] , self.Infos[3][2], self.Infos[3][3], mapID, Network, client, "socket", 2)
        elif self.Infos[3][1] == 4:
            self.board = Board(self.Infos[3][0], self.Infos[3][1] , self.Infos[3][2], self.Infos[3][3], mapID, Network, client, "socket", self.Infos[1][0])
        
        try:
            threading_client = Client(client, self.board, self.Infos)
            threading_client.start()
        except:
            import main
            main()
        
        threading_graphique = Graphique(self.board, "client")
        threading_graphique.start()
        