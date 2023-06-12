import pygame
import os
import threading

class LaunchScreen(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.screen = None
        self.clock = None
        self.status = True
        self.progress = 0


    def run(self):
        pygame.init()
        self.createWindow()
        self.loadPicture()
        
        while self.status:
            self.clock.tick(2)
            self.loadPicture()

        self.destroyWindow()


    def addProgress(self):
        self.progress += 1


    def createWindow(self):
        # Centrage dans l'écran.
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        
        pygame.display.set_caption("Lancement du jeu en cours ...")
        
        # Zone de récupération de la taille écran en fonction de l'os.
        if os.name == "nt":
            screenInfo = pygame.display.Info()
            self.screenWidth = screenInfo.current_w
            self.screenHeight = screenInfo.current_h
        else:
            import pyautogui
            self.screenWidth, self.screenHeight = pyautogui.size()
            self.screenHeight -= 120
        
        self.screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))

        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()


    def loadPicture(self):
        image_path = f"./assets/images/launchScreen/launchScreenState_{self.progress}.png"
        image = pygame.image.load(image_path)
        scaled_image = pygame.transform.scale(image, self.screen.get_size())
        self.screen.blit(scaled_image, (0, 0))
        pygame.display.flip()


    def destroyWindow(self):
        pygame.quit()

