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

goal = (0,9,3,'red')

start_time = time.time()
result = a.blockaStar(sim,goal, stack_heuristic)

print()
print("RESULT: ")
for sim in result:
    print(sim.currentStateMap)
    print(sim.to_list())
    print()

print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result))

