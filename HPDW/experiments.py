from hpdwsimulator import *
from hpdwastar import *
from hpdwheuristics import *
from copy import *
from hla import *
import time as time

###################### TC1
print("TEST CASE 1")
state1=HPDWSimulator(Xrange=(0,10), Zrange=(0,10), Yrange=(0,20), filename='test1initial.txt', loglevel='silent')
print(state1)
goal1=HPDWSimulator(Xrange=(0,10), Zrange=(0,10), Yrange=(0,20), filename='test1goal.txt', loglevel='silent')
goal1.fillWCInY()
print(goal1)

before=time.time()
result1 = blkMovesSearch(state1, moveBlocksHLACost, goal1)
after=time.time()
TC1Time1= after-before
print("Time taken to find HLAs", TC1Time1)

TC1Time2=0
totalPrimitiveActionsTC1=0
for node in result1[0][1:]:
    print(node.creatorAction)    
    for action in node.creatorAction.plan:
        print("  ", action)
        if action.name == 'MoveDrone':
            before=time.time()
            pathResult = dronePathSearch(action.startState, moveDroneCost, action.endState)
            after=time.time()
            TC1Time2 += after-before
            for pathNode in pathResult[0][1:]:
                totalPrimitiveActionsTC1 +=1
                print("    ", pathNode.creatorAction)
        else:
            totalPrimitiveActionsTC1 +=1
print("Start state\n", result1[0][0].state)            
print("End state\n", result1[0][::-1][0].state)
print("Total primitive actions taken to reach goal ", totalPrimitiveActionsTC1)
print("Total time taken to find actions ", TC1Time1 + TC1Time2)

##################### TC2
print( "TEST CASE 2")
state2=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,5), filename='test2initial.txt', loglevel='silent')
print(state2)
goal2=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,5), filename='test2goal.txt', loglevel='silent')
goal2.fillWCInY()
print(goal2)

before=time.time()
result2 = blkMovesSearch(state2, moveBlocksHLACost, goal2)
after=time.time()
TC2Time1= after-before
print("Time taken to find HLAs", TC2Time1)

TC2Time2=0
totalPrimitiveActionsTC2=0
for node in result2[0][1:]:
    print(node.creatorAction)    
    for action in node.creatorAction.plan:
        print("  ", action)
        if action.name == 'MoveDrone':
            before=time.time()
            pathResult = dronePathSearch(action.startState, moveDroneCost, action.endState)
            after=time.time()
            TC2Time2 += after-before
            for pathNode in pathResult[0][1:]:
                totalPrimitiveActionsTC2 +=1
                print("    ", pathNode.creatorAction)
        else:
            totalPrimitiveActionsTC2 +=1
print("Start state\n", result2[0][0].state)            
print("End state\n", result2[0][::-1][0].state)
print("Total primitive actions taken to reach goal ", totalPrimitiveActionsTC2)
print("Total time taken to find actions ", TC2Time1 + TC2Time2)

############### TC3

state3=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,20), filename='test3initial.txt', loglevel='silent')
print(state3)
goal3=HPDWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,20), filename='test3goal.txt', loglevel='silent')
goal3.fillWCInY()
print(goal3)

before=time.time()
result3 = blkMovesSearch(state3, moveBlocksHLACost, goal3)
after=time.time()
TC3Time1= after-before
print("Time taken to find HLAs", TC3Time1)

TC3Time2=0
totalPrimitiveActionsTC3=0
for node in result3[0][1:]:
    print(node.creatorAction)    
    for action in node.creatorAction.plan:
        print("  ", action)
        if action.name == 'MoveDrone':
            before=time.time()
            pathResult = dronePathSearch(action.startState, moveDroneCost, action.endState)
            after=time.time()
            TC3Time2 += after-before
            for pathNode in pathResult[0][1:]:
                totalPrimitiveActionsTC3 +=1
                print("    ", pathNode.creatorAction)
        else:
            totalPrimitiveActionsTC3 +=1
print("Start state\n", result3[0][0].state)            
print("End state\n", result3[0][::-1][0].state)
print("Total primitive actions taken to reach goal ", totalPrimitiveActionsTC3)
print("Total time taken to find actions ", TC3Time1 + TC3Time2)