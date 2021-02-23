# InterfacePython

:::tip

 InterfacePython() est un thread initialiser dans le ```main()``` dans `/network/server.c` (cf. 01_RESEAUX))

 :::

 Cette derniere joue le rôle de serveur et écoute sur la socket `IP_interne:Port_Interne` (exemple: 127.0.0.1:1234) pour récupérer les données du client python et lui transmettre tous les donnés des autres instance de jeu connecté aux réseaux P2P (Peer2Peer).

 Pour se faire elle utilise 2 threads, l'une pour recevoir et l'autre pour émettre.  