from domain.network.clientConfig import ClientConfig
from domain.network.server import Server
import tkinter as tk


def MainThread(callback : tk) -> None:
    root = tk.Tk()
    root.withdraw()
    root.after(0, callback)
    root.mainloop()
    

def joinSession(ip : str, port : int, mapId : int) -> None:
    ClientConfig(ip, port, mapId)


def startSession(port : int, nbr_player : int, size : int, nb_players : int, nb_IA : int, nb_fences : int, mapID : int) -> None:
    Server("", port, nbr_player).server_config(size, nb_players, nb_IA, nb_fences, mapID)
    
    
#startSession(8000, 2, 5, 2, 0, 8, 2)

#ClientConfig("10.128.173.178", 8000, 1)