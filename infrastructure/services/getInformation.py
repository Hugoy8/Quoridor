class GetInformation:
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