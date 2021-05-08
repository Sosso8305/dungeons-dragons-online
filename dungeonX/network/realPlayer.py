from ..map import Map
from dungeonX.characters import Bag

class RealPlayer(object):

    def __init__(self,playersList,username):
        print("other Real player is created !")
        # the real player's username
        self.username=username
        # the list of the 3 other real player's characters (their type is OtherPlayer2)
        self.playersList=playersList
        # bag initialization : empty at the beginning, no weight, no money, no equipment
        self.bag = Bag(500)
        # every players of this RealPlayer must have the same "username" field
        for player in playersList :
            #player.name=username
            #player.username=username
            player.updateName(self.username)
            print("player renamed : "+player.name)
