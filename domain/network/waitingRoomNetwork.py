import threading
from domain.network.waitingRoomUi import WaitingRoomUi
import socket
import pickle


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
        
    
    def refreshTimeOut(self) -> None:
        self.serverClass.socketServer.settimeout(self.serverClass.originalTimeout)
        
        
    def serverWaiting(self) -> None:
        if self.typeGame == 4:
            self.listCheckConnections = {}
            
            while self.serverClass.stateListenServer:
                self.serverClass.socketServer.settimeout(0.2)
                try:
                    (clientSocket, (ip, port))= self.serverClass.socketServer.accept()
                    
                    if len(self.serverClass.listClients) == 3:
                        clientSocket.send("Full".encode('utf-8'))
                        clientSocket.close()
                        continue
                    else:
                        messageAutorisation = "OK"
                        messageAutorisation = messageAutorisation.encode("utf-8")
                        clientSocket.send(messageAutorisation)
                        
                    self.refreshTimeOut()
                
                    numClient = len(self.serverClass.listClients) + 1
                    self.serverClass.listClients[numClient] = clientSocket
                    
                    # Attribution d'un numéro au Client, et enregistrement dans une variable.
                    numTemp = self.serverClass.players[0]
                    self.serverClass.players[0] += 1
                    textTemp = 'Client_' + str(numTemp+1)
                    self.serverClass.players.append(textTemp)
                    
                    from domain.network.checkConnection import CheckConnection
                    self.checkAlgorithm = CheckConnection(clientSocket, numClient, self, self.serverClass)
                    self.listCheckConnections[numClient] = self.checkAlgorithm
                    self.checkAlgorithm.start()
                    
                    self.waitingRoomUi.add()
                    
                    # Envoie des informations d'enregistrement
                    infosList = ([4, numClient])
                    dataSendInfos = pickle.dumps(infosList)
                    clientSocket.send(dataSendInfos)
                    
                    for player, socketClient in self.serverClass.listClients.items():
                        if player != 0 and player != numClient:
                                # Envoie du status de la salle d'attente au client.
                                infosListAttente = ([True, True, numClient, player, False])
                                dataSendInfosAttente = pickle.dumps(infosListAttente)
                                socketClient.send(dataSendInfosAttente)
                except socket.timeout:
                    continue
            self.refreshTimeOut()
            self.disableStateCheck()
            
        elif self.typeGame == 2:
            # Ecoute du serveur sur le réseau.
            try:
                self.serverClass.socketServer.listen(400)
                self.serverClass.statusServer = True
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                self.serverClass.statusServer = False
                exit()
            
            self.listCheckConnections = {}
            
            while self.serverClass.stateListenServer:
                self.serverClass.socketServer.settimeout(0.2)
                try:
                    (socket_client, (ip, port)) = self.serverClass.socketServer.accept()
                    
                    if len(self.serverClass.listClients) == 1:
                        socket_client.send("Full".encode('utf-8'))
                        socket_client.close()
                        continue
                    else:
                        messageAutorisation = "OK"
                        messageAutorisation = messageAutorisation.encode("utf-8")
                        socket_client.send(messageAutorisation)
                    
                    numClient = len(self.serverClass.listClients) + 1
                    self.serverClass.listClients[numClient] = socket_client
                    
                    # Envoie des informations d'enregistrement
                    infosList = ([2, 1])
                    dataSendInfos = pickle.dumps(infosList)
                    socket_client.send(dataSendInfos)
                    
                    from domain.network.checkConnection import CheckConnection
                    self.checkAlgorithm = CheckConnection(socket_client, 1, self, self.serverClass)
                    self.listCheckConnections[1] = self.checkAlgorithm
                    self.checkAlgorithm.start()
                    
                    self.waitingRoomUi.add()
                    
                    self.socketClient = socket_client
                except socket.timeout:
                    continue
            self.refreshTimeOut()
            self.disableStateCheck()
    
    
    def serverSendLaunch(self) -> None:
        if self.typeGame == 4:
            # Envoie du status de la salle d'attente au client.
            infosListAttente = ([False, False, 0, 0, False])
            dataSendInfosAttente = pickle.dumps(infosListAttente)
                        
            for player, socketClient in self.serverClass.listClients.items():
                if player != 0:
                    socketClient.send(dataSendInfosAttente)
                        
        elif self.typeGame == 2:
            # Envoie du status de la salle d'attente au client.
            infosListAttente = ([False, False, 0, 0, False])
            dataSendInfosAttente = pickle.dumps(infosListAttente)
            
            self.socketClient.send(dataSendInfosAttente)

                            
                            
    def clientWaiting(self) -> None:
        while self.__stateWindow:
            try:
                dataRecvServer = self.userSocket.recv(4096)
                InfosAttente = pickle.loads(dataRecvServer)
                
                if InfosAttente[1] == True and InfosAttente[0] == True:
                    if self.typeGame == 4:
                        self.waitingRoomUi.add()

                if InfosAttente[4] == True:
                    
                    self.waitingRoomUi.remove(int(InfosAttente[6]))
                    self.waitingRoomUi.setNumClient(InfosAttente[5])
                    self.waitingRoomUi.configPictures()
                    
                
                self.setStateWindow(InfosAttente[0])
            except:
                print("Le serveur s'est déconnectée pendant la salle d'attente.")
                self.waitingRoomUi.destroyWindow()
                self.userSocket.close()
                import main
                main()
                break
        
        self.waitingRoomUi.status = False
        
    
    def disableStateCheck(self):
        for checkClass in self.listCheckConnections.values():
            checkClass.setStateCheck(False)
            
            
    def stopAllThread(self):
        for checkAlgorithm in self.listCheckConnections.values():
            if checkAlgorithm.is_alive():
                checkAlgorithm.join()