# **SAE 1.02 : Donjon & Dragon \- Premier Rendu**

## **Introduction**

Ce projet implémente un jeu de type "Donjon & Dragon" simplifié, où le joueur incarne le Donjon et doit manipuler l'environnement (les salles) pour intercepter un Aventurier qui cherche à progresser. Le premier rendu couvre les fonctionnalités de base du moteur de jeu et de l'interface graphique, ainsi que l'implémentation d'une variante.

## **Auteurs**

* **\[TAFTAI\]** \- \[IEGOR\]
* **\[ZIANE\]** \- \[ANIS\]
* **\[MALET\]** \- \[JOSEPH\]

## **Structure des Fichiers et Modules**

Le projet est organisé en plusieurs modules Python pour une meilleure modularité et séparation des préoccupations :

* `main.py` : Point d'entrée principal du jeu, contient la boucle de jeu.  
* `engine/` :  
  * `game_context.py` : Définit la structure du contexte de jeu global (`GameContextT`) et les constantes associées.  
  * `game_logic.py` : Contient la logique du jeu (mouvement de l'aventurier, résolution des combats, gestion des tours).  
  * `event_handler.py` : Gère les interactions utilisateur (clics, touches clavier) et les traduit en actions de jeu.  
  * `dungeon_utils.py` : Fonctions utilitaires pour manipuler le donjon (rotations, connexions, limites).  
  * `adventurer_utils.py` : Fonctions spécifiques à l'aventurier (initialisation, déplacement).  
  * `dragon_utils.py` : Fonctions spécifiques aux dragons (initialisation, déplacement).  
  * `state_manager.py` : Gère les différents états du jeu (menu, partie en cours, victoire, défaite).  
* `gui/` :  
  * `render.py` : Fonctions de rendu graphique (dessin du donjon, de l'aventurier, des dragons, etc.) utilisant FLTK.  
* `config/` :  
  * `constants.py` : Définit toutes les constantes numériques et textuelles du jeu.  
  * `log_config.py` : Configuration du système de logs.

## **Fonctionnalités Implémentées (Tâche 1 & 2\)**

Pour ce premier rendu, les fonctionnalités de base suivantes ont été réalisées conformément aux consignes :

### **1\. Moteur de Jeu (`engine/`)**

* **Structure de Données Globale (`GameContextT`)** : Le jeu utilise un dictionnaire (ou une liste, selon votre choix) pour stocker toutes les données de la partie (donjon, aventurier, dragons, état actuel).  
* **Initialisation du Donjon** : Chargement d'une structure de donjon prédéfinie (ou à partir d'un fichier simple pour les tests).  
* **Gestion du Tour par Tour** : Implémentation du cycle Donjon (Joueur) \-\> Aventurier (IA).  
* **Déplacement de l'Aventurier (Intention Manuelle)** :  
  * L'aventurier peut tracer un chemin d'intention sur le donjon.  
  * Validation des chemins : seuls les déplacements entre salles adjacentes et connectées sont autorisés.  
* **Logique de Combat** : Résolution des rencontres entre l'aventurier et les dragons (gain de niveau pour l'aventurier si vainqueur, suppression du dragon).  
* **Conditions de Victoire/Défaite** : Détection de la victoire (aventurier atteint la sortie) et de la défaite (aventurier vaincu par un dragon).  
* **Réinitialisation de la Partie ('R')** : La touche 'R' permet de réinitialiser complètement le donjon, l'aventurier et les dragons à leur état initial, et de redémarrer au tour du Donjon.

### **2\. Interface Graphique (`gui/`)**

* **Affichage du Donjon** : Rendu graphique des salles du donjon, incluant leurs rotations et connexions.  
* **Affichage des Personnages** : Rendu de l'aventurier et des dragons à leurs positions respectives.  
* **Tracé d'Intention** : Visualisation du chemin d'intention de l'aventurier (ligne rouge).  
* **Interactions Utilisateur** :  
  * **Clic Gauche** : Rotation des salles.  
  * **Clic Droit** : Ajout/suppression de points au chemin d'intention de l'aventurier.  
  * **Touche Espace** : Déclenchement du déplacement de l'aventurier le long de son chemin d'intention.  
  * **Touche 'R'** : Réinitialisation de la partie.  
  * **Touche 'Esc'** : Retour au menu ou fermeture de la fenêtre (si implémenté).  
* **Gestion des Logs** : Utilisation du module `src/utils/logging.py` pour afficher des informations de débogage et de traçage en console.

