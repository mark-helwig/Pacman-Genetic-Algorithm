import pygame
from Constants import *

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.spriteSheet = pygame.image.load(filename).convert_alpha()

    def getSprite(self, x, y,rotation):
        match rotation:
            case 0:
                pass
            case 1:
                rotation = 90
            case 2:
                rotation = 180
            case 3:
                rotation = 270
        sprite = pygame.Surface((TILEWIDTH,TILEHEIGHT))
        sprite.set_colorkey(self.spriteSheet.get_at((0,0)))
        sprite.blit(self.spriteSheet,(0,0),(x,y,TILEWIDTH,TILEHEIGHT))
        sprite = pygame.transform.rotate(sprite,rotation)
        return sprite

    def getLargeSprite(self, x, y,rotation):
        match rotation:
            case 0:
                pass
            case 1:
                rotation = 90
            case 2:
                rotation = 180
            case 3:
                rotation = 270
        sprite = pygame.Surface((TILEWIDTH*2,TILEHEIGHT*2))
        sprite.set_colorkey(self.spriteSheet.get_at((0,0)))
        sprite.blit(self.spriteSheet,(0,0),(x,y,TILEWIDTH*4,TILEHEIGHT*4))
        sprite = pygame.transform.rotate(sprite,rotation)
        return sprite
