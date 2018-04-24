
from hpdwsimulator import *
from itertools import product
import numpy as np

def euclidean(source, dest):
    return (source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2

def manhattan(source, dest):
    return abs(source[0]-dest[0]) + abs(source[1]-dest[1]) + abs(source[2]-dest[2])

def moveCostToDronePos(state, destDronePos):
    source = state.dronePos    
    return euclidean(source, destDronePos)

def moveDroneCost(currentState, goalState):
    source = currentState.dronePos
    dest = goalState.dronePos
    productOfXZDimensions = ( abs(source[0]-dest[0]) ) * ( abs(source[1]-dest[1]) )
    return  (source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2 + \
            (source[0]-dest[0])**2 + (source[1]-dest[1])**2 + \
            (source[0]-dest[0])**2 + (source[2]-dest[2])**2 + \
            (source[1]-dest[1])**2 + (source[2]-dest[2])**2 + \
            euclidean(source, dest)
            
def moveBlocksHLACostDebug(currentState, goalState):
    if currentState.isGoal(goalState):
        return 0
    
    cost = 0
    #Current state has a blank and goal state has a block. 
    #So increment the heuristic value by the number of blocks needed to be moved into a place
    
    for goalxz, goaltower in goalState.stateMap.items():
        if currentState.numBlksAt(goalxz) == 0:
            cost = cost + goalState.numBlksAt(goalxz)
            
    print("After crtieria 1 cost= ", cost)        
    #Current state has a block and goal state has a blank. 
    #So increment the heuristic value by the number of blocks needed to be moved out of a place.

    for currentxz, currenttower in currentState.stateMap.items():
        if currentState.numBlksAt(currentxz) > 0 and goalState.numBlksAt(currentxz) == 0:
            cost = cost + currentState.numBlksAt(currentxz)
            
    print("After crtieria 2 cost= ", cost)
    
    #Both states have a block, but they are not the same. The incorrect block must be moved out 
    #and the correct blocks must be moved in. 
    #Increment the heuristic value by the number of these blocks. 
    
    for goalxz, goaltower in goalState.stateMap.items():
        if currentState.numBlksAtIncludeEmpty(goalxz) > 0:
            currenttower = currentState.towerAt(goalxz)
            currentEmptyCntNeedsFill=0
            currentNonEmptyCntNeedsChange=0
            for goalBlkIdx, goalBlk in enumerate(goaltower):
                if (blksEqual(goalBlk, currenttower[goalBlkIdx]) == False):
                    if currenttower[goalBlkIdx] == '':                        
                        currentEmptyCntNeedsFill = currentEmptyCntNeedsFill + 1
                    else:
                        currentNonEmptyCntNeedsChange = currentNonEmptyCntNeedsChange + 2
            
            cost = cost + currentEmptyCntNeedsFill
            cost = cost + currentNonEmptyCntNeedsChange
            
    print("After crtieria 3 cost= ", cost)   
    
    #Both states have a block, and they are the same. However, the position above it is incorrect. 
    #Increment the heuristic value by the number of incorrect positions above the correct block.
    
#     for goalxz, goaltower in goalState.stateMap.items():
#         currentTowerBlkCnt = currentState.numBlksAtIncludeEmpty(goalxz)
#         goalTowerBlkCnt = goalState.numBlksAt(goalxz)
#         if (currentTowerBlkCnt > 0 and currentTowerBlkCnt >= goalTowerBlkCnt):            
#             currenttower = currentState.towerAt(goalxz)
            
#             firstunequalidx = next( (i for i, currentBlk in enumerate(currenttower[:goalTowerBlkCnt]) \
#                                  if (not blksEqual(currentBlk, goaltower[i])) ), None)
            
#             if firstunequalidx is not None:
#                 cost = cost + (goalTowerBlkCnt - firstunequalidx) 
                
#     print("After crtieria 4 cost= ", cost)
    
    
    # For a given (nonempty) place, find the top-most block. Look for its position in the goal state. 
   
    for currentxz, currenttower in currentState.stateMap.items():
            currentTowerBlkCnt = currentState.numBlksAt(currentxz)
            if currentTowerBlkCnt > 0:
                currentTowerTopBlk = currenttower[currentTowerBlkCnt-1]
                print("currenttower at {} {}".format(currentxz, currenttower))            
                for goalxz, goaltower in goalState.stateMap.items():
                    print("goaltower at {} {}".format(goalxz, goaltower)) 
                    goalTowerBootomBlk = goaltower[0]
                    goalTowerBlkCnt = goalState.numBlksAt(currentxz)
                    if ( goalxz != currentxz ):
                        if blksEqual(goalTowerBootomBlk, currentTowerTopBlk) :
                        #If tower top item goes on the bottom row and the place is currently empty, the block can be moved there, 
                        #so decrement heuristic by one.
                            print("Decrement by 1 as top of currenttower equals bottom of goaltower")
                            cost = cost - 1
                        else: 
                        #else if the top-most block doesn't go on bottom row, but all blocks below it in the goal state are 
                        #currently in their correct place, then the block can be moved there, so decrement heuristic by one.
                            print("currentTowerBlkCnt=", currentTowerBlkCnt)
                            print("goalTowerBlkCnt=", goalTowerBlkCnt)
                            if (currentTowerBlkCnt > 1):
                                s=sum(1 for i, currentTowerBlk in enumerate(currenttower[:currentTowerBlkCnt-1]) \
                                      if (blksEqual(currentTowerBlk, goaltower[i])==False) )
                                if s == 0:
                                    print("Decrement by 1 as all blocks below current tower top equals those in goaltower")
                                    cost = cost - 1
                            
    print("After crtieria 4 cost= ", cost)
    return cost

def moveBlocksHLACost(currentState, goalState):
    if currentState.isGoal(goalState):
        return 0
    
    cost = 0
    #Current state has a blank and goal state has a block. 
    #So increment the heuristic value by the number of blocks needed to be moved into a place
    
    for goalxz, goaltower in goalState.stateMap.items():
        if currentState.numBlksAt(goalxz) == 0:
            cost = cost + goalState.numBlksAt(goalxz)
            
#     print("After crtieria 1 cost= ", cost)        
    #Current state has a block and goal state has a blank. 
    #So increment the heuristic value by the number of blocks needed to be moved out of a place.

    for currentxz, currenttower in currentState.stateMap.items():
        if currentState.numBlksAt(currentxz) > 0 and goalState.numBlksAt(currentxz) == 0:
            cost = cost + currentState.numBlksAt(currentxz)
            
#     print("After crtieria 2 cost= ", cost)
    
    #Both states have a block, but they are not the same. The incorrect block must be moved out 
    #and the correct blocks must be moved in. 
    #Increment the heuristic value by the number of these blocks. 
    
    for goalxz, goaltower in goalState.stateMap.items():
        if currentState.numBlksAtIncludeEmpty(goalxz) > 0:
            currenttower = currentState.towerAt(goalxz)
            currentEmptyCntNeedsFill=0
            currentNonEmptyCntNeedsChange=0
            for goalBlkIdx, goalBlk in enumerate(goaltower):
                if (blksEqual(goalBlk, currenttower[goalBlkIdx]) == False):
                    if currenttower[goalBlkIdx] == '':                        
                        currentEmptyCntNeedsFill = currentEmptyCntNeedsFill + 1
                    else:
                        currentNonEmptyCntNeedsChange = currentNonEmptyCntNeedsChange + 2
            
            cost = cost + currentEmptyCntNeedsFill
            cost = cost + currentNonEmptyCntNeedsChange
            
#     print("After crtieria 3 cost= ", cost)   
    
    #Both states have a block, and they are the same. However, the position above it is incorrect. 
    #Increment the heuristic value by the number of incorrect positions above the correct block.
    
#     for goalxz, goaltower in goalState.stateMap.items():
#         currentTowerBlkCnt = currentState.numBlksAtIncludeEmpty(goalxz)
#         goalTowerBlkCnt = goalState.numBlksAt(goalxz)
#         if (currentTowerBlkCnt > 0 and currentTowerBlkCnt >= goalTowerBlkCnt):            
#             currenttower = currentState.towerAt(goalxz)
            
#             firstunequalidx = next( (i for i, currentBlk in enumerate(currenttower[:goalTowerBlkCnt]) \
#                                  if (not blksEqual(currentBlk, goaltower[i])) ), None)
            
#             if firstunequalidx is not None:
#                 cost = cost + (goalTowerBlkCnt - firstunequalidx) 
                
#     print("After crtieria 4 cost= ", cost)
    
    
    # For a given (nonempty) place, find the top-most block. Look for its position in the goal state. 
   
    for currentxz, currenttower in currentState.stateMap.items():
            currentTowerBlkCnt = currentState.numBlksAt(currentxz)
            if currentTowerBlkCnt > 0:
                currentTowerTopBlk = currenttower[currentTowerBlkCnt-1]
#                 print("currenttower at {} {}".format(currentxz, currenttower))            
                for goalxz, goaltower in goalState.stateMap.items():
#                     print("goaltower at {} {}".format(goalxz, goaltower)) 
                    goalTowerBootomBlk = goaltower[0]
                    goalTowerBlkCnt = goalState.numBlksAt(currentxz)
                    if ( goalxz != currentxz ):
                        if blksEqual(goalTowerBootomBlk, currentTowerTopBlk) :
                        #If tower top item goes on the bottom row and the place is currently empty, the block can be moved there, 
                        #so decrement heuristic by one.
#                             print("Decrement by 1 as top of currenttower equals bottom of goaltower")
                            cost = cost - 1
                        else: 
                        #else if the top-most block doesn't go on bottom row, but all blocks below it in the goal state are 
                        #currently in their correct place, then the block can be moved there, so decrement heuristic by one.
#                             print("currentTowerBlkCnt=", currentTowerBlkCnt)
#                             print("goalTowerBlkCnt=", goalTowerBlkCnt)
                            if (currentTowerBlkCnt > 1):
                                s=sum(1 for i, currentTowerBlk in enumerate(currenttower[:currentTowerBlkCnt-1]) \
                                      if (blksEqual(currentTowerBlk, goaltower[i])==False) )
                                if s == 0:
#                                     print("Decrement by 1 as all blocks below current tower top equals those in goaltower")
                                    cost = cost - 1
                            
#     print("After crtieria 4 cost= ", cost)
    return cost
