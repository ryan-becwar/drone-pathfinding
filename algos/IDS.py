def depthLimitedSearch(startState, goalState, possibleActionsF, resultingStateFromActionF, depthLimit):
    if startState == goalState:
        return []
    if depthLimit is 0:
        return 'cutoff' # signal that the depth limit was reached
    cutoffOccurred = False
    for action in possibleActionsF(startState):
        childState, _ = resultingStateFromActionF(startState, action)
        result = depthLimitedSearch(childState, goalState, possibleActionsF, resultingStateFromActionF, depthLimit-1)
        if result is 'cutoff':
            cutoffOccurred = True
        elif result is not 'failure':
            # Add childState to front of partial solution path, in result, returned by depthLimitedSearch
            result= [childState] + result
            return result
        
    if cutoffOccurred:
        return 'cutoff'
    else:
        return 'failure'

def iterativeDeepeningSearch(startState, goalState, possibleActionsF, resultingStateFromActionF, maxDepth):
    for depth in range(maxDepth):
        result = depthLimitedSearch(startState, goalState, possibleActionsF, resultingStateFromActionF, depth)
        if result is 'failure':
            return 'failure'
        elif result is not 'cutoff':  
            #Add startState to front of solution path, in result, returned by depthLimitedSearch  
            result = [startState] + result    
            return result
    return 'cutoff'
