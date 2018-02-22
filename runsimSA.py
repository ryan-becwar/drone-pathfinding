from simulator import *
from algos.heuristics import costHeuristicFunc
import algos.simulatedAnnealing as sa
import time as time


def testF(possible_commandsF):
    print(possible_commandsF())

for i in range(20):

    sim = Simulator.from_file("gamestates/simple")

    goal = (3,3,0,'red')
    before=time.time()
    result = sa.simulatedAnneal(sim, costHeuristicFunc, goal)
    after=time.time()
    print('simple SA {} actions taken in {} seconds'.format(len(result[1]), after-before))

for i in range(20):
    sim = Simulator.from_file("gamestates/simple")

    goal = (3,3,0,'red')
    before=time.time()
    result = sa.simulatedMoreAnnealAtSameT(sim, costHeuristicFunc, goal)
    after=time.time()
    print(' more anneal at same T  SA {} actions taken in {} seconds'.format(len(result[1]), after-before))

