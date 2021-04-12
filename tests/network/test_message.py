from dungeonX.characters.players import Player, Fighter, Mage, Rogue, PlayerEnum
from dungeonX.characters.skills import Skill, SkillFactory, SkillEnum
from dungeonX.network.message import Message,extract, read_id, read_type, read_position, read_attributes, read_HP
from dungeonX.characters.enemies import Enemy, Zombie, Dragon, Goblin
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
players = [player1,player2,player3]

enemy= Zombie (game,(0,0),defaultStats, types) 
enemy2 = Dragon(game,(0,0),defaultStats, types2)
enemy3 = Goblin(game,(0,0),defaultStats, types3)
enemies = [enemy, enemy2, enemy3]

def testMessageCreation():
    message = Message(players,enemies,flag = "wlc")
    message1 = Message(players, enemies, flag = "pos")
    message2 = Message(players, enemies, flag = "hps")
    print(message.create_message())
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    zeros = "00" if len(n1) == 3 else "000"
    zerosm = "00" if len(n) == 3 else "000"
    assert message.create_message() == "wlc"+zeros+n1+"R00000000"+zeros+n2+"M00010002"+zeros+n3+"F00030004" 
    assert message1.create_message(ID = int(n1)) == "pos"+zeros+n1+"00000000" 
    assert message2.create_message(ID = int(n1), IDenemy = int(n))  == "hps"+zeros+n1+"100"+zerosm+n+"100"

def testMessageReadAndExtract():
    message = Message(players,flag = "wlc")
    message1 = Message(players, enemies, flag="pos")
    message2 = Message(players, enemies, flag="hps")
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    zeros = "00" if len(n1) == 3 else "000"
    zerosm = "00" if len(n) == 3 else "000"
    liste = extract(message.create_message(),"wlc",4)
    liste2 = extract(message1.create_message(ID = int(n1)),"pos",3)
    liste3 = extract(message2.create_message(ID = int(n1), IDenemy = int(n)),"hps",4)
    assert liste == [[zeros+n1,"R","0000","0000"],[zeros+n2,"M","0001","0002"],[zeros+n3,"F","0003","0004"]]
    assert liste2 == [zeros+n1,"0000","0000"]
    assert liste3 == [zeros+n1,"100",zerosm+n,"100"]
    assert read_id(liste[0][0]) == int(n1)
    assert read_type(liste[0][1]) == PlayerEnum.Rogue
    assert read_position(liste[0][2],liste[0][3]) == (0,0)
    assert type(read_position(liste[0][2],liste[0][3])) == tuple
    assert read_HP(liste3[1]) == 100
    assert read_HP(liste3[3]) == 100

