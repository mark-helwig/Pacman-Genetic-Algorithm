from Constants import *
import pygame

class Pill(object):
    def __init__(self,screen: pygame.Surface,x: int,y: int):
        """
        param direction: True for horizontal, False for Vertical
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.power = False
        self.rect = pygame.draw.rect(self.screen,YELLOW,pygame.Rect(x,y,TILEWIDTH,TILEHEIGHT))
        self.eaten = False

    def position(self):
        return self.x,self.y

    def draw(self):
        if self.eaten:
            if self.power:
                pygame.draw.circle(self.screen,BLACK,self.rect.center,TILEHEIGHT/2)
            else:    
                pygame.draw.circle(self.screen,BLACK,self.rect.center,TILEHEIGHT/4)
        else:
            if self.power:
                pygame.draw.circle(self.screen,PILLYELLOW,self.rect.center,TILEHEIGHT/2)
            else:
                pygame.draw.circle(self.screen,PILLYELLOW,self.rect.center,TILEHEIGHT/4)

class PillMap():
    def __init__(self,screen,filename):
        self.pillList = []
        self.powerPills = []
        self.screen = screen
        self.loadPills(filename)

    def drawPills(self):
        for pill in self.pillList:
            pill.draw()

    def readPills(self,filename):
        map = []
        with open(filename,'r') as data:
            for row in data.readlines():
                map.append(list(row))
        return map
    
    def noPills(self):
        for pill in self.pillList:
            if pill.eaten:
                condition = True
            else:
                condition = False
                return condition
        return condition

    def loadPills(self,filename):
        map = self.readPills(filename)
        x,y = 0,0
        checkList = ['+','.','p','P',]
        for i in range(len(map)):
            x = 0
            for u in range(len(map[i])):
                currentPos = map[i][u]
                if checkList.__contains__(currentPos):
                    currentPill = Pill(self.screen,x*TILEWIDTH/2,y*TILEHEIGHT)
                    self.pillList.append(currentPill)
                if currentPos == 'P' or currentPos == 'p':
                    currentPill.power = True
                x += 1
            y += 1
            

