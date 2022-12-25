from random import randint
from turtle import speed
from Node import *
import pygame
from SpriteSheet import Spritesheet
from pygame.constants import *
from Constants import *

class Ghost:
    def __init__(self,screen,filename,pacman,spritesheet: Spritesheet, ghostColor, nodeMap: NodeMap) -> None:
        self.map = nodeMap
        self.ghostColor = ghostColor
        self.position = self.map.nodeList[GHOSTSTART]
        self.position.position()
        self.screen = screen
        self.rect = pygame.draw.rect(screen,(0,0,0),pygame.Rect(self.position.position(),(TILEWIDTH,TILEHEIGHT)))
        self.condition = True
        self.direction = False
        self.move = -1
        self.location = pygame.math.Vector2(self.position.position())
        self.mayPass = -1
        self.pacman = pacman
        self.spritesheet = spritesheet
        self.sprite = spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,4*TILEHEIGHT,0)
        self.cover = spritesheet.getLargeSprite(10*TILEWIDTH,4*TILEHEIGHT,0)
        self.speed = GHOSTSPEED
        self.respawn = False
        

    def display(self):
        self.screen.blit(self.cover,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        self.rect = pygame.draw.rect(self.screen,(0,0,0),pygame.Rect((self.location),(TILEWIDTH,TILEHEIGHT)))
        if self.pacman.godMode:
            if self.respawn:
                self.screen.blit(self.sprite,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
            else:
                self.screen.blit(self.spritesheet.getLargeSprite(10*TILEHEIGHT,6*TILEHEIGHT,0),self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        else:
            self.respawn = False
            self.screen.blit(self.sprite,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        
        
    def moveSet(self):
        return randint(0,3)
        
    def checkNode(self):
        if self.location == self.position.vector:
            if self.position.teleport:
                if self.position.right != None:
                    self.position = self.map.nodeList[RIGHTTELE]
                    self.location = pygame.math.Vector2(self.position.position())
                else:
                    self.position = self.map.nodeList[LEFTTELE]
                    self.location = pygame.math.Vector2(self.position.position())
            else:
                self.move = self.moveSet()
        
        match self.move:
            case -1:
                pass
            case 0:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,4*TILEHEIGHT,0)
                if self.mayPass == 2:
                    self.position = self.position.down
                if self.position.up != None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    if self.location != pygame.math.Vector2(self.position.up.position()):
                        self.location += self.speed*self.position.lerp(self.position.up).normalize()
                        self.mayPass = 0
                    else:
                        self.position = self.position.up
                        self.mayPass = -1
            case 1:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,10*TILEHEIGHT,0)
                if self.mayPass == 3:
                    self.position = self.position.left
                if self.position.right != None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    
                    if self.location != pygame.math.Vector2(self.position.right.position()):
                        self.location += self.speed*self.position.lerp(self.position.right).normalize()
                        self.mayPass = 1
                    else:    
                        self.position = self.position.right
                        self.mayPass = -1
            case 2:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,6*TILEHEIGHT,0)
                if self.mayPass == 0:
                    self.position = self.position.up
                if self.position.down != None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    if self.location != pygame.math.Vector2(self.position.down.position()):
                        self.location += self.speed*self.position.lerp(self.position.down).normalize()
                        self.mayPass = 2
                    else:    
                        self.position = self.position.down
                        self.mayPass = -1
            case 3:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,8*TILEHEIGHT,0)
                if self.mayPass == 1:
                    self.position = self.position.right
                if self.position.left != None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    
                    if self.location != pygame.math.Vector2(self.position.left.position()):
                        self.location += self.speed*self.position.lerp(self.position.left).normalize()
                        self.mayPass = 3
                    else:    
                        self.position = self.position.left
                        self.mayPass = -1
                        
        self.display()

    def obliterate(self):
        self.screen.blit(self.cover,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        self.position = self.map.nodeList[GHOSTSTART]
        self.location = pygame.math.Vector2(self.position.position())
        self.rect = pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.location,(TILEWIDTH,TILEHEIGHT)))
        self.respawn = True
        self.move = -1
        self.mayPass = -1
        

                
