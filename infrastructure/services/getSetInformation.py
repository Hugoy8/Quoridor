class GetSetInformation:
    def getInfos(fichier1: str) -> tuple:
        try:
            with open(fichier1, 'r') as f1:
                valeurs_fichier1 = f1.read().strip()
                
                if not valeurs_fichier1: 
                    valeurs_fichier1 = " "
                else:
                    pass
                
            return valeurs_fichier1
        except IOError:
            print("Erreur : impossible de lire les fichiers.")
            
            
    def setUsername(self, username: str) -> None:
        try:
            with open('serverPseudo.txt', 'w') as fichier:
                fichier.write(username + '\n')
        except IOError:
            print("Erreur : impossible d'écrire dans le fichier.")


    def setPassword(self, password: str) -> None:
        try:
            with open('serverPseudo.txt', 'a') as fichier:
                fichier.write(password + '\n')
        except IOError:
            print("Erreur : impossible d'écrire dans le fichier.")
        
        
    def deleteFile(self, file_path : str) -> None:
        try:
            with open(file_path, 'w') as file:
                file.truncate(0)
        except IOError:
            print("Erreur : impossible de vider le fichier.")
        
        
    def isConnected(self, file_path : str) -> str or False:
        try:
            with open(file_path, 'r') as file:
                content = file.read().strip()
                return len(content) == 0
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False


    def get_username(self, file_path : str) -> str or False:
        try:
            with open(file_path, 'r') as file:
                username = file.readline().strip()
                return username
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False
        

    def get_password(self, file_path : str) -> str or False:
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if len(lines) >= 2:
                    password = lines[1].strip() 
                    return password
                else:
                    return False
        except IOError:
            print("Erreur : impossible de lire le fichier.")
            return False
