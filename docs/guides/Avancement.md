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
- Création d’une classe RealPlayer pour gérer un seul vrai joueur disposant de 3 personnages pour créer uniformité et respecter les normes de POO puis revert car non nécéssaire.
- Modification des IDS des personnages  pour respecter le format des messages 
- Préparation des slides du mois pour les séances de suivi.






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




### Juin :
*Zineb*

- Ajout du message « che » pour la gestion du coffre : solution plus intéressante et moins couteuse + méthodes intérmédiares + tests 

*Agathe*
#TODO: explain how it was proper to inventory/modfications
- synchronisation du contenu des coffres quand ils sont ouverts par un joueur
- mise à jour des inventaires pour tous les joueurs quand un joueur récupère des items dans un coffre
- mise à jour des équipements des autres joueurs


