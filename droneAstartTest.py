from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time

def testF(possible_commandsF):
    print(possible_commandsF())

#sim = Simulator.from_file("gamestates/reversestack")
sim = Simulator.from_file("gamestates/simple")


print(sim.state())
print()

#case 1
goal = (3,3,0,'red')

droneGoal = (0,0,5,'d')

#case 2
#goal = (3,3,2,'red')

#case 3
#goal = (5,3,4,'red')

start_time = time.time()
#result = a.aStar(sim,droneGoal,chebyshev_sim)
result = a.aStar(sim,droneGoal,euclidean_sim)



print()
print("Time elapsed", time.time() - start_time)
print("Path length: ", len(result) )

print("RESULT: \n")

for res in result:
    print(res.to_list())

