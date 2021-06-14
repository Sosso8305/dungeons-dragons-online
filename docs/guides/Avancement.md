## Update file sur l'avancement du groupe de projet :

Le document montre l'état de l'avancement de chaque membre/groupes de membres aux dates précisées:

### Jeudi 3 Mars:

*Christine*
- Première étude du code du jeu. (Vu que le sujet choisi n’est pas celui de mon projet Python du 1er semestre).
- Création de la classe Message. (Message sous forme de chaines de caractères avec des délimiteurs).
- Création de la classe OtherPlayer (nécessaire pour contrôler les personnages des joueurs connectés).
- Ajout des tests pour vérifier le bon fonctionnement des différentes fonctions et méthodes reliées à la classe Message.

*Zineb*
- Rajout du bouton Online au front pour le lancement du multijoueur en réseau 
- Création du file test_message.py dans le folder test 

*Agathe* 
- imagination du concept et implémentation rudimentaire d'une classe OtherPlayer (21-2-2020)
- avec Lucas imagination d'un nouveau système de message, traitement en fonction du type du message (switch) et envoit des messages uniquement quand il y a un changement (aucune implémentation)


*Sofiane* 
- Gestion de la partie C en réseau 
- Ajout folder doc

*Lucas* 
- ""API""
- Gestion de la partie Python et communication avec le C 

*Valentin*
- Aide à la partie Python en réseau 

### Jeudi 18 Mars :

*Christine* 
- Réflexion sur les différents types de messages nécessaires.
- En suivant les conseils du prof des modifications ont été apportées à la classe Message (élimination des délimiteurs, définition de plusieurs types de messages et définition d’une taille fixe et maximale).
- Implémentation de toute la classe Message gérant la liaison entre partie réseaux et partie python. A savoir les méthodes de création de message, extraction et vérification. 
- Définition d’une taille maximale pour chaque champ composant le message.
- Ajout d’une fonction de padding à gauche nécessaire pour que les champs atteignent leur taille maximale.

*Zineb*
- Création de la branche Avancement 
- Réalisation des slides suivi du mois 
- Participation aux modifications de l’excel contenant les types de messages retenus pour leur réalisation.


*Sofiane* 
- set la seed et ajout du thread qui accueille le jeu 

*Lucas Sofiane et Valentin*
- Excel pour proposition de modification de la structure "message"

### Avril :
*Christine*
- Définition de nouveaux types de message nécessaires au jeu.
- Etude et modification continue sur l’architecture du jeu pour une meilleure compatibilité avec les modifications ajoutées.
- Première version pour le positionnement et le déplacement des personnages des joueurs connectés (méthodes propres à la classe OtherPlayer).
- Modifications sur la classe Message ainsi que sur la classe OtherPlayer (vu qu’elle est liée à la classe Message).
- Conception sur la façon de stocker les instances des joueurs connectés dans le jeu du joueur lui-même. (Je me suis rendu compte que la meilleure façon de stockage était de créer un dictionnaire ayant comme clé l’ID d’un joueur et comme valeur l’instance de RealPlayer (qui est une classe mère de OtherPlayer) correspondante dans son jeu).
- Conception sur comment avoir un ID unique et propre à chaque joueur. (L’idée est d’utiliser la taille du dictionnaire des joueurs comme ID pour le nouveau joueur connecté)


*Zineb* 
- Proposition de quelques modifications de structure de messages suite au travail pré-existant de Christine.
- Modification des IDS des personnages  pour respecter le format des messages 
- Préparation des slides du mois pour les séances de suivi.






### Mai :
*Christine*
- Réalisation online de la character sheet (character sheet = fenêtre où se trouve toutes les informations du personnage) pour permettre de visualiser les caractéristiques des autres joueurs. J’ai également ajouté une contrainte : on ne visualise que les character sheets des joueurs qui sont autour du personnage selectionné. (+ restreindre la vue de ces character sheets quand ces personnages ne sont plus dans le champ de vision du joueur concerné).
- Premier essai de liaison de la partie python avec la partie réseaux (c.à.d essayer de lancer la connexion réseaux directement dans le jeu).  
- Simuler l’envoi et la réception des messages dans le jeu pour vérifier leur fonctionnement niveau python(vu que la connexion réseaux n’était toujours pas encore établie).
- Conception sur où simuler l’envoi de chaque type de message et où simuler sa réception.
- Garantir l’unicité de la seed parmi les joueurs.
- Génération de la même map chez tous les joueurs après la réception de la seed dans le message wlc.
- Création des personnages du joueur connecté sur la map du joueur actuel après la réception du message new.
- Implémentation du positionnement aléatoire pour les personnages du OtherPlayer.

*Zineb*
- Ajout et gestion entière de la page OnlineScreen 
- Stockage des variables rentrées pur établir la connexion « en ligne » et valeurs par défauts.
- Resolution de bugs suite à certains rajouts 
- Réalisation des slides du mois 
- Ajout du message « ite » pour la gestion des items récupérés par les joueurs comme indiqué sur l’exel des messages
- Correction du bug pour l’inventaire 

*Agathe*
- ajout d'une classe "realPlayer" (pour les "copies" des autres joueurs sur chaque jeu)
- accès à l'inventaire des autres joueurs (mais impossible de modofier les inventaires des autres joueurs)




### Juin :
*Zineb*

- Ajout du message « che » pour la gestion du coffre : solution plus intéressante et moins couteuse + méthodes intérmédiares + tests 

*Agathe*
#TODO: explain how it was proper to inventory/modfications
- synchronisation du contenu des coffres quand ils sont ouverts par un joueur
- mise à jour des inventaires pour tous les joueurs quand un joueur récupère des items dans un coffre
- mise à jour des équipements des autres joueurs


### Lucas (non daté mais en ordre chronologique) :

- 100% de la partie réseau/socket en python : envoie réception thread etc
- Idée du python → C → C → Python a travers le réseau
- Définition des premiers messages
- Définition de notre alternative 3-way handshake pour l'ajout d'un joueur
- Support technique pour la partie jeu
- Documentation poussée avec les DocString de python
- Longues séances de travail en groupe avec Sofiane et Valentin pour ficeler la partie réseau et tout assembler (séances faites tout au long du projet)
