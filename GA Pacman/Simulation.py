from GreedyGhost import GreedyGhost
from Constants import *
from Node import *
from AnnealPills import *
from AutoPlayer import *
from Enemy import Ghost

class Simulation:
    
    def __init__(self):
        self.running = True

        self.filename = 'maze1.txt'
        self.nodeMap = NodeMap(self.filename)

        self.pillMap = GAPillMap(self.nodeMap, self.filename)
        self.pacman = AutoPlayer(self.nodeMap)

        self.pinky = GreedyGhost(self.pacman, PINKY, self.nodeMap)
        self.inky = GreedyGhost(self.pacman, INKY, self.nodeMap)
        self.blinky = GreedyGhost(self.pacman, BLINKY, self.nodeMap)
        self.clyde = GreedyGhost(self.pacman, CLYDE, self.nodeMap)


    def findPath(self,ghost: Ghost, pacman: Pacman, case):
        match case:
            case 0:
                ghostPos = ghost.map.nodeList.index(ghost.position)
                pacPos = pacman.map.nodeList.index(pacman.position)
            case 1:
                ghostPos = ghost.map.nodeList.index(ghost.position)
                if self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y - 2*TILEHEIGHT) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y - 2*TILEHEIGHT)
                elif self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y - TILEHEIGHT) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y - TILEHEIGHT)
                elif self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x + TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + TILEWIDTH,pacman.position.y)
                else:
                    pacPos = pacman.map.nodeList.index(pacman.position)

            case 2:
                ghostPos = ghost.map.nodeList.index(ghost.position)
                if self.nodeMap.fullNodeAt(pacman.position.x + 4*TILEWIDTH,pacman.position.y) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 4*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x + 3*TILEWIDTH,pacman.position.y) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 3*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + 2*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x + TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x + TILEWIDTH,pacman.position.y)
                else:
                    pacPos = pacman.map.nodeList.index(pacman.position)
            case 3:
                ghostPos = ghost.map.nodeList.index(ghost.position)
                if self.nodeMap.fullNodeAt(pacman.position.x - 4*TILEWIDTH,pacman.position.y) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x - 4*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x - 3*TILEWIDTH,pacman.position.y) is not None:
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x - 3*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x - 2*TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x - 2*TILEWIDTH,pacman.position.y)
                elif self.nodeMap.fullNodeAt(pacman.position.x - TILEWIDTH,pacman.position.y):
                    pacPos = self.nodeMap.fullNodeAt(pacman.position.x - TILEWIDTH,pacman.position.y)
                else:
                    pacPos = pacman.map.nodeList.index(pacman.position)
        ghost.findPath(ghostPos,pacPos)

    def buildPath(self, pathList):
        finalList = []
        nodeList = self.nodeMap.nodeList
        finalList.append(self.pacman.findPath(nodeList.index(self.pacman.position), nodeList.index(self.pillMap.pillList[pathList[0]].node))[0])

        for i in range(len(pathList) -1):
            finalList.append(self.pacman.findPath(nodeList.index(self.pillMap.pillList[pathList[i]].node), nodeList.index(self.pillMap.pillList[pathList[i+1]].node))[0])
        
        finalFlatList = self.flatten_list(finalList)
        return finalFlatList

    def simulate(self, path):
        t = 0
        score = 0
        while self.running:
            t+=1
            self.pacman.checkNode(path)
            self.pacman.eat(self.pillMap)


            self.findPath(self.pinky,self.pacman, 0)
            self.findPath(self.inky, self.pacman, 1)
            self.findPath(self.blinky, self.pacman, 3)
            self.findPath(self.clyde, self.pacman, 2)

            self.pinky.checkNode()
            self.inky.checkNode()
            self.blinky.checkNode()
            self.clyde.checkNode()

            self.pacman.checkCollision([self.pinky, self.inky, self.blinky, self.clyde])


            score = self.pacman.points

            if self.pacman.lives == 0 or self.pillMap.noPills() or not path:
                self.running = False
                

        return score, t