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
    message = Message(players,enemies)
    message1 = Message(players, enemies, flag=1)
    message2 = Message(players, enemies, flag=2)
    print(message.create_message())
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    assert message.create_message() == n1+"ID00PlayerEnum.Rogue000(0, 0)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000"+n2+"ID00PlayerEnum.Mage0000(1, 2)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000"+n3+"ID00PlayerEnum.Fighter0(3, 4)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000" 
    assert message1.create_message(ID = int(n1)) == "1"+n1+"ID00"+"(0, 0)00000" 
    assert message2.create_message(ID = int(n1), IDenemy = int(n))  == "2"+n1+"ID00"+"100HP"+n+"ID00"+"100HP"

def testMessageReadAndExtract():
    message = Message(players)
    message1 = Message(players, enemies, flag=1)
    message2 = Message(players, enemies, flag=2)
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    n = str(enemy.ID)
    liste = extract(message.create_message(),0,4)
    liste2 = extract(message1.create_message(ID = int(n1)),1,2)
    liste3 = extract(message2.create_message(ID = int(n1), IDenemy = int(n)),2,4)
    assert liste == [[n1+"ID00","PlayerEnum.Rogue000","(0, 0)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"],[n2+"ID00","PlayerEnum.Mage0000","(1, 2)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"],[n3+"ID00","PlayerEnum.Fighter0","(3, 4)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"]]
    assert liste2 == [n1+"ID00","(0, 0)00000"]
    assert liste3 == [n1+"ID00","100HP",n+"ID00","100HP"]
    assert read_id(liste[0][0]) == int(n1)
    assert read_type(liste[0][1]) == PlayerEnum.Rogue
    assert read_position(liste[0][2]) == (0,0)
    assert type(read_position(liste[0][2])) == tuple
    assert read_attributes(liste[0][3]) == (100,7,2,3,4,5,6,7)
    assert read_HP(liste3[1]) == 100
    assert read_HP(liste3[3]) == 100

