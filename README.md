## Projet-Final - Quoridor

## Installation

Pour installer Python, veuillez vous rendre sur le site officiel : https://www.python.org/downloads/.

Pour installer Tkinter, veuillez exécuter la commande suivante dans votre terminal :

pip install tk

Pour installer Pillow, veuillez exécuter la commande suivante dans votre terminal :

pip install pillow

Pour installer Nmap, veuillez vous rendre sur le site officiel : https://nmap.org/download.html. Si vous êtes sous Windows, pensez à ajouter le chemin d'installation de Nmap à votre variable PATH.

## Lancement du programme

Pour lancer le programme, exécutez le fichier launcher.py. Vous pouvez ensuite choisir de jouer en solo ou en multijoueur (rejoindre ou créer une partie).

Si vous créez une partie en multijoueur ou en solo, vous devez sélectionner tous les paramètres de la partie :

- Choisissez le nombre de joueurs (2 ou 4).
- Choisissez le nombre de bots (0, 1, 2 ou 3), disponible en fonction du nombre de joueurs (non disponible en multijoueur).
- Choisissez la taille du plateau (5, 7, 9 ou 11). Si la taille est incorrecte, le plateau sera de taille 9 par défaut.
- Choisissez le nombre de barrières (elles seront réparties équitablement entre les joueurs). Si le nombre de barrières est incorrect, le nombre de barrières sera de 20 par défaut.
- Cliquez sur le bouton "START".

## Partie Réseau

Pour créer une partie en multijoueur, sélectionnez "créer une partie" dans le menu de gauche, choisissez tous les paramètres de la partie et sélectionnez le port dans la liste proposée. Le serveur se chargera de lancer le programme et de récupérer votre adresse IP. Ensuite, attendez que tous les joueurs rejoignent et lancez la partie.

Pour rejoindre une partie en multijoueur, sélectionnez "rejoindre une partie" dans le menu de gauche. Deux options s'offrent à vous :

- Entrez l'adresse IP et le port du serveur, puis cliquez sur "Rejoindre la partie".
- Cliquez sur le bouton "Rechercher une partie". Tant que le bouton est enfoncé, la recherche est en cours. Lorsqu'elle est terminée, un menu apparaîtra sur la droite avec la liste des serveurs ou aucun résultat. Pour rejoindre le serveur, cliquez simplement sur celui-ci et vous rejoindrez automatiquement la partie.