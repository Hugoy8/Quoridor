class Settings:
    def __init__(self, launcher : object) -> None:
        self.launcher = launcher
        
    
    def saveNotificationVolumeToFile(self, value : float) -> None:
        value = float(value)
        
        with open("settings.txt", "r") as file:
            lines = file.readlines()

        if len(lines) >= 9:
            lines[8] = str(value) + "\n"

        with open("settings.txt", "w") as file:
            file.writelines(lines)
            
            
    def saveNoFenceVolumeToFile(self, value : float) -> None:
        value = float(value)
        
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            
        if len(lines) >= 6:
            lines[5] = str(value) + "\n"
            
        with open("settings.txt", "w") as file:
            file.writelines(lines)
        
        
    def saveFenceVolumeToFile(self, value : float) -> None:
        value = float(value)
        
        # Modifier la cinquième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            
        if len(lines) >= 5:
            lines[4] = str(value) + "\n"
            
        with open("settings.txt", "w") as file:
            file.writelines(lines)
            
            
    def savePionVolumeToFile(self, value : float) -> None:
        value = float(value)
        
        # Modifier la quatrième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            
        if len(lines) >= 4:
            lines[3] = str(value) + "\n"
            
        with open("settings.txt", "w") as file:
            file.writelines(lines)
            
            
    def saveVictoryValueToFile(self, value : float) -> None:
        value = float(value)
        
        # Modifier la troisième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            
        if len(lines) >= 3:
            lines[2] = str(value) + "\n"
            
        with open("settings.txt", "w") as file:
            file.writelines(lines)
            
            
    def saveValueToFile(self, value : float) -> None:
        value = float(value)
        
        # Modifier la deuxième ligne du fichier "settings.txt" avec la nouvelle valeur
        with open("settings.txt", "r") as file:
            lines = file.readlines()
        
        if len(lines) >= 2:
            lines[1] = str(value) + "\n"
        
        with open("settings.txt", "w") as file:
            file.writelines(lines)