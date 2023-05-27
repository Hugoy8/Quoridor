# self.window.minsize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())

import pygame
from pygame.locals import *
from PIL import Image


class WaitingRoomUi:
    def __init__(self, role: str, numPlayers: int, numClient: int):
        pygame.init()
        self.window = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Quoridor")
        self.clock = pygame.time.Clock()
        self.role = role
        self.numPlayers = numPlayers
        self.numClient = numClient
        self.nbr_player_waiting = 1
        self.waiting_room_images = []
        self.status = True
        self.waitingRoomNetwork = None
        
        if self.role == "Server":
            waiting1 = Image.open(f"./assets/images/waitingRoom/waitServer_{self.numPlayers}Players.png")
            waiting1 = waiting1.resize((800, 600))
            self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

            if self.numPlayers == 4:
                waiting2 = Image.open(f"./assets/images/waitingRoom/waitServerAnd1Client_4Players.png")
                waiting2 = waiting2.resize((800, 600))
                self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                waiting3 = Image.open(f"./assets/images/waitingRoom/waitServerAnd2Client_4Players.png")
                waiting3 = waiting3.resize((800, 600))
                self.waiting_room_images.append(pygame.image.fromstring(waiting3.tobytes(), waiting3.size, waiting3.mode))

                waiting4 = Image.open(f"./assets/images/waitingRoom/waitServerAnd3Client_4Players.png")
                waiting4 = waiting4.resize((800, 600))
                self.waiting_room_images.append(pygame.image.fromstring(waiting4.tobytes(), waiting4.size, waiting4.mode))
            elif self.numPlayers == 2:
                waiting2 = Image.open(f"./assets/images/waitingRoom/waitServerAndClient_2Players.png")
                waiting2 = waiting2.resize((800, 600))
                self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

        elif self.role == "Client":
            if self.numPlayers == 2:
                waiting1 = Image.open(f"./assets/images/waitingRoom/waitClientAndServer_2Players.png")
                waiting1 = waiting1.resize((800, 600))
                self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

            elif self.numPlayers == 4:
                if self.numClient == 1:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith1AndServer_4Players.png")
                    waiting1 = waiting1.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

                    waiting2 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith2AndServer_4Players.png")
                    waiting2 = waiting2.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                    waiting3 = Image.open(f"./assets/images/waitingRoom/wait1ClientWith3AndServer_4Players.png")
                    waiting3 = waiting3.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting3.tobytes(), waiting3.size, waiting3.mode))

                elif self.numClient == 2:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait2ClientWith2AndServer_4Players.png")
                    waiting1 = waiting1.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

                    waiting2 = Image.open(f"./assets/images/waitingRoom/wait2ClientWith3AndServer_4Players.png")
                    waiting2 = waiting2.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting2.tobytes(), waiting2.size, waiting2.mode))

                elif self.numClient == 3:
                    waiting1 = Image.open(f"./assets/images/waitingRoom/wait3ClientWith3AndServer_4Players.png")
                    waiting1 = waiting1.resize((800, 600))
                    self.waiting_room_images.append(pygame.image.fromstring(waiting1.tobytes(), waiting1.size, waiting1.mode))

        self.start_game_network_button = pygame.Rect(250, 500, 300, 50)
        self.displayChoice = True


    def setWaitingRoomNetwork(self, waitingRoomNetwork : object) -> None:
        self.waitingRoomNetwork = waitingRoomNetwork
        
        
    def waitNetwork(self):
        while self.status == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == MOUSEBUTTONDOWN:
                    if self.start_game_network_button.collidepoint(event.pos):
                        self.waitingRoomNetwork.serverSendLaunch()
                        self.status = False

            self.window.fill((240, 177, 105))
            self.window.blit(self.waiting_room_images[self.nbr_player_waiting - 1], (0, 0))

            if self.role == "Server":
                pygame.draw.rect(self.window, (43, 176, 237), self.start_game_network_button)
                font = pygame.font.Font(None, 30)
                text = font.render("Lancer la partie", True, (255, 255, 255))
                text_rect = text.get_rect(center=self.start_game_network_button.center)
                self.window.blit(text, text_rect)

            pygame.display.flip()
            self.clock.tick(60)
        self.destroyWindow()


    def add(self):
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


    def setNumWaitPlayers(self, numWaitPlayers: int):
        self.nbr_player_waiting = numWaitPlayers


    def getNumWaitPlayers(self):
        return self.nbr_player_waiting


    def destroyWindow(self):
        pygame.quit()
        self.status = False