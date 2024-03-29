from pygame import color
from dungeonX.characters.enemies.enemy_controller import distanceBetween
import dungeonX
from numpy.lib.function_base import append
import pygame, math
from ..map import Dungeon, Map
from ..constants import TILE_WIDTH, State, ItemList, SKILLS_INFO, cellsrange, Attributes
from ..characters.npc import NPC 
from ..characters.players.classes import Fighter, Mage, Rogue
from ..characters.players import PlayerEnum
from ..characters.enemies import Zombie, Enemy
from ..objects import Chest, Door, Stairs
from ..items import ItemFactory
from ..graphics import Button, Cell
from ..characters.skills import SkillFactory,SkillEnum
from . import Window, MapWindow, BottomBarWindow, PauseMenu, LogWindow, InventoryWindow, SkillWindow, CharacterWindow, StatusWindow,NpcTradingWindow
from copy import deepcopy,copy
from ..network.essaiOtherPlayer import OtherPlayer2
from ..network.realPlayer import RealPlayer
from ..network.message import check_size, Message, extract, read_name


class GameScreen(Window):
	""" This is the main screen, where all the game is rendered
	
	It has a lot of functionalities, such as camera handling
	(animation, optimization of the rendering based on objects in the
	scope), turn logic, keyboard handling, etc...

	Attributes
	----------
	players : list
		List which contains all instances of players
	enemies : list
		List which contains all instances of enemies
	objects : list
		List which contains all instances of game objects
	selectedPlayer : PlayerController
		Contains the current selected player
	dungeon : Dungeon
		Instance of the dungeon. See Dungeon for more information
	mapwindow : MapWindow
		Instance of the map window. See MapWindow for more information
	bottombarwindow : BottomBarWindow
		Instance of the bottom bar window. See BottomBarWindow for
		more information
	pausemenu : PauseMenu
		Instance of the pause menu. See PauseMenu for more information
	state : str
		Stores the current state of the game, it must be one of the
		following values.
		- walk : they aren't any visible enemies so the player can
			move freely
		- input : it is player's turn, and the game is
			waiting for him to input his actions.
		- enemy : it is enemy's turn
		- map_opened : the map is opened, the game is "paused" and the
			mapwindow is shown.
		- paused : the pause menu is opened, the game is "paused"
			and the pause window is shown.
	camera : pygame.Rect
		This rect represents the camera. It contains information about
		it's position, it's size, and allows easy handling of what
		objects should be rendered.
	passTurnButton : Button
		Instance of Button used to validate the player's actions.
	pauseButton : Button
		Instance of Button used to pause the game and show PauseMenu.
	movementCell : Cell
		Instance of Cell used to draw the range of posible movement
		for the selected player
	pathPreviewCell : Cell
		Instance of Cell used to draw the path preview of selected
		player
	pathCell : Cell
		Instance of Cell used to draw the path of selected player
	zoneCell : Cell
		Instance of Cell used to draw the zone of the selected spell

	Methods
	-------
	setCamera(pos)
		Setter for the center of camera. Directly set camera's center
		without animation.
	animateCameraTo(pos)
		Setter for __cameraDestination. Animates smoothly the movement
	setState(state)
		Setter for game's state, this method stores the last state for
		future use
	resumeState()
		Resume the previously stored state
	selectPlayer(p)
		Setter for selectedPlayer. The parameter can either be an
		index in players list or an instance of player.
	update(events)
		Main update method.

	Private Attributes
	------------------
	__viewport : pygame.Surface
		Surface on which every frame of the actual game (everything
		exepted GUI) is rendered. This surface is used to optimize 
		rendering time by a lot. 
	__savedState : str
		Stores a state for later use. It is used to resume the correct
		state of the game when closing the map window.
	__CAMERA_SPEED : int
		This number represent the time taken by the camera to travel
		from one point to another, in milliseconds.
	__cameraDestination : tuple
		This tuple stores the current destination of the camera, if
		not None.
	__cameraMovingSince : int
		This number represent the time elapsed since the camera
		started moving. It is used to animate camera's movement.
	"""
	def __init__(self, game, dungeon=None, saveName=None):
		super().__init__(game)
		self.__viewport = pygame.Surface((40*TILE_WIDTH, 40*TILE_WIDTH/game.RATIO))
		self.game.particleSystem.attachScreen(self.__viewport)
		self.game=game

		self.saveName = saveName
		if dungeon==None:
			self.dungeon = Dungeon(self)
		else:
			self.dungeon = dungeon
			self.dungeon.game = self
			for floor in self.dungeon.floors:
				floor.game = self
			lst = self.dungeon.currentFloor.enemies + self.dungeon.currentFloor.objects
			lst += self.dungeon.players if self.dungeon.players!=None else []
			for ent in lst:
				ent.game = self



		self.enemies = self.dungeon.currentFloor.enemies
		self.objects = self.dungeon.currentFloor.objects
		self.players = self.dungeon.players
		self.npcwindow = NpcTradingWindow(game,self)

		self.selectedPlayer = None if self.players==None or len(self.players)==0 else self.players[0]
		
		self.currentPlayerAction = None
		self.enemyTimeline = None
		self.currentEnemy = None

		self.bottombarwindow = BottomBarWindow(self)
		self.inventorywindow = InventoryWindow(game, self)
		
		
		self.mapwindow = MapWindow(game, self)
		self.pausemenu = PauseMenu(game, self)
		self.skillwindow=SkillWindow(game, self)
		self.characterwindow=CharacterWindow(game, self)
		self.statuswindow = StatusWindow(game, self)
		self.displaycharacterwindow=False
		self.currentCharacterSheet=-1
		self.currentInventory = -1

		self.camera = pygame.Rect((0,0), (self.__viewport.get_width(), self.__viewport.get_height()))
		self.setCamera(Map.posToVect(self.dungeon.currentFloor.startPos))
		self.__CAMERA_SPEED = 500 # in milliseconds
		self.__cameraDestination = None
		self.__cameraMovingSince=0
		self.selectedActionName = None

		self.turnNumber = 0
		self.APRefill = 0
		self.state = "walk"
		self.__savedState = "walk"
		self.passTurnButton = Button(game, (16, 32+self.mapwindow.minimaprect.height), "Pass Turn", textScale=0.33, action=lambda:self.setState('enemy'))
		self.movementCell = Cell((255,255,255, 30))
		self.pathPreviewCell = Cell((0,128,0, 120))
		self.pathCell = Cell((0,128,0, 200))
		self.zoneCell = Cell((128,20,20))
		self.rangeCell = Cell((103,216,239, 120))
		self.pauseButton= Button(game,(self.get_width()-66, 16), '', imgPath = "dungeonX/assets/ui/pause_button.png", size=(50,50), action=lambda:self.setState("paused"))

		# next/previous inventory buttons init
		self.nextButton= Button(game,(self.get_width()-256, 325), '', imgPath = "dungeonX/assets/menu/next_arrow.png", size=(50,50), action=lambda:self.nextInventory(1))
		self.prevButton= Button(game,(77, 325), '', imgPath = "dungeonX/assets/menu/back_arrow.png", size=(50,50), action=lambda:self.nextInventory(-1))

		#next/previous charactersheet buttons
		self.nextButtonC= Button(game,(self.get_width()-40, 150), '', imgPath = "dungeonX/assets/menu/next_arrow.png", size=(30,30), action=lambda:self.nextSheet(1))
		self.prevButtonC= Button(game,(self.get_width()-285, 150), '', imgPath = "dungeonX/assets/menu/back_arrow.png", size=(30,30), action=lambda:self.nextSheet(-1))

		self.lifebar_background = pygame.image.load("dungeonX/assets/ui/lifeBar/background.png").convert()
		self.lifebar_foreground = pygame.image.load("dungeonX/assets/ui/lifeBar/foreground.png").convert()
		self.oplayers = self.dungeon.oplayers
		self.realPlayers = {}
		self.oplayerCreation = False

		self.playerName = ""

	def __getstate__(self):
		return None

	def blitLoadingScreen(self):
		self.game.display.fill((0,0,0))
		self.game.textDisplayer.print("Loading...", (0,0), rectSize=self.get_size(), center=True, center_y=True, screen=self.game.display)
		pygame.display.update()


	def selectDefaultPlayers(self, playerTypes: [PlayerEnum]):
		self.dungeon.players = []
		self.players = self.dungeon.players
		"""
		This shouldn't be here, it's here for the purpose of testing the skillWindow and should be removed eventually
		This is here because we want our players to have access to all the skills(for testing purpose)without triggering
		errors in the tests.
		"""
		defaultSkillrogue=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillrogue2=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillrogue3=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillfighter=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillfighter2=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillfighter3=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		defaultSkillmage=[SkillFactory(SkillEnum.Stealth),SkillFactory(SkillEnum.DisableDevice),SkillFactory(SkillEnum.Perception)]
		#print(f"Here: {self.playerName}")
		for playerType in playerTypes:
			if playerType == PlayerEnum.Rogue:
				self.dungeon.players.append( Rogue(self, (0,0), defaultSkills=defaultSkillrogue))
				defaultSkillrogue=defaultSkillrogue2
				defaultSkillrogue2=defaultSkillrogue3
			elif playerType == PlayerEnum.Fighter:
				self.dungeon.players.append( Fighter(self, (0,0), defaultSkills=defaultSkillfighter) )
				defaultSkillfighter=defaultSkillfighter2
				defaultSkillfighter2=defaultSkillfighter3
			elif playerType == PlayerEnum.Mage:
				self.dungeon.players.append( Mage(self, (0,0), skills=defaultSkillmage))
			else : pass

		if len(self.dungeon.players) != 0: self.selectPlayer(0)
	
	def selectDefaultObject(self):
		for object in self.objects :
			x = object.pos[0]
			y = object.pos[1]
			_range = [(a,b) for a in range(x-1, x+2) for b in range(y-1, y+2) ]
			if (self.selectedPlayer.pos[0], self.selectedPlayer.pos[1]) in _range:
				return object
			else:
				return None

		
	def setCamera(self, pos:tuple):
		""" Setter for the center of camera

		Directly set camera's position without animation.
		"""
		self.camera.center = pos
		self.__cameraDestination = None
		self.__cameraMovingSince = 0

	def animateCameraTo(self, pos:tuple, reset:bool=True):
		""" Setter for __cameraDestination

		Animates smoothly the movement, using __CAMERA_SPEED
		"""
		self.__cameraDestination = pos
		if reset or self.__cameraMovingSince>=self.__CAMERA_SPEED:
			self.__cameraMovingSince = 0

	def resumeState(self):
		""" Resume the previously saved state """
		self.state = self.__savedState

	def setState(self, state):
		""" Setter for the current state

		this method stores the last state for future use.
		"""
		if self.state in ('input', 'walk', 'enemy'):
			self.__savedState = self.state
		self.state = state
	

	def selectPlayer(self, p):
		""" Setter for selectedPlayer

		The parameter p can either be an integer representing the
		index in self.players, or directly an instance of player.
		"""
		if type(p) is int:
			if p in range(len(self.players)):
				self.selectedPlayer = self.players[p]
		else:
			if p in self.players:
				self.selectedPlayer = self.players[self.players.index(p)]
		self.selectedActionName = None
		self.animateCameraTo(self.selectedPlayer.rect.center)
	
	def getCurrentTurnNumber(self):
		return int(self.turnNumber)
	
	def getCurentInitialTurnNumber(self):
		return copy(self.turnNumber)

	def update(self, events):
		""" Main update method

		Updates the surface. Called at every loop turn. This method
		does the following :
		- Handle events
		- Update Camera
		- Handle turn logic
		- Render the game : 
			1. Blit the first layer of the map (floor)
			2. Draw movementCells, pathCells, zoneCell if needeself.selectedPlayer.getLineOfSightCells(d)
			3. Blit all players
			4. Blit the second layer of the map (walls)
			4. Handle and blit fog
			5. Blit the UI (User Interface), i.e mapwindows or passTurnButton
		"""

		mousePosition = pygame.mouse.get_pos()
		absoluteMousePosition = (mousePosition[0]*self.__viewport.get_width()/self.get_width()+self.camera.left, mousePosition[1]*self.__viewport.get_height()/self.get_height()+self.camera.top)
		
		# --- Events Handling --- #
		for event in events:
			if self.state in ("map_opened", "inventory_opened", "paused", "skillwindow_opened","npcwindow_opened"):
				if event.type == pygame.KEYUP:
					keys = [pygame.K_ESCAPE]
					if self.state=="skillwindow_opened": keys = []
					if event.key in keys:
						self.resumeState()
			else:
				if event.type == pygame.KEYUP:
					if event.key == pygame.K_ESCAPE:
						self.pausemenu.mapSaved = False
						self.setState('paused')

				if event.type == pygame.MOUSEBUTTONDOWN:
					if not any((self.passTurnButton.rect.collidepoint(event.pos),
								self.pauseButton.rect.collidepoint(event.pos),
								self.nextButton.rect.collidepoint(event.pos),
								self.prevButton.rect.collidepoint(event.pos),
								self.nextButtonC.rect.collidepoint(event.pos),
								self.prevButtonC.rect.collidepoint(event.pos),
								self.bottombarwindow.rect.collidepoint(event.pos))):
						if event.button==3:
							for player in self.players:
								if player.rect.collidepoint(absoluteMousePosition):
									self.selectPlayer(player)
						if event.button==1:
							if self.state in ('walk', 'input'):
								if self.selectedActionName!=None:
									l = list(filter(lambda c:self.dungeon.currentFloor.get(*c)=='.', map(lambda x:(x[0]+self.selectedPlayer.pos[0], x[1]+self.selectedPlayer.pos[1]), SKILLS_INFO[self.selectedActionName][0])))
									if SKILLS_INFO[self.selectedActionName][1]==None:
										l2 = l
									else:
										l2 = list(filter(lambda x:any(x==e.pos for e in (self.enemies if SKILLS_INFO[self.selectedActionName][1]=='enemy' else self.objects)), l))

									for cx, cy in l2:
										rect = pygame.Rect(cx*TILE_WIDTH, cy*TILE_WIDTH, TILE_WIDTH, TILE_WIDTH)
										if rect.collidepoint(absoluteMousePosition):
											if self.selectedActionName=='Convert_enemy':
												target = filter(lambda x:x.pos==(cx,cy), self.enemies)
												self.selectedPlayer.convertEnemy(next(target))
											elif self.selectedActionName=='Fireball':
												self.selectedPlayer.castSpell(self.selectedPlayer.fireball, (cx,cy))
											elif self.selectedActionName=='AcidStream':
												self.selectedPlayer.castSpell(self.selectedPlayer.acidStream, (cx,cy))
											elif self.selectedActionName=='MeteorSwarm':
												self.selectedPlayer.castSpell(self.selectedPlayer.meteorSwarm, (cx,cy))
											elif self.selectedActionName=='DisableDevice':
												target = filter(lambda x:x.pos==(cx,cy), self.objects)
												self.selectedPlayer.AtemptToApplySkill(SkillEnum.DisableDevice, alwaysSuccess=True, options=target)
									self.selectedActionName = None
								elif not self.selectedPlayer.finalTarget:
									tEnts = [ent for ent in self.objects+self.enemies if ent.rect.collidepoint(absoluteMousePosition)]
									self.selectedPlayer.setTarget(Map.vectToPos(absoluteMousePosition), targetObject=tEnts)
							


		# --- Camera update --- #
		if self.__cameraDestination:
			self.camera.center = pygame.Vector2(self.camera.center).lerp(self.__cameraDestination, self.__cameraMovingSince / self.__CAMERA_SPEED)
			self.__cameraMovingSince += self.game.dt
			if (self.__cameraMovingSince >= self.__CAMERA_SPEED):
				self.__cameraDestination = None


		# ---- Floor rendering ---- #
		self.__viewport.fill((0,0,0))
		self.__viewport.blit(self.dungeon.currentFloor.layers["floor"], (-self.camera.left, -self.camera.top))
		
		# ---- Turn Logic and colored cells rendering ---- #
		if self.state=='walk' or (self.state=='map_opened' and self.__savedState=='walk'):
			self.animateCameraTo(self.selectedPlayer.rect.center, reset=False)
			for player in self.players:
				# player.setActionPoint(player.actionPointMax)
				player.updateState(self.game.dt)
				if player.stepsToTarget:
					self.movementCell.drawCells(self.__viewport, player.stepsToTarget, self.camera.topleft)
					if player.finalTarget:
						self.pathCell.drawCells(self.__viewport, [player.finalTarget], self.camera.topleft)
				elif player==self.selectedPlayer:
					self.movementCell.drawCells(self.__viewport, player._move_zone(), self.camera.topleft)
			for enemy in filter(lambda e:any(Map.distanceBetween(*p.pos, *e.pos)<=p.lineOfSightRadius+3 for p in self.players), self.enemies):
				enemy.playAction(self.game.dt)

			playersAP = list(filter(lambda x:x.getActionPoint()==0, self.players))
			if len(playersAP)>0:
				if self.APRefill < len(self.players):
					for p in playersAP:
						p.setActionPoint(p.actionPointMax)
						self.APRefill+=1
				else:
					for enemy in filter(lambda e:any(Map.distanceBetween(*p.pos, *e.pos)<=p.lineOfSightRadius+3 for p in self.players), self.enemies):
						enemy.makeDecision()
					for player in self.players:
						player.setActionPoint(player.actionPointMax)
					self.APRefill=0
					self.turnNumber += 1

			if self.selectedActionName!=None:
				px,py = self.selectedPlayer.pos
				l = list(filter(lambda c:self.dungeon.currentFloor.get(*c)=='.', map(lambda x:(x[0]+self.selectedPlayer.pos[0], x[1]+self.selectedPlayer.pos[1]), SKILLS_INFO[self.selectedActionName][0])))
				self.rangeCell.drawCells(self.__viewport, l, self.camera.topleft)
				if self.selectedActionName=="Fireball":
					x, y = Map.vectToPos(absoluteMousePosition)
					if (x,y) in l:
						l2 = list(filter(lambda c:self.dungeon.currentFloor.get(*c)=='.', [(cx+x, cy+y) for cx,cy in cellsrange(3)]))
						self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)
				if SKILLS_INFO[self.selectedActionName][1]=='enemy':
					l2 = list(filter(lambda x:any(x==e.pos for e in self.enemies), l))
					self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)
				if SKILLS_INFO[self.selectedActionName][1]=='objects':
					l2 = list(filter(lambda x:any(x==e.pos for e in self.objects), l))
					self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)

			if any(e.pos in p.getLineOfSightCells() for p in self.players for e in self.enemies if not e.finalTarget):
				self.setState('input')
				for p in self.players:
					p.setActionPoint(p.actionPointMax)
					if p.finalTarget:
						p.stepsToTarget=None

		elif self.state == 'input':
			self.animateCameraTo(self.selectedPlayer.rect.center, reset=False)
			for player in self.players:
				player.updateState(self.game.dt)
				if player.stepsToTarget:
					self.pathCell.drawCells(self.__viewport, player.stepsToTarget, self.camera.topleft)
				elif player.rect.collidepoint(absoluteMousePosition) or player==self.selectedPlayer:
					self.pathPreviewCell.drawCells(self.__viewport, player._move_zone(), self.camera.topleft)

			if self.selectedActionName!=None:
				px,py = self.selectedPlayer.pos
				l = list(filter(lambda c:self.dungeon.currentFloor.get(*c)=='.', map(lambda x:(x[0]+self.selectedPlayer.pos[0], x[1]+self.selectedPlayer.pos[1]), SKILLS_INFO[self.selectedActionName][0])))
				self.rangeCell.drawCells(self.__viewport, l, self.camera.topleft)
				if self.selectedActionName=="Fireball":
					x, y = Map.vectToPos(absoluteMousePosition)
					if (x,y) in l:
						l2 = list(filter(lambda c:self.dungeon.currentFloor.get(*c)=='.', [(cx+x, cy+y) for cx,cy in cellsrange(3)]))
						self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)

				if SKILLS_INFO[self.selectedActionName][1]=='enemy':
					l2 = list(filter(lambda x:any(x==e.pos for e in self.enemies), l))
					self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)
				if SKILLS_INFO[self.selectedActionName][1]=='objects':
					l2 = list(filter(lambda x:any(x==e.pos for e in self.objects), l))
					self.zoneCell.drawCells(self.__viewport, l2, self.camera.topleft)

			if not any(e.pos in p.getLineOfSightCells() for p in self.players for e in self.enemies):
				self.setState('walk')

		elif self.state=='enemy':
			if self.enemyTimeline==None:
				self.enemyTimeline = filter(lambda e:any(e.pos in p.getLineOfSightCells() for p in self.players), self.enemies)
			if self.currentEnemy==None:
				try:
					self.currentEnemy = next(self.enemyTimeline)
				except StopIteration:
					self.setState('input')
					self.turnNumber += 1
					self.enemyTimeline = None
					for enemy in self.enemies:
						enemy.decisionMade = False
					for p in self.players:
						p.setActionPoint(p.actionPointMax)
			else:
				if not self.currentEnemy.decisionMade:
					self.currentEnemy.makeDecision()
				self.currentEnemy.playAction(self.game.dt)
				if self.currentEnemy.state=='idle':
					self.currentEnemy = None
				
	
		
		# ---- Entity rendering ---- #

		# self.enemies = []
		# self.dungeon.currentFloor.enemies=[]
		entities = self.players+self.enemies+self.objects+self.oplayers if self.oplayers != None else self.players+self.enemies+self.objects

		for ent in sorted(entities, key=lambda x:x.rect.top):
		#for ent in sorted(self.players+self.enemies+self.objects, key=lambda x:x.rect.top):
			if self.camera.colliderect(ent.rect) and (not isinstance(ent,Enemy) or any(ent.pos in p.getLineOfSightCells() for p in self.players)):
				if isinstance(ent,OtherPlayer2):
					ent.updateAnim(self.game.dt + 30)
				else:
					ent.updateAnim(self.game.dt)
				self.__viewport.blit(ent.image, pygame.Vector2(ent.rect.topleft) - self.camera.topleft)
				if (ent in self.players and self.game.screens['online_screen'].online):
					pygame.draw.rect(self.__viewport, (0,255,0), ent.rect.move(-self.camera.left, -self.camera.top), 1)
				if ent==self.selectedPlayer:
					pygame.draw.rect(self.__viewport, (255,255,255), ent.rect.move(-self.camera.left, -self.camera.top), 1)
				# if ent==self.currentEnemy:
				# 	pygame.draw.rect(self.__viewport, (255,255,255), ent.rect.move(-self.camera.left, -self.camera.top), 1)
				if isinstance(ent, Enemy):
					self.__viewport.blit(self.lifebar_background, pygame.Vector2(ent.rect.topleft) - self.camera.topleft - (8,5))
					w = math.floor(self.lifebar_foreground.get_width()*ent.getHP()/ent.maxHP)
					if w>0:
						fg = pygame.transform.scale(self.lifebar_foreground, (math.floor(self.lifebar_foreground.get_width()*ent.getHP()/ent.maxHP), self.lifebar_foreground.get_height()))
						self.__viewport.blit(fg, pygame.Vector2(ent.rect.topleft) - self.camera.topleft - (8,5))

		# ---- Walls rendering ---- #
		self.__viewport.blit(self.dungeon.currentFloor.layers["walls"], (-self.camera.left, -self.camera.top))

		# ---- Fog rendering ---- #
		fogImg = self.dungeon.currentFloor.layers["fog"].copy()
		for p in self.players:
			self.dungeon.currentFloor.layers["fog"].blit(p.lineOfSightFoW, (p.rect.centerx-p.lineOfSightFoW.get_width()/2, p.rect.bottom-TILE_WIDTH/2-p.lineOfSightFoW.get_height()/2))
			fogImg.blit(p.lineOfSight, (p.rect.centerx-p.lineOfSight.get_width()/2, p.rect.bottom-TILE_WIDTH/2-p.lineOfSight.get_height()/2), special_flags=pygame.BLEND_SUB)
		self.__viewport.blit(fogImg, (-self.camera.left, -self.camera.top), special_flags=pygame.BLEND_SUB)

		# ---- GUI rendering ---- #
		self.game.particleSystem.update(self.game.dt)
		self.blit(pygame.transform.scale(self.__viewport, (self.get_width(), self.get_height())), (0,0))
		
		# liste des joueurs visibles pour afficher en fonction 
		if self.oplayers != None:
			visiblePlayersList = self.selectedPlayer.checkLineOfSight(self.oplayers)
			self.visiblePlayersList=visiblePlayersList

			visibleRealPlayersList=[]
			self.visibleRealPlayersList=visibleRealPlayersList
			
			for visiblePlayer in (visiblePlayersList) :
				for _,realPlayer in self.realPlayers.items() :
					if  (visiblePlayer.parent not in self.visibleRealPlayersList) :
						self.visibleRealPlayersList.append(realPlayer)

		if self.state == 'paused':
			self.pausemenu.update(events)
			self.blit(self.pausemenu, (0,0))
		else:
			if self.state == 'map_opened':
				self.mapwindow.update(events)
				self.blit(self.mapwindow, (0,0))
			elif self.state == 'inventory_opened': 
				if self.visiblePlayersList != []:
					self.nextButton.update(events)
					self.blit(self.nextButton.image,self.nextButton.rect)
					self.prevButton.update(events)
					self.blit(self.prevButton.image,self.prevButton.rect)
					if not (self.currentInventory == -1):
						#print(f"HERE HERE: {self.visibleRealPlayersList[self.currentInventory]}")
						self.inventorywindow.update(events, otherRealPlayer=self.visibleRealPlayersList[self.currentInventory])
						self.blit(self.inventorywindow, (0,0))
					else:
						self.inventorywindow.update(events)
				else:
					self.inventorywindow.update(events)
				self.blit(self.inventorywindow, (0,0))
			elif self.state=='skillwindow_opened':	
				self.blit(self.skillwindow,self.skillwindow.rect)
			elif self.state =='npcwindow_opened':
			 	self.blit(self.npcwindow,self.npcwindow.rect)

				
			else:
				self.mapwindow.updateMinimap(events)
				self.pauseButton.update(events)
				self.blit(self.mapwindow.minimap, self.mapwindow.minimaprect)
				self.blit(self.pauseButton.image,self.pauseButton.rect)
				self.game.log.update(events)
				self.blit(self.game.log,self.game.log.logsrect)
				if self.state == 'input':
					self.passTurnButton.update(events)
					self.blit(self.passTurnButton.image, self.passTurnButton.rect)
				self.statuswindow.handleInput(events)
				if self.displaycharacterwindow:
					# je teste de deplacer pcq j'en ai aussi besoin 
					# self.visiblePlayersList = self.selectedPlayer.checkLineOfSight(self.oplayers)
					try:
						if self.visiblePlayersList != []:
							self.nextButtonC.update(events)
							self.blit(self.nextButtonC.image,self.nextButtonC.rect)
							self.prevButtonC.update(events)
							self.blit(self.prevButtonC.image,self.prevButtonC.rect)
						if not (self.currentCharacterSheet == -1):
							self.characterwindow.update(events,plyr=self.visiblePlayersList[self.currentCharacterSheet])
						else:
							self.characterwindow.update(events)
					except IndexError:
						self.currentCharacterSheet = len(self.visiblePlayersList)-1
						if not (self.currentCharacterSheet == -1):
							self.characterwindow.update(events,plyr=self.visiblePlayersList[self.currentCharacterSheet])
						else:
							self.characterwindow.update(events)

					self.blit(self.characterwindow, self.characterwindow.rect)
				else:
					self.statuswindow.update(events)
					self.blit(self.statuswindow, self.statuswindow.rect)


			self.bottombarwindow.update(events)
			self.blit(self.bottombarwindow, (0,0))
			self.skillwindow.update(events)
			self.npcwindow.update(events)
		#network handling
		if self.game.screens['online_screen'].online:
			self.networkUpdate()
			if (not self.oplayerCreation):
				self.dungeon.oplayers = self.oplayers
				self.oplayerCreation = True
			if self.oplayers != None:
				for oplayer in self.oplayers:
					if (oplayer.pos == oplayer.newPos and oplayer.targets != []):
						oplayer.newPos = oplayer.targets[0]
						oplayer.targets.remove(oplayer.targets[0])
					oplayer.setActionPoint(oplayer.actionPointMax)
					oplayer._dt = self.game.dt
					oplayer.playAction(self.game.dt,(oplayer.newPos))
		
	def nextInventory(self,index):
		if (self.currentInventory+index >= len(self.visibleRealPlayersList) or self.currentInventory+index < -1):
			print("No more players in the line of sight")
			return
		self.currentInventory += index

	def nextSheet(self,index):
		if (self.currentCharacterSheet+index >= len(self.selectedPlayer.checkLineOfSight(self.oplayers)) or self.currentCharacterSheet+index < -1):
			print("No more players in the line of sight")
			return
		self.currentCharacterSheet += index
	
	def changePlayerName(self, name):
		self.playerName = name

	def retrieveChestsFromObjects(self,list):
		"""
		retreives only Chest items from the Object List
		"""
		listOfChests=[]
		for el in list:
			if type(el) == Chest :
				listOfChests.append(el)
		return listOfChests

	def returnPositionsOfChestsInGame(self,list):
		"""
		retreives only Chest items from the Object List
		"""
		listOfChestspos=[]
		for el in list:
			if type(el) == Chest :
				listOfChestspos.append(el.getPosition())
		return listOfChestspos

	def UpdateChestContent(self,Chest : Chest,ID,oPlayerID=None):
		"""
		serves into finding the chest containing item with ID from all Chests in the game and updating it
		"""
		# for el in list: #for all chests in the game
		# 	#for ch in el.getContent() :# for each chest 
		# 		if el.getItemByID(ID)!= None: 
		# 			itemToSubstract=el.getItemByID(ID)
		if oPlayerID!=None:
			# itemToSubstract=Chest.getItemByID(ID)
			# print(itemToSubstract)
			self.realPlayers[oPlayerID].bag.addItem(itemToSubstract)
			#el.UpdateChest(el,itemToSubstract)
			print(f'For Chest n {Chest} : Item {Chest.getItemByID(ID)} was taken from Chest by Another Player')
			print(f'POSITION FOUND & RETURNED {Chest.getPosition()}')
			return Chest.getPosition()	

	def UpdateChestContentV2(self,Chest : Chest,oPlayerID=None,content=""):
		"""
		serves into finding the chest containing item with ID from all Chests in the game and updating it
		"""
		print("UPDATING LOADING HERE ")
		if oPlayerID!=None: # serves Only for testing in file tests 
			print("UPDATING LOADING  ")
			Chest.getItemsFromChest()
			for i in range(len(content)):
				if (content[i]!='0'):
					item=self.initialToObject(content[i])
					maxWeight = 30
					if (item.getWeight() + (self.realPlayers[oPlayerID].getCurrentWeight())  <= maxWeight):
						self.realPlayers[oPlayerID].itemsList.append(item)
			#TODO: content = none 
			return Chest.getPosition()	
				
	
	def FindChestWithID(self,list:[Chest],ID):
		"""
		serves into finding the chest containing item with ID from all Chests in the game and updating it
		"""
		for el in list: #for all chests in the game
			for ch in el.getContent() :# for each chest 
				if el.getItemByID(ID)!= None: 
					print(f'For Chest n {el} : Item with ID {ID}')
					return el

	def FindChestWithPos(self,list:[Chest],Pos:tuple):
		"""
		serves into finding the chest containing item with ID from all Chests in the game and updating it
		"""
		for el in list: #for all chests in the game
			if el.getPosition() == Pos:
				return el
		
					
		
	def networkUpdate(self):
		#print(self.players[0].pos)
		message = self.game.screens['online_screen'].networker.getMessage()
		if message != "" :
			print("MESSAGE: ",message)
		if message[:3] == "con":
			msg_to_send = Message(self.players,flag="wlc").create_message(seed=self.game.screens['map_selector'].seed,ID=1 if self.oplayers ==None else len(self.oplayers)+1)
			print("Messages to send: ",msg_to_send)
			self.game.screens['online_screen'].networker.send(msg_to_send)
		elif message[:3] == "new":
			infos = extract(message[:42])
			print("Second player characters created")
			otherPlayers = [OtherPlayer2([infos[2][0],infos[2][1],infos[2][2]],self),OtherPlayer2([infos[3][0],infos[3][1],infos[3][2]],self)\
				    ,OtherPlayer2([infos[4][0],infos[4][1],infos[4][2]],self)]
			self.realPlayers[infos[0]] = RealPlayer(otherPlayers,read_name(infos[1]))
			print("Real Players Dictionnary: ",self.realPlayers)
			self.dungeon.oplayers= otherPlayers
			self.oplayers = self.dungeon.oplayers
		elif message[:3] == "pos":
			infos = extract(message[:14])
			playerID, characterID = infos[0], int(infos[1])-1
			newPos = (int(infos[2]),int(infos[3]))
			self.realPlayers[playerID].persos[characterID].targets.append(newPos)
			print("Real player Id " + infos[0] +" New position received: ",newPos," Character number "+infos[1])
			#self.realPlayers[playerID].persos[characterID].newPos = newPos
		# elif message[65:68]=="ite":
		# 	info = extract(message[65:])
		# 	ListOfChests= self.retrieveChestsFromObjects(self.objects)
		 	# print(f'MY OWN CHESTS {ListOfChests}')
			# ID = int(info[2])
			# #IDperso= int(info[1])
			# IDofOtherPlayer= info[0]
			# ChestTounlock=self.FindChestWithID(ListOfChests,ID)
			# ChestTounlock.unlock(alwaysSuccess=True)
			# self.UpdateChestContent(ChestTounlock,ID,IDofOtherPlayer)	
		elif message [:3] =="che":
			info = extract(message[:17])
			ListOfChests= self.retrieveChestsFromObjects(self.objects)
			IDofOtherPlayer= info[0]
			chestContent= str(info[3])
			#print("Chest content string is : "+chestContent)
			PosOfChest=(int(info[1]),int(info[2]))
			ChestToModify=self.FindChestWithPos(ListOfChests,PosOfChest)
			#print(f'Chest to modify is at{ChestToModify.getPosition()} ')
			#print(f'BEFORE{self.realPlayers[IDofOtherPlayer].itemsList}')
			self.UpdateChestContentV2(ChestToModify,oPlayerID=IDofOtherPlayer,content=chestContent)
			#print(f'AFTER {self.realPlayers[IDofOtherPlayer].itemsList}')
		elif message[:3] == "pro":
			infos = extract(message[:14])
			position = (int(infos[2]), int(infos[3]))
			proper = 1
			for player in self.players:
				if (position == player.finalTarget or position == player.pos):
					proper = 0
					break
			msg_to_send = Message([None,None,None],flag="ans",ID=int(infos[0])).create_message(prop = proper,pos=position,ID=int(infos[1]))
			self.game.screens['online_screen'].networker.send(msg_to_send)
		elif message[:3] == "ans":
			infos = extract(message[:15])
			index = int(infos[1]) - 1
			if int(infos[4]) == 1:
				target = int(infos[2]), int(infos[3])
				self.players[index].property = True
				self.players[index].setTarget(target)
			else:
				self.players[index].game.game.addToLog("You can't go to this position, it's owned by someone else")
				print("You can't go to this position, it's owned by someone else")
		elif message[:3] == "exi":
			infos = extract(message[:5])
			self.players[0].game.game.addToLog("Player "+self.realPlayers[infos[0]].name+" disconnected")
			oplayersToRmv = [self.realPlayers[infos[0]].persos[0],self.realPlayers[infos[0]].persos[1],self.realPlayers[infos[0]].persos[2]]
			for oplayer in oplayersToRmv:
				self.oplayers.remove(oplayer)
			del self.realPlayers[infos[0]]
			# self.game.screens['online_screen'].networker.stop()
			# self.game.screens['online_screen'].networker.join()
		elif message[:3] == "equ" :
			info = extract(message[:7])
			realPlayerId= info[0]
			playerId = int(info[1])-1
			index = int(info[2])
			item = self.indexToEquipment(index)
			player = self.realPlayers[realPlayerId].persos[playerId]
			# instructions pour enlever du bag l'objet
			itemToRemove=self.realPlayers[realPlayerId].itemOfType(item.getItemType())
			self.realPlayers[realPlayerId].itemsList.remove(itemToRemove)
			# ajout item a l'equipement
			player.equipment[index]=item
			player.increaseStats(item.getEffectiveStats())
			player.maxHP += item.getEffectiveStats()[Attributes.HP]

	
	def getValidLocations(self):
		found = False
	
		while not found:
			pos = self.dungeon.currentFloor.getRandomValidLocation()
			positions = [pos]
			l = [(pos[0]+1,pos[1]),(pos[0]+1,pos[1]+1),(pos[0]-1,pos[1]),(pos[0],pos[1]-1),(pos[0]+2,pos[1]),(pos[0]-2,pos[1])]
			for position in l:
				if self.dungeon.currentFloor.isValidLocation(*position):
					positions.append(position)
				if len(positions) == 3:
					found = True
					break
		print("Available positions: ",positions)
		return positions
	
	def initialToObject(self,initial):
		if initial=='C':
			return ItemFactory(ItemList.Coin)
		if initial=='S':
			return ItemFactory(ItemList.Sword)
		if initial=='A':
			return ItemFactory(ItemList.Armor)
		if initial=='R':
			return ItemFactory(ItemList.Ring)
		if initial=='N':
			return ItemFactory(ItemList.Necklace)
		if initial=='P':
			return ItemFactory(ItemList.Potion)


	def indexToEquipment(self,index):
		if index==0:
			return ItemFactory(ItemList.Sword)
		elif index==1:
			return ItemFactory(ItemList.Armor)
		elif index==2:
			return ItemFactory(ItemList.Necklace)
		elif index in (3,4) :
			return ItemFactory(ItemList.Ring)
