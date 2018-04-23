import numpy as np
import random
import tools.plot as plt


def where_does_my_block_want_to_move(sim, block_goals):
    
    while True:
        
        top_level_blocks = sim.top_level_blocks()
        max_score = 0
        blocks_with_score = []
    
        for block in top_level_blocks:
            blocks_underneath = [(block[0], block[1], y, sim.map[block[0]][block[1]][y]) for y in range(block[2] + 1)]
            score = 0
            move = None
            goal = block_goals[block] if block in block_goals else None
            
            #  Move out of the way for blocks underneath
            for block_underneath in blocks_underneath:
                if block_underneath in block_goals:
                    move = block, (0, 0, 0)
                    score = 1
            
            if goal is None:
                #  Build a pillar to a goal
                for block_goal in block_goals:
                    possible_goal = block_goals[block_goal]
                    if possible_goal[0] == block[0] and possible_goal[1] == block[1]:
                        continue
                    
                    blocks_underneath_goal = [(possible_goal[0], possible_goal[1], y, sim.map[possible_goal[0]][possible_goal[1]][y]) for y in range(possible_goal[2]) if sim.space_taken(possible_goal[0], possible_goal[1], y)]
                    
                    has_goal = False
                    for bl in blocks_underneath_goal:
                        if bl in block_goals:
                            has_goal = True
                    
                    if has_goal:
                        continue
                    
                    #ex = examine_goal(sim, block_goals, possible_goal)
                    #if ex:
                    pillar = sim.pillar_height(possible_goal[0], possible_goal[1])
                    
                    if pillar <= possible_goal[1]:
                        move = block, (possible_goal[0], possible_goal[1], pillar)
                        score = 2
            
            else:
                #  Move into the final goal position
                is_block = sim.space_taken(goal[0], goal[1], goal[2] - 1)
                print("Block", is_block, goal, "'", sim.map[goal[0]][goal[1]], "'")
                if is_block:
                    #ex = examine_goal(sim, block_goals, goal)
                    #if not ex:
                     move = block, (goal[0], goal[1], goal[2])
                     score = 3
                    
            if score > 0:
                if score > max_score:
                    max_score = score
                    blocks_with_score = [move]
                if score == max_score:
                    blocks_with_score.append(move)
                
        
        move = random.choice(blocks_with_score)
        print(max_score)
        print(move)
        if move[0] in block_goals:
            goal = block_goals[move[0]]
            del block_goals[move[0]]
            block_goals[(move[1][0], move[1][1], move[1][2], move[0][3])] = goal
            print(block_goals)
        sim.take_block_action(move)
        #sim.map[move[1][0]][move[1][2]][move[1][1]] = 'black'
        plt.plot(sim)
    
            
def examine_goal(sim, block_goals, goal):
    blocks_under_goal = sim.map[goal[0]][goal[1] + sim.pillar_height(goal[0], goal[2]) - 1][goal[2]]
    
    goal_under_goal = False
    for block_under in blocks_under_goal:
        if block_under in block_goals:
            goal_under_goal = True
            
    if goal_under_goal:
        return False

def stack_heuristic(goal, sim):
    gx, gz, gy, gcolor = goal

    goalcost = 1
    if sim.state()[0][gx][gz][gy] == gcolor:
        goalcost = 0

    goalcol = sim.state()[0][gx][gz][:gy]
    layercost = 0
    for item in goalcol:
        if item == 'd' or item == ' ':
            layercost += 1

    return goalcost + layercost

        
def block_heuristic(goal, sim, pfrom, pto):
    goalColor = goal[3]
    
    #overallHighestGoal = -1
    #for x in range(len(currentStateMap)):
    #    for z in range(len(currentStateMap[x])):
    #        for y in range(len(currentStateMap[x][z])):
    
    
    highestGoal = -1
    for y in range(len(sim.map[pfrom[0]][pfrom[1]])):
        if sim.map[pfrom[0]][pfrom[1]][y] == goalColor:
            highestGoal = y
            
    goalHeight = sim.pillar_height(goal[0], goal[1])
    heightDiff = goalHeight - goal[2]
    
    if goalHeight > goal[2] and pfrom == (goal[0], goal[1]):
        return goalHeight - goal[2]
    
    if goalHeight < goal[2] - 1 and pto == (goal[0], goal[1]):
        return goal[2] - goalHeight
    
    
    
    isGoalType = sim.map[pfrom[0]][pfrom[1]][pfrom[2]] == goalColor
    if isGoalType:
        sat = 0
        if pto[0] == goal[0]:
            sat += 1
        if pto[1] == goal[1]:
            sat += 1
        if pto[2] == goal[2]:
            sat += 1
        if sat == 3:
            return 0
    
    if highestGoal == -1:
        return float('inf')




def find(f, currentStateList):
    for item in currentStateList:
        if f(item): 
              return item
            
