import threading
from domain.network.waitingRoomUi import WaitingRoomUi
import socket
import pickle
import pygame


class WaitingRoomNetwork(threading.Thread):
    def __init__(self, role : str, waitingRoomUi : WaitingRoomUi, typeGame : int, numClient : int, userSocket : socket, serverClass : object) -> None:
        threading.Thread.__init__(self)
        # Variable qui va contenir le type de joueur (client ou server).
        self.role = role
        # Variable qui contient l'object de la class WaitingRoomUi.
        self.waitingRoomUi = waitingRoomUi
        
        # Variable qui permet de stocker l'état de la fenêtre de la salle d'attente.
        self.__stateWindow = True
        
        # Variable qui contient le type de partie (2 ou 4 joueurs).
        self.typeGame = typeGame
        # Variable qui contient le numéro du client.
        self.numClient = numClient
        
        if self.role == "Client":
            # Variable du socket utilisateur.
            self.userSocket = userSocket
        
        # Variable qui contient la liste des joueurs dans la salle d'attente.
        if self.role == "Server":
            # Variable qui contient l'object de la class Server.
            self.serverClass = serverClass
            self.listPlayers = []
            self.listPlayers.append("Server_1")


    def run(self) -> None:
        if self.role == "Server":
            self.serverWaiting()
        elif self.role == "Client":
            self.clientWaiting()
    
    
    def addClient(self, numClient : int) -> None:
        self.listPlayers.append("Client_" + str(numClient))
    
    
    def getListPlayers(self) -> list:
        return self.listPlayers
    
    
    def setStateWindow(self, choice : bool) -> None:
        self.__stateWindow = choice
        
        
    def serverWaiting(self) -> None:
        if self.typeGame == 4:
            print("En attente des connexions des joueurs...")
            while len(self.serverClass.listClients) < (self.serverClass.typeGame - 1):
                (clientSocket, (ip, port))= self.serverClass.socketServer.accept()
                
                print(f"Joueur connecté : {ip}:{port}")
                numClient = len(self.serverClass.listClients) + 1
                self.serverClass.listClients[numClient] = clientSocket
                
                # Attribution d'un numéro au Client, et enregistrement dans une variable.
                numTemp = self.serverClass.players[0]
                self.serverClass.players[0] += 1
                textTemp = 'Client_' + str(numTemp+1)
                self.serverClass.players.append(textTemp)
                
                self.waitingRoomUi.add()
                
                # Envoie des informations d'enregistrement
                infosList = ([4, numClient])
                dataSendInfos = pickle.dumps(infosList)
                clientSocket.send(dataSendInfos)
                
                for player, socketClient in self.serverClass.listClients.items():
                    if player != 0 and player != numClient:
                        try:
                            # Envoie du status de la salle d'attente au client.
                            infosListAttente = ([True, True, numClient, player])
                            dataSendInfosAttente = pickle.dumps(infosListAttente)
                            socketClient.send(dataSendInfosAttente)
                        except socket.error:
                            print("Erreur d'envoie des informations d'enregistrement ...")
                            print("\nLe client %s:%s s'est déconnecté" % (self.serverClass.host, self.serverClass.port))
                            socketClient.close()
                            self.serverClass.socketServer.close()
                            
        elif self.typeGame == 2:
            # Ecoute du serveur sur le réseau.
            try:
                self.serverClass.socketServer.listen(self.typeGame)
                print("Le serveur est démarée et sur écoute ...")
                self.serverClass.statusServer = True
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                self.serverClass.statusServer = False
                exit()
            
            (socket_client, (ip, port)) = self.serverClass.socketServer.accept()
            
            # Envoie des informations d'enregistrement
            infosList = ([2, 1])
            dataSendInfos = pickle.dumps(infosList)
            socket_client.send(dataSendInfos)
            
            self.waitingRoomUi.add()
            
            self.socketClient = socket_client
                    
    
    
    def serverSendLaunch(self):
        if self.typeGame == 4:
            # Envoie du status de la salle d'attente au client.
            infosListAttente = ([False, False, 0, 0])
            dataSendInfosAttente = pickle.dumps(infosListAttente)
                        
            for player, socketClient in self.serverClass.listClients.items():
                if player != 0:
                    try:
                        socketClient.send(dataSendInfosAttente)
                    except socket.error:
                        print("Erreur d'envoie des informations d'enregistrement ...")
                        print("\nLe client %s:%s s'est déconnecté" % (self.serverClass.host, self.serverClass.port))
                        socketClient.close()
                        self.serverClass.socketServer.close()
        elif self.typeGame == 2:
            # Envoie du status de la salle d'attente au client.
            infosListAttente = ([False, False, 0, 0])
            dataSendInfosAttente = pickle.dumps(infosListAttente)
            
            try:
                self.socketClient.send(dataSendInfosAttente)
            except socket.error:
                print("Erreur d'envoie des informations d'enregistrement ...")
                print("\nLe client %s:%s s'est déconnecté" % (self.serverClass.host, self.serverClass.port))
                self.socketClient.close()
                self.serverClass.socketServer.close()
                            
                            
    def clientWaiting(self) -> None:
        while self.__stateWindow:
            dataRecvServer = self.userSocket.recv(4096)
            InfosAttente = pickle.loads(dataRecvServer)
            
            if InfosAttente[1] == True and InfosAttente[0] == True:
                if self.typeGame == 4:
                    self.waitingRoomUi.add()

            self.setStateWindow(InfosAttente[0])
        
        self.waitingRoomUi.status = False