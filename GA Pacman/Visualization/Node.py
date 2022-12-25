from distutils.command.build_scripts import first_line_re
from Constants import *
import pygame

class Node(object):
    def __init__(self,x: int,y: int):
        """
        param direction: True for horizontal, False for Vertical
        """
        self.x = x
        self.y = y
        self.vector = pygame.math.Vector2(x,y)
        self.up = None
        self.right = None
        self.down = None
        self.left = None
        self.teleport = False
        self.parent = None
        

    def setNeighbors(self,list):
        self.up = list[0]
        self.right = list[1]
        self.down = list[2]
        self.left = list[3]
    
    def lerp(self,node):
        vector =  node.vector - self.vector
        return vector

    
    def openDirections(self):
        return [self.allowUp,self.allowRight,self.allowDown,self.allowLeft]
    
    def gridPosition(self):
        return self.x*TILEWIDTH, self.y*TILEHEIGHT

    def position(self):
        return self.x,self.y

class NodeMap():
    def __init__(self,filename):
        self.nodeList = []
        self.loadNodes(filename)
        self.assignNeighbors(filename)

    def readNodes(self,filename):
        map = []
        with open(filename,'r') as data:
            for row in data.readlines():
                map.append(list(row))
        return map

    def loadNodes(self,filename):
        map = self.readNodes(filename)
        checkList = ['p','P','n','+','t']
        x,y = 0,0
        for i in range(len(map)):
            x = 0
            for u in range(len(map[i])):
                currentPos = map[i][u]
                if currentPos == 'X':
                    self.startX,self.startY = x * TILEWIDTH, y * TILEHEIGHT
                elif checkList.__contains__(currentPos):
                    currentNode = Node(x*TILEWIDTH/2,y*TILEHEIGHT)
                    self.nodeList.append(currentNode)
                    if currentPos == 't':
                        currentNode.teleport = True
                else:
                    pass
                x += 1
            y += 1
        NROWS = y
        NCOLS = x

    def nodeAt(self,x,y):
        for node in self.nodeList:
            nodeX,nodeY = node.position()
            if nodeX == x*TILEWIDTH/2 and nodeY == y*TILEHEIGHT:
                return node
    
    def fullNodeAt(self,x,y):
        for node in range(len(self.nodeList)):
            nodeX,nodeY = self.nodeList[node].position()
            if nodeX == x and nodeY == y:
                return node


    def assignNeighbors(self,filename):
        firstCheck = ['.','-',' ','+','p','P','n','+','t']
        checkList = ['.','-',' ']
        nodeList = ['p','P','n','+','t']
        map = self.readNodes(filename)
        for i in range(len(map)):
            for u in range(len(map[i])):
                currentPos = map[i][u]
                if nodeList.__contains__(currentPos):
                    currentNode = self.nodeAt(u,i)
                    if i-1 >= 0 and firstCheck.__contains__(map[i-1][u]):
                        ii = i - 1
                        currentNode.up = self.nodeAt(u,ii)
                    if i+1 < len(map) and firstCheck.__contains__(map[i+1][u]):
                        ii = i + 1
                        currentNode.down = self.nodeAt(u,ii)
                    if u+2 < len(map[i]) and firstCheck.__contains__(map[i][u+2]):
                        uu = u + 2
                        currentNode.right = self.nodeAt(uu,i)
                    if u-2 >= 0 and firstCheck.__contains__(map[i][u-2]):
                        uu = u - 2
                        currentNode.left = self.nodeAt(uu,i)
