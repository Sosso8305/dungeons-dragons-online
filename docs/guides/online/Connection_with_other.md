:::tip

SendStructMyplayerInit() est un thread initialiser dans le ```main()``` dans `/network/server.c`

 :::

 La particulité de cette fonction est qu'elle va demander à l'utilisateur l'IP du joueur auquel on veut se connecter
 Puis envois un demende de connection avec l'agument d'initilisation.


 Cette fonctionnalité rique de changer pour que l'ip soit demander dans le jeu python et non plus dans la console du procesuus en C.