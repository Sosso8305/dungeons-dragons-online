'Un debut de message qui va plus correspondre au niveau type de message. '
'Il faudra y integrer le code de christine (ou l inverse) car les deux sont complementaires !'
'Le but est que les fonctions puissent etre utilisees a n importe-quel endroit du code, comme une librairie.'
'Il faudra lier le rzsultat a l api de Lucas '

'NB : VOUS POUVEZ LANCER CE CODE POUR AVOIR UN APERCU DE CE QUE CA POURRAIT DONNER'

#from dungeonX.characters.enemies.enemy import Enemy
# importer l'api de lucas le bourgeois gentilhomme 



def createMessage(id,perso,type_msg,donnees) :
    '# on pourra utiliser le createMessage a tout moment dans le code : il va creer un message qui sera automatiquement envoye'
    part1=str(id) # une unite pour l'instant, 0->9 
    part2=str(perso) # un caractere : 1,2 ou 3 (les 3 personnages d'un joueur)
    part3=type_msg # fera toujours 3 caracteres
    # TYPES DE MESSAGES A GERER
    # pos -> position
    # typ -> Type
    # ini -> 1er message, arrivee en jeu, initialisation du otherplayer (donnees : type des personnages)
    # nhp -> les hp du personnage 
    # arm -> armor
    # strength -> strength
    # dex -> dexerity 
    # con
    # int -> intelligence
    # wis -> wisdom
    # char -> charism
    # spt -> skillsPoint
    # equ -> equipement 
    part4=str(donnees) # il faudra definir une taille max des donnees et ajouter du padding si necessaire
    chaine=part1+part2+part3+part4
    print("Le message envoye est : ",chaine) # test
    # la fonction send de lucas pour l'envoyer directement, pourquoi creer un message si on ne l'envoit pas ?? (rip les lettres que g jamais envoyees)
    return chaine

# pour la reception je ne sais pas trop comment elle s'integrera au code
def recvMessage(chaine) :
    id=int(chaine[0:1])
    perso=int(chaine[1:2])
    type=chaine[2:5]
    donnee=chaine[5:] # il faudra definir une taille max des donnees et ajouter du padding
    if type=='pos' :
        print("Le message est un message position, il va etre traite comme tel.")
        print("Le joueur d'id ",id," veut faire bouger son personnage ",perso,"a la position [",donnee[0],"x ;",donnee[1],"y] .")
        # il ne reste plus qu'a aller chercher l'otherplayer correspondant a l'id
        # et a update ses champs position avec une methode d'OtherPlayer
        # tableau_otherplayer[id].updatePosition(la position)
        # aled christine 
    elif type=="ini" :
        print("Le message est un message d'initialisation.")
        print("Le joueur vient d'arriver en jeu !")
        # c'est a ce moment qu'on cree un otherPlayer
        # en remplissant avec les stats de base 
        # (on verra apres pour revenir en jeu avec les memes stats apres l'avoir quitte)
    else :
        print("Type de message inconnu pour le moment.")

#### TEST ####

# exemple d'un message cre dans 
chaine=createMessage(1,3,'pos',12)

recvMessage(chaine)

chaine=createMessage(1,3,'ini',12)