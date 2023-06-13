import threading
from infrastructure.database.config import Database
from infrastructure.services.verifConnection import VerifConnection
from infrastructure.services.getSetInformation import GetSetInformation
import time
from pygame import mixer


class VerifNotifs(threading.Thread):
    def __init__(self, db : Database) -> None:
        threading.Thread.__init__(self)
        self.db = db
        self.status = True
        self.friendsNotifs = []
        self.gamesNotifs = []
        
        mixer.init()
        
        self.soundNotifsFriends = mixer.Sound(f"./assets/sounds/notifsFriends.mp3")
        self.soundNotifsGames = mixer.Sound(f"./assets/sounds/notifsGames.mp3")
        
        self.startVerif = False


    def run(self) -> None:
        while self.status:
            if VerifConnection("https://www.google.fr/").isConnectInternet() and VerifConnection("https://www.google.fr/").isConnectDatabase():
                username = GetSetInformation().get_username("serverPseudo.txt")
                
                if username != "":
                    resultFriends = self.db.selectAllInviting(username, False)
                    resultGames = self.db.selectAllInvitingGames(username)
                    
                    
                    if len(resultFriends) > 0:
                        for friend in resultFriends:
                            if len(resultFriends) > len(self.friendsNotifs):
                                if self.startVerif:
                                    if GetSetInformation().getLinesSettings("Settings.txt", 1)[0] == "True":
                                        volumeNotifs = GetSetInformation().getLinesSettings("Settings.txt", 9)[0]
                                        self.soundNotifsFriends.play()
                                        self.soundNotifsFriends.set_volume(float(volumeNotifs))
                                    self.startVerif = True
                                self.friendsNotifs.append(friend)
                                
                    if len(resultGames) > 0:
                        for game in resultGames:
                            if len(resultGames) > len(self.gamesNotifs):
                                if self.startVerif:
                                    if GetSetInformation().getLinesSettings("Settings.txt", 1)[0] == "True":
                                        volumeNotifs = GetSetInformation().getLinesSettings("Settings.txt", 9)[0]
                                        self.soundNotifsGames.play()
                                        self.soundNotifsGames.set_volume(float(volumeNotifs))
                                    self.startVerif = True
                                self.gamesNotifs.append(game)
                        
                    self.startVerif = True
                    
                time.sleep(5)
            else:
                time.sleep(5)