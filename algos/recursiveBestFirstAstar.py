class Node:
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

def aStarSearch(startState, possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF):
    h = heuristicF(startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    return aStarSearchHelper(startNode, possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF, float('inf'))

def aStarSearchHelper(parentNode, possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF, fmax):
    astarNodesCnt = 0
    if goalTestF(parentNode.state):
        return ([parentNode.state], parentNode.g)
    ## Construct list of children nodes with f, g, and h values
    actions = possibleActionsF(parentNode.state)
    if not actions:
        return ("failure", float('inf'), astarNodesCnt)
    children = []
    for action in actions:
	astartNodesCnt = astarNodesCnt + 1
        (childState,stepCost) = resultingStateFromActionF(parentNode.state, action)
        h = heuristicF(childState)
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
        result,bestChild.f = aStarSearchHelper(bestChild, possibleActionsF, resultingStateFromActionF, goalTestF,
                                            heuristicF, min(fmax,alternativef))
        if result is not "failure":               
            result.insert(0,parentNode.state)     
            return (result, bestChild.f, astarNodesCnt) 
