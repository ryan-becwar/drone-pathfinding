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
    numCycles=0
    while True :
        result.append(currentState)
        
        if currentState.goalTest(goal):
            return (result, nodesExplored)
        possibleActions = currentState.possibleActions()

        #print(possibleActions)

        action = pickRandomAction(possibleActions)

        #print('Action chosen ', action, 'dronePos ', currentState.drone_pos)

        actionsTaken.append(action)

        nextState = currentState.resultingStateFromAction(action)[0]

        #print('New dronePos', nextState.drone_pos)

        if nextState.goalTest(goal):
            result.append(nextState)
            return (result, actionsTaken, nodesExplored)

        nextStateCost = heuristicF(goal, nextState.currentStateMap, nextState.drone_pos)
   
        dE = nextStateCost - currentStateCost

        #print('dE={}, nextCost={}, currentCost={}'.format(dE, nextStateCost, currentStateCost)) 

        if T <=0:
            print('T is <=0')
            p=1.0
        else:
            qt = (abs(dE))/T 
            p = np.exp(-qt)
        
        #print('T=', T, 'p=',p)

        if dE <= 0 or p > random.random():
            #print('Chosing next state')                       
            nodesExplored = nodesExplored + 1
            currentState = nextState
            currentStateCost = nextStateCost

        T = T*TdecayFactor

        numCycles = numCycles + 1

def simulatedAnnealV1(startState, heuristicF, goal, TdecayFactor=0.90):
    result =[]
    actionsTaken=[]
    currentState = startState
    currentStateCost = heuristicF(goal, currentState.currentStateMap, currentState.drone_pos)
    T = 1.00000
    dEAvg = 0.00000
    numAccepted=0.0
    numCycles = 0.0

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

        dEAbs = round(abs(dE), 5)

        if not T > 0.00000:
           print('T zero')

        if nextStateCost > currentStateCost:
            # worse
            if numCycles == 0:
               dEAvg = dEAbs

            qt = round((dEAbs)/(dEAvg*T), 5)
            p = np.longdouble(np.exp(-qt))
            if p > np.longdouble(random.random()):
               # but p greater than random p, so accept anyway
               print('worse but high p, accepting')
               accept = True
            else:
               print('worse and low p, not accepting')
               accept = False 
        else:
            # better anyway so accept 
            print('better so accepting')
            accept = True
        
        if accept :
           nodesExplored = nodesExplored + 1 
           currentState = nextState
           currentStateCost = nextStateCost
           numAccepted = numAccepted + 1.0
           dEAvg = round((dEAbs * (numAccepted-1.0) +  dEAbs) / numAccepted, 5)


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
                print('T is <=0')
                probabilityOfAcceptingRandomAction=np.longdouble(1.0)
            else:
                qt = round((abs(dE))/T, 5)
                #qt = round(dE/T, 5)
                probabilityOfAcceptingRandomAction = np.longdouble(np.exp(-qt))

            if dE <= 0 or probabilityOfAcceptingRandomAction > np.longdouble(random.random()):
                nodesExplored = nodesExplored + 1
                currentState = nextState
                currentStateCost = nextStateCost

        T = round(T*TdecayFactor, 5)
    
