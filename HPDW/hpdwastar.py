import operator
from hla import *
from hpdwsimulator import *

class Node:
    def __init__(self, state, f=0, g=0 ,h=0, creatorAction=None):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
        self.creatorAction = creatorAction
    def __repr__(self):
        return "Node(" + repr(self.state) + "\ncreatedBy=" + repr(self.creatorAction) + "\nf=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

class Stats:
    def __init__(self, attempts):
        self.attempts = attempts
        
def dronePathSearch(startState, hF, goal, maxAttempts=1000, doMaxF = False):
    h = hF(goal, startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    stats = Stats(attempts=maxAttempts)
    return dronePathSearchHelper(startNode, hF, goal, float('inf'), doMaxF, stats)

def dronePathSearchHelper(parentNode, hF, goal, fmax, doMaxF, stats):
#     print("Attempts left ", stats.attempts)
    stats.attempts = stats.attempts - 1 
    if stats.attempts == -1:
        return ("failure", float('inf'))
#     print("Current state \n", parentNode.state)
    
    if parentNode.state.dronePos == goal.dronePos: 
        return ([parentNode], parentNode.g) # no actions needed as we are desired drone pos now
    
    ## Construct list of children nodes with f, g, and h values
    
    actions = parentNode.state.possibleDroneMoves()
#     print("Possible actions ", actions)
    
    if not actions or len(actions)==0:
        return ("failure", float('inf'))
    children = []
    
    for action in actions:
        (actionStatus, stepCost, childState) = parentNode.state.takeActionImmutable(action)
        # calulate heuristics for child if actionStatus is success
        
        if actionStatus is True:            
            h = hF(goal, childState)            
            g = parentNode.g + stepCost
            if doMaxF:
                f = max(h+g, parentNode.f)
            else:
                f = h+g
            childNode = Node(state=childState, f=f, g=g, h=h, creatorAction=action)           
            children.append(childNode)
        else:
            print("Failed to take action ", action)
    
    while stats.attempts > 0 :
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
#         print("Sorted children \n")
#         for child in children:
#             print("(created by={}, f={}, g={}, h={})".format(child.creatorAction, child.f, child.g, child.h))            
        
        bestChild = children[0]
        if bestChild.f > fmax or bestChild.f == float('inf'):
#             print ("bestChild.f={} > fmax={}".format(bestChild.f, fmax))
            return ("failure", bestChild.f)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result, bestChild.f = dronePathSearchHelper(bestChild, hF, goal, min(fmax,alternativef), doMaxF, stats)
        if result is not "failure":               
            result.insert(0, parentNode)     
            return (result, bestChild.f)      
    return ("failure", float('inf'))

def getPossibleTowers(currentState, goalState):    
    possibleTowers = []
    goalCopy = deepcopy(goalState)
    goalCopy.fillWC()
    for goalxz, goaltower in goalState.stateMap.items():
        if goalxz == ('?', '?'):
            # find best destination
            towersWithBlock = deepcopy(currentState.towersWithBlks())
            towersWithBlock.sort(key = lambda n: currentState.numBlksAt(n[0])) # sort
            possibleTowers.append((towersWithBlock[::-1][0][0], goalCopy.stateMap[towersWithBlock[::-1][0][0]]))
        else:
            possibleTowers.append((goalxz, goaltower))
    return possibleTowers

def getPossibleBlkMoves1(currentState, goalState): 
    hlas = []
    for xz, xzTower in currentState.stateMap.items():
        xzBlkCnt = sum(1 for item in xzTower if item != '' and item !='d')
        if (xzBlkCnt > 0 ):
            for destxz in currentState.getPossibleXZs():
                if destxz != xz:
                    hla = MoveBlk(startState=currentState, srcxz=xz, destxz=destxz)
                    hlas.append(hla)    
    return hlas

def getPossibleBlkMoves(currentState, goalState): 
    hlas = []
    for xz, xzTower in currentState.stateMap.items():
        xzBlkCnt = sum(1 for item in xzTower if item != '' and item !='d')
        if (xzBlkCnt > 0 ):
            for destxz, desttower in goalState.stateMap.items():
                if destxz != xz:
                    hla = MoveBlk(startState=currentState, srcxz=xz, destxz=destxz)
                    hlas.append(hla)    
    return hlas

def getPossibleBlkMovesFromPossibleTowers(currentState, goalState): 
    hlas = []
    for xz, xzTower in currentState.stateMap.items():
        xzBlkCnt = sum(1 for item in xzTower if item != '' and item !='d')
        if (xzBlkCnt > 0 ):
            for (destxz, desttower) in getPossibleTowers(currentState, goalState) :
                if destxz != xz:
                    hla = MoveBlk(startState=currentState, srcxz=xz, destxz=destxz)
                    hlas.append(hla)    
    return hlas

def blkMovesSearch(startState, hF, goalState, maxAttempts=1000, doMaxF = False):
    goal=goalState.fillWCWithPossibleTowers(getPossibleTowers(startState, goalState))
    h = hF(currentState=startState, goalState=goal)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    stats = Stats(attempts=maxAttempts)
    return blkMovesSearchHelper(startNode, hF, goal, float('inf'), doMaxF, stats)

def blkMovesSearchHelper(parentNode, hF, goal, fmax, doMaxF, stats):
    print("Attempts left ", stats.attempts)
    stats.attempts = stats.attempts - 1 
    if stats.attempts == -1:
        return ("failure", float('inf'))
#     print("Current state \n", parentNode.state)
    
    if parentNode.state.isGoal(goal):
        return ([parentNode], parentNode.g) # no actions needed
    ## Construct list of children nodes with f, g, and h values
   
    blkMoveHlas = getPossibleBlkMovesFromPossibleTowers(currentState=parentNode.state, goalState=goal)
#     print("Possible moves \n", blkMoveHlas)
    
    if not blkMoveHlas or len(blkMoveHlas)==0:
        return ("failure", float('inf'))
    children = []    
    for blkMoveHla in blkMoveHlas:
        blkMoveHla.evalPlans()
        childState = blkMoveHla.endState
        stepCost = 0
        # calulate heuristics for child 
        h = hF(currentState=childState, goalState=goal)            
        g = parentNode.g + stepCost
        if doMaxF:
            f = max(h+g, parentNode.f)
        else:
            f = h+g
        childNode = Node(state=childState, f=f, g=g, h=h, creatorAction=blkMoveHla)           
        children.append(childNode)       
    
    while stats.attempts > 0 :
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
#         print ("bestChild.f={} > fmax={}".format(bestChild.f, fmax))
        if bestChild.f > fmax or bestChild.f == float('inf'):
            return ("failure", bestChild.f)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result, bestChild.f = blkMovesSearchHelper(bestChild, hF, goal, min(fmax,alternativef), doMaxF, stats)
        if result is not "failure":               
            result.insert(0, parentNode)     
            return (result, bestChild.f)      
    return ("failure", float('inf'))