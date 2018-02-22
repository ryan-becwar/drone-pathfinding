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

goal = (0,9,0,'red')

start_time = time.time()
#result = a.aStar(sim,goal, costHeuristicFunc)
result = a.aStar(sim,goal, distance_heuristic)

print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result))



start_time = time.time()
#result = a.aStar(sim,goal, costHeuristicFunc)
result = ra.aStarSearch(sim, costHeuristicFunc, goal)

print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result))
