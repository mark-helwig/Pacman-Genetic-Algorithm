'''
Please use the Simulate.py file to run the code below.

In the case of the pacman's travel, the solution reached is almost certainly a
local minima and not the best path.
'''

from itertools import permutations
import math
from random import *
from random import choices
from AutoPlayer import AutoPlayer
from Pill import PillMap
import pygame
from Tiles import *
from Constants import *
from SpriteSheet import Spritesheet
from Node import *
from Enemy import Ghost
from AnnealPills import AnnealPillMap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.Surface(SCREENSIZE)
        self.window = pygame.display.set_mode((SCREENSIZE))
        self.running = True
        self.clock = pygame.time.Clock()

        spritesheet = Spritesheet('spritesheet.png')
        self.filename = 'maze1.txt'
        self.nodeMap = NodeMap(self.filename)

        
        self.pillMap = AnnealPillMap(self.window,self.filename,self.nodeMap)
        self.map = TileMap(self.filename,'maze1_rotation.txt', spritesheet)
        self.pacman = AutoPlayer(self.window,self.filename, spritesheet, self.nodeMap)

        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()

    def findPillPath(self, start, end):
        start = self.nodeMap.nodeList.index(self.pillMap.pillList[start].node)
        end = self.nodeMap.nodeList.index(self.pillMap.pillList[end].node)
        cost = self.pacman.findPath(start,end)[1]
        return cost

    def defineStateSpace(self):
        dict = {}
        lst = []
        for i in range(ANNEALCOUNT):
            for u in range(ANNEALCOUNT):
                cost = self.findPillPath(i,u)
                dict[(i,u)] = cost
            lst.append(i)
        lst = list(permutations(lst))

        graph = {}
        for i in range(len(lst)):
            totalcost = 0
            for u in range(len(lst[i])-1):
                 totalcost += dict[(lst[i][u],lst[i][u+1])]
            graph[lst[i]] = totalcost
        return graph,lst

    #Handles the annealing
    def annealingLoop(self, dict, lst):
        startPos = randint(0,len(dict) -1)
        current = (dict[lst[startPos]],startPos)
        condition = True
        i = 0
        while condition:
            probability = math.pow(math.e,i/(ANNEALRATE*len(dict)))
            try:
                neighborLeft = (dict[lst[current[1] - 1]], current - 1)
            except:
                neighborLeft = current
            try:
                neighborRight = (dict[lst[current[1] + 1]], current + 1)
            except:
                neighborRight = current
            
            
            if i == len(dict) and neighborLeft[0] >= current[0] and neighborRight[0] >= current[0]:
                condition = False
            if neighborLeft[0] < current[0] and neighborRight[0] < current[0]:
                current = choices([neighborLeft,neighborRight],weights=[.5,.5])[0]
            elif neighborLeft[0] >= current[0] and neighborRight[0] >= current[0]:
                current = choices([neighborLeft,neighborRight],weights=[.5,.5])[0]
            elif neighborLeft[0] < current[0]:
                current = choices([neighborLeft,neighborRight],weights=[1 - probability,probability])[0]
            elif neighborRight[0] < current[0]:
                current = choices([neighborRight,neighborLeft],weights=[1 - probability,probability])[0]
            if i < len(dict):
                i +=1
        return lst[current[1]]

    #builds final path from results of annealing 
    def buildPath(self, pathList):
        finalList = []
        nodeList = self.nodeMap.nodeList
        finalList.append(self.pacman.findPath(nodeList.index(self.pacman.position), nodeList.index(self.pillMap.pillList[pathList[0]].node))[0])

        for i in range(len(pathList) -1):
            finalList.append(self.pacman.findPath(nodeList.index(self.pillMap.pillList[pathList[i]].node), nodeList.index(self.pillMap.pillList[pathList[i+1]].node))[0])
        
        finalFlatList = self.flatten_list(finalList)
        return finalFlatList

    def flatten_list(self, _2d_list):
        flatList = []
        for element in _2d_list:
            del element[0]
        for element in _2d_list:
            if type(element) is list:
                # If the element is of type list, iterate through the sublist
                for item in element:
                    flatList.append(item)
            else:
                flatList.append(element)
        return flatList

    def findPath(self,ghost: Ghost, pacman, case):
        match case:
            case 0:
                ghostPos = ghost.map.nodeList.index(ghost.position)
                pacPos = pacman.map.nodeList.index(pacman.target)
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

    def waitForInput(self):
        waiting = True
        myFont = pygame.font.Font('joystix.ttf',15)
        waitMsg = myFont.render("Press Space to start the game.",1,WHITE)
        while waiting:
            self.window.blit(waitMsg,WAITDISPLAY)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def waitForInputAnneal(self):
        waiting = True
        myFont = pygame.font.Font('joystix.ttf',15)
        annealMsg = myFont.render("Simulated annealing is finished.",1,WHITE)  
        waitMsg = myFont.render("Press Space to start the game.",1,WHITE)
        while waiting:
            self.window.blit(annealMsg, ANNEALDISPLAY)
            self.window.blit(waitMsg,WAITDISPLAY)   
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False

    def pause(self):
        waiting = True
        myFont = pygame.font.Font('joystix.ttf',15)
        waitMsg = myFont.render("Press Space to resume the game.",1,WHITE)
        while waiting:
            self.window.blit(waitMsg,WAITDISPLAY)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
        
        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()

    def endGame(self,screen):
        myFont = pygame.font.Font('joystix.ttf',40)
        waitMsg = myFont.render("GAME OVER",1,WHITE)
        screen.blit(waitMsg,ENDDISPLAY)
        pygame.display.update()
        pygame.time.wait(2000)

    def simulate(self):
        self.waitForInput()
        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()

        myFont = pygame.font.Font('joystix.ttf',15)
        annealMsg = myFont.render("Simulated annealing is running.",1,WHITE)  
        waitMsg = myFont.render("Please wait around 30 seconds.",1,WHITE) 
        self.window.blit(annealMsg, ANNEALDISPLAY)
        self.window.blit(waitMsg,WAITDISPLAY)   
        pygame.display.update()

        graph,lst = self.defineStateSpace()
        sequences = self.annealingLoop(graph,lst)
        path = self.buildPath(sequences)

        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()

        self.waitForInputAnneal()

        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()

        while self.running:
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    if event.key == pygame.K_SPACE:
                        self.pause()
            #if self.nodeMap.fullNodeAt(self.pacman.location.x,self.pacman.location.y) is not None:
            #    path = self.pacman.autoMove(path)

            self.pacman.checkNode(path)
            self.pacman.eat(self.pillMap)
            self.pillMap.drawPills()
            #self.pacman.display()

            pygame.display.update()
            self.clock.tick(TICK)
            if self.pacman.lives == 0 or self.pillMap.noPills():
                self.running = False

        self.endGame(self.window)
        pygame.quit()
        exit()
