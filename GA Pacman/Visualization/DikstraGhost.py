import math
from queue import Queue
from tracemalloc import start
import numpy as np
from Node import Node
from Enemy import Ghost
from SpriteSheet import Spritesheet

class DikstraGhost(Ghost):
    def __init__(self,screen,filename,pacman,spritesheet: Spritesheet, ghostColor,nodeMap):
        Ghost.__init__(self,screen,filename,pacman,spritesheet, ghostColor)
        self.finalString = ""
        self.nodeMap = nodeMap
        self.createMatrix()


    def createMatrix(self):
        nodeList = self.nodeMap.nodeList
        pathWeight = 1
        self.verticeCount = len(nodeList)
        length = self.verticeCount
        self.matrix = [[0 for i in range(length)] for j in range(length)]
        for node in nodeList:
        
            if node.up is not None:
                self.matrix[nodeList.index(node)][nodeList.index(node.up)] = pathWeight
            if node.right is not None:
                self.matrix[nodeList.index(node)][nodeList.index(node.right)] = pathWeight
            if node.down is not None:
                self.matrix[nodeList.index(node)][nodeList.index(node.down)] = pathWeight
            if node.left is not None:
                self.matrix[nodeList.index(node)][nodeList.index(node.left)] = pathWeight

    def findNeighbors(self, shortestDistances, currentNode, toVisit):
        i = 0
        for i in range(self.verticeCount):
            if (self.matrix[currentNode][i] != 0 and shortestDistances[currentNode] + self.matrix[currentNode][i] < shortestDistances[i] ):
                shortestDistances[i] = shortestDistances[currentNode] + self.matrix[currentNode][i]
                toVisit.put(i)

    def findPath(self, startNode: int, destination: int) :
        self.path = []
        self.startNode = self.map.nodeList[startNode]
        self.destination = self.map.nodeList[destination]
        pathArray = np.empty(self.verticeCount)
        toExplore = Queue(1000)
        currentNode = 0
        nodesVisited = "Nodes Visited: " + str(startNode) + ", "
        for i in range(len(pathArray)):
            pathArray[i] = math.inf

        pathArray[startNode] = 0
        currentNode = startNode

        self.findNeighbors(pathArray, currentNode, toExplore)
        while toExplore.empty() is False:
            currentNode = toExplore.get()
            self.findNeighbors(pathArray, currentNode, toExplore)
            nodesVisited = nodesVisited + str(currentNode) + ", "
        
        if pathArray[destination] != math.inf:
            self.pathString(pathArray, destination, startNode)
            return self.path
        
        else:
            return 

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

    def pathString(self, pathArray, destination, start):
        minimumNode = destination

        self.finalString = str(destination) + " -> " + self.finalString;
        self.path.insert(0, destination)
        if destination == start:
            return
        
        for i in range(len(pathArray)):
            if self.matrix[i][destination] != 0 and pathArray[i] + self.matrix[i][destination] <= pathArray[minimumNode] + self.matrix[minimumNode][destination]:
                minimumNode = i
            
        self.pathString(pathArray, minimumNode, start);

    
            
        
     
