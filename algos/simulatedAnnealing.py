import random as random
import numpy as np
from copy import deepcopy

def pickRandomAction(actions):
    return random.choice(actions)


def simulatedAnneal(startState, heuristicF, goal, TdecayFactor=0.99):

    result =[]
    actionsTaken=[]
    currentState = startState
    currentStateCost = heuristicF(goal, currentState.currentStateMap, currentState.drone_pos)
    T = 1.0

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
        dE = nextStateCost - currentStateCost


        probabilityOfAcceptingRandomAction = np.exp(-dE/T)

        if dE < 0 or probabilityOfAcceptingRandomAction > random.random():
            nodesExplored = nodesExplored + 1
            currentState = nextState
            currentStatecost = nextStateCost

        T = T*TdecayFactor


def simulatedMoreAnnealAtSameT(startState, heuristicF, goal, TdecayFactor=0.99, numAnnealAtSameT=100):

    result=[]
    actionsTaken=[]
    currentState = startState
    currentStateCost = heuristicF(goal, currentState.currentStateMap, currentState.drone_pos)
    T = 1.0

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
            dE = nextStateCost - currentStateCost

            probabilityOfAcceptingRandomAction = np.exp(-dE/T)

            if dE < 0 or probabilityOfAcceptingRandomAction > random.random():
                nodesExplored = nodesExplored + 1
                currentState = nextState
                currentStatecost = nextStateCost

        T = T*TdecayFactor
    
