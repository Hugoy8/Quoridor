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
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                exit()
            
            (socket_client, (ip, self.port)) = self.socketServer.accept()
            
            if self.typeGame == 4:
                self.socketClients.append(socket_client)
                print(self.socketClients)
            
            treading_server = ClientThread(ip, self.port, socket_client, self.typeGame, self.players, self.playerPlayed, self.socketServer)
            
            # Variable qui stocke la class du jeu.
            Network = True
            self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, treading_server, "instance")

            treading_server.startThread(self.board)
            self.players[0] += 1
        
        threading_graphique = Graphique(self.board)
        threading_graphique.start()

class ClientThread(threading.Thread):
    def __init__(self, host : str, port : int, socket_client : socket, typeGame : str, playersList : list, playerPlayed : int, socketServer : socket) -> None:
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
        
        # Variable qui stocke la class de jeu.
        self.board = None
        
        print("[+] Nouveau thread crée pour le client sur "+str(self.host)+":"+str(self.port))
        
    def startThread(self, boardInfos : object) -> None:
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
                self.serverStop()
                    
            
            if self.typeGameThread == 2:
                # Envoie du tableau de base avec le changement côté serveur à tous les joueurs (Le premier coup du premier joueur de la partie, soit le serveur)

                dataPositionX = input('\nAvancer de combien de case en X : ')
                dataPositionY = input('\nAvancer de combien de case en Y : ')
                
                self.board.move(int(dataPositionX),int(dataPositionY))
                self.board.resetPossibleCaseMovement() 
                self.board.refreshCurrentPlayer()
                self.board.refreshPossibleCaseMovementForCurrentPlayer()
                self.board.displayBoard()

                
                
                DataMove = (
                    [int(dataPositionX), int(dataPositionY)])
                dataSendtable = pickle.dumps(DataMove)
                
                try:
                    self.socket_client.send(dataSendtable)
                    time.sleep(1)
                except socket.error:
                    print("Erreur d'envoie du tableau ...")
                    print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                    self.socket_client.close()
                    self.serverStop()
                
                
                while True:
                    print('\nEn attente du joueur 2')
                    dataRecvArray = self.socket_client.recv(4096)
                    dataRecvClient = pickle.loads(dataRecvArray)
                    print("\nC'est à votre tour !")
                    print('\nVoici le tableau reçu du second joueur : ')
                    
                    print(dataRecvClient)
                        
                    self.board.move(int(dataRecvClient[0]),int(dataRecvClient[1]))
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshCurrentPlayer()
                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                    self.board.displayBoard()
                    
                    dataPositionX = input('\nAvancer de combien de case en X : ')
                    dataPositionY = input('\nAvancer de combien de case en Y : ')
                    
                    self.board.move(int(dataPositionX),int(dataPositionY))
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshCurrentPlayer()
                    self.board.refreshPossibleCaseMovementForCurrentPlayer()
                    self.board.displayBoard()
                    
                    DataMove = (
                        [int(dataPositionX), int(dataPositionY)])
                    dataSendArray = pickle.dumps(DataMove)
                    
                    try:
                        self.socket_client.send(dataSendArray)
                    except socket.error:
                        print("Erreur d'envoie du tableau ...")
                        print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
                        self.socket_client.close()
                        self.serverStop()
                    
            else:
                pass
                # while True:
                #     if self.playerPlayedThread == 1:
                #         print('\nEn attente du joueur 4')
                #         dataRecvArray = self.socket_client.recv(4096)
                #         dataRecvClient = pickle.loads(dataRecvArray)
                #         print("\nC'est à votre tour !")
                #         print('\nVoici le tableau reçu par les autres joueurs : ')
                        
                #         for j in range(len(dataRecvClient)):
                #             print(dataRecvClient[j])
                            
                #         dataPositionX = input('\nEntrez les nouvelles coordonnées X de votre pion : ')
                #         dataPositionY = input('\nEntrez les nouvelles coordonnées Y de votre pion : ')

                #         dataRecvClient[dataPositionY][dataPositionX] = ('P'+self.playerPlayedThread)
                #         dataSendArray = pickle.dumps(dataRecvClient)
                        
                #         try:
                #             self.socket_client.send(dataSendArray)
                #         except socket.error:
                #             print("Erreur d'envoie du tableau ...")
                #             exit()
                        
                #         if self.playerPlayedThread == 2:
                #             self.playerPlayedThread = 1
                #         else:
                #             if self.playerPlayedThread == 4:
                #                 self.playerPlayedThread = 1
                #             else:
                #                 self.playerPlayedThread += 1
                #     else:
                #         print('\nEn attente du joueur ', self.playerPlayedThread)
                #         dataRecvArray = self.socket_client.recv(4096)
                #         dataRecvClient = pickle.loads(dataRecvArray)
                #         print("\nC'est au tour du joueur ", self.playerPlayedThread)
                #         print('\nVoici le tableau du joueur ', self.playerPlayedThread, ' : ')
                        
                #         for j in range(len(dataRecvClient)):
                #             print(dataRecvClient[j])
                        
                #         if self.playerPlayedThread == 2:
                #             self.playerPlayedThread = 1
                #         else:
                #             if self.playerPlayedThread == 4:
                #                 self.playerPlayedThread = 1
                #             else:
                #                 self.playerPlayedThread += 1
        except:
            print("\nLe client %s:%s s'est déconnecté" % (self.host, self.port))
            self.socket_client.close()
            self.serverStop()
        
    def SendBoard(self, x : int, y : int) -> None:
        print(x, y)
    
    def serverStop(self) -> None:
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
        self.board = Board(size, nb_players , nb_IA, nb_fences, mapID, Network, client, "socket")
        
        threading_client = Client(client, self.board)
        threading_client.start()
        
        threading_graphique = Graphique(self.board)
        threading_graphique.start()
        

