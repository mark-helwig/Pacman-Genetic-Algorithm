from AnnealPills import *
from Node import *
from Constants import *

class Pacman:
    def __init__(self, nodeMap: NodeMap) -> None:
        self.map = nodeMap
        self.position = self.map.nodeList[STARTNODE]
        self.position.position()
        self.move = -1
        self.mayPass = -1
        self.wantMove = -1
        self.lives = LIVES
        self.points = 0
        self.godMode = False
        self.godCount = 0
        self.mouth = 0
        self.closed = 0
        
    def display(self):
        self.mouth +=1
        self.checkGod()
        if self.godMode:
            self.godCount+=1

    def checkGod(self):
        if self.godCount == GODTIME:
            self.godMode = False
            self.godCount = 0

    def keyboardMove(self,event):
        move = self.moveConvert(event)
        self.readMovement(move)

    def readMovement(self, move):
        match move:
            case 0:
                if self.position.up is not None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):                    
                    self.move = 0
                if not (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.wantMove = 0
            case 1:
                if self.position.right is not None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.move = 1
                if not (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.wantMove = 1
            case 2:
                if self.position.down is not None and (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.move = 2
                if not (self.mayPass == 0 or self.mayPass == 2 or self.mayPass == -1):
                    self.wantMove = 2
            case 3:
                if self.position.left is not None and (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.move = 3
                if not (self.mayPass == 1 or self.mayPass == 3 or self.mayPass == -1):
                    self.wantMove = 3

    def checkCollision(self,ghostList):
        for ghost in ghostList:
            if self.position.vector == ghost.position.vector:
                if self.godMode:
                    if ghost.respawn == False:
                        ghost.obliterate()
                        self.points += 100
                        return False
                for ghost in ghostList:
                    ghost.obliterate()
                self.obliterate()
                self.lives -= 1
                return True

    def obliterate(self):
        self.position = self.map.nodeList[STARTNODE]
        self.move = -1
        self.mayPass = -1
        self.wantMove = -1

    def eat(self, map: GAPillMap):
        self.pillMap = map
        for pill in self.pillMap.pillList:
            if self.position == pill.node and pill.eaten == False:
                self.points += 1
                pill.eaten = True
                if pill.power:
                    self.godMode = True
                    self.godCount = 0