## **Variante Implémentée**

Nous avons choisi d'implémenter la variante **Déplacement des Dragons** pour ce premier rendu.

### **Déplacement des Dragons**

* **Comportement** : Après chaque tour de l'aventurier (et avant le tour du Donjon), chaque dragon restant se déplace d'une case.  
* **Règles de Mouvement** : Les dragons choisissent une direction accessible (portes ouvertes vers une salle valide) de manière **aléatoire**.  
* **Interaction** : Si un dragon se déplace dans la même salle que l'aventurier, un combat est immédiatement déclenché. La partie se poursuit si l'aventurier est victorieux.

## **Installation et Lancement**

1. **Prérequis** : Assurez-vous d'avoir Python 3 installé.  

**Lancement** : Exécutez le fichier `main.py` **DEPUIS LE REPERTOIRE SOURCE DU PROJET**:  
Bash
sae_prog1$ python main.py

3. 

## **Utilisation**

* **Rotation des salles** : Cliquez-gauche sur une salle.  
* **Tracer l'intention** : Cliquez sur une salle adjacente et connectée pour ajouter un segment au chemin de l'aventurier.  
* **Confirmer l'intention** : Appuyez sur la touche **Espace** pour alterner entre le tour du donjon et l'aventurier.
* **Réinitialiser la partie** : Appuyez sur la touche **R**.  
* **Quitter** : Appuyez sur la touche **Esc**.

## **Difficultés rencontrées et solutions apportées**

Les principaux défis de ce projet n'étaient pas d'ordre algorithmique, mais de nature **architecturale**, en raison des contraintes strictes imposées par le sujet : **l'interdiction d'utiliser des classes**, **des variables globales**, et **des modules externes non vus en cours**.

* **Contournement de l'interdiction des Classes et de l'Héritage :**  
  * Nous avons dû simuler des structures d'objets (comme l'Aventurier ou le Dragon) en utilisant des **listes** et des **dictionnaires**.  
  * Pour garantir la clarté, nous avons défini des **constantes** spécifiques (ex: `ENTITY_ROOM_POS`, `ADVENTURER_LEVEL`) pour accéder aux éléments via des indices, transformant ainsi les listes en structures rigides qui agissent comme des classes manuelles.  
* **Gestion du Contexte de Jeu (Interdiction des Variables Globales) :**  
  * L'interdiction des variables globales nous a obligés à créer une seule et massive structure de données, `GameContextT`, qui encapsule tous les états globaux du jeu (donjon, personnages, état actuel, etc.).  
  * Pour que toutes les fonctions puissent modifier l'état du jeu, nous avons dû **passer cette liste (`GameContextT`) comme argument** à presque toutes les fonctions, en nous appuyant sur le fait que les listes sont des objets mutables passés par référence en Python.  
* **Manipulation d'Images et Rotations (Interdiction des Modules Externes) :**  
  * L'absence d'un module de traitement d'image standard (comme Pillow) a rendu la gestion des graphismes compliquée. Au lieu de charger une seule feuille de style (spritesheet) et d'appliquer des rotations par code, nous avons dû **prédécouper** manuellement les images et **créer un fichier image distinct pour chaque orientation possible** (0°, 90°, 180°, 270°) de chaque type de salle.  
* **Gestion des Copies Profondes et de la Réinitialisation :**  
  * Malgré l'utilisation de `deepcopy` du module `copy`, l'initialisation et la réinitialisation de l'état du jeu (`R`) ont nécessité une attention particulière pour s'assurer que les structures imbriquées complexes (comme le donjon) étaient bien copiées de manière profonde, empêchant ainsi les modifications du jeu actif d'affecter la copie de l'état initial.  
* **Ordre des Tours et des Interactions** : Assurer le bon enchaînement entre les actions du joueur (rotation, intention) et les actions de l'IA (déplacement de l'aventurier, mouvement des dragons) a nécessité une structuration rigoureuse de la boucle de jeu et du `event_handler`.  
* **Débogage des Connexions de Salles** : L'implémentation de la détection de salles connectées, en particulier avec la gestion des rotations et des limites de la carte, a demandé une attention particulière aux indices et aux déplacements relatifs.

## **Améliorations futures (pour le Rendu 2\)**

* Chargement de donjons depuis des fichiers textes externes.  
* Implémentation des autres variantes (Trésors, Sauvegarde/Chargement).  
* Amélioration de l'interface utilisateur (menus, affichage des scores/niveaux).  
* Optimisation des performances (si nécessaire).

