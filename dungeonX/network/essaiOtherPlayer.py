import pygame,math,os,random
from dungeonX.network.message import read_position, read_attributes,read_type, read_mod
from dungeonX.constants import TILE_WIDTH, MAX_HP, serializeSurf, unserializeSurf,DEFAULT_ACTION_POINT,OTHERPLAYERNAME
from dungeonX.characters.character import Character
from ..map import Map
from dungeonX.characters import Bag

def vectToPos(vect):
    if type(vect) in (tuple, list):
        if len(vect)!=2:
            raise ValueError("invalid vector : "+str(vect))
        return (math.floor(vect[0]/TILE_WIDTH), math.floor(vect[1]/TILE_WIDTH))
    return (math.floor(vect.x/TILE_WIDTH), math.floor(vect.y/TILE_WIDTH))

def posToVect(pos):
    return pygame.Vector2(pos)*TILE_WIDTH

def distanceBetween(xA, yA, xB, yB):
    """ Returns the distance between A and B """
    return math.sqrt((xB-xA)*(xB-xA) + (yB-yA)*(yB-yA))

class OtherPlayer2(Character):

    def __init__(self, liste_str,game,actionPointMax=DEFAULT_ACTION_POINT):
        print("Player created")
        super().__init__(game,read_position(liste_str[1],liste_str[2]), actionPointMax,100, 5, 6, 11, 3, 12, 8, 9) #( HP, armor, strength, dex, con, intell, wis, cha )

        self.type = read_type(liste_str[0])
        self.mod = read_mod(liste_str[0])
        self.pos = read_position(liste_str[1],liste_str[2])
        self.exp = 0 #we have to modify this later if we create a message type for exp
        self.name=OTHERPLAYERNAME # default name before realPlayer's username assignment 
        self.equipment=[]

        self.timeToMove = 300
        self.animationSpeed = {'idle': 120, 'run': 100}
        self.rect = pygame.Rect((0,0), (TILE_WIDTH, math.floor(TILE_WIDTH*24/16)))
        self.rect.midbottom = posToVect(self.pos) + (TILE_WIDTH/2, TILE_WIDTH)
        self.state = 'idle'
        self.direction = 0
        self.currentTarget = None
        self.finalTarget    = None
        self.stepsToTarget  = None
        self.equipment = [None, None, None, None, None] # Weapon, Armor, Necklace, Left Ring, Right Ring

         # Load all frames
        self.images = dict()
        for state in ('idle', 'run'):
            self.images[state] = [[], []]
            for i in range(4):
                if os.path.isfile("dungeonX/assets/characters/" + '_'.join([self.mod, state, 'f'+str(i)]) + ".png"):
                    img = pygame.image.load("dungeonX/assets/characters/" + '_'.join([self.mod, state, 'f'+str(i)]) + ".png").convert()
                else:
                    print("Warning: Missing texture \"dungeonX/assets/characters/" + '_'.join([self.mod, state, 'f'+str(i)]) + ".png\"")
                    img = pygame.image.load("dungeonX/assets/missing.png").convert()
                img.set_colorkey((0,0,0))
                self.images[state][0].append(img)
                self.images[state][1].append(pygame.transform.flip(img, True, False))

        self.positions = None
        self.frames = self.frameIter()
        self._dt = 0
        self.image = next(self.frames)
        self.game = game
        self.actionPoint = actionPointMax
        
        self.level = 1 #we have to change this later when we define a message type for this
        #self._bag=self.MessageBag

    def __getstate__(self):
        d = dict(serializeSurf(self.__dict__))
        del d["positions"]
        del d["frames"]
        return d
    
    def updateName(self,name):
        self.name=name

    def __setstate__(self, state):
        state["positions"] = None
        state["frames"] = self.frameIter()
        self.__dict__ = unserializeSurf(state)

    def nextTarget(self):
        """ This method handles iteration through stepsToTarget

        It also computes the direction based on the next movement
        along X.
        """
        if self.stepsToTarget:
            t = self.stepsToTarget.pop(0)
            self.currentTarget = pygame.Vector2(t[0]+0.5, t[1]+1)*TILE_WIDTH
            movementX = self.currentTarget.x - posToVect(self.pos).x
            self.direction = 0 if movementX > 0 else 1 if movementX < 0 else self.direction
            self.pos = t
        else:
            print("ELSE")
            self.stepsToTarget = None
            self.currentTarget = None
            self.finalTarget = None

    def positionsIter(self):
        """ This iterator go through every absolute positions that may be
        taken by the player.
        """
        elapsedTime = 0
        while (elapsedTime < self.timeToMove):
            print("Elapsed time\n",elapsedTime,self._dt)
            yield pygame.Vector2(self.rect.midbottom).lerp(self.currentTarget, elapsedTime / self.timeToMove)
            elapsedTime += self._dt
            print("Elapsed time 1\n",elapsedTime)
        yield self.currentTarget


    def frameIter(self):
        """ This iterator go througn every frames that may be rendered,
        based on current state and animationSpeed.
        """
        print("frameIter")
        elapsedTime = 0
        frame = random.randint(0, len(self.images[self.state][self.direction])-1)
        while True:
            elapsedTime += self._dt

            if elapsedTime > self.animationSpeed[self.state]:
                elapsedTime = 0
                frame += 1

            if frame>len(self.images[self.state]):
                frame=0
            yield self.images[self.state][self.direction][frame]

    def setTarget(self, target:tuple):
        """ Setter for finalTarget """
        self.stepsToTarget = self.pathfind(target)
        print("self.steps\n",self.stepsToTarget)
        if self.stepsToTarget:
            self.finalTarget = target            
            if not self.currentTarget:
                self.nextTarget()


    def updateAnim(self, dt:int):
        """ Updates the frame that may be rendered.

        This method must be
        called at every loop turn if the player is within the camera
        scope.
        """
        self._dt = dt # Stored for future use (in positionsIter and frameIter)
        self.image = next(self.frames)

    def playAction(self,dt:int,tup):
        self.setTarget(tup)
        if self.currentTarget:
            self.state = 'run'

            if not self.positions:
                self.positions = self.positionsIter()

            try:
                self.rect.midbottom = next(self.positions)

            except StopIteration:
                print('erreur playaction')
                self.state = 'idle'
                self.positions = None
                self.nextTarget()
        else:
            self.state = 'idle'
        return self.state

    def getLevel(self) :
        return self.level
        
    def checkPresence(self,crews):
        """
        This function is made to avoid repeating the same crew in the list crews
        """
        if self.parent.persos in crews: return True
        return False