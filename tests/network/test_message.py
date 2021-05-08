from dungeonX.characters.players import Player, Fighter, Mage, Rogue, PlayerEnum
from dungeonX.characters.skills import Skill, SkillFactory, SkillEnum
from dungeonX.network.message import Message,extract, read_id, read_type, read_position, read_attributes, read_int, read_IP, read_name
from dungeonX.characters.enemies import Enemy, Zombie, Dragon, Goblin
from dungeonX.items.Item import ItemList, ItemFactory
from dungeonX import Game



game = Game().screens["game"]
types = "Zombie"
types2 = "Dragon"
types3 = "Goblin"

hp          = 100
armor       = 7
strength    = 2
dex         = 3
con         = 4
intell      = 5
wis         = 6
cha         = 7
skillsPoint = 0
defaultStats = (hp, armor, strength, dex, con, intell, wis, cha) 
defaultSkills = [SkillFactory(SkillEnum.Stealth)]

player1 = Player(game, (0,0), PlayerEnum.Rogue,10, skills = defaultSkills, stats=defaultStats,lineOfSightRadius=5)
player2 = Player(game, (1,2), PlayerEnum.Mage,10, stats=defaultStats,lineOfSightRadius=5)
player3 = Player(game, (3,4), PlayerEnum.Fighter,10, stats=defaultStats,lineOfSightRadius=5)
player1.name="Alice"
players = [player1,player2,player3]

enemy= Zombie (game,(0,0),defaultStats, types) 
enemy2 = Dragon(game,(0,0),defaultStats, types2)
enemy3 = Goblin(game,(0,0),defaultStats, types3)
enemies = [enemy, enemy2, enemy3]
swordItem = ItemFactory(ItemList.Sword)

def testMessageCreation():
    message = Message(players,enemies,flag = "wlc")
    message1 = Message(players, enemies, flag = "pos")
    message2 = Message(players, enemies, flag = "hps")
    message3 = Message([None,None,None],flag="con",IP="121.0.0.7",port=8000)
    message4 = Message(players,flag = "new")
    message5 = Message(players,flag="ite")
    #print(message.create_message())
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    zerosm = "00" if len(n) == 3 else "000"
    assert message.create_message() == "wlc0100000Alice"+n1+"R00000000"+n2+"M00010002"+n3+"F00030004" 
    assert message1.create_message(ID = int(n1)) == "pos01"+n1+"00000000" 
    assert message2.create_message(ID = int(n1), IDenemy = int(n))  == "hps01"+n1+"100"+zerosm+n+"100"
    assert message3.create_message() == "con000000121.0.0.708000" 
    assert message4.create_message() == "new0100000Alice"+"R00000000M00010002F00030004"
    assert message5.create_message(ID = int(n1), IDItem= swordItem.id) == "ite01"+n1+"0"+str(swordItem.id)


def testMessageReadAndExtract():
    message = Message(players,flag = "wlc")
    message1 = Message(players, enemies, flag="pos")
    message2 = Message(players, enemies, flag="hps")
    message3 = Message([None,None,None],flag="con",IP="121.0.0.7",port=8000)
    message4 = Message(players,flag = "new")
    message5 = Message(players,flag="ite")
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    zerosm = "00" if len(n) == 3 else "000"
    liste = extract(message.create_message(),"wlc",4)
    liste1 = extract(message1.create_message(ID = int(n1)),"pos",4)
    liste2 = extract(message2.create_message(ID = int(n1), IDenemy = int(n)),"hps",5)
    liste3 = extract(message3.create_message(), "con",2)
    liste4 = extract(message4.create_message(),"new",3)
    liste5 = extract(message5.create_message(ID = int(n1), IDItem= swordItem.id),"ite",3)
    assert liste == ["01","00000Alice",[n1,"R","0000","0000"],[n2,"M","0001","0002"],[n3,"F","0003","0004"]]
    assert liste1 == ["01",n1,"0000","0000"]
    assert liste2 == ["01",n1,"100",zerosm+n,"100"]
    assert liste3 == ["000000121.0.0.7","08000"]
    assert liste4 == ["01","00000Alice",["R","0000","0000"],["M","0001","0002"],["F","0003","0004"]]
    assert liste5 == ["01",n1,"0"+str(swordItem.id)]

    # assert read_id(liste[1][0]) == int(n1)
    # assert read_type(liste[1][1]) == PlayerEnum.Rogue
    # assert read_position(liste[1][2],liste[1][3]) == (0,0)
    # assert type(read_position(liste[1][2],liste[1][3])) == tuple
    # assert read_int(liste2[2]) == 100
    # assert read_int(liste2[4]) == 100
    # assert read_IP(liste3[0]) == "121.0.0.7"
    # assert read_int(liste3[1]) == 8000
    assert read_name(liste[1]) == "Alice"

