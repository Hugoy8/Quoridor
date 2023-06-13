from domain.network.clientConfig import ClientConfig
from domain.network.server import Server
import tkinter as tk


def mainThread(callback : tk) -> None:
    root = tk.Tk()
    root.withdraw()
    root.after(0, callback)
    root.mainloop()
    

def joinSession(ip : str, port : int, mapId : int) -> None:
    ClientConfig(ip, port, mapId)


def startSession(port : int, nbr_player : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int, listInfosInvit : list, GameInvit : bool) -> None:
    Server("127.0.0.1", port, nbr_player).server_config(size, nb_players, nb_IA, nb_fences, mapID, listInfosInvit, GameInvit)