from dungeonX.characters.players import Player, Fighter, Mage, Rogue, PlayerEnum
from dungeonX.characters.skills import Skill, SkillFactory, SkillEnum
from dungeonX.network.packet import Packet,read_packet,read_position,read_attributes,read_enemies_dict,read_list,read_type
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
    assert packet.create_packet() == "PlayerEnum.Rogue//$$//(0, 0)//$$//(100, 7, 2, 3, 4, 5, 6, 7)//$$//[]//$$////perso//PlayerEnum.Mage//$$//(1, 2)//$$//(100, 7, 2, 3, 4, 5, 6, 7)//$$//[]//$$////perso//PlayerEnum.Fighter//$$//(3, 4)//$$//(100, 7, 2, 3, 4, 5, 6, 7)//$$//[]//$$//None//$$////perso//" 
                     
def testPacketReadAndExtract():
    packet =Packet(players)
    liste = read_packet(packet.create_packet())
    assert liste == [["PlayerEnum.Rogue","(0, 0)","(100, 7, 2, 3, 4, 5, 6, 7)","[]"],["PlayerEnum.Mage","(1, 2)","(100, 7, 2, 3, 4, 5, 6, 7)","[]"],["PlayerEnum.Fighter","(3, 4)","(100, 7, 2, 3, 4, 5, 6, 7)","[]","None"]]
    assert read_position(liste[0][1]) == (0,0)
    assert type(read_position(liste[0][1])) == tuple
    assert read_attributes(liste[0][2]) == (100,7,2,3,4,5,6,7)
    assert read_type(liste[0][0]) == PlayerEnum.Rogue
    #TODO: test read_ennemies_dict and read_list
