from AutoPlayer import AutoPlayer
from Pill import PillMap
import pygame
from Tiles import *
from Constants import *
from SpriteSheet import Spritesheet
from Player import Pacman
from Node import *
from Enemy import Ghost
from DikstraGhost import DikstraGhost
from BFSGhost import BFSGhost
from UCSGhost import UCSGhost
from GreedyGhost import GreedyGhost
from AStarGhost import AStarGhost

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

        
        self.pillMap = PillMap(self.window,self.filename)
        self.map = TileMap(self.filename,'maze1_rotation.txt', spritesheet)
        self.pacman = AutoPlayer(self.window,self.filename, spritesheet, self.nodeMap)
        
        '''
        I might have mixed up the colors a little.
        Pinky should be pink, inky is blue, blinky is blinky, clyde is red
        The algorithms correspond to any mistakes I made with the colors 
        '''
        self.pinky = GreedyGhost(self.window,self.filename, self.pacman, spritesheet, PINKY, self.nodeMap)
        self.inky = GreedyGhost(self.window,self.filename, self.pacman, spritesheet, INKY, self.nodeMap)
        self.blinky = GreedyGhost(self.window,self.filename, self.pacman, spritesheet, BLINKY, self.nodeMap)
        self.clyde = GreedyGhost(self.window,self.filename, self.pacman, spritesheet, CLYDE, self.nodeMap)

        self.window.fill(BLACK)
        self.map.drawMap(self.window)
        self.pillMap.drawPills()
        pygame.display.update()
    
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

    def buildPath(self, filename):
        f = open(filename, "r")
        path = [int(x) for x in f.read().split()]
        f.close()
        return path

    def run(self):
        path = self.buildPath(PATHFILE)
        self.waitForInput()
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

            self.pacman.checkNode(path)
            self.pacman.eat(self.pillMap)
            self.pillMap.drawPills()
            self.pacman.display()

            if self.pacman.checkCollision([self.pinky, self.inky, self.blinky, self.clyde]):
                pygame.time.wait(2000)
            
            self.findPath(self.pinky,self.pacman, 0)
            self.findPath(self.inky, self.pacman, 1)
            self.findPath(self.blinky, self.pacman, 3)
            self.findPath(self.clyde, self.pacman, 2)
            
            self.pinky.checkNode()
            self.inky.checkNode()
            self.blinky.checkNode()
            self.clyde.checkNode()

            #do this for all four ghosts
            
            pygame.display.update()
            self.clock.tick(TICK)
            if self.pacman.lives == 0 or self.pillMap.noPills() or not path:
                self.running = False

        self.endGame(self.window)
        pygame.quit()
        exit()
