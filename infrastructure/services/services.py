from tkinter import *
import socket
import pickle
from domain.player.player import Player
from PIL import Image, ImageTk
import time
from pygame import mixer
from infrastructure.database.config import Database


class Board:
    def __init__(self, size : int, nb_players : int, nb_IA : int, nb_fence : int, select_map : int, Network : bool, InstanceNetwork : object, typeNetwork : str, playerUser : int, db : Database) -> None:
        # Lancement de la class d'initialisation des variables, images, sons...
        from infrastructure.services.initGame import InitGame
        initGame = InitGame(self)
        
        initGame.startInit(size, nb_players, nb_IA, nb_fence, select_map, Network, InstanceNetwork, typeNetwork, playerUser, db)
        
        
    def loadVolumeSettings(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 6:
                self.volume_map = float(lines[1].strip())
                self.volume_victory = float(lines[2].strip())
                self.volume_pion = float(lines[3].strip())
                self.volume_fence = float(lines[4].strip())
                self.volume_nofence = float(lines[5].strip())
                self.button_fence = str(lines[7].strip())
        self.sound_map = mixer.Sound(f"./assets/sounds/{self.map}.mp3")
        self.sound_map.play(loops=-1)
        self.sound_map.set_volume(self.volume_map)
    

    def setLevelIa(self, newDificultyIA : int) -> None:
        self.dificultyIA = newDificultyIA
        
        
    def get_size(self):
        return self.size
    
    def caseClicked(self, event : int) -> None:
        if self.settings.popup != None:
            self.settings.popup.destroy()
            self.settings.popup = None
        item_id = event.widget.find_closest(event.x, event.y)[0]
        tags = self.canvas.gettags(item_id)
        x = int(tags[0])
        y = int(tags[1])
        
        if self.networkStatus == True:
            if self.typeNetwork == "instance":
                self.InstanceNetwork.SendBoard(x, y, 0, self.fence_orientation)
            elif self.typeNetwork == "socket":
                SendBoardClient(x, y, 0, self.InstanceNetwork, self.fence_orientation, self.playerUser)

        self.movement.move(x,y)
        # son de déplacement
        sound_move = mixer.Sound("./assets/sounds/move.mp3")
        sound_move.play()
        sound_move.set_volume(self.volume_pion)
        if self.victory() == True :
            self.displayBoard(False)
            self.canvas.unbind_all("<Button-1>")
            for child in self.window.winfo_children():
                if child.winfo_exists():
                    child.destroy()
            self.windowVictory()
        else:
            self.resetPossibleCaseMovement() 
            self.refreshCurrentPlayer()

            if self.networkStatus == True:
                if self.current_player.get_player() == self.playerUser:
                    self.refreshPossibleCaseMovementForCurrentPlayer()
                else:
                    pass
            else:
                self.refreshPossibleCaseMovementForCurrentPlayer()

            self.displayBoard(False)
        while self.current_player.get_IALevel() != 0 :
            self.bot.currentBotPlaysBasedOnDifficulty(self.current_player.get_IALevel())
            if self.victory() == True :
                self.displayBoard(False)
                self.canvas.unbind_all("<Button-1>")
                for child in self.window.winfo_children():
                    if child.winfo_exists():
                        child.destroy()
                self.windowVictory()
                break
            else:
                self.resetPossibleCaseMovement() 
                self.refreshCurrentPlayer()
                self.refreshPossibleCaseMovementForCurrentPlayer()
                self.displayBoard(False)
                
        
    def windowVictory(self) -> None:
        self.sound_map.stop()
        # background de fond
        if self.networkStatus == True:
            try:
                self.db.addGame(self.pseudo)
            except Exception as e:
                print("Erreur" + str(e)) 
        self.bg_image = Image.open(f"./assets/images/{self.map}/background{self.nb_players}{self.name_bg}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.displayBoard(False)
        # Affichage de l'image de victoire
        if self.current_player.get_player() == 1:
            img_win_p1 = Image.open(f"./assets/images/{self.map}/victory_p1.png")
            img_win_p1 = img_win_p1.resize((485, 480))
            self.img_win_p1 = ImageTk.PhotoImage(img_win_p1)
            
            label = Label(self.window, image=self.img_win_p1, bd=0, highlightthickness=0)
            label.place(relx=0.5, rely=0.5, anchor=CENTER)
            
        elif self.current_player.get_player() == 2:
            img_win_p2 = Image.open(f"./assets/images/{self.map}/victory_p2.png")
            img_win_p2 = img_win_p2.resize((485, 480))
            self.img_win_p2 = ImageTk.PhotoImage(img_win_p2)
            
            label = Label(self.window, image=self.img_win_p2,  bd=0, highlightthickness=0)
            label.place(relx=0.5, rely=0.5, anchor=CENTER)
            
        elif self.current_player.get_player() == 3:
            img_win_p3 = Image.open(f"./assets/images/{self.map}/victory_p3.png")
            img_win_p3 = img_win_p3.resize((485, 480))
            self.img_win_p3 = ImageTk.PhotoImage(img_win_p3)
            
            label = Label(self.window, image=self.img_win_p3,  bd=0, highlightthickness=0)
            label.place(relx=0.5, rely=0.5, anchor=CENTER)
            
        elif self.current_player.get_player() == 4:
            img_win_p4 = Image.open(f"./assets/images/{self.map}/victory_p4.png")
            img_win_p4 = img_win_p4.resize((485, 480))
            self.img_win_p4 = ImageTk.PhotoImage(img_win_p4)
            
            label = Label(self.window, image=self.img_win_p4,  bd=0, highlightthickness=0)
            label.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Ajout des boutons
        def rejouer():
            self.window.destroy()
            from domain.launcher.launcher import QuoridorLauncher

            run = QuoridorLauncher("")
        
        # Quitter la partie
        def quitgame():
            self.window.destroy()
            from infrastructure.services.deletePycache import deletePycache
            deletePycache()
        
        replay_button = Label(self.window, image=self.restart_game_victory, bd=0, highlightthickness=0)
        replay_button.place(relx=0.445, rely=0.675, anchor=CENTER)
        replay_button.bind("<Button-1>", lambda e:rejouer())
        
        quit_button = Label(self.window, image=self.leave_game_victory, bd=0, highlightthickness=0)
        quit_button.place(relx=0.55, rely=0.675, anchor=CENTER)
        quit_button.bind("<Button-1>", lambda e:quitgame())
        
        # Son de victoire
        sound_victory = mixer.Sound("./assets/sounds/victory.mp3")
        sound_victory.play()
        sound_victory.set_volume(self.volume_victory)
        if self.networkStatus == True:
            if self.typeNetwork == "instance" :
                username = self.db.selectUsername(self.db.ip, self.db.port,  self.current_player.get_player())
                self.db.addWin(username)
                self.db.addMoney(username)
    
    
    def popUpNoFence(self, player_name):
        #PopUp plus de barrière
        leavepopup = Image.open(f"./assets/images/{self.map}/no_fence{player_name}.png")
        leavepopup = leavepopup.resize((600, 50))
        self.leavepopup = ImageTk.PhotoImage(leavepopup)
        
        label_no_fence = Label(self.window, image=self.leavepopup, bd=0)
        if self.size == 5:
            y = 0.18
        else:
            y = 0.12
        label_no_fence.place(relx=0.5, rely=y, anchor='center')
        self.window.after(2000, label_no_fence.destroy)


    def displayBoard(self, leave: bool) -> None: 
        player_colors = {
            1: "red",
            2: "green",
            3: "blue",
            4: "#C137BC"
        }
        self.canvas = Canvas(self.window, width=self.canvas_game_width, height=self.canvas_game_height, bg="#F0B169", bd=0, highlightthickness=0)
        self.canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        # Placement des joueurs
        window_width = self.window.winfo_screenwidth()
        window_height = self.window.winfo_screenheight()

        
        # Affichage Tour du joueur
        current_player_number = self.current_player.get_player()

        # Sélection de l'image du joueur en fonction du numéro
        if current_player_number == 1:
            current_player_image = self.current_player1_image
        elif current_player_number == 2:
            current_player_image = self.current_player2_image
        elif current_player_number == 3:
            current_player_image = self.current_player3_image
        elif current_player_number == 4:
            current_player_image = self.current_player4_image
        else:
            current_player_image = None

        if current_player_image:
            if self.display_current_player:
                self.display_current_player.destroy()
                
            if self.map == "jungle":
                coX, coY = 0.82, 0.913
            elif self.map == "space":
                coX, coY = 0.826, 0.916
            elif self.map == "hell":
                coX, coY = 0.822, 0.913
            elif self.map == "ice":
                coX, coY = 0.82, 0.915
            elif self.map == "electricity":
                coX, coY = 0.82, 0.915
            elif self.map == "sugar":
                coX, coY = 0.822, 0.915
                
            self.display_current_player = Label(self.window, image=current_player_image, bd=0, highlightthickness=0, anchor=CENTER)
            self.display_current_player.place(relx=coX, rely=coY, anchor="center")

        
        for index, nbr_fence_player in enumerate(self.players):
            a = nbr_fence_player.get_player()
            b = nbr_fence_player.get_nb_fence()
            player_color = player_colors.get(a, "red")
            
            window_width = self.window.winfo_screenwidth()
            window_height = self.window.winfo_screenheight()
            
            if self.nb_players == 2:
                if index == 0:
                    # Joueur 1 (en haut au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=window_width/2.2, y=73, anchor="center")
                elif index == 1:
                    # Joueur 2 (en bas au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=window_width/1.8, y=window_height-70, anchor="center")
            elif self.nb_players == 4:
                if index == 0:
                    # Joueur 1 (en haut au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=window_width/2.2, y=70, anchor="center")
                elif index == 1:
                    # Joueur 2 (en bas au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=window_width/1.8, y=window_height-70, anchor="center")
                elif index == 2:
                    # Joueur 3 (en bas au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=60, y=window_height/1.72, anchor="w")
                elif index == 3:
                    # Joueur 4 (à gauche au milieu)
                    Label(self.window, text=f"{b}", font=("Arial", 16), foreground=player_color).place(x=window_width-60, y=window_height/2.4, anchor="e")
                    
        if leave == True:
            #PopUp de leave d'un joueur
            leavepopup = Image.open(f"./assets/images/leavepopup.png")
            leavepopup = leavepopup.resize((self.window.winfo_screenwidth() // 2, 100))
            self.leavepopup = ImageTk.PhotoImage(leavepopup)
            
            label = Label(self.window, image=self.leavepopup)
            label.place(relx=0.5, rely=0.05, anchor='center')
            
        self.window.bind(f"{self.button_fence}", self.fenceStructure.changeFenceOrientation)
        tab =[]
        self.pillar_rects = []
        for i in range(self.size*2-1):
            if i%2 == 0 :
                tab2 = []
                for j in range(self.size*2-1):
                    if j%2 == 0 :
                        case = self.board[i][j]
                        tab2.append(case.displayPlayer())
                        if case.displayPlayer() == "P0" :
                            if case.get_possibleMove() != 0 and self.victory() == False:
                                position = self.current_player.displayPlace()
                                self.movement.move_case = self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.moove_possible, anchor="nw", tags=case.get_possibleMove())
                                self.canvas.tag_bind(self.movement.move_case, "<Button-1>", self.caseClicked)
                            else :
                                self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.no_player, anchor="nw")
                        elif case.displayPlayer() == "P1" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_1, anchor="nw")
                        elif case.displayPlayer() == "P2" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_2, anchor="nw")
                        elif case.displayPlayer() == "P3" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_3, anchor="nw")
                        elif case.displayPlayer() == "P4" :
                            self.canvas.create_image(j*self.widget_space, i*self.widget_space, image=self.image_player_4, anchor="nw")
                    else :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*self.widget_space+(self.widget_space-self.epaisseur_barriere), i*self.widget_space, image=self.fence_height, anchor="nw", tags=str(i) + "_" + str(j))
                        else :
                            self.canvas.create_image(j*self.widget_space+(self.widget_space-self.epaisseur_barriere), i*self.widget_space, image=self.fence_height_vide, anchor="nw", tags=str(i) + "_" + str(j))

                tab.append(tab2)
            else :
                tab2 = []
                for j in range(self.size*2-1):
                    if j%2 == 0 :
                        fence = self.board[i][j]
                        tab2.append(fence.displayFence())
                        if fence.displayFence() == "F1" :
                            self.canvas.create_image(j*self.widget_space ,i*self.widget_space+(self.widget_space-self.epaisseur_barriere), image=self.fence_width, anchor="nw", tags=str(i) + "_" + str(j))
                        else:
                            self.canvas.create_image(j*self.widget_space ,i*self.widget_space+(self.widget_space-self.epaisseur_barriere), image=self.fence_width_vide, anchor="nw", tags=str(i) + "_" + str(j))
                    else :
                        pillar = self.board[i][j]
                        tab2.append(pillar.displayPillar())
                        if pillar.displayPillar() == "B1" :
                            self.pillar_rects.append(self.canvas.create_image(j*self.widget_space+(self.widget_space-self.epaisseur_barriere), i*self.widget_space+(self.widget_space-self.epaisseur_barriere), image=self.pillar, anchor="nw", tags=[i,j]))
                        else :
                            self.pillar_rects.append(self.canvas.create_image(j*self.widget_space+(self.widget_space-self.epaisseur_barriere), i*self.widget_space+(self.widget_space-self.epaisseur_barriere), image=self.pillar_vide, anchor="nw", tags=[i,j]))
                        
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Button-1>", self.buildFenceOnClick)
                            else:
                                pass
                        else:
                            self.canvas.tag_bind(self.pillar_rects[-1], "<Button-1>", self.buildFenceOnClick)
                            
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                if self.victory() == False:
                                    self.canvas.tag_bind(self.pillar_rects[-1], "<Enter>", self.on_hover)
                                    self.canvas.tag_bind(self.pillar_rects[-1], "<Leave>", self.on_leave)
                            else:
                                pass
                        else:
                            if self.victory() == False:
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Enter>", self.on_hover)
                                self.canvas.tag_bind(self.pillar_rects[-1], "<Leave>", self.on_leave)
                tab.append(tab2)
            
    def buildFenceOnClick(self,event):
        if self.settings.popup != None:
            self.settings.popup.destroy()
            self.settings.popup = None
            
        if self.fenceStructure.playerHasFence() == True :
            item_id = event.widget.find_withtag("current")[0], 
            tags = self.canvas.gettags(item_id)
            if len(tags) >= 2 :
                x = int(tags[0])
                y = int(tags[1])
                if self.fenceStructure.isPossibleFence(x,y) == True :
                    self.fenceStructure.buildFence(x,y)
                    if self.movement.fenceNotCloseAccesGoal()==False :
                        self.fenceStructure.deBuildFence(x,y)
                        self.displayBoard(False)
                        sound_build_fence = mixer.Sound("./assets/sounds/no_fence.mp3")
                        sound_build_fence.play()
                        sound_build_fence.set_volume(self.volume_nofence)
                    else :
                        for index, nbr_fence_player in enumerate(self.players):
                            a = nbr_fence_player.get_player()
                            b = nbr_fence_player.get_nb_fence()
                            
                            if b == 0 and a not in self.pop_up_no_fence:
                                self.pop_up_no_fence.append(a)
                                self.popUpNoFence(a)
                
                        # Son de pose de barrière
                        sound_build_fence = mixer.Sound("./assets/sounds/build_fence.mp3")
                        sound_build_fence.play()
                        sound_build_fence.set_volume(self.volume_fence)
                        if self.networkStatus == True:
                            if self.typeNetwork == "instance":
                                self.InstanceNetwork.SendBoard(x, y, 1, self.fence_orientation)
                            elif self.typeNetwork == "socket":
                                SendBoardClient(x, y, 1, self.InstanceNetwork, self.fence_orientation, self.playerUser)
                        
                        self.resetPossibleCaseMovement() 
                        self.refreshCurrentPlayer()
                        
                        if self.networkStatus == True:
                            if self.current_player.get_player() == self.playerUser:
                                self.refreshPossibleCaseMovementForCurrentPlayer()
                            else:
                                pass
                        else:
                            self.refreshPossibleCaseMovementForCurrentPlayer()
                            
                        self.displayBoard(False)
                        while self.current_player.get_IALevel() != 0 :
                            self.bot.currentBotPlaysBasedOnDifficulty(self.current_player.get_IALevel())
                            if self.victory() == True :
                                self.displayBoard(False)
                                self.canvas.unbind_all("<Button-1>")
                                for child in self.window.winfo_children():
                                    if child.winfo_exists():
                                        child.destroy()
                                self.windowVictory()
                                break
                            else:
                                self.resetPossibleCaseMovement() 
                                self.refreshCurrentPlayer()
                                self.refreshPossibleCaseMovementForCurrentPlayer()
                                self.displayBoard(False)     
                        
    def on_hover(self, event):
        if self.fenceStructure.playerHasFence() == True :
            item_id = event.widget.find_withtag("current")[0]
            tags = self.canvas.gettags(item_id)
            if len(tags) >= 2 and item_id in self.pillar_rects:
                x = int(tags[0])
                y = int(tags[1])
                if self.fenceStructure.isPossibleFence(x,y) == True :
                    self.canvas.itemconfig(item_id, image=self.pillar_hover)
                    if self.fence_orientation == "vertical":
                        fence = self.canvas.find_withtag(str(x-1) + "_" + str(y))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_height_hover)
                        fence = self.canvas.find_withtag(str(x+1) + "_" + str(y))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_height_hover)
                    else :
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y-1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_hover)
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y+1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_hover)
    
    def on_leave(self, event):
        item_id = event.widget.find_withtag("current")[0]
        tags = self.canvas.gettags(item_id)
        if item_id in self.pillar_rects:
            x = int(tags[0])
            y = int(tags[1])
            if self.fenceStructure.isPossibleFence(x,y) == True :
                pillar = self.board[x][y]
                if pillar.get_build() != 1:
                    self.canvas.itemconfig(item_id, image=self.pillar_vide)
                if self.fence_orientation == "vertical":
                    fence = self.canvas.find_withtag(str(x-1) + "_" + str(y))
                    item_id = fence[0]
                    self.canvas.itemconfig(item_id, image=self.fence_height_vide)
                    fence = self.canvas.find_withtag(str(x+1) + "_" + str(y))
                    item_id = fence[0]
                    self.canvas.itemconfig(item_id, image=self.fence_height_vide)
                else :
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y-1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_vide)
                        fence = self.canvas.find_withtag(str(x) + "_" + str(y+1))
                        item_id = fence[0]
                        self.canvas.itemconfig(item_id, image=self.fence_width_vide)


    def decideIALevel(self, player : int) -> bool:
        if player > self.nb_players - self.nb_IA:
            return self.dificultyIA
        return False


    def start(self) -> None:
        nb_fence_each_player = int(self.nb_fence / self.nb_players)
        case = self.board[0][self.size-1]
        case.set_player(1)
        self.players.append(Player(0,self.size-1,1,nb_fence_each_player,self.decideIALevel(1)))
        case = self.board[-1][self.size-1]
        case.set_player(2)
        self.players.append(Player((self.size-1)*2,self.size-1,2,nb_fence_each_player,self.decideIALevel(2)))
        if self.nb_players == 4 :
            case = self.board[self.size-1][0]
            case.set_player(3)
            self.players.append(Player(self.size-1,0,3,nb_fence_each_player,self.decideIALevel(3)))
            case = self.board[self.size-1][-1]
            case.set_player(4)
            self.players.append(Player(self.size-1,(self.size-1)*2,4,nb_fence_each_player,self.decideIALevel(4)))
        self.current_player = self.players[0]
        self.bot.updateNeighborsForEachFence()
        
    
    def refreshCurrentPlayer(self) -> None:
        if self.current_player.get_player() == self.nb_players :
            self.current_player = self.players[0]
        else :
            self.current_player = self.players[self.current_player.get_player()]
    
    
    def victory(self) -> bool:
        position = self.current_player.displayPlace()
        if self.current_player.get_player() == 1 :
            if position[0] == (self.size-1)*2 :
                return True
        elif self.current_player.get_player() == 2 : 
            if position[0] == 0 :
                return True
        elif self.current_player.get_player() == 3 : 
            if position[1] == (self.size-1)*2 :
                return True
        elif self.current_player.get_player() == 4 : 
            if position[1] == 0 :
                return True
        return False
        
    
    def alreadyChecked(self, x : int, y : int) -> bool:
        for i in self.list_case_check:
                    if i[0] == x and i[1] == y:
                        return True
        return False
    
    
    def refreshPossibleCaseMovementForCurrentPlayer(self) -> None:
        position = self.current_player.displayPlace()
        list_possible_move = self.movement.allPossibleMoveForPlayer(self.current_player)
        for coord in list_possible_move :
            case = self.board[position[0]+coord[0]][position[1]+coord[1]]
            case.set_possibleMove([coord[0],coord[1]])
            
    def resetPossibleCaseMovement(self) -> None:
        for i in range(self.size*2-1):
            if i%2 == 0 :
                for j in range(self.size*2-1):
                    if j%2 == 0 :
                        case = self.board[i][j]
                        case.set_possibleMove(0)

def SendBoardClient(x : int, y : int, typeClick : int, client : socket, orientation : str, playerUser : int) -> None:
    # typeClick = 0 (caseClicked)
    # typeClick = 1 (fenceClicked)
    
    # orientation = 0 (vertical)
    # orientation = 1 (horizontal)
    
    if orientation == "vertical":
        orientation = 0
    else: 
        orientation = 1
        
    DataMove = ([int(x), int(y), int(typeClick), int(orientation), int(playerUser)])
    dataSendArray = pickle.dumps(DataMove)
    
    try:
        client.send(dataSendArray)
        time.sleep(0.1)
    except socket.error:
        print("Erreur d'envoie du tableau ...")
        exit()
    

def restartGame(size : int, nb_players : int, nb_IA : int, nb_fences : int, select_map : int, dificultyIA : int) -> None:
    jeu = Board(size, nb_players , nb_IA, nb_fences, select_map, False, "", "", 0, "")
    jeu.setLevelIa(dificultyIA)
    jeu.start()
    jeu.refreshPossibleCaseMovementForCurrentPlayer()
    jeu.displayBoard(False)


if __name__ == "__main__":
    restartGame(5, 2, 0, 8, 2)
    mainloop()