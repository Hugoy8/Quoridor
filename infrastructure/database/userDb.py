from infrastructure.database.config import Database
from infrastructure.services.getSetInformation import GetSetInformation
import hashlib


class UserDb:
    def __init__(self) -> None:
        self.statusConnection = False
    
    
    def verifUserPassword(self, username : str) -> bool:
        passwordUserDataBase = Database().selectPassword(username)
        
        if passwordUserDataBase != []:
            passwordUserLocal = GetSetInformation().get_password('serverPseudo.txt')
            
            if passwordUserLocal == False:
                return (False, self)
            else:
                if passwordUserDataBase[0][0] == passwordUserLocal:
                    self.statusConnection = True
                    return (True, self)
                else:
                    return (False, self)
        else:
            return (False, self)

    
    def loginUser(self, launcher : object) -> None:
        launcher.db.connectDb()
        select_query = launcher.db.select()
        query = "SELECT * FROM users WHERE username = %s"
        username = launcher.loginUsername.get().rstrip()
        password = launcher.loginPassword.get().replace(" ", "")

        select_query.execute(query, (username,))
        result = select_query.fetchone()
        select_query.close()

        if result is not None:
            stored_password = result[2]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if stored_password == hashed_password:
                launcher.pseudo = username
                
                GetSetInformation().setUsername(username)
                GetSetInformation().setPassword(hashed_password)
                    
                launcher.menuCreateGameSolo(event=None)
                return launcher.pseudo
            else:
                print("Mot de passe incorrect")
        else:
            print("Utilisateur introuvable")
        
        
    def createAccount(self, launcher : object) -> None:
        username = launcher.registerUsername.get().rstrip()
        password = launcher.registerPassword.get().replace(" ", "")
        confirm_password = launcher.registerPasswordConfirm.get()

        if not username or not password or not confirm_password:
            print("Veuillez remplir tous les champs")
        elif password != confirm_password:
            print("Les mots de passe ne correspondent pas")
        else:
            # Check si le username existe deja.
            launcher.db.connectDb()
            select_query = launcher.db.select()
            select_query.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = select_query.fetchone()
            select_query.close()

            if existing_user:
                print("Ce pseudo existe déjà")
            else:
                try:
                    # Si le pseudo est unique on l'insère dans la base de données
                    insert_query = launcher.db.insert()
                    query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                    hashed_password = hashlib.sha256(password.encode()).hexdigest()

                    params = (username, hashed_password)
                    insert_query.execute(query, params)
                    
                    # Fermeture de la requête d'insertion
                    insert_query.close()

                    # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                    launcher.pseudo = username
                    launcher.bg_not_connected.destroy()
                    launcher.menuCreateGameSolo(event=None)
                    
                    passwordDataBaseReceived = Database().selectPassword(username)
                    print(passwordDataBaseReceived)
                    
                    GetSetInformation().setUsername(username)
                    GetSetInformation().setPassword(passwordDataBaseReceived[0][0])
                    
                    self.statusConnection = True
                finally:
                    # Fermeture de la connexion à la base de données
                    launcher.db.close()


    def deconnexionUser(self, file_path : str, launcher : object) -> None:
        GetSetInformation().deleteFile(file_path)
        
        self.statusConnection = False
        
        launcher.profile_account_label.destroy()
        launcher.friends_canvas.destroy()
        launcher.account_button.destroy()
        launcher.createMenu(launcher.getStatut())
        
        if launcher.is_shop == True:
            launcher.displayShop()