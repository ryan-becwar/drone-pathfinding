from hpdwsimulator import *
from hpdwastar import *
from hpdwheuristics import *
from copy import *
from hla import *
import time as time

state1=HPDWSimulator(Xrange=(0,10), Zrange=(0,10), Yrange=(0,20), filename='test1initial.txt', loglevel='silent')
print(state1)
goal1=HPDWSimulator(Xrange=(0,10), Zrange=(0,10), Yrange=(0,20), filename='test1goal.txt', loglevel='silent')
goal1.fillWCInY()
print(goal1)
before=time.time()
result = blkMovesSearch(state1, moveBlocksHLACost, goal1)
after=time.time()
print("Time Taken ", after-before)
print(len(result[0]))
print(result[0])

state2=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,5), filename='test2initial.txt', loglevel='silent')
print(state2)
goal2=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,5), filename='test2goal.txt', loglevel='silent')
goal2.fillWCInY()
print(goal2)
before=time.time()
result = blkMovesSearch(state2, moveBlocksHLACost, goal2)
after=time.time()
print("Time Taken ", after-before)
print(len(result[0]))
print(result[0])

state3=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,20), filename='test3initial.txt', loglevel='silent')
print(state3)
goal3=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,20), filename='test3goal.txt', loglevel='silent')
goal3.fillWCInY()
print(goal3)
before=time.time()
result = blkMovesSearch(state3, moveBlocksHLACost, goal3)
after=time.time()
print("Time Taken ", after-before)
print(len(result[0]))
print(result[0])

#### Drone moves
destTowerXZ = (0,0)
destTowerHt = sum(1 for item in state1.stateMap[destTowerXZ] if item != '')
droneDest = (destTowerXZ[0], destTowerXZ[1], destTowerHt)
HLA_move_goal_1_1 = state1.moveDroneImmutable((droneDest))
HLA_move_goal_1_1

result = dronePathSearch(state1, moveDroneCost, HLA_move_goal_1_1)

print("Path Length=", len(result[0])-1)
print()
for state in result[0]:
    print(state)