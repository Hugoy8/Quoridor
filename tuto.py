import tkinter as tk

# Créer la fenêtre principale
root = tk.Tk()

# Obtenir la largeur et la hauteur de l'écran
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 500
height = 300
# Calculer les coordonnées x et y de la fenêtre
x = (screen_width // 2) - (width // 2)
y = (screen_height // 2) - (height // 2)

# Définir la taille et la position de la fenêtre

root.geometry(f"{width}x{height}+{x}+{y}")

# Afficher la fenêtre
root.mainloop()