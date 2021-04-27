import pygame, io
from . import Window
from ..graphics import Button, TextInput
from ..map import Map
from ..constants import TILE_WIDTH
START_BUTTON_WIDTH = 200
START_BUTTON_HEIGHT = 100

class OnlineScreen(Window):
    def __init__(self,game):
        super().__init__(game)

        self.rect = self.get_rect()
        self.background = pygame.image.load("dungeonX/assets/menu/background.png")
        self.backbutton = Button(game,(20,+20), "",size=(50,50),imgPath="dungeonX/assets/menu/back_arrow.png", textScale=0.3,action=lambda:self.game.setScreen('main_menu'))
        self.background = pygame.transform.scale(self.background, (self.rect.width, self.rect.height))
        self.nextButton = Button(game,(self.get_width()-2.5*START_BUTTON_WIDTH,5*self.get_height()//6-START_BUTTON_HEIGHT//2),"Next",(START_BUTTON_WIDTH, START_BUTTON_HEIGHT))
        self.OptionalButton = Button(game,(self.get_width()-1000,5*self.get_height()//6-100//2),"Optional Parameters",(200, 100),textScale=0.3) 
        self.IPAddressInput = TextInput(game, (self.get_width()//2-325, (self.get_height())//2-75),width=15, textScale=0.6)
        self.currentscreen = 'online_screen'
        
    def update(self, events):
        # --- Render --- #
        self.blit(self.background, (0,0))
        self.game.textDisplayer.print("Enter your IP address To login",(0,50), rectSize=(self.get_width(),200), center=True, scale=0.55)
        self.blit(self.nextButton.image,self.nextButton.rect)
        self.blit(self.OptionalButton.image,self.OptionalButton.rect)

        
        self.IPAddressInput.update(events)
        self.blit(self.IPAddressInput, self.IPAddressInput.rect)


        self.backbutton.update(events)
        self.blit(self.backbutton.image,self.backbutton.rect)




