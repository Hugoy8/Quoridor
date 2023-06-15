from tkinter import Label, CENTER, Scale
import tkinter as tk
from tkinter import ttk


class SettingsLauncher:
    def __init__(self, launcher, window, db):
        self.launcher = launcher
        self.window = window
        self.db = db
    
    
    def setBind(self, event=None):
        if self.changeButton:
            touche = event.keysym
            if touche == "space":
                touche_affichee = "space"
            else:
                touche_affichee = touche[0]

            self.addBindToFile(touche_affichee)
            self.launcher.changeButton = False
            self.wait_bind.destroy()  


    def modifyBind(self):
        self.wait_bind = Label(image=self.launcher.bind_changing, bd=0, highlightthickness=0)
        self.wait_bind.place(relx=0.6, rely=0.8, anchor=CENTER)
        self.wait_bind.bind("<Button-1>", lambda event: self.setBind(event))
        self.changeButton = True
        self.window.unbind("<Key>")
        self.window.bind("<Key>", self.setBind)
        self.bindActual()
        self.label_touche.destroy()


    def displayButtonChangeBind(self):
        bind_actual = Label(self.window, image=self.launcher.bind, cursor="hand2", bd=0, highlightthickness=0)
        bind_actual.place(relx=0.6, rely=0.8, anchor=CENTER)
        bind_actual.bind("<Button-1>", lambda event: self.modifyBind())

        self.bindActual()
    
    
    def addBindToFile(self, touche):
        with open("settings.txt", "r") as file:
            lignes = file.readlines()

        if len(lignes) >= 8:
            lignes[7] = f"<{touche}>\n" 
            with open("settings.txt", "w") as file:
                file.writelines(lignes)
            
            self.bindActual()  
        else:
            print("Le fichier settings.txt ne contient pas suffisamment de lignes.")
    
    
    def bindActual(self):
        with open("settings.txt", "r") as file:
            lignes = file.readlines()

        if len(lignes) >= 8:
            touche = lignes[7].strip()
            texte = f"{touche.upper().replace('<', '').replace('>', '')}"
            if texte == "SPACE":
                texte = "ESPACE"
                size_font = 9
            else:
                size_font = 15

            if hasattr(self, "label_touche"): 
                self.label_touche.destroy()  

            text_bind_actual = Label(self.window, text="Direction des barrières :", background="#0F2234", bd=0, highlightthickness=0, fg="white", font=("Arial", 13))
            text_bind_actual.place(relx=0.6, rely=0.75, anchor=CENTER)
            self.label_touche = Label(self.window, text=texte, background="#102C42", bd=0, highlightthickness=0, fg="white", font=("Arial", size_font), cursor="hand2")
            self.label_touche.place(relx=0.6, rely=0.8, anchor=CENTER)
            self.label_touche.bind("<Button-1>", lambda event: self.modifyBind())
        else:
            print("Le fichier settings.txt ne contient pas suffisamment de lignes.")
            
            
    def choiceFavoriteMap(self) -> None:
        def action(event) -> None:
            selected_value = listMap.get()
            try:
                if selected_value == "Jungle":
                    self.selectFavoriteMap = 1
                elif selected_value == "Space":
                    self.selectFavoriteMap = 2
                elif selected_value == "Hell":
                    self.selectFavoriteMap = 3
                elif selected_value == "Ice":
                    self.selectFavoriteMap = 4
                elif selected_value == "Electricity":
                    self.selectFavoriteMap = 5
                elif selected_value == "Sugar":
                    self.selectFavoriteMap = 6
        
                with open("settings.txt", "r") as file:
                    lines = file.readlines()
                if len(lines) >= 7:
                    lines[6] = str(self.selectFavoriteMap) + "\n"
                with open("settings.txt", "w") as file:
                    file.writelines(lines)
                    
            except ValueError:
                print(f"Error: '{selected_value}' is not a valid map")

        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        if __getSetInformation.isConnected("serverPseudo.txt") == False:
            username = __getSetInformation.get_username("serverPseudo.txt")
            listMaps = self.db.getMapByUsername(username)
        else:
            listMaps = ["Jungle", "Space", "Hell"]
        
        self.selectFavoriteMap = min(self.launcher.selectFavoriteMap, len(listMaps))  
        
        listMap = ttk.Combobox(self.window, values=listMaps, state="readonly")
        listMap.current(self.selectFavoriteMap - 1)
            
        listMap.place(relx=0.6, rely=0.68, anchor=CENTER)
        listMap.bind("<<ComboboxSelected>>", action)
        
        nameMap = Label(self.window, text="Votre carte favorite:", font=("Arial", 13), bg="#0F2234", fg="#E3F8FF")
        nameMap.place(relx=0.6, rely=0.65, anchor=CENTER)

    
    # Activer ou désactiver le son des notifications de demande d'amis
    def settingsActiveNotificationsSond(self) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 1:
                self.active_sound_notification = lines[0].strip() == "True"

        def changeStatutSoundNotification(event):
            if self.active_sound_notification:
                self.active_sound_notification = False
            else:
                self.active_sound_notification = True
            update_statut()
            lines[0] = str(self.active_sound_notification) + "\n"  

            with open("settings.txt", "w") as file:
                file.writelines(lines)  

        def update_statut():
            if self.active_sound_notification:
                self.launcher.image_statut_notification = self.launcher.yes_sound_notifications_image
            else:
                self.launcher.image_statut_notification = self.launcher.no_sound_notifications_image
            statut_sound_notification.config(image=self.launcher.image_statut_notification)

        sound_notification = Label(self.window, text="Notifications", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_notification.place(relx=0.6, rely=0.5, anchor=CENTER)

        statut_sound_notification = Label(self.window, image=self.launcher.yes_sound_notifications_image, bd=0, highlightthickness=0, cursor="hand2")
        statut_sound_notification.place(relx=0.6, rely=0.54, anchor=CENTER)
        update_statut()
        statut_sound_notification.bind("<Button-1>", changeStatutSoundNotification)
    
    
    # Modifier le son de la map
    def settingsSoundMap(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 2:
                self.sound_map = float(lines[1].strip())
                
        sound_map_texte = Label(self.window, text="Volume du son d'ambiance", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_map_texte.place(relx=0.25, rely=0.5, anchor=CENTER)
        self.slider = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider.set(self.sound_map)  
        self.slider.place(relx=0.25, rely=0.54, anchor=CENTER)
        self.slider.config(command=settingClass.saveValueToFile)
        
        
    # Modifier le son de la victoire 
    def settingsSoundVictory(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 3:
                self.sound_victory = float(lines[2].strip())
                
        sound_victory_texte = Label(self.window, text="Son de la victoire", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        sound_victory_texte.place(relx=0.43, rely=0.5, anchor=CENTER)
        self.slider_victory = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_victory.set(self.sound_victory) 
        self.slider_victory.place(relx=0.43, rely=0.54, anchor=CENTER)
        self.slider_victory.config(command=settingClass.saveVictoryValueToFile)
        
        
    # Modifier le volume du pion
    def settingsPionVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 4:
                self.pion_volume = float(lines[3].strip())
                
        pion_volume_texte = Label(self.window, text="Volume de la pose du pion", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        pion_volume_texte.place(relx=0.25, rely=0.65, anchor=CENTER)
        self.slider_pion_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_pion_volume.set(self.pion_volume)  
        self.slider_pion_volume.place(relx=0.25, rely=0.68, anchor=CENTER)
        self.slider_pion_volume.config(command=settingClass.savePionVolumeToFile)
        
        
    # Modifier le volume des clôtures
    def settingsFenceVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 5:
                self.fence_volume = float(lines[4].strip())
                
        fence_volume_texte = Label(self.window, text="Volume des barrières", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        fence_volume_texte.place(relx=0.25, rely=0.78, anchor=CENTER)
        self.slider_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_fence_volume.set(self.fence_volume)  
        self.slider_fence_volume.place(relx=0.25, rely=0.82, anchor=CENTER)
        self.slider_fence_volume.config(command=settingClass.saveFenceVolumeToFile)
        
        
    # Modifier le volume du son "no fence"
    def settingsNoFenceVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 6:
                self.no_fence_volume = float(lines[5].strip())
                
        no_fence_volume_texte = Label(self.window, text="Volume du son barrière incorrecte", bd=0, highlightthickness=0, cursor="hand2",  bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        no_fence_volume_texte.place(relx=0.43, rely=0.65, anchor=CENTER)
        self.slider_no_fence_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_no_fence_volume.set(self.no_fence_volume) 
        self.slider_no_fence_volume.place(relx=0.43, rely=0.68, anchor=CENTER)
        self.slider_no_fence_volume.config(command=settingClass.saveNoFenceVolumeToFile)
        
        
    def settingsNotificationVolume(self, settingClass : object) -> None:
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 9:
                self.notification_volume = float(lines[8].strip())

        notification_volume_texte = Label(self.window, text="Volume des notifications", bd=0, highlightthickness=0, cursor="hand2", bg="#0F2538", fg="#FFFFFF", font=("Helvetica", 13))
        notification_volume_texte.place(relx=0.43, rely=0.78, anchor=CENTER)
        self.slider_notification_volume = Scale(self.window, from_=0, to=1, resolution=0.1, orient=tk.HORIZONTAL, length=200, bg="#0F2538", fg="#FFFFFF", troughcolor="#2BB1ED", highlightthickness=0, cursor="hand2")
        self.slider_notification_volume.set(self.notification_volume)
        self.slider_notification_volume.place(relx=0.43, rely=0.82, anchor=CENTER)
        self.slider_notification_volume.config(command=settingClass.saveNotificationVolumeToFile)
    
    def loadFavoriteMap(self):
        with open("settings.txt", "r") as file:
            lines = file.readlines()
            if len(lines) >= 7:
                try:
                    return int(lines[6].strip())
                except ValueError:
                    print("Error: Invalid value for favorite map")
        return 1