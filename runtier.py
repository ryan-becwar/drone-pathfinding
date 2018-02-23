from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time

def testF(possible_commandsF):
    print(possible_commandsF())

sim = Simulator.from_file("gamestates/reversestack")
#sim = Simulator.from_file("gamestates/simple")


print(sim.state())
print()

goal = (5,3,4,'red')

start_time = time.time()
result = a.blockaStar(sim,goal, stack_heuristic)

dronePath = []
for i in range(1,len(result)):
    sim, action = result[i]
    xd0, zd0, yd0, _ = action[0]
    xd1, zd1, yd1 = action[1]

    droneResult1 = a.aStar(sim,(xd0, zd0, yd0,'d'), chebyshev_sim)
    droneResult2 = a.aStar(sim,(xd1, zd1, yd1,'d'), chebyshev_sim)
    dronePath.extend(droneResult1)
    dronePath.extend(droneResult2)


print()
print("Time elapsed", time.time() - start_time)
print("Path length: ", len(dronePath))
print()
print("RESULT: ")
for sim in result:
    print(sim[0].currentStateMap)
    print(sim[0].to_list())
    print(sim[1])
    print()


print("\nDRONE RESULT: ")
for sim in dronePath:
    print(sim.currentStateMap)
