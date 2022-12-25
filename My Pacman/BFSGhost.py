import math
from queue import Queue
from tracemalloc import start
import numpy as np
from Node import Node
from Enemy import Ghost
from SpriteSheet import Spritesheet

class BFSGhost(Ghost):
    def __init__(self,screen,filename,pacman,spritesheet: Spritesheet, ghostColor,nodeMap):
        Ghost.__init__(self,screen,filename,pacman,spritesheet, ghostColor)
        self.nodeMap = nodeMap
        self.createDict()

    #creates the graph for BFS function
    def createDict(self):
        nodeList = self.nodeMap.nodeList
        self.verticeCount = len(nodeList)
        self.dict = {}
        for node in nodeList:
        
            if nodeList.index(node) not in self.dict:
                    self.dict[nodeList.index(node)] = []

            if node.up is not None:
                self.dict[nodeList.index(node)].append(nodeList.index(node.up))
            if node.right is not None:
                self.dict[nodeList.index(node)].append(nodeList.index(node.right))
            if node.down is not None:
                self.dict[nodeList.index(node)].append(nodeList.index(node.down))
            if node.left is not None:
                self.dict[nodeList.index(node)].append(nodeList.index(node.left))

    #standard BFS algorithm
    def findPath(self, startNode: int, destination: int) :
        explored = []
        queue = [[startNode]]
        path = []

        if startNode == destination:
            return startNode

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node not in explored:
                neighbors = self.dict[node]
                for neighbor in neighbors:
                    path2 = list(path)
                    path2.append(neighbor)
                    queue.append(path2)

                    if neighbor == destination:
                        self.path = path2
                        return path2

                explored.append(node)
        return

    #converts BFS output into moves for the Ghost
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


    
            
        
     
