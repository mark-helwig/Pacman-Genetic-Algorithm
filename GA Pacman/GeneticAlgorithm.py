'''
Elitist Genetic Algorithm for Pacman
'''

import time
import numpy as np
from AnnealPills import *
from Constants import *
import random
from Simulation import Simulation

class Chromosome:
    def __init__(self, path) -> None:
        self.path = path
        self.points = 0
        self.time = -1


class GA:

    def __init__(self):
        self.filename = 'maze1.txt'
        self.nodeMap = NodeMap(self.filename)
        self.pillMap = GAPillMap(self.nodeMap, self.filename)
        self.chromosomes = []
        random.seed(RANDOMSEED)

    #initial population
    def fillList(self):
        for i in range(POPULATION):
            self.chromosomes.append(Chromosome(self.randomGeneratePath()))

    #generate list of directions
    def randomGeneratePath(self):
        newPath = []
        newPath.append(3)
        for i in self.nodeMap.nodeList:
            for j in range(int(STATEMULTIPLE)):
                newPath.append(random.randint(0,3))
        return newPath

    #simulate each path and assign results
    def evaluateFitness(self):
        #print("evaluation initiated.")
        for chromosome in self.chromosomes:
            evaluation = Simulation()
            chromosome.points, chromosome.time = evaluation.simulate(chromosome.path.copy())
        #print("evaluation complete.")

    #sort chromosomes by points
    def sort(self):
        self.chromosomes.sort(key=self.key,reverse=True)

    def key(self, chromosome):
        return chromosome.points

    #perform crosses for "reproduction" based on constants (SPLITNUMBER)
    def crossParents(self):
        #print("crossing parents")
        newPopulation = []
        newPopulation.append(self.chromosomes[0])
        for i in range(len(self.chromosomes)):
            if i % 2 == 1:
                new1 = []
                new2 = []
                x = self.chromosomes[i].path
                y = self.chromosomes[i+1].path
                newX = self.listSplit(x)
                newY = self.listSplit(y)

                for i in range(len(newX)):
                    if i % 2 == 1:
                        new1.append(newX[i])
                        new2.append(newY[i])
                    else:
                        new1.append(newY[i])
                        new2.append(newX[i])

                new1flat = [item for sublist in new1 for item in sublist]
                new2flat = [item for sublist in new2 for item in sublist]
                newPopulation.append(Chromosome(new1flat))
                newPopulation.append(Chromosome(new2flat))
        self.chromosomes = newPopulation

    #partition list according to constants
    def listSplit(self, lst):
        chunked_list = [list(array) for array in np.array_split(np.array(lst), SPLITNUMBER)]
        return chunked_list

    #GA function
    def run(self):
        start = time.time()

        self.fillList()
        for i in range(GENERATIONS):
            self.evaluateFitness()
            self.sort()
            self.crossParents()
        self.evaluateFitness()
        self.sort()
        self.determineBestPath()
        end = time.time()
        print("Time elapsed: " + str((end - start)))
        
    def determineBestPath(self):
        print("Best path: " + str(self.chromosomes[0].path))
        print("Best score: " + str(self.chromosomes[0].points))
        f = open(PATHFILE, "w")
        for i in self.chromosomes[0].path:
            f.write(str(i) + " ")
        f.close()
        return self.chromosomes[0].path
