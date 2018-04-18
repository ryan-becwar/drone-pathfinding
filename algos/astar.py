import operator
class Node:
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

class ActionCosts:
    def __init__(self, action, f, g, h):
        self.action = action
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "{" + repr(self.action) + ", f=" + repr(self.f) + ", g=" + repr(self.g) + ", h=" + repr(self.h) + "}"

class Stats:
    def __init__(self, attempts):
        self.attempts = attempts
        
def aStarSearchImmutable(startState, hF, goal):
    h = hF(goal, startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    #stats = Stats(attempts=maxAttempts)
    return aStarSearchImmutablehHelper(startNode, hF, goal, float('inf'))

def aStarSearchImmutablehHelper(parentNode, hF, goal, fmax):
    #print("Attempts left ", stats.attempts)
    #stats.attempts = stats.attempts - 1    
    if parentNode.state.isGoal(goal):
        return (parentNode.state, parentNode.g) # no actions needed
    ## Construct list of children nodes with f, g, and h values
    
    actions = parentNode.state.possibleActions()
    #print("Possible actions ", actions)
    if not actions or len(actions)==0:
        return ("failure", float('inf'))
    children = []
    
    for action in actions:
        (actionStatus, stepCost, childState) = parentNode.state.takeActionImmutable(action)
        # calulate heuristics for child if actionStatus is success
        # Note that parentNode.state is new child state due to takeAction
        if actionStatus is True: 
            h = hF(goal, parentNode.state)
            g = parentNode.g + stepCost
            f = max(h+g, parentNode.f)
            childNode = Node(state=childState, f=f, g=g, h=h)           
            children.append(childNode)
        else:
            print("Failed to take action ", action)
    
    while True :
        # find best child
        children.sort(key = lambda n: n.f) # sort by f value
        bestChild = children[0]
        if bestChild.f > fmax or bestChild.f == float('inf'):
            return ("failure", bestChild.f)
        # next lowest f value
        alternativef = children[1].f if len(children) > 1 else float('inf')
        # expand best child, reassign its f value to be returned value
        result, bestChild.f = aStarSearchImmutablehHelper(bestChild, hF, goal, min(fmax,alternativef))
        if result is not "failure":               
            result.insert(0, parentNode.state)     
            return (result, bestChild.f)      
    #return ("failure", float('inf'))                                             


def aStarSearch(startState, hF, goal, maxAttempts=50):    
    h = hF(goal, startState)
    startNode = Node(state=startState, f=0+h, g=0, h=h)
    stats = Stats(attempts=maxAttempts)
    return aStarSearchHelper(startNode, hF, goal, float('inf'))

def aStarSearchHelper(parentNode, hF, goal, fmax):
    #print(parentNode.state)
    #stats.attempts = stats.attempts - 1
    #print("Attempts left ", stats.attempts)
    if parentNode.state.isGoal(goal):
        return ([], parentNode.g) # no actions needed
    ## Construct list of children nodes with f, g, and h values
    #if stats.attempts == 0 :
    #    return ("failure", float('inf'))
    actions = parentNode.state.possibleActions()
    #print("Possible actions ", actions)
    if not actions or len(actions)==0:
        return ("failure", float('inf'))
    children = []
    actionsMap = {}
    for action in actions:
        (actionStatus,stepCost) = parentNode.state.takeAction(action)
        # calulate heuristics for child if actionStatus is success
        # Note that parentNode.state is new child state due to takeAction
        if actionStatus is True: 
            h = hF(goal, parentNode.state)
            g = parentNode.g + stepCost
            f = max(h+g, parentNode.f)
            
            actionsMap[f] = ActionCosts(action=action, f=f, g=g, h=h)
            # flip the state back as this just exploring costs from action resulting children
            parentNode.state.revertAction(action)
        else:
            print("Failed to take action ", action)
    
    while True :
        # find best child i.e. find best cost action from actions map
        sortedActions = sorted(actionsMap.items(), key=operator.itemgetter(0))
        #print(sortedActions)
        bestAction = sortedActions[0][1].action
        fBestAction = sortedActions[0][1].f
        hBestAction = sortedActions[0][1].h
        gBestAction = sortedActions[0][1].g
        #print("Best action f {} fmax {}".format(fBestAction, fmax))
        if fBestAction > fmax or fBestAction == float('inf'):
            return ("failure", fBestAction)
        
        # expand best child, reassign its f value to be returned value
        # first take the best action to get state to transition to best child.
        #print("Taking best action ", bestAction)
        (bestActionStatus, bestActionStepCost) = parentNode.state.takeAction(bestAction)
        #print("Drone Position after action ", parentNode.state.dronePos)
        
        bestChild = Node(state = parentNode.state, f=fBestAction, g=gBestAction, h=hBestAction)
        # next lowest f value        
        alternativef = sortedActions[1][1].f if len(sortedActions) > 1 else float('inf')
        #if len(sortedActions) > 1:
        #    print("Next best action ", sortedActions[1][1].action)
        #print("alternative f for next best action ", alternativef)
        #print("Calling search on best child..", bestChild)
        result, bestChild.f = aStarSearchHelper(bestChild, hF, goal, min(fmax,alternativef))
        
        if result is not "failure":               
            result.insert(0, bestAction) # return actions taken so far by prepending to the list the calling bestAction    
            return (result, bestChild.f)
        else:
            parentNode.state.revertAction(bestAction)
    #return ("failure", float('inf'))                                             


def rbfsAStar(startState, hF, goal):
   
    def RBFS(node, hF, goal, flimit):
        if node.state.isGoal(goal):
            return node, 0   # (The second value is immaterial)
        actions = node.state.possibleActions()
        #print("Possible actions ", actions)
        successorNodes = []
        for action in actions:
            (actionStatus, stepCost, childState) = node.state.takeActionImmutable(action)
            # calulate heuristics for child if actionStatus is success
            # Note that parentNode.state is new child state due to takeAction
            if actionStatus is True: 
                h = hF(goal, node.state)
                g = node.g + stepCost
                f = max(h+g, node.f)
                successorNode = Node(state=childState, f=f, g=g, h=h)           
                successorNodes.append(successorNode)
            else:
                print("Failed to take action ", action)
            
        if len(successorNodes) == 0:
            return None, infinity
        
        while True:
            # Order by lowest f value
            successorNodes.sort(key=lambda x: x.f)
            bestSuccesorNode = successorNodes[0]
            if bestSuccesorNode.f > flimit:
                return None, bestSuccesorNode.f
            if len(successorNodes) > 1:
                alternative = successorNodes[1].f
            else:
                alternative = float('inf')
            result, bestSuccesorNode.f = RBFS(bestSuccesorNode, hF, goal, min(flimit, alternative))
            if result is not None:
                return result, bestSuccesorNode.f

    h = hF(goal, startState)
    node = Node(state=startState, f = 0+h, g = 0, h = h)
    
    result, bestf = RBFS(node, hF, goal, float('inf'))
    return result


## test
#from heuristics import *
#from astar import *
#result = aStarSearchImmutable(simProf, costHeuristicFunc, (0,0,2,'r'))

#result = aStarSearch(simProf, costHeuristicFunc, (0,0,2,'r'))