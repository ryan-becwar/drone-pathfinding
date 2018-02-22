from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a


def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/simple")

print(sim.state())
print()

goal = (0,9,0,'red')
#result = a.aStar(sim,goal, costHeuristicFunc)
result = a.aStar(sim,goal, distance_heuristic)

print()
print(result)
print("RESULT ABOVE")

for sim in result:
    print(sim)
    print(sim.currentStateMap)
