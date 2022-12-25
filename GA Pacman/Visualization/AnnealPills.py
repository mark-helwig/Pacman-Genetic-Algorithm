from Node import *
from Constants import *
from random import randint

class Pill(object):
    def __init__(self, node: Node):
        """
        param direction: True for horizontal, False for Vertical
        """
        self.node = node
        self.x = self.node.x
        self.y = self.node.y
        self.power = False
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


class GAPillMap():
    def __init__(self, nodeMap: NodeMap, filename):
        self.pillList = []
        self.nodeMap = nodeMap
        self.filename = filename
        self.loadPills()

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

    def loadPills(self):
        map = self.readPills(self.filename)
        x,y = 0,0
        checkList = ['+','.','p','P',]
        for i in range(len(map)):
            x = 0
            for u in range(len(map[i])):
                currentPos = map[i][u]
                if checkList.__contains__(currentPos):
                    currentPill = Pill(self.nodeMap.nodeList[self.nodeMap.fullNodeAt(x*TILEWIDTH/2,y*TILEHEIGHT)])
                    self.pillList.append(currentPill)
                if currentPos == 'P' or currentPos == 'p':
                    currentPill.power = True
                x += 1
            y += 1
