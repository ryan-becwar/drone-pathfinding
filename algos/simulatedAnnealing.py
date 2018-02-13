import random as random
import numpy as np

def pickRandomAction(actions):
    return random.choice(actions)

def simulatedAnneal(startState, possibleActionsF, stateFromActionAppliedF, heuristicF, goalTestF, TdecayFactor=0.99):
    
    result =[]
    currentState = startState  
    currentStateCost = heuristicF(currentState)
    T = 1.0
    
    nodesExplored = 0
    while true: 
        result.append(currentState)
        if goalTestF(currentState):
            return (result, nodesExplored)
        possibleActions = possibleActionsF(currentState)
        action = pickRandomAction(possibleActions)
        
        nextState = stateFromActionAppliedF(currentState, action)            
        nextStateCost = heuristicF(nextState)
        dE = nextStateCost - currentStateCost
        
        probabilityOfAcceptingRandomAction = np.exp(-dE/T)
        
        if dE < 0 or probabilityOfAcceptingRandomAction > random():
            nodesExplored = nodesExplored + 1
            currentState = newState
            currentStatecost = newStateCost

        T = T*TdecayFactor
    
