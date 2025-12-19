# **SAE 1.02 : Donjon & Dragon \- Second Rendu**

## **Introduction**

Ce projet implémente un jeu de type "Donjon & Dragon" simplifié, où le joueur incarne le Donjon et doit manipuler l'environnement (les salles) pour intercepter un Aventurier qui cherche à progresser.

Ce second rendu valide l'intégration du chargement de donjons complexes via fichiers texte, ainsi que l'intégralité des variantes de gameplay demandées (Trésors, Sauvegarde et Dragons mobiles).

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
  
**SECOND RENDU** L'architecture a été étendue pour supporter le parsing et la persistance :
* `engine/` :
  * `treasure.py` : Nouvelle structure pour la gestion des trésors.
  * `parsing.py` : Coeur du système de chargement. Traduit les caractères Unicode (╔, ╩, etc.) en structures de données et gère la sérialisation JSON.

src/utils/file_utils.py : Gestion sécurisée des lectures de fichiers en UTF-8.

src/engine/structs/treasure.py : Nouvelle structure pour la gestion des récompenses éphémères.

dungeons/ : Contient les fichiers .txt des niveaux prédéfinis.

## **Fonctionnalités Implémentées (Tâche 3 & Section 2)**

### 1. Chargement et Encodage (Tâche 3)
* `Interprétation Unicode` : Le moteur reconnaît les caractères de "Box-drawing" pour définir les ouvertures des salles.
* `Fichiers Hybrides` : Lecture de fichiers contenant à la fois la structure de la grille et les métadonnées des entités (Aventurier, Dragons, nombre de Trésors).

### 2. Variantes de Gameplay (Section 2)
* `Système de Trésors` :
  * Le donjon peut placer un trésor (clic droit) pour attirer l'aventurier.
  * L'aventurier est programmé pour prioriser les trésors sur les dragons.
  * Limitation stricte à un seul trésor présent simultanément.
* `Sauvegarde et Chargement` :
  * Utilisation du module standard json pour exporter l'état exact de la partie.
  * Gestion de la sérialisation des tuples Python (non supportés nativement par JSON) via un encodeur personnalisé.
* `Déplacement des Dragons` :
  * Mouvement aléatoire des dragons à la fin de chaque cycle.
  * Vérification des collisions immédiates après déplacement.

### **1\. Moteur de Jeu (`engine/`)**

* `Révision de la Structure Globale (GameContextT)` : Afin d'éviter d'avoir une structure "à plat" trop encombrée, nous avons réorganisé l'état global du jeu. Désormais, game_context contient principalement l'état du jeu (game_state), les données actives (game_data) et une copie de sauvegarde pour la réinitialisation (original_game_data).
  * `GameDataT regroupe` :
    * `dungeon` : La grille de salles.
    * `entities` : Une liste contenant l'aventurier (adventurer), la liste des dragons (dragons) et le trésor actuel (treasure) s'il y en a un.
    * `treasure_count` : Le nombre de trésors disponibles pour le niveau.
  * `Initialisation du Donjon` : Chargement de la structure depuis des fichiers textes ou via une structure prédéfinie.

## **Installation et Lancement**

**Lancement** : Exécutez le fichier `main.py` **DEPUIS LE REPERTOIRE SOURCE DU PROJET**:  
Bash
sae_prog1$ python main.py

## **Utilisation**

* **Rotation des salles** : Cliquez-gauche sur une salle.
* **Tracer l'intention** : se fait automatiquement.
* **Confirmer l'intention** : Appuyez sur la touche **Espace** pour confirmer l'intention.
* **Réinitialiser la partie** : Appuyez sur la touche **R**.
* **Sauvegarder la partie** : Appuyez sur la touche **S**.
* **Charger une partie sauvegardée** : Appuyez sur la touche **I** (i comme importer).
* **Quitter** : Appuyez sur la touche **Esc**.

## **Difficultés rencontrées et solutions apportées**

* **Parsing Unicode et Distinction des Données** : La difficulté majeure a été de traiter des fichiers texte mélangeant une grille graphique (caractères de "Box-drawing") et des lignes de données (A, D, T). Nous avons dû implémenter un système de détection de ligne basé sur le premier caractère pour séparer le donjon des entités.
* **Extraction des Champs d'Entités** : Une fois les lignes isolées, le parsing a nécessité un découpage précis des champs (coordonnées, niveaux, compteurs) pour remplir dynamiquement nos structures Python, tout en gérant les types (conversion str vers int).
* **Architecture Imbriquée** : Le passage à une structure imbriquée (game_context -> game_data -> entities) a demandé de mettre à jour de nombreuses fonctions, mais cela a considérablement simplifié la logique de sauvegarde et de reset (copie profonde d'un seul bloc de données).


