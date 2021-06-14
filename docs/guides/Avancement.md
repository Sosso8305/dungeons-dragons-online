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
- imagination du concept et implémentation rudimentaire d'une classe OtherPlayer 
- avec Lucas imagination d'un nouveau système de message, traitement en fonction du type du message (switch) et envoit des messages uniquement quand il y a un changement (aucune implémentation)

*Sofiane* 
- Gestion de la partie C en réseau 
- La majorité des thread creer et gérer pour le réseaux
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

*Agathe* 
- Branche feature realPlayer pour tester l'idée d'un objet realPlayer et ajout d'un objet Bag aux realPlayers
- Liste des "joueurs visibles" en fonctions des personnages visibles par notre personnage sélectionné
- Accès aux Bag des autres joueurs quand ils sont dans le champ de vision
- Corrections d'erreurs d'affichage (flèches de navigation)


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
- Merge de l'inventaire de la feature realPlayer vers develop
- Adaptation du codage de l'inventaire aux modifications qui ont été apportées entre temps sur develop (dictionnaire de realPlayers)
- correction du bug de réception du premier message "wlc" 

*Sofiane*
-fix des erreeur de typo qui reférencé pas la bonne varibles
-change notation "host" par first Player"
-Use REUSADDR pour  faciliter les teste avec les datagrammes
-désactiver la fonctionnaliter de se connecter grace au shell en C
-faire en sorte que le Processus C s'esxecute grace au python 


### Juin :

*Christine*

- Envoi et réception réels des messages wlc et new et création de nouveaux types avec leurs tests :"ini","pro","ans","exi".
- Implémentation du déplacement pour les personnages de la classe OtherPlayer avec toutes les animations nécessaires.
- Suppression du message "ini" pour l'incorporer à "wlc"
- Création et gestion de la notion de propriété pour les cases de la map.
- Ajout des couleurs pour les personnages du joueur local pour les distinguer.
- Supprimer les personnages d’un joueur qui s’est déconnecté des maps des autres joueurs.
- Donner la possibilité aux autres joueurs de continuer à jouer même si un des joueurs s’est déconnecté. 
-  A noter qu’à chaque modification ou ajout d’un type de message je modifiais le tableau excel qui contient tous les types de message.

*Zineb*

- Ajout du message « che » pour la gestion du coffre : solution plus intéressante et moins couteuse + méthodes intérmédiares + tests 


*Sofiane*
- ajout du flag MSG_WAITALL pour les recev dans le python et le C
- rajout d'une function pour simuler l'arriver de message, facilitant les tests
- corriger la maniere de padder les messages (avec christine)

*Agathe* 
- Modification majeure de l'inventaire des autres joueurs : leur Bag est remplacé par une simple liste d'items
- Modification du message chest "che" y ajouter les objets trouvés par un joueur à tous les autres joueurs
- Mise à jour des inventaires pour tous les joueurs quand un joueur récupère des items dans un coffre
- Ajout du message "equ" quand un joueur équipe un item (armure, épée...) : mise à jour des équipements pour tous les joueurs 

### Lucas (non daté mais en ordre chronologique) :

- 100% de la partie réseau/socket en python : envoie réception thread etc
- Idée du python → C → C → Python a travers le réseau
- Définition théorique des premiers messages (longueur, sens des paddings, contenu etc...)
- Définition théorique de notre alternative 3-way handshake pour l'ajout d'un joueur
- Support technique pour la partie jeu
- Documentation poussée avec les DocString de python
- Longues séances de travail en groupe avec Sofiane et Valentin pour ficeler la partie réseau et tout assembler (séances faites tout au long du projet)

### Valentin (non daté mais en ordre chronologique) :

- participation à la partie réseau/socket en python : envoie réception thread etc
- Idée de solution pour fixer l'aléatoire du jeu et la création de map (seed)
- Définition théorique des premiers messages (longueur, sens des paddings, contenu etc...)
- Longues séances de travail en groupe avec Sofiane et Lucas pour ficeler la partie réseau et tout assembler (séances faites tout au long du projet)
