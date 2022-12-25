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
            self.move = self.moveSet()
        
        match self.move:
            case -1:
                pass
            case 0:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,4*TILEHEIGHT,0)
                
                if self.position.up != None:
                    if self.location != pygame.math.Vector2(self.position.up.position()):
                        self.location += self.speed*self.position.lerp(self.position.up).normalize()
                    else:
                        self.position = self.position.up
            case 1:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,10*TILEHEIGHT,0)
                if self.position.right != None:
                    
                    if self.location != pygame.math.Vector2(self.position.right.position()):
                        self.location += self.speed*self.position.lerp(self.position.right).normalize()
                    else:    
                        self.position = self.position.right
            case 2:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,6*TILEHEIGHT,0)
                
                if self.position.down != None:
                    if self.location != pygame.math.Vector2(self.position.down.position()):
                        self.location += self.speed*self.position.lerp(self.position.down).normalize()
                    else:    
                        self.position = self.position.down
            case 3:
                self.sprite = self.spritesheet.getLargeSprite(self.ghostColor*TILEHEIGHT,8*TILEHEIGHT,0)
                
                if self.position.left != None:
                    
                    if self.location != pygame.math.Vector2(self.position.left.position()):
                        self.location += self.speed*self.position.lerp(self.position.left).normalize()
                    else:    
                        self.position = self.position.left
                        
        self.display()

    def obliterate(self):
        self.screen.blit(self.cover,self.rect.topleft-pygame.math.Vector2(TILEWIDTH/2,TILEHEIGHT/2))
        self.position = self.map.nodeList[GHOSTSTART]
        self.location = pygame.math.Vector2(self.position.position())
        self.rect = pygame.draw.rect(self.screen,(0,0,0),pygame.Rect(self.location,(TILEWIDTH,TILEHEIGHT)))
        self.respawn = True
        self.move = -1
        self.mayPass = -1
        

                
