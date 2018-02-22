import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from simulator import *
#goal = (3,3,0,'red')


class Node:
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"


#Takes a simulator as an initial state
def aStarSearch(startState, heuristicF, goal):
    h = heuristicF(goal, startState.currentStateMap, startState.drone_pos)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    return aStarSearchHelper(startNode, heuristicF, float('inf'), goal)

def aStarSearchHelper(parentNode, heuristicF, fmax, goal):
    astarNodesCnt = 0
    if parentNode.state.goalTest(goal):
        return ([parentNode.state], parentNode.g, astarNodesCnt)
    ## Construct list of children nodes with f, g, and h values
    actions = parentNode.state.possibleActions()
    if not actions:
        return ("failure", float('inf'), astarNodesCnt)
    children = []
    for action in actions:
        astartNodesCnt = astarNodesCnt + 1
        (childState,stepCost) = parentNode.state.resultingStateFromAction(action)
        h = heuristicF(goal, childState.currentStateMap, childState.drone_pos)
        g = parentNode.g + stepCost
        f = max(h+g, parentNode.f)
        childNode = Node(state=childState, f=f, g=g, h=h)
        children.append(childNode)
    while True:
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
        if bestChild.f > fmax or bestChild.f == float('inf'):
            return ("failure",bestChild.f, astarNodesCnt)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result,bestChild.f, _ = aStarSearchHelper(bestChild, heuristicF, min(fmax,alternativef), goal)
        if result is not "failure":               
            result.insert(0,parentNode.state)     
            return (result, bestChild.f, astarNodesCnt) 
