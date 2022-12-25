from SpriteSheet import Spritesheet
import pygame
from Constants import *

class Tile(pygame.sprite.Sprite):
    def __init__(self,x,y,spritesheet,spriteX,spriteY,rotation):
        self.image = spritesheet.getSprite(spriteX,spriteY,rotation)
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self,filename,rotationfile,spritesheet: Spritesheet):
        self.tileSize = TILEHEIGHT
        self.startX, self.startY = 0,0
        self.spritesheet = spritesheet
        self.tiles = self.loadTiles(filename,rotationfile)
        self.mapSurface = pygame.Surface((self.width,self.height))
        self.mapSurface.set_colorkey(self.spritesheet.spriteSheet.get_at((0,0)))
        self.loadMap()
    
    def drawMap(self,surface: pygame.Surface):
        surface.blit(self.mapSurface,(0,0))

    def loadMap(self):
        for tile in self.tiles:
            tile.draw(self.mapSurface)

    def readFile(self,filename,rotationfile):
        map,rmap = [],[]
        with open(filename,'r') as data:
            for row in data.readlines():
                map.append(list(row))
        with open(rotationfile,'r') as rdata:
            for row in rdata.readlines():
                rmap.append(list(row))
        return map,rmap

    def loadTiles(self,filename,rotationfile):
        tiles = []
        map,rmap = self.readFile(filename,rotationfile)
        x,y = 0,0
        for i in range(len(map)):
            x = 0
            for u in range(len(map[i])):
                rot = rmap[i][u]
                if map[i][u] == 'X':
                    self.startX,self.startY = x * self.tileSize, y * self.tileSize
                elif map[i][u] == ' ':
                    x -= 1
                elif map[i][u] == '0':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,12 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '1':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,13 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '2':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,14 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '3':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,15 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '4':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,16 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '5':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,17 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '6':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,18 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '7':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,19 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '8':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,20 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                elif map[i][u] == '9':
                    tiles.append(Tile(x * self.tileSize, y * self.tileSize, self.spritesheet,21 * TILEWIDTH,0 * TILEHEIGHT,int(rot)))
                    
                x += 1
            y += 1

        self.width, self. height = x * self.tileSize, y * self.tileSize
        return tiles