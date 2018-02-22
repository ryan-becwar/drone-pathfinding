import random as random
import numpy as np
from copy import deepcopy

def pickRandomAction(actions):
    return random.choice(actions)


def simulatedAnneal(startState, heuristicF, goal, TdecayFactor=0.90):
    result =[]
    actionsTaken=[]
    currentState = startState
    currentStateCost = heuristicF(goal, currentState.currentStateMap, currentState.drone_pos)
    T = 1.00000

    nodesExplored = 0
    while True:
        result.append(currentState)
        if currentState.goalTest(goal):
            return (result, nodesExplored)
        possibleActions = currentState.possibleActions()
        action = pickRandomAction(possibleActions)
        actionsTaken.append(action)

        nextState = currentState.resultingStateFromAction(action)[0]

        if nextState.goalTest(goal):
            result.append(nextState)
            return (result, actionsTaken, nodesExplored)

        nextStateCost = heuristicF(goal, nextState.currentStateMap, nextState.drone_pos)
        dE = round(nextStateCost - currentStateCost, 5)


        if T <=0:
            print('T is <=0')
            probabilityOfAcceptingRandomAction=np.longdouble(1.0)
        else:
            qt = -dE/T
            probabilityOfAcceptingRandomAction = np.longdouble(np.exp(round(qt, 5)))
            #   print('dE={}, T={}, rounded -dE/T={}'.format(dE, T, round(-dE/T, 5)))

        if dE <= 0 or probabilityOfAcceptingRandomAction > np.longdouble(random.random()):
            nodesExplored = nodesExplored + 1
            currentState = nextState
            currentStatecost = nextStateCost

        T = round(T*TdecayFactor,5)


def simulatedMoreAnnealAtSameT(startState, heuristicF, goal, TdecayFactor=0.8, numAnnealAtSameT=10):

    result=[]
    actionsTaken=[]
    currentState = startState
    currentStateCost = heuristicF(goal, currentState.currentStateMap, currentState.drone_pos)
    T = 1.00000

    nodesExplored = 0
    while True:
        result.append(currentState)
        if currentState.goalTest(goal):
            return (result, actionsTaken, nodesExplored)

        for  i in range(numAnnealAtSameT):
            
            possibleActions = currentState.possibleActions()
            action = pickRandomAction(possibleActions)
            actionsTaken.append(action)

            nextState = currentState.resultingStateFromAction(action)[0]

            if nextState.goalTest(goal):
                result.append(nextState)
                return (result, actionsTaken, nodesExplored)

            nextStateCost = heuristicF(goal, nextState.currentStateMap, nextState.drone_pos)
            dE = round(nextStateCost - currentStateCost, 5)
           
            if T <=0:
                #print('T is <=0')
                probabilityOfAcceptingRandomAction=np.longdouble(1.0)
            else:
                qt = -dE/T
                probabilityOfAcceptingRandomAction = np.longdouble(np.exp(round(qt,5)))

            if dE <= 0 or probabilityOfAcceptingRandomAction > np.longdouble(random.random()):
                nodesExplored = nodesExplored + 1
                currentState = nextState
                currentStatecost = nextStateCost

        T = round(T*TdecayFactor, 5)
    
