from Pill import *
from Node import *
import pygame
from SpriteSheet import Spritesheet
from pygame.constants import *
from Constants import *

class Pacman:
    def __init__(self,screen: pygame.Surface,filename, spritesheet: Spritesheet, nodeMap: NodeMap) -> None:
        self.map = nodeMap
        self.position = self.map.nodeList[STARTNODE]
        self.position.position()
        self.screen = screen
        self.rect = pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.position.position(),(TILEWIDTH,TILEHEIGHT)))
        self.move = -1
        self.location = pygame.math.Vector2(self.position.position())
        self.mayPass = -1
        self.wantMove = -1
        self.lives = LIVES
        self.points = 0
        self.godMode = False
        self.godCount = 0
        self.spritesheet = spritesheet
        self.sprite = spritesheet.getLargeSprite(0,0,0)
        self.mouth = 0
        self.closed = 0
        
    def display(self):
        self.mouth +=1
        self.checkMouth()
        #self.pillMap.drawPills()
        pygame.draw.circle(self.screen,(0,0,0),self.rect.center,TILEHEIGHT)
        pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(LIFECOVER,(4*TILEWIDTH,4*TILEHEIGHT)))
        pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(SCORECOVER,(8*TILEWIDTH,4*TILEHEIGHT)))
        myFont = pygame.font.Font('joystix.ttf',30)
        lifeMsg = myFont.render(str(self.lives),True, WHITE)
        self.screen.blit(lifeMsg, LIFEDISPLAY)
        self.rect = pygame.draw.rect(self.screen,(0,0,0),pygame.Rect((self.location),(TILEWIDTH,TILEHEIGHT)))
        self.checkGod()
        if self.godMode:
            self.godCount+=1
        self.screen.blit(self.sprite,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        scoreMsg = myFont.render(str(self.points),True, WHITE)
        self.screen.blit(scoreMsg, SCOREDISPLAY)

    def checkMouth(self):
        if self.mouth == 10:
            if self.closed == 0:
                self.closed = 1
            elif self.closed == 1:
                self.closed = 2
            elif self.closed == 2:
                self.closed = 3
            elif self.closed == 3:
                self.closed = 0
            self.mouth = 0

    def checkGod(self):
        if self.godCount == GODTIME:
            self.godMode = False
            self.godCount = 0

    def moveConvert(self,event):
        if event.type == KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    return 0
                case pygame.K_RIGHT:
                    return 1
                case pygame.K_DOWN:
                    return 2
                case pygame.K_LEFT:
                    return 3
        return -1

    def keyboardMove(self,event):
        move = self.moveConvert(event)
        self.readMovement(move)

    def readMovement(self, move):
        match move:
            case 0:
                if self.position.up is not None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):                    
                    self.move = 0
                if not (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.wantMove = 0
            case 1:
                if self.position.right is not None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.move = 1
                if not (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.wantMove = 1
            case 2:
                if self.position.down is not None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.move = 2
                if not (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.wantMove = 2
            case 3:
                if self.position.left is not None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.move = 3
                if not (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.wantMove = 3
    
    def checkNode(self):      
        if self.location == self.position.vector:
            if self.position.teleport:
                if self.position.right != None:
                    self.position = self.map.nodeList[RIGHTTELE]
                    self.location = pygame.math.Vector2(self.position.position())
                    self.wantMove = 3
                else:
                    self.position = self.map.nodeList[LEFTTELE]
                    self.location = pygame.math.Vector2(self.position.position())
                    self.wantMove = 1

            
            match self.wantMove:
                case 0:
                    if self.position.up != None:
                        self.move = 0
                        self.wantMove = -1
                case 1:
                    if self.position.right != None:
                        self.move = 1
                        self.wantMove = -1
                case 2:
                    if self.position.down != None:
                        self.move = 2
                        self.wantMove = -1
                case 3:
                    if self.position.left != None:
                        self.move = 3
                        self.wantMove = -1
        
        match self.move:
            case -1:
                self.target = self.position
            case 0:
                if self.closed == 0:
                    self.sprite = self.spritesheet.getLargeSprite(8*TILEWIDTH,0*TILEHEIGHT,0)
                elif self.closed == 1 or self.closed == 3:
                    self.sprite = self.spritesheet.getLargeSprite(6*TILEWIDTH,0,0)
                else:
                    self.sprite = self.spritesheet.getLargeSprite(6*TILEWIDTH,2*TILEHEIGHT,0)
                if self.mayPass == 2:
                    self.position = self.position.down
                if self.position.up != None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    if self.location != pygame.math.Vector2(self.position.up.position()):
                        self.location += SPEED*self.position.lerp(self.position.up).normalize()
                        self.mayPass = 0
                        self.target = self.position.up
                    else:
                        self.position = self.position.up
                        self.mayPass = -1
                
            case 1:
                if self.closed == 0:
                    self.sprite = self.spritesheet.getLargeSprite(8*TILEWIDTH,0*TILEHEIGHT,0)
                elif self.closed == 1 or self.closed == 3:
                    self.sprite = self.spritesheet.getLargeSprite(2*TILEWIDTH,0,0)
                else:
                    self.sprite = self.spritesheet.getLargeSprite(2*TILEWIDTH,2*TILEHEIGHT,0)
                if self.mayPass == 3:
                    self.position = self.position.left
                if self.position.right != None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    
                    if self.location != pygame.math.Vector2(self.position.right.position()):
                        self.location += SPEED*self.position.lerp(self.position.right).normalize()
                        self.mayPass = 1
                        self.target = self.position.right
                    else:    
                        self.position = self.position.right
                        self.mayPass = -1
            case 2:
                if self.closed == 0:
                    self.sprite = self.spritesheet.getLargeSprite(8*TILEWIDTH,0*TILEHEIGHT,0)
                elif self.closed == 1 or self.closed == 3:
                    self.sprite = self.spritesheet.getLargeSprite(4*TILEWIDTH,0,0)
                else:
                    self.sprite = self.spritesheet.getLargeSprite(4*TILEWIDTH,2*TILEHEIGHT,0)
                if self.mayPass == 0:
                    self.position = self.position.up
                if self.position.down != None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    if self.location != pygame.math.Vector2(self.position.down.position()):
                        self.location += SPEED*self.position.lerp(self.position.down).normalize()
                        self.mayPass = 2
                        self.target = self.position.down
                    else:    
                        self.position = self.position.down
                        self.mayPass = -1
            case 3:
                if self.closed == 0:
                    self.sprite = self.spritesheet.getLargeSprite(8*TILEWIDTH,0*TILEHEIGHT,0)
                elif self.closed == 1 or self.closed == 3:
                    self.sprite = self.spritesheet.getLargeSprite(0*TILEWIDTH,0,0)
                else:
                    self.sprite = self.spritesheet.getLargeSprite(0*TILEWIDTH,2*TILEHEIGHT,0)
                if self.mayPass == 1:
                    self.position = self.position.right
                if self.position.left != None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    
                    if self.location != pygame.math.Vector2(self.position.left.position()):
                        self.location += SPEED*self.position.lerp(self.position.left).normalize()
                        self.mayPass = 3
                        self.target = self.position.left
                    else:    
                        self.position = self.position.left
                        self.mayPass = -1

    def checkCollision(self,ghostList):
        for ghost in ghostList:
            if self.rect.colliderect(ghost.rect):
                if self.godMode:
                    if ghost.respawn == False:
                        ghost.obliterate()
                        self.points += 100
                        return False
                for ghost in ghostList:
                    ghost.obliterate()
                self.obliterate()
                self.lives -= 1
                return True

    def obliterate(self):
        pygame.draw.circle(self.screen,(0,0,0),self.rect.center,TILEHEIGHT)
        self.position = self.map.nodeList[STARTNODE]
        self.position.position()
        self.rect = pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.position.position(),(TILEWIDTH,TILEHEIGHT)))
        self.move = -1
        self.location = pygame.math.Vector2(self.position.position())
        self.mayPass = -1
        self.wantMove = -1

    def eat(self, map: PillMap):
        self.pillMap = map
        for pill in self.pillMap.pillList:
            if self.rect.colliderect(pill.rect) and pill.eaten == False:
                self.points += 1
                pill.eaten = True
                if pill.power:
                    self.godMode = True
                    self.godCount = 0
