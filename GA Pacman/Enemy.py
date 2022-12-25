from random import randint
from Node import *
from Constants import *
from Vector import Vector2

class Ghost:
    def __init__(self,pacman, ghostColor, nodeMap: NodeMap) -> None:
        self.map = nodeMap
        self.ghostColor = ghostColor
        self.position = self.map.nodeList[GHOSTSTART]
        self.position.position()
        self.condition = True
        self.direction = False
        self.move = -1
        self.location = Vector2(self.position.position())
        self.mayPass = -1
        self.pacman = pacman
        self.speed = GHOSTSPEED
        self.respawn = False
        self.last = self.position
           
    def moveSet(self):
        return randint(0,3)
        


    def obliterate(self):
        self.position = self.map.nodeList[GHOSTSTART]
        self.location = Vector2(self.position.position())
        self.respawn = True
        self.move = -1
        self.mayPass = -1
        

                
