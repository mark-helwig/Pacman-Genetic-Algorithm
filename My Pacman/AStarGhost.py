import math
from operator import index
from queue import PriorityQueue, Queue
from random import randint
from tracemalloc import start

from Constants import *
import numpy as np
from Node import Node
from Enemy import Ghost
from SpriteSheet import Spritesheet

class AStarGhost(Ghost):
    def __init__(self,screen,filename,pacman,spritesheet: Spritesheet, ghostColor,nodeMap):
        Ghost.__init__(self,screen,filename,pacman,spritesheet, ghostColor, nodeMap)
        self.createDict()

    #creates the graph
    def createDict(self):
        nodeList = self.map.nodeList
        self.dict = {}
        for node in nodeList:
        
            pathWeight = TILEHEIGHT
            if nodeList.index(node) not in self.dict:
                    self.dict[nodeList.index(node)] = []

            if node.up is not None:
                self.dict[nodeList.index(node)].append((nodeList.index(node.up),pathWeight))
            if node.right is not None:
                self.dict[nodeList.index(node)].append((nodeList.index(node.right),pathWeight))
            if node.down is not None:
                self.dict[nodeList.index(node)].append((nodeList.index(node.down),pathWeight))
            if node.left is not None:
                self.dict[nodeList.index(node)].append((nodeList.index(node.left),pathWeight))

    #creates a heuristic value for every node on the map
    def createHeuristic(self, goalNode):
        nodeList = self.map.nodeList
        self.heuristic = [0]*len(nodeList)
        for node in range(len(nodeList)):
            self.heuristic[node] = math.sqrt(abs(math.pow(nodeList[goalNode].x - nodeList[node].x,2) + math.pow(nodeList[goalNode].y - nodeList[node].y,2)))

    #special insert for AStar triple
    def insert(self, lst, value):
        if not lst:
            lst.append(value)
            return
        for i in range(len(lst)):
            if value[1] + value[2] <= lst[i][1] + lst[i][2]:
                lst.insert(i,value)
                return
        lst.append(value)

    #A* algorithm
    def findPath(self, startNode: int, destination: int):
        self.createHeuristic(destination)
        queue = []
        queue.append(([startNode],0,self.heuristic[startNode]))
        explored = []
        while queue:
            dataPair = queue[0]
            del queue[0]
            path = dataPair[0]
            current = path[-1]
            if current == destination:
                self.path = path
                return path
            explored.append(current)
            for node in self.dict[current]:
                check = node[0]
                if check not in explored:
                    newPath = list(dataPair[0])
                    newPath.append(node[0])
                    self.insert(queue,(((newPath), dataPair[1] + node[1],self.heuristic[node[0]])))
    
    #converts path found into moves for the Ghost
    def moveSet(self):
        try:
            goalNode = self.map.nodeList[self.path[1]]
        except:
            goalNode = None
        match goalNode:
            case None:
                return -1
            case self.position.up:
                return 0
            case self.position.right:
                return 1
            case self.position.down:
                return 2
            case self.position.left:   
                return 3    
