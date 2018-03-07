from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time

def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/simple")

print(sim.state())
print()

#case 1
#goal = (3,3,0,'red')

goal = (3,3,1,'red')

start_time = time.time()
#result = a.aStar(sim,goal, costHeuristicFunc)
result = a.aStar(sim,goal, distance_heuristic)

print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result))

for res in result:
    print(res.currentStateMap)



start_time = time.time()
#result = a.aStar(sim,goal, costHeuristicFunc)
#result = ra.aStarSearch(sim, costHeuristicFunc, goal)
result = ra.aStarSearch(sim, distance_heuristic, goal)

print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result[0]))

for res in result[0]:
    print(res.currentStateMap)
