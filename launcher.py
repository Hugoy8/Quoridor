from tkinter import *
from PIL import Image, ImageTk

window = Tk()
window.geometry("1400x700")
window.title("Quoridor")
window.maxsize(1400, 700)
window.minsize(1400, 700)
window.iconbitmap('./assets/logo.ico')

# Images

# Chargement de l'image de fond
bg_image = Image.open("./assets/launcher.png")

# Redimensionnement de l'image en fonction de la taille de la fenêtre
bg_image = bg_image.resize((window.winfo_screenwidth()-300, window.winfo_screenheight()-200))

# Conversion de l'image en format compatible avec Tkinter
bg_photo = ImageTk.PhotoImage(bg_image)

# Création d'un widget Label pour afficher l'image de fond
bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


first_section_image = PhotoImage(file="./assets/first_section.png")
second_section_image = PhotoImage(file="./assets/second_section.png")
third_section_image = PhotoImage(file="./assets/third_section.png")

# Buttons
# Themes
# Boutons de thème
theme_buttons_frame = Frame(window, bg="#0D2338")
theme_buttons_frame.place(x=273, y=520)

def toggle_checkbox_map():
    # Désactive les autres cases à cocher
    if map.get() == 1:
        theme_button_space.configure(state="disabled")
        theme_button_forest.configure(state="disabled")
    elif map2.get() == 1:
        theme_button_evil.configure(state="disabled")
        theme_button_forest.configure(state="disabled")
    elif map3.get() == 1:
        theme_button_evil.configure(state="disabled")
        theme_button_space.configure(state="disabled")
    # Réactive toutes les cases à cocher si aucune n'est cochée
    else:
        theme_button_evil.configure(state="normal")
        theme_button_space.configure(state="normal")
        theme_button_forest.configure(state="normal")
        
map = IntVar()
map2 = IntVar()
map3 = IntVar()
theme_button_evil = Checkbutton(theme_buttons_frame, text="Evil", bg="#0D2338", fg="#FFF", variable=map, cursor="hand2", command=toggle_checkbox_map)
theme_button_evil.pack(side="left")

theme_button_space = Checkbutton(theme_buttons_frame, text="Space", bg="#0D2338", fg="#FFF", variable=map2, cursor="hand2", command=toggle_checkbox_map)
theme_button_space.pack(side="left")

theme_button_forest = Checkbutton(theme_buttons_frame, text="Forest", bg="#0D2338", fg="#FFF", variable=map3, cursor="hand2", command=toggle_checkbox_map)
theme_button_forest.pack(side="left")

# Nombre d'IA
def toggle_checkbox_ia():
    if nbr_ia.get() == 1:
        ia_3.configure(state="disabled")
    elif nbr_ia_2.get() == 1:
        ia_1.configure(state="disabled")
    else:
        ia_1.configure(state="normal")
        ia_3.configure(state="normal")
        
nbr_ia = IntVar()
nbr_ia_2 = IntVar()
ia_1 = Checkbutton(window, text="1", bg="#0D2338", fg="#FFF", variable=nbr_ia, cursor="hand2", command=toggle_checkbox_ia)
ia_1.place(x=470, y=520)

ia_3 = Checkbutton(window, text="3", bg="#0D2338", fg="#FFF", variable=nbr_ia_2, cursor="hand2", command=toggle_checkbox_ia)
ia_3.place(x=520, y=520)

# Difficulté d'IA...
def toggle_checkbox_difficulty_ia():
    # Désactive les autres cases à cocher
    if level1.get() == 1:
        difficulty2.configure(state="disabled")
        difficulty3.configure(state="disabled")
        difficulty4.configure(state="disabled")
    elif level2.get() == 1:
        difficulty1.configure(state="disabled")
        difficulty3.configure(state="disabled")
        difficulty4.configure(state="disabled")
    elif level3.get() == 1:
        difficulty2.configure(state="disabled")
        difficulty1.configure(state="disabled")
        difficulty4.configure(state="disabled")
    elif level4.get() == 1:
        difficulty2.configure(state="disabled")
        difficulty3.configure(state="disabled")
        difficulty1.configure(state="disabled")
    # Réactive toutes les cases à cocher si aucune n'est cochée
    else:
        difficulty1.configure(state="normal")
        difficulty2.configure(state="normal")
        difficulty3.configure(state="normal")
        difficulty4.configure(state="normal")
        
level1 = IntVar()
level2 = IntVar()
level3 = IntVar()
level4 = IntVar()
difficulty1 = Checkbutton(window, text="Niveau 1", bg="#0D2338", fg="#FFF", variable=level1, cursor="hand2", command=toggle_checkbox_difficulty_ia)
difficulty1.place(x=660, y=510)

difficulty2 = Checkbutton(window, text="Niveau 2", bg="#0D2338", fg="#FFF", variable=level2, cursor="hand2", command=toggle_checkbox_difficulty_ia)
difficulty2.place(x=660, y=530)

difficulty3 = Checkbutton(window, text="Niveau 3", bg="#0D2338", fg="#FFF", variable=level3, cursor="hand2", command=toggle_checkbox_difficulty_ia)
difficulty3.place(x=660, y=550)

difficulty4 = Checkbutton(window, text="Niveau 4", bg="#0D2338", fg="#FFF", variable=level4, cursor="hand2", command=toggle_checkbox_difficulty_ia)
difficulty4.place(x=660, y=570)

# Ajout un bouton pour start l'application
start = Button(window, text="START", command=window.destroy, bg="#0D2338", fg="#FFF", font=("Arial", 15), width=10, cursor="hand2")
start.place(x=775, y=550)

window.mainloop()




