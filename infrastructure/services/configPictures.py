from tkinter import NE, Label

class ConfigPictures:
    def __init__(self, launcher) -> None:
        self.launcher = launcher
    
    
    def labelConfigWidthHeight(self, label : Label, width : int, height : int) -> None:
        label.configure(width=width, height=height, bg=label["bg"])
        
        
    def labelPlaceXandYTopRight(self, label : Label, decalageX : int, decalageY : int, launcher : object) -> None:
        positionX = 1 - (decalageX / self.launcher.widthWindowLauncher)
        positionY = (decalageY / self.launcher.heightWindowLauncher)

        label.place(relx=positionX, rely=positionY, anchor=NE)