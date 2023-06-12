from tkinter import NE, Label

class ConfigPictures:
    def __init__(self) -> None:
        pass
    
    
    def labelConfigWidthHeight(self, label : Label, width : int, height : int) -> None:
        label.configure(width=width, height=height, bg=label["bg"])
        
        
    def labelPlaceXandYTopRight(self, label : Label, decalageX : int, decalageY : int, launcher : object) -> None:
        positionX = 1 - (decalageX / launcher.widthWindowLauncher)
        positionY = (decalageY / launcher.heightWindowLauncher)

        label.place(relx=positionX, rely=positionY, anchor=NE)