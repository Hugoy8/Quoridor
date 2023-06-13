from tkinter import *

class Authentification:
    def __init__(self, launcher, window, statut, db):
        self.launcher = launcher
        self.window = window
        self.statut = statut
        self.login = True
        self.db = db


    def getStatut(self) -> int:
        return self.statut
    
    
    def displayAccount(self) -> None:
        self.launcher.changeMode()
        self.launcher.is_shop = False
        statut = self.getStatut()
        self.launcher.statut = 4
        self.launcher.background(self.launcher.statut)
        self.launcher.createMenu(statut, "")
        self.launcher.leaveLauncher()
        self.addLogin()
    
    
    def authentification(self) -> None:
        if self.login == True:
            image_actual_login = self.launcher.login_image
            image_actual_register = self.launcher.register_false_image
            self.login = False

        elif self.login == False:
            image_actual_login = self.launcher.login_false_image
            image_actual_register = self.launcher.register_image
            self.login = True
        
        relXButtonMove = 0.271
        self.login_button = Label(self.window, image=image_actual_login, bd=0, highlightthickness=0, cursor="hand2")
        self.login_button.place(relx=relXButtonMove, rely=0.48, anchor=CENTER)
        self.login_button.bind("<Button-1>", lambda event:self.addLogin())
        
        self.register_button = Label(self.window, image=image_actual_register, bd=0, highlightthickness=0, cursor="hand2")
        self.register_button.place(relx=(relXButtonMove + (((189 * 100) / self.window.winfo_screenwidth()) / 100)), rely=0.48, anchor=CENTER)
        self.register_button.bind("<Button-1>", lambda event:self.addRegister())


    def addLogin(self):
        self.authentification()

        def addLoginUserFunc() -> None:
            from infrastructure.services.verifConnection import VerifConnection
            if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
                from infrastructure.database.userDb import UserDb
                UserDb().loginUser(self.launcher, self)
            else:
                self.launcher.errorClientNetwork("noNetwork")
            
        if len(self.launcher.widget_register) > 0:
            for widget in self.launcher.widget_register:
                widget.destroy()
                
        relXLabel = 0.271
        username = Label(self.window, text="Pseudo :", font=("Arial", 16), bg="#0F2234", fg="#E3F8FF")
        username.place(relx=relXLabel, rely=0.55, anchor=NW)
        
        self.loginUsername = Entry(self.launcher.login, fg="white", width=31, font=("Arial", 16), background="#062037", highlightbackground="#486581")
        self.loginUsername.place(relx=relXLabel, rely=0.58, anchor=NW)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 16), bg="#0F2234", fg="#E3F8FF")
        password.place(relx=relXLabel, rely=0.65, anchor=NW)
        
        self.loginPassword = Entry(self.launcher.login, show="*", fg="white", width=31, font=("Arial", 16), background="#062037", highlightbackground="#486581")
        self.loginPassword.place(relx=relXLabel, rely=0.68, anchor=NW)

        self.loginButton =  Label(self.launcher.login, image=self.launcher.login_button, cursor="hand2", bd=0, highlightthickness=0)
        self.loginButton.place(relx=0.318, rely=0.78, anchor=CENTER)
        self.loginButton.bind("<Button-1>", lambda event:addLoginUserFunc())
        
        self.launcher.widget_login = [username, self.loginUsername, password, self.loginPassword, self.loginButton]
        
        
    def addRegister(self):
        self.authentification()
        
        def addAccountFunc() -> None:
            from infrastructure.services.verifConnection import VerifConnection
            if VerifConnection("").isConnectDatabase() and VerifConnection("https://google.com").isConnectInternet():
                from infrastructure.database.userDb import UserDb
                UserDb().createAccount(self.launcher, self)
            else:
                self.launcher.errorClientNetwork("noNetwork")
                
            
        if len(self.launcher.widget_login) > 0:
            for widget in self.launcher.widget_login:
                widget.destroy()
            
        relXLabel = 0.271
        username = Label(self.window, text="Pseudo :", font=("Arial", 16), bg="#0F2234", fg="#E3F8FF")
        username.place(relx=relXLabel, rely=0.5, anchor=NW)
        self.registerUsername = Entry(self.launcher.register, fg="white", width=31, font=("Arial", 16), background="#062037", highlightbackground="#486581")
        self.registerUsername.place(relx=relXLabel, rely=0.53, anchor=NW)

        password = Label(self.window, text="Mot de passe :", font=("Arial", 16), bg="#0F2234", fg="#E3F8FF")
        password.place(relx=relXLabel, rely=0.58, anchor=NW)
        self.registerPassword = Entry(self.launcher.register, show="*", fg="white", width=31, font=("Arial", 16), background="#062037", highlightbackground="#486581")
        self.registerPassword.place(relx=relXLabel, rely=0.61, anchor=NW)

        passwordConfirm = Label(self.window, text="Confirmer le mot de passe :", font=("Arial", 16), bg="#0F2234", fg="#E3F8FF")
        passwordConfirm.place(relx=relXLabel, rely=0.66, anchor=NW)
        self.registerPasswordConfirm = Entry(self.launcher.register, show="*", fg="white", width=31, font=("Arial", 16), background="#062037", highlightbackground="#486581")
        self.registerPasswordConfirm.place(relx=relXLabel, rely=0.69, anchor=NW)
            
        self.registerButton = Label(self.window, image=self.launcher.register_button, cursor="hand2", bd=0, highlightthickness=0)
        self.registerButton.place(relx=0.318, rely=0.78, anchor=CENTER)
        self.registerButton.bind("<Button-1>", lambda event:addAccountFunc())
        self.launcher.widget_register = [username, self.registerUsername, password, self.registerPassword, passwordConfirm, self.registerPasswordConfirm, self.registerButton]