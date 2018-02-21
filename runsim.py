from simulator import *
from algos.heuristics import costHeuristicFunc
import algos.recursiveBestFirstAstar as a


def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/simple")

actions = sim.possible_commands()
print(actions)
print()
after = resultingStateFromAction(sim.state(), actions[0])
print(after)

print()
print(testF(sim.possible_commands))


result = a.aStarSearch(sim.state(), possibleActions, resultingStateFromAction, goalTest, costHeuristicFunc)

print()
print(result)