class Client(threading.Thread):
    def __init__(self, client : socket, boardInfos : object) -> None:
        threading.Thread.__init__(self, group=None, target=self.runClient, args=(client,))
        
        # Variable qui stocke la class de jeu.
        self.board = boardInfos
        
    def runClient(self, client : socket) -> None:
        # Réception des informations d'enregistrement côté serveur.
        dataRecvInfos = client.recv(4096)
        self.Infos = pickle.loads(dataRecvInfos)
        print('\nVoici les informations d\'enregistrement reçu par le serveur : ', self.Infos)
        
        if self.Infos[0] == 2:
            while True:
                print('\nEn attente du joueur 1')
                dataRecvArray = client.recv(4096)
                dataRecvServer = pickle.loads(dataRecvArray)
                print("\nC'est à votre tour !")
                print('\nVoici le tableau reçu par le premier joueur : ')
                
                print(dataRecvServer)
                
                self.board.move(int(dataRecvServer[0]),int(dataRecvServer[1]))
                self.board.resetPossibleCaseMovement() 
                self.board.refreshCurrentPlayer()
                self.board.refreshPossibleCaseMovementForCurrentPlayer()
                self.board.displayBoard()
                    
                    
                dataPositionX = input('\nAvancer de combien de case en X : ')
                dataPositionY = input('\nAvancer de combien de case en Y : ')
                
                self.board.move(int(dataPositionX),int(dataPositionY))
                self.board.resetPossibleCaseMovement() 
                self.board.refreshCurrentPlayer()
                self.board.refreshPossibleCaseMovementForCurrentPlayer()
                self.board.displayBoard()
                
                DataMove = (
                    [int(dataPositionX), int(dataPositionY)])
                dataSendArray = pickle.dumps(DataMove)
                
                try:
                    client.send(dataSendArray)
                except socket.error:
                    print("Erreur d'envoie du tableau ...")
                    exit()
                    
                if self.Infos[2] == 2:
                    self.Infos[2] = 1
                else:
                    if self.Infos[2] == 4:
                        self.Infos[2] = 1
                    else:
                        self.Infos[2] += 1
                                
            client.close()
        else:
            pass
            # while True:
            #     if self.Infos[2] == self.Infos[1][0]:
            #         print('\nEn attente du joueur')
            #         dataRecvArray = client.recv(4096)
            #         array_test = pickle.loads(dataRecvArray)
            #         print("\nC'est à votre tour !")
            #         print('\nVoici le tableau reçu par les autres joueurs : ')
                    
            #         for j in range(len(array_test)):
            #             print(array_test[j])
                        
            #         dataPositionX = input('\nEntrez les nouvelles coordonnées X de votre pion : ')
            #         dataPositionY = input('\nEntrez les nouvelles coordonnées Y de votre pion : ')
                    
            #         array_test[int(dataPositionY)][int(dataPositionX)] = ('P'+str(self.Infos[2]))
            #         dataSendArray = pickle.dumps(array_test)
                    
            #         try:
            #             client.send(dataSendArray)
            #         except socket.error:
            #             print("Erreur d'envoie du tableau ...")
            #             exit()
                        
            #         if self.Infos[2] == 2:
            #             self.Infos[2] = 1
            #         else:
            #             if self.Infos[2] == 4:
            #                 self.Infos[2] = 1
            #             else:
            #                 self.Infos[2] += 1
                    
            #     else:
            #         print('En attente du joueur ', self.Infos[2])
            #         dataRecvArray = client.recv(4096)
            #         array_test = pickle.loads(dataRecvArray)
            #         print("\nC'est au tour du joueur ", self.Infos[2])
            #         print('\nVoici le tableau du joueur ', self.Infos[2], ' : ')
                    
            #         for j in range(len(array_test)):
            #             print(array_test[j])
                        
            #         if self.Infos[2] == 2:
            #             self.Infos[2] = 1
            #         else:
            #             if self.Infos[2] == 4:
            #                 self.Infos[2] = 1
            #             else:
            #                 self.Infos[2] += 1
            # client.close()

class Graphique(threading.Thread):
    def __init__(self, boardInfo : object) -> None:
        threading.Thread.__init__(self)
        #Variable qui stocke la class de jeu.
        self.board = boardInfo
        
        MainThread(self.runGraphique())
    
    def runGraphique(self) -> None:
        print(self.board)
        self.board.start()
        self.board.refreshPossibleCaseMovementForCurrentPlayer()
        self.board.displayBoard()
        mainloop()
        

def SendBoardClient(x : int, y : int, client : socket) -> None:
        print(x, y)
        print(client)

def joinSession(ip : str, port : int) -> None:
    ClientConfig(ip, port, 5, 2, 0, 8, 1)


def startSession(port : int, nbr_player : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
    Server("", port, nbr_player, size, nb_players , nb_IA, nb_fences).server_config(size, nb_players, nb_IA, nb_fences, mapID)
    

#startSession(8000, 2, 5, 2, 0, 8, 1)

ClientConfig("10.128.173.188", 8000, 5, 2, 0, 8, 2)
