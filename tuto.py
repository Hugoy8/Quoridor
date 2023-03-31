import random

def choisir_mot():
    liste_mots = ['python', 'ordinateur', 'chat', 'chien', 'voiture', 'maison', 'avion', 'bateau']
    return random.choice(liste_mots)

def afficher_pendu(essais_restants):
    etapes = [
        """
           _______
          |/      |
          |      
          |      
          |       
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |      
          |       
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |       |
          |       
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |       |\\
          |       
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |      /|\\
          |       
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |      /|\\
          |      /
          |      
          |
        __|________
        """,
        """
           _______
          |/      |
          |      (_)
          |      /|\\
          |      / \\
          |      
          |
        __|________
        """
    ]
    print(etapes[6 - essais_restants])

def jouer():
    mot = choisir_mot()
    mot_masque = ['_' for _ in mot]
    essais_restants = 6
    lettres_trouvees = []

    while essais_restants > 0 and '_' in mot_masque:
        afficher_pendu(essais_restants)
        print(' '.join(mot_masque))
        lettre = input("Entrez une lettre : ").lower()

        if lettre in lettres_trouvees:
            print("Lettre déjà essayée.")
            continue

        lettres_trouvees.append(lettre)

        if lettre in mot:
            for i, c in enumerate(mot):
                if c == lettre:
                    mot_masque[i] = lettre
        else:
            essais_restants -= 1

    if '_' not in mot_masque:
        print("Félicitations, vous avez gagné ! Le mot était :", mot)
    else:
        afficher_pendu(essais_restants)
        print("Dommage, vous avez perdu. Le mot était :", mot)

if __name__ == '__main__':
    jouer()