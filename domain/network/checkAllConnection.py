import threading
import time
import socket
from domain.network.serverPlayers import ServerPlayers


class CheckAllConnection(threading.Thread):
    def __init__(self, serverPlayers : ServerPlayers, serverClass : object) -> None:
        threading.Thread.__init__(self)
        # Variable qui contient l'object de la class ServerPlayers.
        self.serverPlayers = serverPlayers
        # Variable qui contient l'object de la class Server.
        self.serverClass = serverClass
        # Variable qui contient l'état du thread de check.
        self.stateCheck = True
        # Variable qui contient la liste de tous les sockets clients dans le serveur.
        self.listClientsSockets = self.serverClass.listClients
        
        
    def run(self) -> None:
        # Ensemble de gestion de timeout du serveur.+
        self.originalTimeout = None
        possibleCheck = True
        while self.stateCheck:
            for player, socketClient in self.listClientsSockets.items():
                if player != 0 and socketClient != self.serverPlayers.ClientToPlay:
                    
                    for playerDisconnect, typePlayer in self.serverPlayers.diconnectPlayers.items():
                        if player != playerDisconnect:
                            possibleCheck = True
                            break
                        else:
                            possibleCheck = False
                    
                    if possibleCheck:
                        socketClient.settimeout(0.2)
                        try:
                            dataCheck = socketClient.recv(4096)
                            
                            if not dataCheck:
                                raise Exception('Server disconnected')
                            
                            socketClient.settimeout(self.originalTimeout)
                            time.sleep(1)
                        except socket.timeout:
                            continue
                        except Exception as e:
                            self.serverPlayers.diconnectPlayers[player] = "Bot"
                        
                    possibleCheck = True
                        
                        
    def setStateCheck(self, state : bool) -> None:
        self.stateCheck = state
        
        
    def checkDeconnection(self) -> None:
        self.stateCheck = False
        self.socketClient.close()
        
        import time
        time.sleep(2)
        
        self.playError("errorClientOfServer")
        
        
    def playError(self, errorStyle : str) -> None:
        from domain.launcher.launcher import QuoridorLauncher
        
        runError = QuoridorLauncher(errorStyle)