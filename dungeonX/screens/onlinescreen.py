import pygame, io, os
from . import Window
from ..graphics import Button, TextInput,TextInputOnline
from ..map import Map
from ..constants import TILE_WIDTH
import ipaddress
from PygameUtils import checkbox

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
        self.isPressedN = False   

        self.rect = self.get_rect()
        self.background = pygame.image.load("dungeonX/assets/menu/background.png")
        self.backbutton = Button(game,(20,+20), "",size=(50,50),imgPath="dungeonX/assets/menu/back_arrow.png", textScale=0.3,action=lambda:self.game.setScreen('main_menu'))
        self.background = pygame.transform.scale(self.background, (self.rect.width, self.rect.height))
        self.choiceBackground = pygame.transform.scale(pygame.image.load("dungeonX/assets/ui/map_editor/choice.png").convert(), (558, 354))
        self.choiceBackground.set_colorkey((0,0,0))
        self.infoBackground = pygame.transform.scale(pygame.image.load("dungeonX/assets/ui/map_editor/info.png").convert(), (600, 164))
        self.infoBackground.set_colorkey((0,0,0))

        self.nextButton = Button(game,(self.get_width()-2.5*START_BUTTON_WIDTH,5*self.get_height()//6-START_BUTTON_HEIGHT//2),"Next",(START_BUTTON_WIDTH, START_BUTTON_HEIGHT),action=self.saveIPaddress)
        # import os
        # os.system("pwd")
        # os.system("cd ... && make all && ./...")
        self.OptionalButton = Button(game,(self.get_width()-1000,5*self.get_height()//6-100//2),"Optional Parameters",(200, 100),textScale=0.3) 
        self.saveButton = Button(game, (self.get_width()//2-140-5, (self.get_height()+self.choiceBackground.get_height())//2-64-15), "Save", size=(140, 64), textScale=0.3,action=self.saveOptionalParam)
        self.cancelButton = Button(game, (self.get_width()//2+5, (self.get_height()+self.choiceBackground.get_height())//2-64-15), "Cancel", size=(140, 64), imgPath="dungeonX/assets/ui/button_red.png", textScale=0.3) #action=self.cancelDialog)
        self.okayButton = Button(game, (self.get_width()//2-75, (self.get_height()+self.infoBackground.get_height())//2-64-15), "Okay", size=(140, 64), textScale=0.3)

        self.IPAddressInput = TextInputOnline(game, (self.get_width()//2-325, (self.get_height())//2-75),width=15, textScale=0.6,IP=True)
        self.AddPortInInput = TextInputOnline(game, (self.get_width()//2-160, (self.get_height()//2)),width=8,textScale=0.6,text="5555")
        self.AddPortCInput = TextInputOnline(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-80),width=8,text="5555")
        self.AddIPInput = TextInputOnline(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-120),width=15,text="127.0.0.1",IP=True)
        self.AddPortInput = TextInputOnline(game, (self.get_width()//2-120, (self.get_height()+self.choiceBackground.get_height())//2-64-160),width=8,text="5133")

        self.IPaddress="" #Ip du joueur auquel on veut se connecter 
        self.PortIn="" #port distant auquel on veut se connecter
        self.Port=""  #Port interne de l'interface python
        self.PortC="" #Port distant du C de se jeu
        self.IPC="" #IP ou se trouve le C
        self.checkFirstPlayer = checkbox((0,0,0),200,200,25,25,text="First player")

        self.currentscreen = 'online_screen'
    

    def saveall(self):
        self.saveIPaddress()
        self.saveOptionalParam()

    def saveIPaddress(self):
        if self.IPAddressInput.text!='':
            self.IPaddress= self.IPAddressInput.text
 #           self.dungeon.save('dungeonX/saves/'+self.IPAddressInput.text.replace(' ', '_')+'.txt')
 #           self.dialogState = "save_confirmed"
            self.IPAddressInput.unfocus()
            self.IPSaved = True
        if self.AddPortInInput.text!='':
            self.PortIn= self.AddPortInInput.text
            self.AddPortInInput.unfocus()

    def saveOptionalParam(self):
        if self.AddPortInput.text!='':
            self.Port=self.AddPortInput.text
            self.AddPortInput.unfocus()
        if self.AddPortCInput.text!='':
            self.PortC=self.AddPortCInput.text
            self.AddPortCInput.unfocus()
        if self.AddIPInput.text!='':
            self.IPC=self.AddIPInput.text
            self.AddIPInput.unfocus()
        self.OpParamSaved = True

    def isvalidIPFormat(self,IP:str):
        def isIPv4(s):
         try: return str(int(s)) == s and 0 <= int(s) <= 255
         except: return False
        if IP.count(".") == 3 and all(isIPv4(i) for i in IP.split(".")):
            return True
        return False
        

    def update(self, events):
        # --- Render --- #
        if not self.isPressed and not self.isPressedN:
            self.blit(self.background, (0,0))
            self.game.textDisplayer.print("Enter your IP address To login",(0,50), rectSize=(self.get_width(),200), center=True, scale=0.55)
            self.blit(self.nextButton.image,self.nextButton.rect)
            self.blit(self.OptionalButton.image,self.OptionalButton.rect)
            self.IPAddressInput.update(events)
            self.blit(self.IPAddressInput, self.IPAddressInput.rect)
            
            self.AddPortInInput.update(events)
            self.blit(self.AddPortInInput, self.AddPortInInput.rect)
            
            for event in events:  
                if self.checkFirstPlayer.isOver(pygame.mouse.get_pos()) and event.type == pygame.MOUSEBUTTONDOWN:
                    self.checkFirstPlayer.convert()
                    print("Clicked")
                print(self.checkFirstPlayer.isChecked())
        self.checkFirstPlayer.draw(self.background)
                
        self.OptionalButton.update(events)
        if self.OptionalButton.isPressed() or self.isPressed:
            self.isPressed = True
            self.blit(self.choiceBackground, (pygame.Vector2(self.game.DISPLAY_SIZE)-self.choiceBackground.get_size())//2)
            self.game.textDisplayer.print("Add: Port , IPC , Port C", (pygame.Vector2(self.game.DISPLAY_SIZE)-self.choiceBackground.get_size())//2, rectSize=(580,150), center=True, scale=0.3)
            

            self.AddPortCInput.update(events, concurrentTextInputs=[self.AddIPInput, self.AddPortInput])
            self.blit(self.AddPortCInput, self.AddPortCInput.rect)
            self.AddIPInput.update(events, concurrentTextInputs=[self.AddPortCInput, self.AddPortInput])
            self.blit(self.AddIPInput, self.AddIPInput.rect)
            self.AddPortInput.update(events, concurrentTextInputs=[self.AddIPInput, self.AddPortCInput])
            self.blit(self.AddPortInput, self.AddPortInput.rect)

            self.saveButton.update(events)
            self.blit(self.saveButton.image, self.saveButton.rect)
            if self.saveButton.isPressed():
                self.isPressed = False

            self.cancelButton.update(events)
            self.blit(self.cancelButton.image, self.cancelButton.rect)
            if self.cancelButton.isPressed():
                self.isPressed = False
                
        self.nextButton.update(events)
        if self.nextButton.isPressed() or self.isPressedN:
            #TODO : Condition si c'est le tout premier joueur qui lance le jeu if not then : character choice directly with map already in check !!!
            if self.isvalidIPFormat(self.IPaddress) and self.isvalidIPFormat(self.IPC):
                self.game.setScreen('map_selector') 
                os.system("cd ./dungeonX/network/ && make && cd ../..")
                os.system("./dungeonX/network/server.out "+self.Port+" "+self.PortC+"> ./logs/logsofiane.log 2>&1 &")       
                from ..network.client import Network
                Networker = Network(self.IPC, int(self.Port), True)
                self.game.network = Networker
                print("Game.network after online screen : "+str(self.game.network))
                Networker.start()
                if not self.checkFirstPlayer.isChecked():
                    Networker.connexion(self.IPaddress,int(self.PortIn))
                
            else : # Blit Real visual WARNING 
                self.isPressedN = True
                self.blit(self.infoBackground, (pygame.Vector2(self.game.DISPLAY_SIZE)-self.infoBackground.get_size())//2)
                self.game.textDisplayer.print("Invalid IP address Format : example 127.0.0.1", (pygame.Vector2(self.game.DISPLAY_SIZE)-self.infoBackground.get_size())//2, rectSize=(600,80), center=True, scale=0.3)
                #print("IP adress format Invalid : example 127.0.0.1")    
                self.okayButton.update(events)
                self.blit(self.okayButton.image, self.okayButton.rect)
                if self.okayButton.isPressed():
                    self.isPressedN = False
            #TODO: take off the fact that you always need to save OptionalParamaters 

        
        if self.backbutton.isPressed():
            self.isPressed = False
        self.backbutton.update(events)
        self.blit(self.backbutton.image,self.backbutton.rect)
