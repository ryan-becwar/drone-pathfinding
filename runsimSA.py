from simulator import *
from algos.heuristics import costHeuristicFunc
import algos.simulatedAnnealing as sa
import time as time


def testF(possible_commandsF):
    print(possible_commandsF())

numactions=0
times=0
for i in range(20):
    sim = Simulator.from_file("gamestates/simple")

    goal = (3,3,0,'red')
    before=time.time()
    result = sa.simulatedAnneal(sim, costHeuristicFunc, goal)
    after=time.time()
    print('[{}]simple SA {} actions taken in {} seconds'.format(i,len(result[1]), after-before))

    numactions = numactions + len(result[1])
    times = times + after-before
print('Average {} actions taken in average {} seconds with simple SA'.format(numactions/20, times/20))

numactionsMore=0
timesMore=0
for i in range(20):
    sim = Simulator.from_file("gamestates/simple")

    goal = (3,3,0,'red')
    before=time.time()
    result = sa.simulatedMoreAnnealAtSameT(sim, costHeuristicFunc, goal)
    after=time.time()
    print('[{}]SA with more anneal at same T {} actions taken in {} seconds'.format(i,len(result[1]), after-before))

    numactionsMore = numactionsMore + len(result[1])
    timesMore = timesMore + after-before
print('Average {} actions taken in average {} seconds for SA with more anneal at same T'.format(numactionsMore/20, timesMore/20))


