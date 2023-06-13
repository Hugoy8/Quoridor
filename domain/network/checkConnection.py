import threading
import time
import socket
from domain.network.waitingRoomNetwork import WaitingRoomNetwork
from domain.network.server import Server

class CheckConnection(threading.Thread):
    def __init__(self, socketClient : socket, numClient : int, waitingNetwork : WaitingRoomNetwork, serverClass : Server) -> None:
        threading.Thread.__init__(self)
        # Variable qui contient l'instance de la class Server.
        self.socketClient = socketClient
        # Variable qui contient l'état du thread de check.
        self.stateCheck = True
        # Variable qui contient le numéro du client.
        self.numClient = numClient
        # Variable qui contient l'instance de la class WaitingRoomNetwork.
        self.waitingNetwork = waitingNetwork
        # Variable qui contient l'instance de la class Server.
        self.serverClass = serverClass
    
    def run(self) -> None:
        # Ensemble de gestion de timeout du serveur.
        self.originalTimeout = self.socketClient.gettimeout()
        
        while self.stateCheck:
            self.socketClient.settimeout(0.2)
            try:
                dataCheck = self.socketClient.recv(1)
                self.refreshTimeOut()
                
                if not dataCheck:
                    raise Exception('Client disconnected')
                
                time.sleep(1)
            except socket.timeout:
                continue
            except Exception as e:
                if self.waitingNetwork.typeGame == 2:
                    self.waitingNetwork.waitingRoomUi.remove(3)
                elif self.waitingNetwork.typeGame == 4:
                    self.waitingNetwork.waitingRoomUi.remove(0)
                for keyToSocket, socketClientList in self.serverClass.listClients.items():
                    if socketClientList == self.socketClient:
                        del self.serverClass.listClients[keyToSocket]
                        break
                for player in list(self.serverClass.listClients.keys()):
                    if player != 0:
                        if player > self.numClient:
                            newPlayer = player - 1
                            socketClient = self.serverClass.listClients[player]
                            del self.serverClass.listClients[player]
                            self.serverClass.listClients[newPlayer] = socketClient
                            self.refreshNumClient()
                self.sendNewPlayer()
                break
        self.refreshTimeOut()
        
                
    def setStateCheck(self, state : bool) -> None:
        self.stateCheck = state
        

    def refreshTimeOut(self) -> None:
        self.socketClient.settimeout(self.originalTimeout)
        
        
    def refreshNumClient(self) -> None:
        for player, socketClient in self.serverClass.listClients.items():
            if socketClient == self.serverClass.listClients[self.numClient]:
                self.numClient = player
                break
        

    def sendNewPlayer(self) -> None:
        import pickle
        numClient = len(self.serverClass.listClients) + 1
        for player, socketClient in self.serverClass.listClients.items():
            if player != 0 and socketClient != self.socketClient:
                if self.numClient < player+1:
                    infosListAttente = ([True, False, numClient, 0, True, player, 1])
                else:
                    infosListAttente = ([True, False, numClient, 0, True, player, 0])
                dataSendInfosAttente = pickle.dumps(infosListAttente)
                socketClient.send(dataSendInfosAttente)