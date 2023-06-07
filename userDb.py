import tkinter as tk

def ouvrir_menu():
    # Créer une fenêtre pour afficher le menu déroulant
    menu_window = tk.Toplevel(root)
    
    # Définir les dimensions du menu déroulant
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    menu_width = int(screen_width * 0.1)
    menu_height = screen_height
    
    # Définir la taille et la position du menu déroulant
    menu_window.geometry(f"{menu_width}x{menu_height}+{screen_width-menu_width}+0")
    
    # Créer un cadre dans le menu déroulant
    menu_frame = tk.Frame(menu_window)
    menu_frame.pack(fill=tk.BOTH, expand=True)
    
    # Liste d'amis fictifs
    amis = ["Ami 1", "Ami 2", "Ami 3", "Ami 4", "Ami 5"]
    
    # Afficher les amis dans une liste déroulante
    for ami in amis:
        label = tk.Label(menu_frame, text=ami)
        label.pack()

# Créer la fenêtre principale
root = tk.Tk()

# Créer un bouton pour ouvrir le menu déroulant
bouton = tk.Button(root, text="Ouvrir le menu", command=ouvrir_menu)
bouton.pack()

# Démarrer la boucle principale
root.mainloop()