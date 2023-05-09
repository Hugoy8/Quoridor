# Projet-Final

## Installation
Pour installer Tkinter : pip install tk
Pour installer Pillow : pip install pillow

## Lancement du programme
Pour lancer le programme, il faut lancer le fichier launcher.py
Pour sélectionner il faut cliquer sur les cases blanches obligatoirement
  - Sélectionner le nombre de joueurs (1, 2, 3, 4) 
  - Sélectionner le nombres de bots (0, 1, 2, 3 / disponible en fonction du nombre de joueurs)
  - Sélectionner la taille du plateau (5, 7, 9, 11) -> Si la taille est incorrect le plateau sera de 9 par défaut
  - Sélectionner le nombre de barrières (seront reparti équitablement entre les joueurs) -> Si le nombre de barrières est incorrect, le nombre de barrières sera de 20 par défaut
  - Appuyer sur le bouton "START"


## Partie Réseau
Pour lancer le système réseau, il faut lancer le fichier network.py en choisissant soit la classe Server soit la classe Client (mettre en commentaire celle que l'on ne veut pas utiliser)
  - Pour le serveur, l'addresse ip est automatiquement récupérée, il suffit de renseigner le port et lancer le programme
  - Pour le client, il faut renseigner l'addresse ip du serveur et le port, puis lancer le programme

Le réseau n'est pas encore totalement fonctionnel, il faut encore le relier au jeu pour que les joueurs puissent jouer en réseau.
