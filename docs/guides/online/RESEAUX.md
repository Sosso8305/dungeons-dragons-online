# Architecture Réseaux

Notre architecture se base sur 2 processus un en python et l'autre en C.
Le premier va transmettre une structure de donné via une socket pour que le processus en C la récupère.

exemple structure en:
```python
def strucPython():
```
## Processus en C

Ce dernier va utilser le fonctionnement des threads pour communiquer avec le processus en python et avec les autres instance de jeu en "simultanée".

::: warning Attention 

Le jeu est fait pour du online, c'est à dire , que deux instance du jeu ne dois pas exister sur la même machine (sinon rique de bind des sockets identiques car tout les joueurs on la même version du jeu)

:::

### Main()

Nous travaillons sur le fichier `/network/server.c`.

Donc la fonction ```main()``` va lancer 3 threads:

1. Le thread qui va s'occcuper de l'`interface Python`( cf 02_InterfacePython)
2. Le thread qui gérer le `réseaux P2P`(cf 03_Peer2Peer)
3. Le thread qui est une `interface utilisateur`( cf04_Connection_with_other) pour l'initialisation (risque de changer)

Il y a une petite suptilité car on lance la premiere thread et avant de lancer les autres on attand que le processus python se connnecte à l'interface.
