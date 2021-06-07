import math, pygame
from dungeonX import Game
from dungeonX.screens import GameScreen
from dungeonX.items import Item,ItemFactory
from dungeonX.constants import ItemList
from dungeonX.objects import Chest,Door,Stairs
from dungeonX.constants import State
from dungeonX.graphics import TextDisplayer, ParticleSystem

game = Game()
gameScreen=GameScreen(game)
defaultPos=(1,1)
swordItem = ItemFactory(ItemList.Sword)
swordItem1 = ItemFactory(ItemList.Sword)
coinItem = ItemFactory(ItemList.Coin)
chest1=Chest(defaultPos, content=[swordItem,swordItem1], state=State.unlocked)
chest2=Chest((4,6), content=[coinItem], state=State.unlocked)

list =[Stairs((3,5), down=False),chest1,chest2]

def testReturnChestListOnly():
    print(gameScreen.retrieveChestsFromObjects(list))
    assert gameScreen.retrieveChestsFromObjects(list) == [chest1,chest2]

# def testUpdateChestSithItemID():
#     ListOfChests= gameScreen.retrieveChestsFromObjects(list)
#     assert chest1.getContent()==[swordItem,swordItem1]
#     assert gameScreen.UpdateChestContent(ListOfChests,swordItem1.id)==chest1.getPosition()
#     assert chest1.getContent()==[swordItem]


# def testGameCreation():
# 	assert math.isclose(game.RATIO, game.DISPLAY_SIZE[0]/game.DISPLAY_SIZE[1])
# 	assert game.dt == 0
# 	assert not game.running

# 	assert type(game.display) is pygame.Surface
# 	assert game.display.get_size() == game.DISPLAY_SIZE
	
# 	assert type(game.textDisplayer) is TextDisplayer
# 	assert type(game.particleSystem) is ParticleSystem

# 	assert game.currentScreen in game.screens
# 	assert game.keymap is not None

# def testSetScreen():
# 	oldScreen = game.currentScreen
# 	game.setScreen("invalid screen")
# 	assert game.currentScreen == oldScreen

# 	game.setScreen("main_menu")
# 	assert game.currentScreen == "main_menu"

