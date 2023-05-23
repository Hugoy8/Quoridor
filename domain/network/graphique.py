import threading
from tkinter import mainloop
from infrastructure.services.services import Board


class Graphique(threading.Thread):
    def __init__(self, boardInfo : Board, playerUser : str) -> None:
        threading.Thread.__init__(self)
        #Variable qui stocke la class de jeu.
        self.board = boardInfo
        # Variable qui contient le numéro de l'utilisateur.
        self.playerUser = playerUser

        from domain.network.network import MainThread
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