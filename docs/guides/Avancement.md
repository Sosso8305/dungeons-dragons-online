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
- ajout d'une classe "realPlayer" (pour les "copies" des autres joueurs sur chaque jeu)
- accès à l'inventaire des autres joueurs (mais impossible de modofier les inventaires des autres joueurs)
- synchronisation du contenu des coffres quand ils sont ouverts par un joueur
- mise à jour des inventaires pour tous les joueurs quand un joueur récupère des items dans un coffre
- mise à jour des équipements des autres joueurs

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

*Valentin*
- set la seed et ajout du thread qui accueille le jeu 

*Lucas Sofiane et Valentin*
- Excel pour proposition de modification de la structure "message"


