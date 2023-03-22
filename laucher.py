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

# Texts

# map_theme = Label(window, text="Thème de la carte : ", font=("Helvetica", 10), bg="#0D2338", fg="#FFFFFF")
# map_theme.place(x=273, y=483)

# Canvas
# canvas = Canvas(window, width=54, height=54, bg="#2BAEDD", highlightthickness=0)
# canvas.place(x=44, y=247)
# canvas.create_image(27, 27, image=first_section_image)

# canvas = Canvas(window, width=55, height=55, bg="#0B69A3", highlightthickness=0)
# canvas.place(x=42, y=322)
# canvas.create_image(27, 27, image=second_section_image)

# canvas = Canvas(window, width=55, height=55, bg="#0B69A3", highlightthickness=0)
# canvas.place(x=42, y=399)
# canvas.create_image(27, 27, image=third_section_image)


# Buttons
# Themes
# Boutons de thème
theme_buttons_frame = Frame(window, bg="#0D2338")
theme_buttons_frame.place(x=273, y=520)

theme_button_evil = Button(theme_buttons_frame, text="Evil", fg="#e3f8ff", bg="#0D2338", bd=2, relief="groove")
theme_button_evil.pack(side="left", padx=10)

theme_button_space = Button(theme_buttons_frame, text="Space", fg="#e3f8ff", bg="#0D2338", bd=2, relief="groove")
theme_button_space.pack(side="left", padx=10)

theme_button_forest = Button(theme_buttons_frame, text="Forest", fg="#e3f8ff", bg="#0D2338", bd=2, relief="groove")
theme_button_forest.pack(side="left", padx=10)


def validate_entry(text):
    if text in ('1', '3'):
        return True
    else:
        return False
# Ajout de la zone de saisie
entry = Entry(window, validate="key")
entry['validatecommand'] = (entry.register(validate_entry), '%S')
entry.place(x=448, y=520)

# Focus sur la zone de saisie
entry.focus_set()

# Fonction appelée lorsqu'on appuie sur Entrée

def validate():
    nbr_ia = int(entry.get())
    if nbr_ia == 1:
        print("Vous avez choisi 1 IA")
    elif nbr_ia == 3:
        print("Vous avez choisi 3 IA")
        
# Ajout du bouton pour valider la saisie
button = Button(window, text="Valider", command=validate)
button.place(x=488, y=560)

# Ajout un bouton pour quitter l'application
start = Button(window, text="Start", command=window.destroy, bg="#0D2338", fg="#FFF")
start.place(x=850, y=560)


window.mainloop()