import tkinter as tk

# Créer le canevas
root = tk.Tk()
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Ajouter des éléments
rectangle = canvas.create_rectangle(50, 50, 100, 100, fill='red')
cercle = canvas.create_oval(75, 75, 125, 125, fill='blue')

# Trouver les éléments au-dessus du point (100, 100)
elements = canvas.find_above(100, 100)  # Correction : ne fournir que deux arguments
print(elements)  # Output: [2]

# Déplacer le cercle au-dessus du rectangle
canvas.tag_raise(cercle, rectangle)

# Trouver les éléments au-dessus du point (100, 100) à nouveau
elements = canvas.find_above(100, 100)  # Correction : ne fournir que deux arguments
print(elements)  # Output: [1, 2]
