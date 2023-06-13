import requests
import mysql.connector

class VerifConnection:
    def __init__(self, pathSite : str) -> None:
        self.pathSite = pathSite
    
    
    def isConnectInternet(self) -> bool:
        try:
            response = requests.get(self.pathSite, timeout=5)
            return response.status_code == 200
        except requests.ConnectionError or requests.Timeout:
            print("No internet connection")
            return False
        except:
            print("No internet connection")
            return False


    def isConnectDatabase(self) -> bool:
        try:
            connectBdd = mysql.connector.connect(
                host="sql859.main-hosting.eu",
                user="u338035582_hugo",
                password="123456789Quoridor",
                database="u338035582_Quoridor"
            )
            connectBdd.close()
            return True
        except mysql.connector.Error:
            print("No bdd connection")
            return False
        except:
            print("No bdd connection")
            return False