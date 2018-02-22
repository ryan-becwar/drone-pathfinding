import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from simulator import *
#goal = (3,3,0,'red')


class Node:
    def __init__(self, state, f=0, g=0 ,h=0):
        self.state = state
        self.f = f
        self.g = g
        self.h = h
    def __repr__(self):
        return "Node(" + repr(self.state) + ", f=" + repr(self.f) + \
               ", g=" + repr(self.g) + ", h=" + repr(self.h) + ")"

def aStar(start, goal, heuristicF):
    closed = set()
    open = set([start])

    cameFrom = {}
    gscore = {}
    gscore[start] = 0
    fscore = {}
    fscore[start] = heristicF(goal, start.currentStateMap, start.drone_pos)

    while open:
        #current is the node with the smallest fscore
        current = min(fscore, key=fscore.get)
        if current.goalTest(goal):
            return reconstruct_path(cameFrom, current)

        open.remove(current)
        closed.add(current)

        for action in current.possibleActions():
            nextState, nextCost = current.resultingStateFromAction(action)
            if nextState in closed:
                continue

            if nextState not in open:
                open.add(nextState)
                gscore[nextState] = float("inf")
                fscore[nextState] = float("inf")

            tentative_gscore = gscore[current] + nextCost
            if tentative_gscore >= gscore[neighbor]:
                continue #not a good path

            cameFrom[nextState] = current
            gscore[nextState] = tentative_gscore
            fscore[nextState] = gscore[nextState] + heuristicF(goal, nextState, nextState.drone_pos)

        return "failure"



def reconstruct_path(cameFrom, current):
    total_path = [current]
    while current in cameFrom:
        current = cameFrom[current]
        total_path.append(current)
    return total_path
