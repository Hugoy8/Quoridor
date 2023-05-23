import threading
from PIL import Image, ImageTk
from tkinter import *
from network.network import MainThread

class WaitingRoomNetwork(threading.Thread):
    def __init__(self, role : str, nbr_player_waiting: int) -> None:
        threading.Thread.__init__(self)
        self.window = Tk()
        self.window.title("Quoridor")
        self.window.minsize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.iconbitmap('./assets/logo.ico')
        self.window.configure(bg="#F0B169")
        self.waiting_room1 = None
        self.waiting_room2 = None
        self.nbr_player_waiting = 1
        self.role = role
        
        MainThread(self.waitNetwork(nbr_player_waiting))

    def waitNetwork(self, nbr_player_waiting : int) -> None:
        waiting1 = Image.open(f"./assets/wait1.png")
        waiting1 = waiting1.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.waiting_room1 = ImageTk.PhotoImage(waiting1)

        waiting2 = Image.open(f"./assets/wait2.png")
        waiting2 = waiting2.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.waiting_room2 = ImageTk.PhotoImage(waiting2)

        if self.nbr_player_waiting == 1:
            label = Label(self.window, image=self.waiting_room1)
            label.place(x=0, y=0)
        elif self.nbr_player_waiting == 2:
            label = Label(self.window, image=self.waiting_room2)
            label.place(x=0, y=0)
        if self.role == "server":
            start_game_network = Button(self.window, text="Lancer la partie", bg="#2BB0ED", font=("Arial", 15), fg="white", 
                                    width=self.window.winfo_screenwidth()//70, activebackground="#2BB0ED", activeforeground="white", command=self.add)
            start_game_network.place(x=self.window.winfo_screenwidth()//5, y=self.window.winfo_screenheight()//1.2)
        self.window.mainloop()

    def add(self) -> None:
        if self.nbr_player_waiting == 1:
            self.nbr_player_waiting += 1
        elif self.nbr_player_waiting == 2:
            self.nbr_player_waiting -= 1
        self.waitNetwork(self.nbr_player_waiting)
        
    def destroyWindow(self) -> None:
        self.window.destroy()
        