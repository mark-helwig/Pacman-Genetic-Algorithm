from Pill import PillMap
from Node import *
from Constants import *
from random import randint

class Pill(object):
    def __init__(self,screen: pygame.Surface,node: Node):
        """
        param direction: True for horizontal, False for Vertical
        """
        self.screen = screen
        self.node = node
        self.x = self.node.x
        self.y = self.node.y
        self.power = False
        self.rect = pygame.draw.rect(self.screen,YELLOW,pygame.Rect(self.x,self.y,TILEWIDTH,TILEHEIGHT))
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

class AnnealPillMap(PillMap):
    def __init__(self, screen, filename, nodeMap: NodeMap):
        self.pillList = []
        self.screen = screen
        self.nodeMap = nodeMap
        self.loadPills()

    def loadPills(self):
        for i in range(ANNEALCOUNT):
            random = randint(0,len(self.nodeMap.nodeList)-1)
            currentPill = Pill(self.screen,self.nodeMap.nodeList[random])
            self.pillList.append(currentPill)
