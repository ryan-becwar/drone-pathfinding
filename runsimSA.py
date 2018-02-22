from simulator import *
from algos.heuristics import costHeuristicFunc
import algos.simulatedAnnealing as sa


def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/simple")

print(sim.state())
print()





goal = (3,3,0,'red')
#result = sa.simulatedAnneal(sim, costHeuristicFunc, goal)
result = sa.simulatedMoreAnnealAtSameT(sim, costHeuristicFunc, goal)
print()
print(result[1])
print('{} actions taken'.format(len(result[1])))

#for sim in result[0]:
#    print(sim.to_list())
