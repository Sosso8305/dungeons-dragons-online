## Update file sur l'avancement du groupe de projet :

Le document montre l'état de l'avancement de chaque membre/groupes de membres aux dates précisées:

### Jeudi 3 Mars:
*Christine*

- première version du packet(message) avec les méthodes repectives :

  - creation du message (chaine de caractères )
  - lecture et extraction du packet
  - méthodes intermédiaires (pour le padding , vérification de taille,...)
  - Reprise de la classe Otherplayer et Premier affichage des personnages(OtherPlayer) sur la map 

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
- Modifications à la classe packet devenue message :
- ajout de flags pour une gestion de plusieurs types de paquets 
- Modification de la structure du packet avec une délimitation par taille pour le parsing
- Définition de nouveaux types nécessaires au jeu.
- ......
*Zineb*
- Création de la branche Avancement 
- Réalisation des slides suivi du mois 
- Participation aux modifications de l’excel contenant les types de messages retenus pour leur réalisation.


*Sofiane* 
- set la seed et ajout du thread qui accueille le jeu 

*Lucas Sofiane et Valentin*
- Excel pour proposition de modification de la structure "message"

### Avril :

*Zineb* 
- Proposition de quelques modifications de structure de messages suite au travail pré-existant de Christine.
- Modification des IDS des personnages  pour respecter le format des messages 
- Préparation des slides du mois pour les séances de suivi.

*Agathe* 
- Branche feature realPlayer pour tester l'idée d'un objet realPlayer
- Ajout d'un objet Bag aux realPlayers
- Liste des "joueurs visibles" en fonctions des personnages visibles par notre personnage sélectionné
- Affichage des inventaires des autres joueurs quand ils sont dans le champ de vision 
- Corrections d'erreurs d'affichage (flèches de navigation)


### Mai :
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
- Merge de l'inventaire de la feature realPlayer vers develop
- Adaptation du codage de l'inventaire aux modifications qui ont été apportées entre temps sur develop (dictionnaire de realPlayers)

*Sofiane*
-fix des erreeur de typo qui reférencé pas la bonne varibles
-change notation "host" par first Player"
-Use REUSADDR pour  faciliter les teste avec les datagrammes
-désactiver la fonctionnaliter de se connecter grace au shell en C
-faire en sorte que le Processus C s'esxecute grace au python 


### Juin :
*Zineb*

- Ajout du message « che » pour la gestion du coffre : solution plus intéressante et moins couteuse + méthodes intérmédiares + tests 


*Sofiane*
- ajout du flag MSG_WAITALL pour les recev dans le python et le C
- rajout d'une function pour simuler l'arriver de message, facilitant les tests
- corriger la maniere de padder les messages (avec christine)

*Agathe* 
- Modification majeure de l'inventaire des autres joueurs : leur Bag est remplacé par une simple liste d'items
- Modification du message chest "che" pour communiquer les objets trouvés par un joueur à tous les autres joueurs
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
