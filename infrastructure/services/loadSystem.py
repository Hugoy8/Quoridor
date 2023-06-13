from tkinter import Label, CENTER

class LoadSystem:
    def __init__(self, launcher : object) -> None:
        self.launcher = launcher
        
        
    def displayLoadBar(self, progress : int) -> None:
        if progress == 1:
            self.loadBarSystemLabel = Label(self.launcher.window, image=self.launcher.loadBarScreen_1, cursor="hand2", bd=0, highlightthickness=0)
            self.loadBarSystemLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        elif progress == 2:
            self.loadBarSystemLabel = Label(self.launcher.window, image=self.launcher.loadBarScreen_2, cursor="hand2", bd=0, highlightthickness=0)
            self.loadBarSystemLabel.place(relx=0.5, rely=0.5, anchor=CENTER)
        else:
            self.loadBarSystemLabel.destroy()