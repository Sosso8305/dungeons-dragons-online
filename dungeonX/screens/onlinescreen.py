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
        self.dungeon = None
        self.IPSaved = False
        self.OpParamSaved = False
        self.__viewport = pygame.Surface((40*TILE_WIDTH, 40*TILE_WIDTH/game.RATIO))
        self.isPressed = False


        self.rect = self.get_rect()
        self.background = pygame.image.load("dungeonX/assets/menu/background.png")
        self.backbutton = Button(game,(20,+20), "",size=(50,50),imgPath="dungeonX/assets/menu/back_arrow.png", textScale=0.3,action=lambda:self.game.setScreen('main_menu'))
        self.background = pygame.transform.scale(self.background, (self.rect.width, self.rect.height))
        self.choiceBackground = pygame.transform.scale(pygame.image.load("dungeonX/assets/ui/map_editor/choice.png").convert(), (558, 354))
        self.choiceBackground.set_colorkey((0,0,0))
        self.nextButton = Button(game,(self.get_width()-2.5*START_BUTTON_WIDTH,5*self.get_height()//6-START_BUTTON_HEIGHT//2),"Next",(START_BUTTON_WIDTH, START_BUTTON_HEIGHT),action=self.saveIPaddress)
        self.OptionalButton = Button(game,(self.get_width()-1000,5*self.get_height()//6-100//2),"Optional Parameters",(200, 100),textScale=0.3) 
        self.saveButton = Button(game, (self.get_width()//2-140-5, (self.get_height()+self.choiceBackground.get_height())//2-64-15), "Save", size=(140, 64), textScale=0.3)
        self.cancelButton = Button(game, (self.get_width()//2+5, (self.get_height()+self.choiceBackground.get_height())//2-64-15), "Cancel", size=(140, 64), imgPath="dungeonX/assets/ui/button_red.png", textScale=0.3) #action=self.cancelDialog)

        self.IPAddressInput = TextInput(game, (self.get_width()//2-325, (self.get_height())//2-75),width=15, textScale=0.6)
        self.AddInput = TextInput(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-80),width=8)
        self.Add1Input = TextInput(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-120),width=15)
        self.Add2Input = TextInput(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-160),width=8)

       



        self.currentscreen = 'online_screen'
        


    def saveIPaddress(self):
        if self.IPAddressInput.text!='':
            self.dungeon.save('dungeonX/saves/'+self.IPAddressInput.text.replace(' ', '_')+'.txt')
            self.dialogState = "save_confirmed"
            self.filenameInput.unfocus()
            self.IPSaved = True

    def saveOptionalParameters (self):
        if self.AddInput.text!='':
            self.dungeon.save('dungeonX/saves/'+self.AddInput.text.replace(' ', '_')+'.txt')
            self.dialogState = "save_confirmed"
            self.filenameInput.unfocus()
            self.OpParamSaved = True


    def update(self, events):
        # --- Render --- #
        if not self.isPressed:
            self.blit(self.background, (0,0))
            self.game.textDisplayer.print("Enter your IP address To login",(0,50), rectSize=(self.get_width(),200), center=True, scale=0.55)
            self.blit(self.nextButton.image,self.nextButton.rect)
            self.blit(self.OptionalButton.image,self.OptionalButton.rect)
            self.IPAddressInput.update(events)

            self.blit(self.IPAddressInput, self.IPAddressInput.rect)
            self.nextButton.update(events)
        if self.nextButton.isPressed():
            self.game.setScreen('character_choice')
        self.OptionalButton.update(events)
        if self.OptionalButton.isPressed() or self.isPressed:
            self.isPressed = True
            self.blit(self.choiceBackground, (pygame.Vector2(self.game.DISPLAY_SIZE)-self.choiceBackground.get_size())//2)
            self.game.textDisplayer.print("Add: Port , IPC , Port C", (pygame.Vector2(self.game.DISPLAY_SIZE)-self.choiceBackground.get_size())//2, rectSize=(580,150), center=True, scale=0.3)
            self.AddInput.update(events)
            self.blit(self.AddInput, self.AddInput.rect)
            self.Add1Input.update(events)
            self.blit(self.Add1Input, self.Add1Input.rect)
            self.Add2Input.update(events)
            self.blit(self.Add2Input, self.Add2Input.rect)
            
            self.saveButton.update(events)
            self.blit(self.saveButton.image, self.saveButton.rect)
            self.cancelButton.update(events)
            self.blit(self.cancelButton.image, self.cancelButton.rect)
            if self.cancelButton.isPressed():
                self.isPressed = False

        if self.backbutton.isPressed():
            self.isPressed = False
        self.backbutton.update(events)
        self.blit(self.backbutton.image,self.backbutton.rect)




