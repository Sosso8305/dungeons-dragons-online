:::tip

la fonction serverPeer() est un thread initialiser dans le ```main()``` dans `/network/server.c`

 :::

 C'est la fonction qui va créer une soket principale d'écoute (partie server)
 A l'arriver d'une nouvelle connection il y a deux cas possibles:

 1. si c'est un connection d'initialisation ,la fonction va générer 2 threads, l'une pour recevoir l'arrivé de donnée de ce nouveau joueur et un autre qui va créer un client qui va se connecter à l'adresse IP povenant du nouveaux joueur. (partie Client)
 
 2. Si c'est connection de non-initialistaion, il va créer seulement un theard en plus pour recevoir des données.   