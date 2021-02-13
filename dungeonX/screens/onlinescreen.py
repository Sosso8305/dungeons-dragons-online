import pygame, io
from . import Window
from ..graphics import Button, TextInput
from ..map import Map
from ..constants import TILE_WIDTH

class OnlineScreen(Window):
    def __init__(self,game):
        super().__init__(game)

        self.rect = self.get_rect()
        self.background = pygame.image.load("dungeonX/assets/menu/background.png")
        self.backbutton = Button(game,(20,+20), "",size=(50,50),imgPath="dungeonX/assets/menu/back_arrow.png", textScale=0.3,action=lambda:self.game.setScreen('main_menu'))
        self.background = pygame.transform.scale(self.background, (self.rect.width, self.rect.height))

        self.currentscreen = 'online_screen'


    def update(self, events):
        # --- Render --- #
        self.blit(self.background, (0,0))
        self.backbutton.update(events)
        self.blit(self.backbutton.image,self.backbutton.rect)




