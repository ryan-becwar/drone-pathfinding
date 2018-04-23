from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time
import tools.plot as plt
import tools.goalAssigner as assign

def testF(possible_commandsF):
    print(possible_commandsF())

#sim = Simulator.from_file("gamestates/reversestack")
sim = Simulator.from_file("gamestates/draper/state1")

plt.plot(sim)

#case 1
#goal = (3,3,0,'red')

#case 2
#goal = (3,3,2,'red')

#case 3
#goal = (5,3,4,'red')

goals = [(0, 1, 0, 'black'), (0, 1, 15, 'red')]


block_goals = assign.assignGoals(sim, goals)
res = where_does_my_block_want_to_move(sim, block_goals)

start_time = time.time()
result = a.blockaStar(sim,goal, stack_heuristic)

dronePath = []
for i in range(0,len(result)-1):
    sim, action = result[i]
    print(result[i])
    xd0, zd0, yd0, _ = action[0]
    xd1, zd1, yd1 = action[1]

    droneResult1 = a.aStar(sim,(xd0, zd0, yd0,'d'), chebyshev_sim)
    droneResult2 = a.aStar(sim,(xd1, zd1, yd1,'d'), chebyshev_sim)
    dronePath.extend(droneResult1)
    dronePath.extend(droneResult2)


print()
print("Time elapsed", time.time() - start_time)
print("Path length: ", len(dronePath) + 2 * (len(result)-1))
print()
print("RESULT: ")
for sim in result:
    print(sim[0].to_list())
    print(sim[1])
    print()


print("\nDRONE RESULT: ")
for sim in dronePath:
    print(sim.to_list())
