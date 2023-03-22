import tkinter as tk

# dimensions du tableau
rows = 10
columns = 10

# créer une fenêtre Tkinter
window = tk.Tk()

# créer un canvas pour afficher les images
canvas = tk.Canvas(window, width=columns*20, height=rows*20)
canvas.pack()

# créer des images pour les cases
white_image = tk.PhotoImage(width=20, height=20, file="./assets/case_space.png")
brown_image = tk.PhotoImage(width=20, height=20, file="./assets/case.png")

# créer une liste pour stocker les éléments du tableau
tableau = []

# initialiser le tableau avec des 0
for i in range(rows):
    row = []
    for j in range(columns):
        row.append(0)
        # afficher l'image blanche pour les 0
        canvas.create_image(j*20, i*20, image=white_image, anchor="nw")
    tableau.append(row)

# changer certaines valeurs du tableau en 1
tableau[2][3] = 1
tableau[5][7] = 1
tableau[8][1] = 1

# afficher l'image marron pour les 1
for i in range(rows):
    for j in range(columns):
        if tableau[i][j] == 1:
            canvas.create_image(j*20, i*20, image=brown_image, anchor="nw")

# démarrer la boucle principale Tkinter
window.mainloop()