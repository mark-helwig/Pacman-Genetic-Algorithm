There are three parts to this pacman:

My Pacman contains both the simulated annealing and the original pacman game
run by Simulate.py and Pacman.py, respectively.

GA Pacman contains the Genetic Algorithm run by GASimulate.py. 
The randomness inside of the GA is currently seeded to produce testable results. 
All seeding and GA knobs can be tuned in the first chunk of the Constants.py (lines 1-8).

Currently the seeding is in place so the algorithm takes little time to run 
because the algorithm has run anywhere from 10 seconds to several hours depending 
on generation and population.

To visualize the path ran by Pacman, use the Visualization folder and run Visualize.py once
the Genetic Algorithm has ran once.