def euclidean(source, dest):
    return np.sqrt((source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2)

def chebyshev(source, dest):
    return max(abs(source[0] - dest[0]), abs(source[1] - dest[1]), abs(source[2] - dest[2]))

def chebyshev_sim(goal, sim):
    gx,gz,gy,_ = goal
    return chebyshev((gx,gz,gy), sim.drone_pos)


# to work around empty blocks in pillar blocks list
def findCntBlocksOnPillar(pillarBlocksList):
    return sum(1 for blk in pillarBlocksList if blk != ' ')

def costHeuristicFunc(goal, currentStateMap, dronePos, maxY=5):
    goalPillar = (goal[0], goal[1])
    if goalPillar not in currentStateMap:
        goalPillarBlocksList=[]
    else:
        goalPillarBlocksList = currentStateMap[goalPillar]
        
    goalPillarTopY = findCntBlocksOnPillar(goalPillarBlocksList)
    
    if goalPillarTopY-1 >= goal[2] and goalPillarBlocksList[goal[2]] == goal[3]:
        # already goal achieved, return zero cost
        return 0

    # find current drone pos
    # dronePos = find(lambda item: item[3] == 'd', currentStateList)

    # to be removed once we have refactored the algos to extract dronePos from current simulator.dronePos
    #for pillar, pillarBlocksList in currentStateMap.items():
    #    if 'd' in pillarBlocksList:
    #        dronePos = (pillar[0], pillar[1], pillarBlocksList.index('d'))
    #        break

    # euclidean dist from drone pos to goal x, goal z, max(goal pillar y) +1 = len(goalPillarList)

    
    droneDistToGoalPillarTop = euclidean(dronePos, (goal[0], goal[1], goalPillarTopY))

    #print('droneDistToGoalPillarTop=', droneDistToGoalPillarTop)
    #based on goal x, goal y, goal z and current stuff on goal x, goal z - the current pillar at goal x, goal z,
    #determine how many blocks on goal x, goal z pillar needs move out ? - let's call it cntMoveOuts

    cntMoveOuts = (goalPillarTopY - 1 - goal[2]) + 1

    # For each moveout, examine each of the other (101*101)-1 pillars on table (minus to exclude goal pillar) and try to
    # fit as many blocks out of cntMoveOuts from 3.1 above on to these destination pillars. Cost for these moveouts is:
    #   moveoutscost= Sum of all such

    #      (attach=1 +
    #      2*move=2*(euclidean from goal x, goal z, tobemovedout y on goal pillar to moveout destination x,y,z) +
    #      release=1)
    #      move cost is doubled for drone to and fro trips.

    #print('cntMoveOuts=', cntMoveOuts)
    moveOutCost=0
    toBeMovedOut=cntMoveOuts

    for pillar, pillarBlocksList in currentStateMap.items():
        if toBeMovedOut == 0:
            break
        if (pillar != goalPillar):
            pillarTopY = findCntBlocksOnPillar(pillarBlocksList)
            destsOnPillar = maxY - pillarTopY

            for i in range(destsOnPillar):
                distToDestOnPillar = euclidean((goal[0], goal[1], goalPillarTopY-1-i), (pillar[0], pillar[1], pillarTopY-1-i, ))
                moveOutCost = moveOutCost + 2*distToDestOnPillar + 1 + 1
                toBeMovedOut = toBeMovedOut-1
                if toBeMovedOut == 0:
                    break
    # How many blocks we need to move in to goal pillar? let's call it cntMoveIns
    #print('moveOutCost=', moveOutCost)

    cntMoveIns = (goal[2] + 1) - (goalPillarTopY-cntMoveOuts)
    #print('cntMoveIns=', cntMoveIns)
    #For each move in, examine each of the other (101*101)-1 pillars on table (minus to exclude goal pillar) and try to
    # accumulate as many blocks out of cntMoveIns from 3.3 above from these source pillars. Cost for these moveins is:
    #     moveinscost= Sum of all such

    #     (attach=1 +
    #     2*move=2*(euclidean from source x, y, z to goal x, goal z, tobemovedin y on goal pillar) +
    #     release=1)
    #     move cost is doubled for drone to and fro trips.

    moveInCost=0
    for pillar, pillarBlocksList in currentStateMap.items():
        if cntMoveIns == 0:
            break
        if (pillar != goalPillar):
            sourcesOnPillar = len(pillarBlocksList)
            pillarTopY = findCntBlocksOnPillar(pillarBlocksList)

            for i in range(sourcesOnPillar):
                distFromSrcOnPillar = euclidean((goal[0], goal[1], goalPillarTopY-1+i), (pillar[0], pillar[1], pillarTopY-1-i))
                moveInCost = moveInCost + 2*distFromSrcOnPillar + 1 + 1
                cntMoveIns = cntMoveIns-1
                if cntMoveIns == 0:
                    break
    #print('moveInCost=', moveInCost)
    return droneDistToGoalPillarTop + moveOutCost + moveInCost

# test

dwElementBlock1=(0, 0, 0, 'red')
dwElementBlock2=(0, 0, 1, 'yellow')
dwElementBlock3=(0, -1, 0, 'blue')
dwElementBlock4=(-1, -1, 0, 'green')
dwElementBlock5=(-1, 0, 0, 'yellow')
dwElementDrone =(0, -1, 0, 'd')
currentStateList = [dwElementBlock1, dwElementBlock2, dwElementBlock3, dwElementBlock4, dwElementBlock5, dwElementDrone]
currentStateMap ={}
currentStateMap[(0,0)]=['red', 'yellow']
currentStateMap[(0,-1)]=['blue', 'd']
currentStateMap[(-1,-1)]=['green']
currentStateMap[(-1,0)]=['yellow']

#print(currentStateList)

#for stateElement in currentStateList:
#    print(stateElement)
#    print(stateElement[3])

#for pillarcoordinate, pillar in currentStateMap.items():
#    print(pillarcoordinate)
#    print(pillar)
    
goal = (0,0,1,'green')

#print('cost to achieve {} is {}'.format(goal, costHeuristicFunc(goal, currentStateMap, maxY=2)))

goal = (0,0,1,'yellow')
#print('cost to achieve {} is {}'.format(goal, costHeuristicFunc(goal, currentStateMap, maxY=2)))
