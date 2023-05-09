import socket
import threading
import pickle
import time
from main import*
import tkinter as tk


def MainThread(callback):
    root = tk.Tk()
    root.withdraw()
    root.after(0, callback)
    root.mainloop()
    
    
class Server:
    def __init__(self, host, port, typeGame):
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
        else:
            print('Nombre de joueur de la partie non valide')
            exit()

        
    def server_config(self):
        # Variable du socket du client.
        socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Recupération de l'ip du pc qui souhaite héberger un serveur.
        ip = ([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")][0])
        print("Voici l'ip d'hébergement du serveur de jeu : "+str(ip))
        
        # Attribution du port et de l'adresse ip.
        try: 
            socket_server.bind((ip,self.port))
        except socket.error:
            print("[-] Erreur pendant le lancement du serveur.")
            exit()

        while self.players[0] < self.typeGame:
            # Ecoute du serveur sur le réseau.
            try:
                socket_server.listen(10)
                print("Le serveur est démarée et sur écoute ...")
            except socket.error:
                print("[-] Erreur pendant le lancement du serveur.")
                exit()
            
            (socket_client, (ip, self.port)) = socket_server.accept()
            
            if self.typeGame == 4:
                self.socketClients.append(socket_client)
                print(self.socketClients)
            
            treading_server = ClientThread(ip, self.port, socket_client, self.typeGame, self.players, self.playerPlayed)
            treading_server.start()
            self.players[0] += 1
        
        threading_graphique = Graphique(5, 2, 0, 8)
        threading_graphique.start()

class ClientThread(threading.Thread):
    def __init__(self, host, port, socket_client, typeGame, playersList, playerPlayed):
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
        
        print("[+] Nouveau thread crée pour le client sur "+str(self.host)+":"+str(self.port))

    def run(self): 
        
        print("Connexion du client %s:%s" % (self.host, self.port))

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
            exit()
                
        
        if self.typeGameThread == 2:
            # Envoie du tableau de base avec le changement côté serveur à tous les joueurs (Le premier coup du premier joueur de la partie, soit le serveur)
            array_test = (
                [['P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0'],
                ['F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0'],
                ['P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0'],
                ['F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0'],
                ['P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0'],
                ['F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0'],
                ['P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0', 'F0', 'P0'],
                ['F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0', 'B0', 'F0'],
                ['P0', 'F0', 'P0', 'F0', 'P2', 'F0', 'P0', 'F0', 'P0']])
            
            dataPositionX = input('\nEntrez les nouvelles coordonnées X de votre pion : ')
            print("testX")
            dataPositionY = input('\nEntrez les nouvelles coordonnées Y de votre pion : ')
            print("testY")
            
            array_test[int(dataPositionY)][int(dataPositionX)] = 'P1'
            
            dataSendtable = pickle.dumps(array_test)
            
            try:
                self.socket_client.send(dataSendtable)
                time.sleep(1)
            except socket.error:
                print("Erreur d'envoie du tableau ...")
                exit()
            
            
            while True:
                print('\nEn attente du joueur 2')
                dataRecvArray = self.socket_client.recv(4096)
                dataRecvClient = pickle.loads(dataRecvArray)
                print("\nC'est à votre tour !")
                print('\nVoici le tableau reçu du second joueur : ')
                
                for j in range(len(dataRecvClient)):
                    print(dataRecvClient[j])
                    
                dataPositionX = input('\nEntrez les nouvelles coordonnées X de votre pion : ')
                dataPositionY = input('\nEntrez les nouvelles coordonnées Y de votre pion : ')

                dataRecvClient[int(dataPositionY)][int(dataPositionX)] = 'P1'
                dataSendArray = pickle.dumps(dataRecvClient)
                
                try:
                    self.socket_client.send(dataSendArray)
                except socket.error:
                    print("Erreur d'envoie du tableau ...")
                    exit()
                
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


class Client:
    def __init__(self, host, port):
        # Variable de l'adresse ip de connexion.
        self.host = host
        # Variable du port de connexion.
        self.port = port
        # Liste qui stocke tous les messages reçu de la part du serveur.
        self.total_message = []
        # Liste qui contient toutes les informations d'enregistrement reçu par le serveur.
        self.Infos = []
    
    def client_config(self):
        # Variable du socket du client.
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client.connect((self.host, self.port))
        except socket.error:
            print("\nErreur de connexion au serveur "+str(self.host)+":"+str(self.port))
            print("\n\nTentaive de reconnection ...\n")
            Client(self.host, self.port).client_config()
        
        print("\nConnexion reussie au serveur "+str(self.host)+":"+str(self.port))
        
        # Réception des informations d'enregistrement côté serveur.
        dataRecvInfos = client.recv(4096)
        self.Infos = pickle.loads(dataRecvInfos)
        print('\nVoici les informations d\'enregistrement reçu par le serveur : ', self.Infos)
        
        if self.Infos[0] == 2:
            while True:
                print('\nEn attente du joueur 1')
                dataRecvArray = client.recv(4096)
                array_test = pickle.loads(dataRecvArray)
                print("\nC'est à votre tour !")
                print('\nVoici le tableau reçu par le premier joueur : ')
                
                for j in range(len(array_test)):
                    print(array_test[j])
                    
                dataPositionX = input('\nEntrez les nouvelles coordonnées X de votre pion : ')
                dataPositionY = input('\nEntrez les nouvelles coordonnées Y de votre pion : ')
                
                array_test[int(dataPositionY)][int(dataPositionX)] = 'P2'
                dataSendArray = pickle.dumps(array_test)
                
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
    def __init__(self, size, nb_players, nb_IA, nb_fences):
        threading.Thread.__init__(self)
        # Variable de la taille du plateau de jeu.
        self.size = size
        # Variable du nombre de joueurs.
        self.nb_players = nb_players
        # Variable du nombre d'IA.
        self.nb_IA = nb_IA
        # Variable du nombre de barrières au total.
        self.nb_fences = nb_fences
        
        MainThread(self.runGraphique())
    
    def runGraphique(self):
        restartGame(self.size, self.nb_players, self.nb_IA, self.nb_fences)
        mainloop()
        print("TestGraphiqueEnd")

def joinSession(ip, port):
    Instance = Client(ip, port)
    Instance.client_config()

def startSession(port, nbr_player):
    Server("", port, nbr_player).server_config()

# Server("", 8000, 2).server_config()