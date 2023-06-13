import pygame
from pygame.locals import *
from PIL import Image
import ctypes
import time
import os
import pygame.mouse


class WaitingRoomUi:
    def __init__(self, role: str, numPlayers: int, numClient: int, serverClass : object) -> None:
        # Zone de récupération de la taille écran en fonction de l'os.
        if os.name == "nt":
            user32 = ctypes.windll.user32
            self.screen_width, self.screen_height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
        else:
            import pyautogui
            self.screen_width, self.screen_height = pyautogui.size()
            self.screen_height -= 120

        pygame.init()
        flags = pygame.DOUBLEBUF
        self.window = pygame.display.set_mode((self.screen_width, self.screen_height), flags)
        pygame.display.set_caption("Quoridor")
        self.clock = pygame.time.Clock()
        self.role = role
        self.waiting_room_images = []
        self.numPlayers = numPlayers
        self.numClient = numClient
        self.nbr_player_waiting = 1
        self.status = True
        self.waitingRoomNetwork = None
        if self.role == "Server":
            self.serverClass = serverClass

        # Initialisation de toutes les images.
        self.configPictures()
    
    
    def configPictures(self) -> None:
        self.waiting_room_images = []
        
        leaveGame = Image.open(f"./assets/images/launcher/leaveGameNetwork.png")
        leaveGame = leaveGame.resize((90, 90))
        self.leaveGame = pygame.image.fromstring(leaveGame.tobytes(), leaveGame.size, leaveGame.mode)
            
        if self.role == "Server":
            startGame = Image.open(f"./assets/images/waitingRoom/startGame.png")
            startGame = startGame.resize((169, 49))
            self.startGame = pygame.image.fromstring(startGame.tobytes(), startGame.size, startGame.mode)
            
            infosGameServer = Image.open(f"./assets/images/waitingRoom/infosGameServer.png")
            infosGameServer = infosGameServer.resize((200, 238))
            self.infosGameServer = pygame.image.fromstring(infosGameServer.tobytes(), infosGameServer.size, infosGameServer.mode)
            
            waiting1 = Image.open(f"./assets/images/waitingRoom/waitServer_{self.numPlayers}Players.png")
            waiting1 = waiting1.resize((self.screen_width, self.screen_height))
            self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

            if self.numPlayers == 4:
                waiting2 = Image.open(f"./assets/images/waitingRoom/waitServerAnd1Client_4Players.png")
                waiting2 = waiting2.resize((self.screen_width, self.screen_height))
                self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                waiting3 = Image.open(f"./assets/images/waitingRoom/waitServerAnd2Client_4Players.png")
                waiting3 = waiting3.resize((self.screen_width, self.screen_height))
                self.waiting_room_images.append(pygame.image.fromstring(waiting3.tobytes(), waiting3.size, waiting3.mode))

                waiting4 = Image.open(f"./assets/images/waitingRoom/waitServerAnd3Client_4Players.png")
                waiting4 = waiting4.resize((self.screen_width, self.screen_height))
                self.waiting_room_images.append(pygame.image.fromstring(waiting4.tobytes(), waiting4.size, waiting4.mode))
            elif self.numPlayers == 2:
                waiting2 = Image.open(f"./assets/images/waitingRoom/waitServerAndClient_2Players.png")
                waiting2 = waiting2.resize((self.screen_width, self.screen_height))
                self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

        elif self.role == "Client":
            if self.numPlayers == 2:
                waiting1 = Image.open(f"./assets/images/waitingRoom/waitClientAndServer_2Players.png")
                waiting1 = waiting1.resize((self.screen_width, self.screen_height))
                self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

            elif self.numPlayers == 4:
                if self.numClient == 1:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith1AndServer_4Players.png")
                    waiting1 = waiting1.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

                    waiting2 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith2AndServer_4Players.png")
                    waiting2 = waiting2.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                    waiting3 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith3AndServer_4Players.png")
                    waiting3 = waiting3.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting3.tobytes(), waiting3.size, waiting3.mode))

                elif self.numClient == 2:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait2ClientWith2AndServer_4Players.png")
                    waiting1 = waiting1.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

                    waiting2 = Image.open(f"./assets/images/waitingRoom/wait2ClientWith3AndServer_4Players.png")
                    waiting2 = waiting2.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                elif self.numClient == 3:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait3ClientWith3AndServer_4Players.png")
                    waiting1 = waiting1.resize((self.screen_width, self.screen_height))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

        self.start_game_network_button = pygame.Rect(250, 500, 300, 50)
        self.displayChoice = True


    def setWaitingRoomNetwork(self, waitingRoomNetwork : object) -> None:
        self.waitingRoomNetwork = waitingRoomNetwork
        
        
    def waitNetwork(self) -> None:
        self.startGameBtn = None
        timeSleep = True
        while self.status == True:
            for event in pygame.event.get():
                            
                if event.type == QUIT:
                    self.status = False

                if event.type == MOUSEBUTTONDOWN:
                    if hasattr(self, 'leaveGameRect'):
                        if self.leaveGameRect.collidepoint(event.pos):
                            self.status = False
                            self.leaveGameNetwork()
                        
                    if self.role == "Server":
                        if (self.serverClass.typeGame == 2 and len(self.serverClass.listClients) == 1) or (self.serverClass.typeGame == 4 and len(self.serverClass.listClients) == 3): 
                            if self.startGameBtn.collidepoint(event.pos):
                                self.waitingRoomNetwork.serverSendLaunch()
                                timeSleep = False
                                self.serverClass.stateListenServer = False
                        
            if pygame.display.get_init():
                self.window.fill((240, 177, 105))
                self.window.blit(self.waiting_room_images[self.nbr_player_waiting - 1], (0, 0))

                if self.role == "Server":
                    # Image information du serveur
                    infoGameX = self.window.get_width() - 300
                    infoGameY = self.window.get_height() - 300
                    self.infosGameServerRect = pygame.Rect(infoGameX, infoGameY, self.infosGameServer.get_width(), self.infosGameServer.get_height())
                    self.window.blit(self.infosGameServer, (infoGameX, infoGameY))
                    # print(self.serverClass.ip, self.serverClass.port)
                
                    if (self.serverClass.typeGame == 2 and len(self.serverClass.listClients) == 1) or (self.serverClass.typeGame == 4 and len(self.serverClass.listClients) == 3): 
                        startGameBtnX = 350
                        startGameBtnY = self.window.get_height() - 200
                        self.startGameBtn = pygame.Rect(startGameBtnX, startGameBtnY, self.startGame.get_width(), self.startGame.get_height())
                        self.window.blit(self.startGame, (startGameBtnX, startGameBtnY))

                # Image de leave.
                leaveGameX = 69.5
                leaveGameY = self.window.get_height() - 159.5
                self.leaveGameRect = pygame.Rect(leaveGameX, leaveGameY, self.leaveGame.get_width(), self.leaveGame.get_height())
                self.window.blit(self.leaveGame, (leaveGameX, leaveGameY))
                
                pygame.display.flip()
                if timeSleep:
                    time.sleep(2)
                    
        self.destroyWindow(False)


    def add(self) -> None:
        if self.numPlayers == 2:
            if self.nbr_player_waiting == 2:
                self.nbr_player_waiting = 1
            else:
                self.nbr_player_waiting += 1
        elif self.numPlayers == 4:
            if self.nbr_player_waiting == 4:
                self.nbr_player_waiting = 1
            else:
                self.nbr_player_waiting += 1


    def remove(self, position : int) -> None:
        if self.numPlayers == 4 and position == 1:
            if self.nbr_player_waiting == 1:
                self.nbr_player_waiting = 1
            elif self.nbr_player_waiting == 2:
                self.nbr_player_waiting = 2
        elif self.numPlayers == 4 and position == 0:
            if self.nbr_player_waiting == 1:
                self.nbr_player_waiting = 1
            else:
                self.nbr_player_waiting -= 1
        elif self.numPlayers == 2 and position == 3:
            if self.nbr_player_waiting == 1:
                self.nbr_player_waiting = 1
            elif self.nbr_player_waiting == 2:
                self.nbr_player_waiting -= 1

    
    def leaveGameNetwork(self) -> None:
        if self.role == "Server":
            self.waitingRoomNetwork.serverClass.stateListenServer = False
            self.waitingRoomNetwork.serverClass.statusServer = False
            
            self.waitingRoomNetwork.disableStateCheck()
            self.waitingRoomNetwork.stopAllThread()
            
            self.status = False
            
            self.serverClass.socketServer.close()
                
        elif self.role == "Client":
            self.waitingRoomNetwork.stateWindow = False
            
            self.status = False
            
            self.waitingRoomNetwork.userSocket.close()
        
        self.destroyWindow(True)
    
    
    def setNumWaitPlayers(self, numWaitPlayers: int) -> None:
        self.nbr_player_waiting = numWaitPlayers


    def setNumClient(self, newNumClient : int) -> None:
        self.numClient = newNumClient
        
        
    def getNumWaitPlayers(self) -> None:
        return self.nbr_player_waiting


    def destroyWindow(self, choice : bool) -> None:
        self.status = False
        pygame.quit()
        
        if choice:
            from domain.launcher.launcher import QuoridorLauncher
        
            run = QuoridorLauncher("")