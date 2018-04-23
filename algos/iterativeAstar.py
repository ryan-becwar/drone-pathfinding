import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from simulator import *
#goal = (3,3,0,'red')


#class Node:
#    def __init__(self, state, f=0, g=0 ,h=0):
#        self.state = state
#        self.f = f
#        self.g = g
#        self.h = h
#    def __repr__(self):
#        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
#               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

def aStar(start, goal, heuristicF):
    closed = set()
    open = set([start.__hash__()])

    hashdict = {}
    hashdict[start.__hash__()] = start
    cameFrom = {}
    gscore = {}
    gscore[start.__hash__()] = 0
    fscore = {}
    fscore[start.__hash__()] = heuristicF(goal, start)

    while open:
        #current is the node with the smallest fscore
        current = hashdict[min(open, key=fscore.get)]
        print(current.to_list())
        if current.attached:
            print("ATTACHED")
        currentHash = current.__hash__()
        #print(current.currentStateMap)
        if current.goalTest(goal):
            hashpath = reconstruct_path(cameFrom, currentHash)
            return [hashdict[x] for x in hashpath]

        open.remove(currentHash)
        closed.add(currentHash)

        for action in current.possibleActions():
            nextState, nextCost = current.resultingStateFromAction(action)
            nextHash = nextState.__hash__()
            hashdict[nextHash] = nextState
            if nextHash in closed:
                continue

            if nextHash not in open:
                open.add(nextHash)
                gscore[nextHash] = float("inf")
                fscore[nextHash] = float("inf")

            tentative_gscore = gscore[currentHash] + nextCost
            if tentative_gscore >= gscore[nextHash]:
                continue #not a good path

            cameFrom[nextHash] = currentHash
            gscore[nextHash] = tentative_gscore
            fscore[nextHash] = gscore[nextHash] + heuristicF(goal, nextState)

    return "failure"

def blockaStar(start, goal, heuristicF):
    closed = set()
    open = set([start.__hash__()])

    hashdict = {}
    hashdict[start.__hash__()] = (start, "start")
    cameFrom = {}
    gscore = {}
    gscore[start.__hash__()] = 0
    fscore = {}
    fscore[start.__hash__()] = heuristicF(goal, start)

    while open:
        #current is the node with the smallest fscore
        current = hashdict[min(open, key=fscore.get)]
        currentHash = current[0].__hash__()
        #print(current[0].currentStateMap)
        if current[0].goalTest(goal):
            hashpath = reconstruct_path(cameFrom, currentHash)
            return [hashdict[x] for x in hashpath]

        open.remove(currentHash)
        closed.add(currentHash)

        for action in current[0].possible_block_moves():
            nextState, nextCost = current[0].resultingStateFromBlockAction(action)
            nextHash = nextState.__hash__()
            hashdict[nextHash] = (nextState, action)
            if nextHash in closed:
                continue

            if nextHash not in open:
                open.add(nextHash)
                gscore[nextHash] = float("inf")
                fscore[nextHash] = float("inf")

            tentative_gscore = gscore[currentHash] + nextCost
            if tentative_gscore >= gscore[nextHash]:
                continue #not a good path

            cameFrom[nextHash] = currentHash
            gscore[nextHash] = tentative_gscore
            fscore[nextHash] = gscore[nextHash] + heuristicF(goal, nextState)

    return "failure"


def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return total_path
