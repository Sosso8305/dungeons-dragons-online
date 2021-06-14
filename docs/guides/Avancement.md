## Update file sur l'avancement du groupe de projet :

Le document montre l'état de l'avancement de chaque membre/groupes de membres aux dates précisées:

### Jeudi 3 Mars:
*Christine et Zineb* 

- première version du packet(message) avec les méthodes repectives :

  - creation du message (chaine de caractères )
  - lecture et extraction du packet
  - méthodes intermédiaires (pour le padding , vérification de taille,...)
  - Reprise de la classe Otherplayer et Premier affichage des personnages(OtherPlayer) sur la map 
- Rajout du bouton Online au front pour le lancement du multijoueur en réseau 
- Création du file test_message.py dans le folder test avec vérification des méthodes pour la classe message et OtherPlayer


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

*Christine et Zineb* 
- Modifications à la classe packet devenue message :
- ajout de flags pour une gestion de plusieurs types de paquets 
- Modification de la structure du packet avec une délimitation par taille pour le parsing

*Christine*

- Définition de nouveaux types nécessaires au jeu.
- ......

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






### Juin :
*Zineb*

- Ajout du message « che » pour la gestion du coffre : solution plus intéressante et moins couteuse



