from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time

def testF(possible_commandsF):
    print(possible_commandsF())

def run():
    #sim = Simulator.from_file("gamestates/reversestack")
    sim = Simulator.from_file("gamestates/simple")


    print(sim.state())
    print(sim.possible_block_moves())
    print()

    #case 1
    #goal = (3,3,0,'red')

    #case 2
    #goal = (3,3,2,'red')

    #case 3
    goal = (3,3,3,'red')

    start_time = time.time()
    result = a.blockaStar(sim,goal, stack_heuristic)
    print(result)

    block_time = time.time()

    dronePath = []
    for i in range(0,len(result)-1):
        sim, action = result[i]
        print(result[i])
        xd0, zd0, yd0, _ = action[0]
        xd1, zd1, yd1 = action[1]

        droneResult1 = a.aStar(sim,(xd0, zd0, yd0+1,'d'), euclidean_sim)
        droneResult2 = a.aStar(sim,(xd1, zd1, yd1+1,'d'), euclidean_sim)
        dronePath.extend(droneResult1)
        dronePath.extend(droneResult2)


    print()
    print("Time elapsed", time.time() - start_time, "block time: ", block_time - start_time)
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

if __name__ == "__main__":
    run()
