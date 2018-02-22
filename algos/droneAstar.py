import os,sys,inspect,heuristics
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
def aStarSearch(startState, goal):
    #h = block_heuristic(goal, startState.currentStateMap)
    h = float('inf')
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    return aStarSearchHelper(startNode, float('inf'), goal)

def aStarSearchHelper(parentNode, fmax, goal):
    astarNodesCnt = 0
    if parentNode.state.goalTest(goal):
        return ([parentNode.state], parentNode.g)
    ## Construct list of children nodes with f, g, and h values
    actions = parentNode.state.possible_block_moves()
    if not actions:
        return ("failure", float('inf'), astarNodesCnt)
    children = []
    for action in actions:
        astartNodesCnt = astarNodesCnt + 1
        (childState,stepCost) = parentNode.state.resultingStateFromAction(action)
        print(action)
        h = heuristics.block_heuristic(goal, childState, action[0], action[1])
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
        result,bestChild.f, _ = aStarSearchHelper(bestChild, min(fmax,alternativef), goal)
        if result is not "failure":               
            result.insert(0,parentNode.state)
            return (result, bestChild.f, astarNodesCnt)
        
        
        
        

print(aStarSearch(Simulator.from_file("../gamestates/pillar"), (3, 3, 0, 'red')))