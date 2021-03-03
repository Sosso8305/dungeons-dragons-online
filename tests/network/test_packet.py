from dungeonX.characters.players import Player, Fighter, Mage, Rogue, PlayerEnum
from dungeonX.characters.skills import Skill, SkillFactory, SkillEnum
from dungeonX.network.packet import Packet,extract, read_id, read_type, read_position, read_attributes
from dungeonX import Game



game = Game().screens["game"]
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

def testPacketCreation():
    packet = Packet(players)
    print(packet.create_packet())
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    assert packet.create_packet() == n1+"ID00PlayerEnum.Rogue000(0, 0)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000"+n2+"ID00PlayerEnum.Mage0000(1, 2)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000"+n3+"ID00PlayerEnum.Fighter0(3, 4)00000(100, 7, 2, 3, 4, 5, 6, 7)0000000" 
                     
def testPacketReadAndExtract():
    packet =Packet(players)
    n1, n2, n3 = str(player1.ID), str(player2.ID), str(player3.ID)
    liste = extract(packet.create_packet())
    assert liste == [[n1+"ID00","PlayerEnum.Rogue000","(0, 0)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"],[n2+"ID00","PlayerEnum.Mage0000","(1, 2)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"],[n3+"ID00","PlayerEnum.Fighter0","(3, 4)00000","(100, 7, 2, 3, 4, 5, 6, 7)0000000"]]
    assert read_id(liste[0][0]) == int(n1)
    assert read_type(liste[0][1]) == PlayerEnum.Rogue
    assert read_position(liste[0][2]) == (0,0)
    assert type(read_position(liste[0][2])) == tuple
    assert read_attributes(liste[0][3]) == (100,7,2,3,4,5,6,7)

