from simulator import *
from algos.heuristics import *
import algos.iterativeAstar as a
import algos.recursiveBestFirstAstar as ra
import time
import tools.plot as plt
import tools.goalAssigner as assign

def testF(possible_commandsF):
    print(possible_commandsF())

#sim = Simulator.from_file("gamestates/reversestack")  #min parameters(w,l,h)
sim = Simulator.from_file("gamestates/draper/state1") #(?,?,?)
#sim = Simulator.from_file("gamestates/draper/state2") #(101,101,3)
#sim = Simulator.from_file("gamestates/draper/state3") #(11,11,18)

#plt.plot(sim)

#case 1
#goal = (3,3,0,'red')

#case 2
#goal = (3,3,2,'red')

#case 3
#goal = (5,3,4,'red')


goals1 = [(0,1,0,'black'),(0,1,15,'red')]
goals2 = [(0,0,1,'black'),(0,0,0,'red')]

goals3 = [('?', '?', 0, '?'), ('?', '?', 1, '?'), ('?', '?', 2, '?'), ('?', '?', 3, '?'), ('?', '?', 4, '?'), ('?', '?', 5, '?'), ('?', '?', 6, '?'), ('?', '?', 7, '?'), ('?', '?', 8, '?'), ('?', '?', 9, '?'), ('?', '?', 10, '?'), ('?', '?', 11, '?'), ('?', '?', 12, '?'), ('?', '?', 13, '?'), ('?', '?', 14, '?'), ('?', '?', 15, '?'), ('?', '?', 16, '?'), ]

start_time = time.time()

block_goals = assign.assignGoals(sim, goals1)
#block_goals = assign.assignGoals(sim, goals2)
#block_goals = assign.assignGoals(sim, goals3)
res = where_does_my_block_want_to_move(sim, block_goals)

print()
print("Time elapsed", time.time() - start_time)
