from dungeonX.characters.players import Player, Fighter, Mage, Rogue, PlayerEnum
from dungeonX.characters.skills import Skill, SkillFactory, SkillEnum
from network.packet import Packet,extract
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
                     