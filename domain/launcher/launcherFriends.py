from tkinter import *
import tkinter as tk
from domain.network.network import joinSession, startSession

class launcherFriends:
    def __init__(self, launcher, window, db, launcherMenu):
        self.launcher = launcher
        self.window = window
        self.db = db
        self.launcherMenu = launcherMenu
    
    
    def displayFriends(self) -> None:
        friends_panel = Label(self.window, image=self.launcher.list_friends, bd=0, highlightthickness=0)
        friends_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayListFriends(friends_panel)
        
        
    def quit_friends_list(self, panel) -> None:
        panel.destroy()
        self.launcherMenu.createAccountMenu()
        if self.launcher.delete_friend_popup_label is not None:
            self.launcher.delete_friend_popup_label.destroy()
            
        
    def display_notifications(self, friends_panel : Label) -> None:
        def destroy_friends_list():
            friends_panel.destroy()
            
        destroy_friends_list()
        notifications_panel = Label(self.window, image=self.launcher.list_notifications, bd=0, highlightthickness=0)
        notifications_panel.place(relx=0.90, rely=0.5, anchor=CENTER)

        self.displayInvitatins(notifications_panel, True)
        
        self.displayGameInvitations(notifications_panel, False)
        
        self.notifications_panel = notifications_panel
        
        
    def quit_notifications(self, notifications_panel) -> None:
        notifications_panel.destroy()
        self.launcherMenu.createAccountMenu()
        if self.launcher.delete_friend_popup_label is not None:
            self.launcher.delete_friend_popup_label.destroy()


    def back_friends_list(self, notifications_panel) -> None:
        notifications_panel.destroy()
        self.displayFriends()
            
            
    def displayGameInvitations(self, notifications_panel : Label, btnDisplay : bool) -> None:
        def blink_text(label):
            current_color = label.cget("fg")
            new_color = "#D7D03A" if current_color == "#93904D" else "#93904D"
            label.config(fg=new_color)
            label.after(500, blink_text, label)
        
        if btnDisplay:
            button_leave_friends = Label(notifications_panel, image=self.launcher.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
            button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.launcher.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.1, rely=0.045, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
        
        text_invitation = Label(notifications_panel, text="Invitation à des parties :", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
        text_invitation.place(relx=0.09, rely=0.5, anchor=NW)
        friend_game_demands = self.db.selectAllInvitingGames(self.launcher.getInformation.get_username("serverPseudo.txt")) # demande de partie via la bdd
        if len(friend_game_demands) == 0:
            no_friend_demand = Label(notifications_panel, image=self.launcher.no_notification_text, bd=0, highlightthickness=0)
            no_friend_demand.place(relx=0.09, rely=0.55, anchor=NW)
        else:
            for index, friend in enumerate(friend_game_demands):
                friend = friend[:19] + ".." if len(friend) > 21 else friend
                label_game_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="#D7D03A", bg="#102A43")
                label_game_demand.place(relx=0.1, rely=0.54 + index * 0.05, anchor=NW)
                blink_text(label_game_demand)

                accept_game_demand = Label(notifications_panel, image=self.launcher.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
                accept_game_demand.place(relx=0.75, rely=0.55 + index * 0.05, anchor=CENTER)
                accept_game_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptGameDemand(friend))
                
                refuse_game_demand = Label(notifications_panel, image=self.launcher.delete_friends, bd=0, highlightthickness=0, cursor="hand2",)
                refuse_game_demand.place(relx=0.9, rely=0.55 + index * 0.05, anchor=CENTER)
                refuse_game_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseGameDemand(friend))


    def displayInvitatins(self, notifications_panel : Label, btnDisplay: bool) -> None:
        if btnDisplay:
            button_leave_friends = Label(notifications_panel, image=self.launcher.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
            button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
            button_leave_friends.bind("<Button-1>", lambda event: self.quit_notifications(notifications_panel))

            back_list_friends = Label(notifications_panel, image=self.launcher.back_list_friends, bd=0, highlightthickness=0, cursor="hand2")
            back_list_friends.place(relx=0.1, rely=0.045, anchor=CENTER)
            back_list_friends.bind("<Button-1>", lambda event: self.back_friends_list(notifications_panel))
        
        text_friend_demand = Label(notifications_panel, text="Demande d'amis :", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
        text_friend_demand.place(relx=0.09, rely=0.1, anchor=NW)
        
        friend_demands = self.db.selectAllInviting(self.launcher.getInformation.get_username("serverPseudo.txt"), False)  # demande d'amis à récupérer depuis la bdd
        if len(friend_demands) == 0:
            no_friend_demand = Label(notifications_panel, image=self.launcher.no_notification_text, bd=0, highlightthickness=0)
            no_friend_demand.place(relx=0.09, rely=0.145, anchor=NW)
        else:
            for index, friend in enumerate(friend_demands):
                friend = friend[:19] + ".." if len(friend) > 21 else friend
                label_friend_demand = Label(notifications_panel, text=friend, cursor="hand2", bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
                label_friend_demand.place(relx=0.09, rely=0.14 + index * 0.05, anchor=NW)

                valid_friend_demand = Label(notifications_panel, image=self.launcher.valid_friends, bd=0, highlightthickness=0, cursor="hand2")
                valid_friend_demand.place(relx=0.75, rely=0.15 + index * 0.05, anchor=CENTER)
                valid_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.acceptFriendDemand(friend))

                delete_friend_demand = Label(notifications_panel, image=self.launcher.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
                delete_friend_demand.place(relx=0.9, rely=0.15 + index * 0.05, anchor=CENTER)
                delete_friend_demand.bind("<Button-1>", lambda event, friend=friend: self.refuseFriendDemand(friend))


    def displayListFriends(self, friends_panel : Label) -> None:
        if len(self.db.selectAllInviting(self.launcher.getInformation.get_username("serverPseudo.txt"), False)) != 0 or len(self.db.selectAllInvitingGames(self.launcher.getInformation.get_username("serverPseudo.txt"))) != 0:
            image_notifications = self.launcher.notifications
        else:
            image_notifications = self.launcher.no_notification
        button_notifications = Label(friends_panel, image=image_notifications, bd=0, highlightthickness=0, cursor="hand2")
        button_notifications.place(relx=0.1, rely=0.045, anchor=CENTER)
        button_notifications.bind("<Button-1>", lambda event: self.display_notifications(friends_panel))

        button_leave_friends = Button(friends_panel, image=self.launcher.leave_friends, bd=0, highlightthickness=0, cursor="hand2")
        button_leave_friends.place(relx=0.9, rely=0.045, anchor=CENTER)
        button_leave_friends.bind("<Button-1>", lambda event: self.quit_friends_list(friends_panel))

        ResultFriends = self.db.selectAllFriends(self.launcher.getInformation.get_username("serverPseudo.txt"))  # liste des amis à récupérer depuis la bdd
        friends = ResultFriends[1]
        for index, friend in enumerate(friends):
            
            label_friend = Label(friends_panel, text=friend, bd=0, highlightthickness=0, font=("Arial", 13), fg="white", bg="#102A43")
            label_friend.place(relx=0.09, rely=0.2 + index * 0.05, anchor=NW)

            invite_friend = Label(friends_panel, image=self.launcher.invite_friends, bd=0, highlightthickness=0, cursor="hand2")
            invite_friend.place(relx=0.75, rely=0.21 + index * 0.05, anchor=CENTER)
            invite_friend.bind("<Button-1>", lambda event, friend=friend: self.invitFriend(friend))

            delete_friend = Label(friends_panel, image=self.launcher.delete_friends, bd=0, highlightthickness=0, cursor="hand2")
            delete_friend.place(relx=0.9, rely=0.21 + index * 0.05, anchor=CENTER)
            delete_friend.bind("<Button-1>", lambda event, friend=friend: self.deleteFriends(friend))

        self.entry_friend = Entry(friends_panel, bd=3, width=25, font=("Arial", 13), background="#102A43", foreground="white", insertbackground="white", highlightbackground="#2BB0ED", highlightcolor="#2BB0ED", highlightthickness=1, relief=FLAT)
        self.entry_friend.place(relx=0.42, rely=0.13, anchor=CENTER)

        search_button = Button(friends_panel, image=self.launcher.search_friends, bd=0, highlightthickness=0, cursor="hand2", command=lambda: self.searchFriend(self.entry_friend.get()))
        search_button.place(relx=0.9, rely=0.13, anchor=CENTER)
        
        self.friends_panel = friends_panel
        
        
    def invitFriend(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        listInfosInvitGames = [self.db, str(GetSetInformation().get_username("serverPseudo.txt")), friend[0]]
        self.window.destroy()
        startSession(8003, 2, 9, 2, 0, 20, GetSetInformation().getLinesSettings("settings.txt", 7)[0], listInfosInvitGames, True)
        
        
    def acceptFriendDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.acceptInviting(str(GetSetInformation().get_username("serverPseudo.txt")), friend[0])
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseFriendDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.deleteInviting(friend[0], str(GetSetInformation().get_username("serverPseudo.txt")))
        self.notifications_panel.config(text="")
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def acceptGameDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        resultGameInfo = self.db.acceptInvitingGames(str(GetSetInformation().get_username("serverPseudo.txt")), friend[0])
        (ip, port) = resultGameInfo[0][0].split(":")
        
        mapFavoritePlayer = GetSetInformation().getLinesSettings("settings.txt", 7)
        
        joinSession(ip, int(port), int(mapFavoritePlayer[0]))
        
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
    
    
    def refuseGameDemand(self, friend : tuple) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        
        self.db.deleteInvitingGames(friend[0], str(GetSetInformation().get_username("serverPseudo.txt")))
        for widget in self.notifications_panel.winfo_children():
            widget.destroy()
        self.displayInvitatins(self.notifications_panel, True)
        
        self.displayGameInvitations(self.notifications_panel, False)
        
        
    def searchFriend(self, friend : str) -> None:
        from infrastructure.services.getSetInformation import GetSetInformation
        __getSetInformation = GetSetInformation()
        
        friend = friend.replace(" ", "")
        invList = self.db.selectAllInviting(__getSetInformation.get_username("serverPseudo.txt"), False)
        ResultFriends = self.db.selectAllFriends(__getSetInformation.get_username("serverPseudo.txt"))
        friendsList = ResultFriends[1]
        
        if friend != "" and friend != __getSetInformation.get_username("serverPseudo.txt") and not any(friend in tupleInfos for tupleInfos in friendsList) and not any(friend in tupleInfosInv for tupleInfosInv in invList):
            self.db.sendInviting(__getSetInformation.get_username("serverPseudo.txt"), friend)
            
        self.entry_friend.delete(0, tk.END)
        
        
    def deleteFriends(self, friend):
        self.launcher.delete_friend_popup_label = Label(self.window, image=self.launcher.delete_friend_popup, bd=0, highlightthickness=0, cursor="hand2")
        self.launcher.delete_friend_popup_label.place(relx=0.5, rely=0.5, anchor=CENTER)
        
        
        def on_yes_click():
            from infrastructure.services.getSetInformation import GetSetInformation
            __getSetInformation = GetSetInformation()
        
            self.launcher.delete_friend_popup_label.destroy()
            self.db.deleteFriends(__getSetInformation.get_username("serverPseudo.txt"), friend[0])
            self.db.deleteFriends(friend[0], __getSetInformation.get_username("serverPseudo.txt"))
            self.displayListFriends(self.friends_panel)
            
        def on_no_click():
            self.launcher.delete_friend_popup_label.destroy()
            
            
        if len(friend) > 15:
                friend = friend[:15] + ".."
        label = Label(self.launcher.delete_friend_popup_label, text=f"Souhaitez-vous vraiment supprimer \n{friend[0]} de vos amis ?", bd=0,
                    highlightthickness=0, font=("Inter", 22), fg="#E3F8FF", bg="#102A43")
        label.place(relx=0.05, rely=0.35, anchor=NW)
        label.config(justify="left")
        
        
        yes_button = Label(self.launcher.delete_friend_popup_label, image=self.launcher.delete_friend_button,bd=0, highlightthickness=0, cursor="hand2")
        yes_button.place(relx=0.05, rely=0.78, anchor=NW)
        yes_button.bind("<Button-1>", lambda event: on_yes_click())
        
        no_button = Button(self.launcher.delete_friend_popup_label, image=self.launcher.no_delete_friend_button,bd=0, highlightthickness=0, cursor="hand2")
        no_button.place(relx=0.38, rely=0.78, anchor=NW)
        no_button.bind("<Button-1>", lambda event: on_no_click())