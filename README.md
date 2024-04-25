# Projet-Final - Quoridor

Bienvenue sur le projet Quoridor ! Ce fichier README contient toutes les instructions nécessaires pour installer et lancer le jeu.

## Installation

### Prérequis
- **Python** : Visitez le [site officiel de Python](https://www.python.org/downloads/) pour télécharger et installer la dernière version.

### Dépendances
Installez les dépendances nécessaires en exécutant les commandes suivantes dans votre terminal :

```bash
# Installation de Tkinter
pip install tk

# Installation de Pillow pour la gestion des images
pip install pillow

# Installation de Nmap pour la gestion réseau
# Visitez https://nmap.org/download.html pour les instructions spécifiques à votre système
# Sur Windows, ajoutez Nmap à votre variable PATH
```

## Lancement du programme

### Exécuter le jeu
Pour démarrer le jeu, exécutez le fichier `launcher.py`. Vous aurez l'option de jouer en solo ou en multijoueur.

### Configuration de la partie
Avant de lancer une partie, vous devez configurer les paramètres suivants :

- **Nombre de joueurs** : Choisissez entre 2 ou 4.
- **Nombre de bots** : Sélectionnez entre 0, 1, 2, ou 3 (uniquement disponible en solo).
- **Taille du plateau** : Options disponibles : 5, 7, 9, ou 11. Par défaut, la taille sera de 9 si la valeur est incorrecte.
- **Nombre de barrières** : Les barrières seront réparties équitablement entre les joueurs. Par défaut, 20 barrières si la valeur est incorrecte.

Après avoir sélectionné les options, cliquez sur le bouton **START** pour débuter la partie.

## Mode réseau

### Créer une partie en multijoueur
1. Sélectionnez **"créer une partie"** dans le menu de gauche.
2. Configurez les paramètres de la partie.
3. Sélectionnez le port dans la liste proposée.
4. Le serveur lancera le programme et récupérera votre adresse IP.
5. Attendez que tous les joueurs rejoignent avant de lancer la partie.

### Rejoindre une partie en multijoueur
1. Sélectionnez **"rejoindre une partie"** dans le menu de gauche.
2. Pour rejoindre une partie :
   - Entrez l'adresse IP et le port du serveur, puis cliquez sur **"Rejoindre la partie"**.
   - Ou cliquez sur **"Rechercher une partie"**. Continuez à appuyer sur le bouton jusqu'à ce que la recherche soit complète. Sélectionnez ensuite un serveur dans le menu qui apparaîtra à droite pour rejoindre automatiquement la partie.
