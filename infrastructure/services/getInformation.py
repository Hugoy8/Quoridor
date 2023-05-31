class GetInformation:
    def setIP(ip):
        try:
            with open('serverIP.txt', 'w') as fichier:
                fichier.write(ip + '\n')
            print("IP enregistrée avec succès dans le fichier.")
        except IOError:
            print("Erreur : impossible d'écrire l'ip dans le fichier.")


    def setPort(port):
        try:
            with open('serverPort.txt', 'w') as fichier:
                fichier.write(str(port) + '\n')
            print("Port enregistré avec succès dans le fichier.")
        except IOError:
            print("Erreur : impossible d'écrire le port dans le fichier.")
            
    
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