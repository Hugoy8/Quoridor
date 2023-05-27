from tkinter import *
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from infrastructure.services.services import restartGame
from domain.network.network import joinSession, startSession
from domain.network.scanNetwork import ScanNetwork
from infrastructure.database.config import Database
import hashlib

class QuoridorLauncher:
    def __init__(self, db: Database) -> None:
        self.window = Tk()
        self.window.title("Quoridor")
        self.window.state('zoomed')
        self.window.attributes("-fullscreen", True)
        self.window.minsize(self.window.winfo_screenwidth(), self.window.winfo_screenheight())
        self.window.iconbitmap('./assets/images/logo.ico')
        self.statut = 0
        self.modeToSolo()
        self.selectPlayer = 2
        self.selectIA = 0
        self.selectSize = 5
        self.selectFence = 4
        self.selectMap = 1
        self.ip = None
        self.port = None
        
        self.loginPassword = None
        self.loginButton = None
        self.winButton = None
        self.loginUsername = None
        self.login = None
        self.registerButton = None
        self.register = None
        self.registerUsername = None
        self.registerPassword = None
        self.db = db
        self.insert_query = None
        
        self.login_created = None
        self.register_created = None
        
        self.pseudo = " "

    def background(self) -> None:
        # Image de fond
        self.bg_image = Image.open(f"./assets/images/launcher/launcher{self.statut}.png")
        self.bg_image = self.bg_image.resize((self.window.winfo_screenwidth(), self.window.winfo_screenheight()))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        self.bg_label = Label(self.window, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    def addText(self) -> None:
        # Ajout du texte
        self.text = Label(self.window, text="Nombre de joueurs", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.267, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//2.8)
        self.text = Label(self.window, text="bientôt disponible", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.85, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.1)
        
        
        self.text = Label(self.window, text="Taille du tableau : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.267, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.5)
        self.text = Label(self.window, text="Nombre de barrière : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.5, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.5)
        self.text = Label(self.window, text="Choix de la map : ", font=("Arial", 10), bg="#0D2338", fg="#FFF")
        self.text.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.8, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.5)
    
    def numberIA(self) -> None:
        def action(event) -> None:
            self.selectIA = int(listIA.get())
            print("IA : ", self.selectIA)
            
        listIAs=[0, 1, 2, 3]
        listIA = ttk.Combobox(self.window, values=listIAs, state="readonly")
        listIA.current(0)
        listIA.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.49, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.1)
        listIA.bind("<<ComboboxSelected>>", action)

    def numberPlayer(self) -> None:
        def action(event) -> None:
            self.selectPlayer = int(listPlayer.get())
            print("Player : ", self.selectPlayer)

        listPlayers=[1, 2, 3, 4]
        listPlayer = ttk.Combobox(self.window, values=listPlayers, state="readonly")
        listPlayer.current(1)
        listPlayer.place(x=360, y=650)
        if self.statut==1:
            listPlayer.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.49, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.1)
        listPlayer.bind("<<ComboboxSelected>>", action)
        
    def sizeBoard(self) -> None:
        def action(event) -> None:
            self.selectSize = int(listSize.get())
            print("Board : ", self.selectSize)

        listSizes=[5, 7, 9, 11]
        listSize = ttk.Combobox(self.window, values=listSizes, state="readonly")
        listSize.current(0)
        listSize.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.267, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//4)
        if self.statut==2:
            listSize.place(x= self.window.winfo_screenwidth()//1.68, y=self.window.winfo_screenheight()//1.48)
        listSize.bind("<<ComboboxSelected>>", action)
        
    def numberFence(self) -> None:
        def action(event) -> None:
            self.selectFence = int(listFence.get())
            print("Fence : ", self.selectFence)

        listFences = []
        for i in range(4, 41):
            if i % 4 == 0:
                listFences.append(i)

        listFence = ttk.Combobox(self.window, values=listFences, state="readonly")
        listFence.current(0)
        listFence.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.5, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//4)
        if self.statut==2:
            listFence.place(x= self.window.winfo_screenwidth()//1.38, y=self.window.winfo_screenheight()//1.48)
        listFence.bind("<<ComboboxSelected>>", action)

    def choiceMap(self) -> None:
        def action(event) -> None:
            selected_value = listMap.get()
            print("Value : ", selected_value)
            try:
                if selected_value == "Jungle":
                    self.selectMap = 1
                elif selected_value == "Space":
                    self.selectMap = 2
                elif selected_value == "Hell":
                    self.selectMap = 3
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")

        listMaps=["Jungle", "Space", "Hell"]
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(0)
        listMap.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.8, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//4)
        if self.statut == 1 or self.statut == 3:
            listMap.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//2, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//4)
        elif self.statut == 2:
            listMap.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.53, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.05)
        listMap.bind("<<ComboboxSelected>>", action)
        
    def buttonStart(self) -> None:
        def start_game() -> None:
            grid_size = self.selectSize
            nbr_fences = self.selectFence
            nb_ia = self.selectIA
            nb_player = self.selectPlayer + self.selectIA
            map = self.selectMap
            self.window.destroy()
            if grid_size == 5 and nbr_fences > 20:
                nbr_fences = 20
            restartGame(grid_size, nb_player, nb_ia, nbr_fences, map)

        start = Button(self.window, text="START", command=start_game, bg="#0D2338", fg="#FFF", font=("Arial", 15), width=10, cursor="hand2",  activebackground="#035388",  activeforeground="white")
        start.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//2.3, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//3.8)
        
    def changeMode(self) -> None:
        for child in self.window.winfo_children():
            if child.winfo_exists():
                child.destroy()
                
    def choiceMode(self) -> None:
        image_path = "./assets/images/launcher/fond_menu.png"
        img = Image.open(image_path)
        img = img.resize((int(self.window.winfo_screenwidth()/18), int(self.window.winfo_screenheight()-self.window.winfo_screenheight()/1.45)))
        fond_menu = ImageTk.PhotoImage(img)

        menu_label = Label(self.window, image=fond_menu, bg="#035388")
        menu_label.image = fond_menu
        menu_label.place(x=self.window.winfo_screenwidth()-self.window.winfo_screenwidth()//1.03, y=self.window.winfo_screenheight()-self.window.winfo_screenheight()//1.43)

        image_path = "./assets/images/launcher/solo_mode.png"
        img = Image.open(image_path)
        img = img.resize((int(self.window.winfo_screenwidth()/18), int(self.window.winfo_screenheight()-self.window.winfo_screenheight()/1.1)))
        solo_mode = ImageTk.PhotoImage(img)

        image_path = "./assets/images/launcher/rejoindre.png"
        img2 = Image.open(image_path)
        img2 = img2.resize((int(self.window.winfo_screenwidth()/23), int(self.window.winfo_screenheight()-self.window.winfo_screenheight()/1.09)))
        rejoindre = ImageTk.PhotoImage(img2)

        image_path = "./assets/images/launcher/host.png"
        img3 = Image.open(image_path)
        img3 = img3.resize((int(self.window.winfo_screenwidth()/23), int(self.window.winfo_screenheight()-self.window.winfo_screenheight()/1.09)))
        host = ImageTk.PhotoImage(img3)

        solo = Button(menu_label, image=solo_mode, command=self.modeToSolo, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        solo.image = solo_mode  
        solo.place(x=2, y=10)

        rejoindre_mode = Button(menu_label, image=rejoindre, command=self.modeToSelectGame, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        rejoindre_mode.image = rejoindre
        rejoindre_mode.place(x=10, y=110)

        host_mode = Button(menu_label, image=host, command=self.modeToCreateGame, cursor="hand2", highlightthickness=0, bd=0, bg="#035388", activebackground="#035388")
        host_mode.image = host 
        host_mode.place(x=10, y=210)
        
    def modeToSolo(self) -> None:
        self.changeMode()
        self.statut = 0
        self.background()
        self.numberIA()
        self.choiceMode()
        self.addText()
        self.numberFence()
        self.numberPlayer()
        self.sizeBoard()
        self.choiceMap()
        self.buttonStart()
        
        
    def create_entries(self) -> None:
        self.entry1 = Entry(self.window, width=20)
        self.entry1.place(x=self.window.winfo_screenwidth()//4.6, y=self.window.winfo_screenheight()//1.48)

        self.entry2 = Entry(self.window, width=20)
        self.entry2.place(x=self.window.winfo_screenwidth()//2.85, y=self.window.winfo_screenheight()//1.48)

        self.entry3 = Entry(self.window, width=20)
        self.entry3.place(x=self.window.winfo_screenwidth()//2.08, y=self.window.winfo_screenheight()//1.48)
        
        start = Button(self.window, text="Rejoindre la partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.joinGameNewtork)
        start.place(x=self.window.winfo_screenwidth()//5, y=self.window.winfo_screenheight()//1.35)
        
        reset_button = Button(self.window, text="Rechercher une partie", font=("Arial", 13),  cursor="hand2", fg="#FFF",  bg="#486581", command=self.displayIp, width=25, activebackground="#486581",  activeforeground="white")
        reset_button.place(x=self.window.winfo_screenwidth()//3, y=self.window.winfo_screenheight()//1.35)
        
    def joinGameNewtork(self) -> None:
        ip = self.entry1.get()
        port = int(self.entry2.get())
        self.window.destroy()
        self.db.insertUsername(ip, port, self.pseudo)
        joinSession(ip, port, self.selectMap)
        
    def startGame(self) -> None:
        ip = "127.0.0.1"
        port = int(self.entry_port.get())
        nbr_player = int(self.nbr_player_network.get())
        self.window.destroy()
        grid_size = self.selectSize
        nbr_fences = self.selectFence
        map = self.selectMap
        if grid_size == 5 and nbr_fences > 20:
            nbr_fences = 20
        
        self.db.dropTableIfExists(ip, port)
        self.db.createTableGame(ip, port)
        self.db.insertUsername(ip, port, self.pseudo)
        startSession(port, nbr_player, grid_size, nbr_player, 0, nbr_fences, map)
    

    def entriesNetwork(self) -> None:
        self.nbr_player_network = Entry(self.window, width=20)
        self.nbr_player_network.place(x= self.window.winfo_screenwidth()//4.5, y=self.window.winfo_screenheight()//1.48)
        
        self.entry_port = Entry(self.window, width=20)
        self.entry_port.place(x= self.window.winfo_screenwidth()//1.16, y=self.window.winfo_screenheight()//1.48)

    def startButtonNetwork(self) -> None:
        start = Button(self.window, text="Créer une partie", bg="#2BB0ED", fg="#FFF", font=("Arial", 13), width=20, height=2,  cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.startGame)
        start.place(x= self.window.winfo_screenwidth()//4.8, y=self.window.winfo_screenheight()//1.35)

    def displayIp(self) -> None:
        scanNetwork = ScanNetwork(8000, 8005)
        scanNetwork.scan()
        listip = scanNetwork.getIp()
        print(listip)
        if len(listip) == 0:
            self.statut = 3
            self.modeToSelectGame()
        for i, address in enumerate(listip):
            ip, port = address.split(":")
            frame = tk.LabelFrame(self.window, text=ip, fg="white", bg="blue", width=200)
            x = self.window.winfo_screenwidth() - 200 - 10  
            y = (i+1)/(len(listip)+1) * self.window.winfo_screenheight()
            frame.place(x=x, y=y, anchor='ne')
            label = tk.Label(frame, text="Port: " + port, fg="white", bg="blue")
            label.pack(padx=5, pady=5)
            frame.bind("<Button-1>", lambda event, ip=ip, port=port: self.onIpClick(event, port))
            
    def onIpClick(self, event, port):
        ip = event.widget['text']
        port = int(port)
        self.window.destroy()
        self.db.insertUsername(ip, port, self.pseudo)
        joinSession(ip, port, self.selectMap)
        
    def modeToSelectGame(self) -> None:
        self.changeMode()
        if self.statut != 3:
            self.statut = 1
        self.background()
        self.choiceMode()
        self.create_entries()
        # self.displayIp()
        self.choiceMap()
        self.buttonConnexion()
        self.buttonRegister()
        
    def modeToCreateGame(self) -> None:
        self.changeMode()
        self.statut = 2
        self.background()
        self.choiceMode()
        self.entriesNetwork()
        self.startButtonNetwork()
        self.sizeBoard()
        self.choiceMap()
        self.numberFence()
        self.buttonConnexion()
        self.buttonRegister()
        
# -------------------------DATABASE ---------------------------
    def buttonConnexion(self):
        login = Button(self.window, text="Se connecter", bg="#2BB0ED", fg="#FFF", 
                       font=("Arial", 13), width=20, height=2,  cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.connexion)
        login.pack(side=RIGHT)
    
    def buttonRegister(self):
        register = Button(self.window, text="S'inscrire", bg="#2BB0ED", fg="#FFF", 
                          font=("Arial", 13), width=20, height=2,  cursor="hand2", activebackground="#035388",  activeforeground="white", command=self.inscription)
        register.pack(side=RIGHT, pady=50)
        
    def addRegister(self):
        if not self.register_created:
            self.register = Frame(self.window)
            self.register.pack()

            self.registerUsername = Entry(self.register)
            self.registerUsername.pack()

            self.registerPassword = Entry(self.register)
            self.registerPassword.pack()

            self.registerButton = Button(self.register, text="Register", command=self.createAccount)
            self.registerButton.pack()

            self.register_created = True

        if self.login_created:
            self.login.pack_forget()  # Masquer le widget login s'il est affiché


    def createAccount(self):
        self.db.connectDb()
        username = self.registerUsername.get()
        password = self.registerPassword.get()
        if not username or not password:
            # Vérifier si le label existe déjà, le mettre à jour sinon le créer
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="Please complete all mandatory fields.")
            else:
                self.infoLabel = Label(self.window, text="Please complete all mandatory fields.")
                self.infoLabel.pack()
        else:
            # Check if the username already exists
            select_query = self.db.select()
            select_query.execute("SELECT username FROM users WHERE username = %s", (username,))
            existing_user = select_query.fetchone()
            select_query.close()

            if existing_user:
                # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text=f"This username '{username}' already exists. Please choose another.")
                else:
                    self.infoLabel = Label(self.window, text=f"This username '{username}' already exists. Please choose another.")
                    self.infoLabel.pack()
            else:
                # Username is unique, register
                insert_query = self.db.insert()
                query = "INSERT INTO users (username, password) VALUES (%s, %s)"

                hashed_password = hashlib.sha256(password.encode()).hexdigest()

                params = (username, hashed_password)
                insert_query.execute(query, params)
                insert_query.close()
                # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text=f"{username} you have successfully subscribed !")
                    self.pseudo = username
                    return self.pseudo
                else:
                    self.infoLabel = Label(self.window, text=f"{username} you have successfully subscribed !")
                    self.infoLabel.pack()
                    self.pseudo = username
                    return self.pseudo
        
    def addLogin(self):
        if not self.login_created:
            self.login = Frame(self.window)
            self.login.pack()

            self.loginUsername = Entry(self.login)
            self.loginUsername.pack()

            self.loginPassword = Entry(self.login)
            self.loginPassword.pack()

            self.loginButton = Button(self.login, text="Login", command=self.loginUser)
            self.loginButton.pack()

            self.login_created = True

        if self.register_created:
            self.register.pack_forget() 

    def loginUser(self):
        self.db.connectDb()
        select_query = self.db.select()
        query = "SELECT * FROM users WHERE username = %s"
        username = self.loginUsername.get()
        password = self.loginPassword.get()

        select_query.execute(query, (username,))
        result = select_query.fetchone()
        select_query.close()

        if result is not None:
            stored_password = result[2]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()

            if stored_password == hashed_password:
                # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text="You are logged")
                    self.pseudo = username
                    return self.pseudo
                else:
                    self.infoLabel = Label(self.window, text="You are logged")
                    self.infoLabel.pack()
                    self.pseudo = username
                    return self.pseudo
            else:
                # Vérifier si le label existe déjà, le mettre à jour sinon le créer
                if hasattr(self, "infoLabel"):
                    self.infoLabel.config(text="Incorrect password")
                else:
                    self.infoLabel = Label(self.window, text="Incorrect password")
                    self.infoLabel.pack()
        else:
            # Vérifier si le label existe déjà, le mettre à jour sinon le créer
            if hasattr(self, "infoLabel"):
                self.infoLabel.config(text="User not found")
            else:
                self.infoLabel = Label(self.window, text="User not found")
                self.infoLabel.pack()
    
    def inscription(self):
        self.addRegister()
        self.login_created = False  # Réinitialiser l'état du widget login

    def connexion(self):
        self.addLogin()
        self.register_created = False  # Réinitialiser l'état du widget register
        
run = QuoridorLauncher(Database())  
run.window.mainloop()
        