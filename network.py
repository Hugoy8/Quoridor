import socket
import threading
import pickle
import time
from tkinter import *
import tkinter as tk
from main import Board
from scanNetwork import ScanNetwork
from PIL import Image, ImageTk


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

class ServerThread(threading.Thread):
    def __init__(self, host : str, port : int, socket_client : socket, typeGame : str, playersList : list, playerPlayed : int, socketServer : socket, statusServer : bool, listInfosBoard : list, instanceRoomWaiting : object) -> None:
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
        # L'instance de la class WaitingRoomNetwork.
        self.instanceRoomWaiting = instanceRoomWaiting
        
        # Variable qui stocke la class de jeu.
        self.board = None
        # Liste qui stocke toutes les infos de la board sélectionnées par le serveur.
        self.listInfosBoard = listInfosBoard
        
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
            infoList = ([self.typeGameThread, self.playersThread, self.playerPlayedThread, self.listInfosBoard])
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
                        
                        victory = self.board.victory()
                        if victory == True:
                            self.board.windowVictory()
                        else:
                            self.board.refreshCurrentPlayer()
                            victory = self.board.victory()
                            if victory == True:
                                self.board.windowVictory()
                            else:
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
            # self.instanceRoomWaiting.add()
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
        

class Client(threading.Thread):
    def __init__(self, client : socket, boardInfos : Board, Infos : list) -> None:
        threading.Thread.__init__(self, group=None, target=self.runClient, args=(client,))
        
        # Variable qui stocke la class de jeu.
        self.board = boardInfos
        # Liste qui contient tous les paramètres reçu par le serveur.
        self.Infos = Infos
        
    def runClient(self, client : socket) -> None:
        # Boucle en de jeu en 2 joueurs.
        if self.Infos[0] == 2:
            while True:
                # Réception des informations du serveur.
                dataRecvArray = client.recv(4096)
                dataRecvServer = pickle.loads(dataRecvArray)
                
                # Affichage graphique des changements du serveur.
                if dataRecvServer[2] == 0:
                    self.board.move(int(dataRecvServer[0]),int(dataRecvServer[1]))
                    self.board.resetPossibleCaseMovement() 
                    self.board.refreshCurrentPlayer()
                    
                    victory = self.board.victory()
                    if victory == True:
                        self.board.windowVictory()
                    else:
                        self.board.refreshCurrentPlayer()
                        victory = self.board.victory()
                        if victory == True:
                            self.board.windowVictory()
                        else:
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
        
        
class WaitingRoomNetwork(threading.Thread):
    def __init__(self, role : str, nbr_player_waiting: int) -> None:
        threading.Thread.__init__(self)
        self.window = Tk()
        self.window.title("Quoridor")
        self.window.minsize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.iconbitmap('./assets/logo.ico')
        self.window.configure(bg="#F0B169")
        self.waiting_room1 = None
        self.waiting_room2 = None
        self.nbr_player_waiting = 1
        self.role = role
        
        MainThread(self.waitNetwork(nbr_player_waiting))

    def waitNetwork(self, nbr_player_waiting : int) -> None:
        waiting1 = Image.open(f"./assets/wait1.png")
        waiting1 = waiting1.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.waiting_room1 = ImageTk.PhotoImage(waiting1)

        waiting2 = Image.open(f"./assets/wait2.png")
        waiting2 = waiting2.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.waiting_room2 = ImageTk.PhotoImage(waiting2)

        if self.nbr_player_waiting == 1:
            label = Label(self.window, image=self.waiting_room1)
            label.place(x=0, y=0)
        elif self.nbr_player_waiting == 2:
            label = Label(self.window, image=self.waiting_room2)
            label.place(x=0, y=0)
        if self.role == "server":
            start_game_network = Button(self.window, text="Lancer la partie", bg="#2BB0ED", font=("Arial", 15), fg="white", 
                                    width=self.window.winfo_screenwidth()//70, activebackground="#2BB0ED", activeforeground="white", command=self.add)
            start_game_network.place(x=self.window.winfo_screenwidth()//5, y=self.window.winfo_screenheight()//1.2)
        self.window.mainloop()

    def add(self) -> None:
        if self.nbr_player_waiting == 1:
            self.nbr_player_waiting += 1
        elif self.nbr_player_waiting == 2:
            self.nbr_player_waiting -= 1
        self.waitNetwork(self.nbr_player_waiting)
        
    def destroyWindow(self) -> None:
        self.window.destroy()
        

def joinSession(ip : str, port : int, mapId : int) -> None:
    ClientConfig(ip, port, mapId)


def startSession(port : int, nbr_player : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
    Server("", port, nbr_player).server_config(size, nb_players, nb_IA, nb_fences, mapID)
    
    
# startSession(8000, 2, 5, 2, 0, 8, 2)

# ClientConfig("10.128.173.173", 8000, 1)