from simulator import *
from algos.heuristics import costHeuristicFunc
import algos.recursiveBestFirstAstar as a


def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/simple")

print(sim.state())
print()
#after = resultingStateFromAction(sim.state(), actions[0])
#print(after)

#sim.move(-1,0,0)

#print(sim.state())



#result = a.aStarSearch(sim.state(), possibleActions, resultingStateFromAction, goalTest, costHeuristicFunc)
goal = (3,3,0,'red')
result = a.aStarSearch(sim, costHeuristicFunc, goal)
print()
print(result)

for sim in result[0]:
    print(sim.to_list())
