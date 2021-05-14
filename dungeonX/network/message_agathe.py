from dungeonX.characters.players.player import Player, PlayerEnum
from .essaiOtherPlayer import *
from .realPlayer import *

'Un debut de message qui va plus correspondre au niveau type de message. '
'Il faudra y integrer le code de christine (ou l inverse) car les deux sont complementaires !'
'Le but est que les fonctions puissent etre utilisees a n importe-quel endroit du code, comme une librairie.'
'Il faudra lier le rzsultat a l api de Lucas '

'NB : VOUS POUVEZ LANCER CE CODE POUR AVOIR UN APERCU DE CE QUE CA POURRAIT DONNER'

#from dungeonX.characters.enemies.enemy import Enemy
# importer l'api de lucas le bourgeois gentilhomme 


def check_size(string : str,n : int):
    zero_str=""
    if len(string)!=n :
        for i in range (n-len(string)) :
            zero_str+='0'
            i+=1
    return zero_str+string

def searchRealPlayer(id,RealPlayersList):
    for realPlayer in RealPlayersList:
        if id == realPlayer.id:
            print("RealPlayer found !")
            return RealPlayersList.index(realPlayer)
    print("No RealPlayer found with id "+str(id))

def suppPadding(string : str):
    string = string.replace('0','')
    return string

def get_initial(ptype):
    if ptype == PlayerEnum.Rogue:
        return 'R'
    elif ptype == PlayerEnum.Fighter:
        return 'F'
    elif ptype == PlayerEnum.Mage:
        return 'M'
    

def createMessage(flag,myPlayersList=None,myId=None,myEnnemies=None,myUsername="Test",seed=None,playerSelected=None) :
    'automatization of the message creation. We suppose that messages creation is always from the players that have the information he send on HIS game'
    message_str = flag 
    if (flag == "wlc"or flag == "new"):
        if (flag == "wlc"):
            message_str += check_size(seed,5)
        #message form : new01xF00780032M00770032M0076003200Lorenzza
        message_str += check_size(str(myId),2)+'x'
        for player in (myPlayersList) :
            print("Position :"+str(player.pos))
            message_str += get_initial(player.PlayerType)+check_size(str(player.pos[0]),4)+check_size(str(player.pos[1]),4)
        message_str += check_size(myUsername,10)
    if (flag == "pos"):
        message_str += check_size(str(myId),2) + check_size(str(playerSelected.playerId),1)
        message_str += check_size(str(playerSelected.pos[0]),4)+check_size(str(playerSelected.pos[1]),4)
    print("Message cree :\n"+message_str)

def extractMessage(message,game) :
    flag=message[0:3]
    if (flag == "new"):
        # message form : new01xF00780032M00770032M0076003200Lorenzza
        # [3:5] id RealPlayer [5:6] 'x' [6:7][15:16][24:25] F, M or R, otherPlayer types
        # [7:11][16:20][25:29] x position in 4 char [11:15][20:24][29:33] y position in 4 char
        # [33:43] RealPlayer's username in 10 char, suppPadding to supp forbidden char 00Lorenzza --> Lorenzza
        otherplayer1=OtherPlayer2([message[6:7],message[7:11],message[11:15]],game)
        game.dungeon.oplayers.append(otherplayer1)
        otherplayer2=OtherPlayer2([message[15:16],message[16:20],message[20:24]],game)
        game.dungeon.oplayers.append(otherplayer2)
        otherplayer3=OtherPlayer2([message[24:25],message[25:29],message[29:33]],game)
        game.dungeon.oplayers.append(otherplayer3)
        game.oplayers = game.dungeon.oplayers
        game.realPlayersList.append(RealPlayer([otherplayer1,otherplayer2,otherplayer3],suppPadding(message[33:43]),int(message[3:5])))
    if (flag == "pos"):
        # message form : pos01000800032
        realPlayer=game.realPlayersList[searchRealPlayer(int(message[3:5]),game.realPlayersList)]
        player=realPlayer.playersList[int(message[5:6])]
        #player.teleport((int(message[6:10]),int(message[10:14])))
        print("Message pos target : ("+str(int(message[6:10]))+","+str(int(message[10:14]))+")")
        player.setTarget((int(message[6:10]),int(message[10:14])))
        player.playAction(game.game.dt,(int(message[6:10]),int(message[10:14])))
        #print(player.stepsToTarget)
        #player.setTarget((int(message[6:10]),int(message[10:14])))

    print("Message "+flag+" has been extracted")


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
