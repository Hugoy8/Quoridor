from tkinter import *
import tkinter as tk

class SettingsGame:
    def __init__(self, window: Tk, popup_escape_game: Label, button_popup_resumegame: Button, button_popup_quitgame: Button, board: object) -> None:
        """Initialise les paramètres du jeu"""
        self.window = window
        self.popup_escape_game = popup_escape_game
        self.button_popup_resumegame = button_popup_resumegame
        self.button_popup_quitgame = button_popup_quitgame
        self.popup = None
        self.board = board
    
    
    def displayBreakGame(self, event) -> None:
        """Affiche le menu pause du jeu"""
        if self.popup is None:
            self.popup = Label(self.window, image=self.popup_escape_game, bd=0, highlightthickness=0)
            self.popup.pack(side=LEFT, anchor=N)
            self.buttonResumeGame()
            self.buttonQuitGame()
        else:
            self.resumeGame()


    def resumeGame(self) -> None:
        """Reprend la partie"""
        if self.popup is not None:
            self.popup.destroy()
        self.popup = None


    def buttonResumeGame(self) -> None:
        """Bouton pour reprendre la partie"""
        button_resume_game = Label(self.popup, image=self.button_popup_resumegame, bd=0, highlightthickness=0, cursor="hand2")
        button_resume_game.place(relx= 0.5, rely=0.4, anchor=CENTER)
        button_resume_game.bind("<Button-1>", lambda event:self.resumeGame())


    def quitGame(self) -> None:
        """Quitte le jeu"""
        import os
        self.board.sound_map.stop()
        self.window.destroy()
        if self.board.networkStatus:
            if self.board.nb_players == 2:
                if self.board.typeNetwork == "instance":
                    self.board.InstanceNetwork.statusServer = False
                    self.board.InstanceNetwork.socket_client.close()
                    self.board.InstanceNetwork.socketServer.close()
                elif self.typeNetwork == "socket":
                        self.clientClass.statusListenClient = False
            elif self.board.nb_players == 4:
                if self.board.typeNetwork == "instance":
                    self.board.InstanceNetwork.checkAllAlorithm.setStateCheck(False)
                    self.board.InstanceNetwork.socketServer.close()
                elif self.typeNetwork == "socket":
                        self.clientClass.statusListenClient = False
        os._exit(0)


    def buttonQuitGame(self) -> None:
        """Affiche le bouton quitter"""
        button_quit_game = Label(self.popup, image=self.button_popup_quitgame, bd=0, highlightthickness=0, cursor="hand2")
        button_quit_game.place(relx= 0.5, rely=0.5, anchor=CENTER)
        button_quit_game.bind("<Button-1>", lambda event:self.quitGame())