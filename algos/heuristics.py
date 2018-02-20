import numpy as np


def find(f, currentStateList):
    for item in currentStateList:
        if f(item): 
              return item
            
def euclidean(source, dest):
    return np.sqrt((source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2)

def costHeuristicFunc(goal, currentStateList, currentStateMap, maxZ=50):
    # find current drone pos
    dronePos = find(lambda item: item[3] == 'drone', currentStateList)
        
    # euclidean dist from drone pos to goal x, goal y, max(goal pillar z) +1 = len(goalPillarList)
    goalPillar = (goal[0], goal[1])
    goalPillarBlocksList = currentStateMap[goalPillar]
    goalPillarTopZ = len(goalPillarBlocksList)
    droneDistToGoalPillarTop = euclidean(dronePos, (goal[0], goal[1], goalPillarTopZ))
    
    #print(droneDistToGoalPillarTop)
    #based on goal x, goal y, goal z and current stuff on goal x, goal y - the current pillar at goal x, goal y, 
    #determine how many blocks on goal x, goal y pillar needs move out ? - let's call it cntMoveOuts
    
    cntMoveOuts = goalPillarTopZ - 1 - goal[2]
    
    # For each moveout, examine each of the other (101*101)-1 pillars on table (minus to exclude goal pillar) and try to 
    # fit as many blocks out of cnt_moveouts from 3.1 above on to these destination pillars. Cost for these moveouts is:
    #   moveoutscost= Sum of all such

    #      (attach=1 + 
    #      2*move=2*(euclidean from goal x, goal y, tobemovedout z on goal pillar to moveout destination x,y,z) +
    #      release=1)
    #      move cost is doubled for drone to and fro trips.

    #print(cntMoveOuts)
    moveOutCost=0
    toBeMovedOut=cntMoveOuts
    for pillar, pillarBlocksList in currentStateMap.items():
        if toBeMovedOut == 0:
            break
        if (pillar != goalPillar):
            pillarTopZ = len(pillarBlocksList)
            destsOnPillar = maxZ - pillarTopZ
            
            for i in range(destsOnPillar):
                distToDestOnPillar = euclidean((goal[0],goal[1], goalPillarTopZ-1-i), (pillar[0], pillar[1], pillarTopZ-1-i))
                moveOutCost = moveOutCost + 2*distToDestOnPillar + 1 + 1
                toBeMovedOut = toBeMovedOut-1
                if toBeMovedOut == 0:
                    break
    # How many blocks we need to move in to goal pillar? let's call it cntMoveIns
    #print(moveOutCost)
    
    cntMoveIns = goal[2] - (goalPillarTopZ-1-cntMoveOuts) + 1
    #print(cntMoveIns)  
    #For each move in, examine each of the other (101*101)-1 pillars on table (minus to exclude goal pillar) and try to 
    # accumulate as many blocks out of cnt_moveins from 3.3 above from these source pillars. Cost for these moveins is:
    #     moveinscost= Sum of all such

    #     (attach=1 + 
    #     2*move=2*(euclidean from source x, y, z to goal x, goal y, tobemovedin z on goal pillar) +
    #     release=1)
    #     move cost is doubled for drone to and fro trips.

    moveInCost=0
    for pillar, pillarBlocksList in currentStateMap.items():
        if cntMoveIns == 0:
            break
        if (pillar != goalPillar):
            sourcesOnPillar = len(pillarBlocksList) 
            pillarTopZ = len(pillarBlocksList)
            
            for i in range(sourcesOnPillar):
                distFromSrcOnPillar = euclidean((goal[0],goal[1], goalPillarTopZ-1+i), (pillar[0], pillar[1], pillarTopZ-1-i))
                moveInCost = moveInCost + 2*distFromSrcOnPillar + 1 + 1
                cntMoveIns = cntMoveIns-1
                if cntMoveIns == 0:
                    break
    #print(moveInCost)                
    return droneDistToGoalPillarTop + moveOutCost + moveInCost

# test

dwElementBlock1=(0, 0, 0, 'red')
dwElementBlock2=(0, 0, 1, 'yellow')
dwElementBlock3=(0, -1, 0, 'blue')
dwElementBlock4=(-1, -1, 0, 'green')
dwElementBlock5=(-1, 0, 0, 'yellow')
dwElementDrone = (0, -1, 1, 'drone')
currentStateList = [dwElementBlock1, dwElementBlock2, dwElementBlock3, dwElementBlock4, dwElementBlock5, dwElementDrone]
currentStateMap ={}
currentStateMap[(0,0)]=['red', 'yellow']
currentStateMap[(0,-1)]=['blue', 'drone']
currentStateMap[(-1,-1)]=['green']
currentStateMap[(-1,0)]=['yellow']

print(currentStateList)

for stateElement in currentStateList:
    print(stateElement)
    print(stateElement[3])

for pillarcoordinate, pillar in currentStateMap.items():
    print(pillarcoordinate)
    print(pillar)
    
goal = (0,0,1,'green')

print('cost to achieve {} is {}'.format(goal, costHeuristicFunc(goal, currentStateList, currentStateMap, maxZ=2)))
    
