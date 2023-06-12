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
        if os.name == "nt":
            pygame.display.init()
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            pygame.display.set_mode((1920, 1080))

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


