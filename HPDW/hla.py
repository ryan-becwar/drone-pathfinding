from copy import *
from hpdwsimulator import *

class Plan:
    def __init__(self, startState=None, endState=None):
        self.startState = startState
        self.endState = endState        
        self.actions = []
    
    def __repr__(self):
        output =''
        for i, action in enumerate(self.actions):
            if i > 0:
                output += "," + repr(action)
            else:
                output += repr(action)
        
        return output
    
    def addAction(self, action):
        self.actions.append(action)
    
    def getPlanCost(self):
        return sum(action.getBestPlanCost() for action in actions)

class A:
    def __init__(self, name, startState):
        self.name = name
        self.startState = startState
        self.endState = None        
        self.possiblePlans = [] # possible plans sorted by cost
        self.cost = 0 
        
    def __repr__(self, name):
        return "A:" + repr(name)  
    
    def evalPlans(self):
        return
    
    def addPlan(self, possiblePlan):
        self.possiblePlans.append(possiblePlan)
        self.possiblePlans.sort(key = lambda n: n.getPlanCost()) # sort by cost of plan
        
    def getBestPlanCost(self):
        return 0
   
    
class BuildTower(A):
    def __init__(self, startState, xz, tower):
        A.__init__(self, name="BuildTower", startState=startState)
        self.xz = xz
        self.tower = tower # list of blocks - where each block can be either a colore or '*' meaning any color
    
    def __repr__(self):
        return self.name + " " + repr(self.tower) + " at " + repr(self.xz) 
    
    def evalPlans(self):
        # eval plans required to achieve this, cost and endstate, set them on base action. 
        # based on start state find how many blocks to move to dest tower        
        plans=[]
        currentTower = self.startState.towerAt(self.xz)
        currentTowerBlkCnt = self.startState.numBlksAt(self.xz)
        moreBlksRequiredInTower = len(self.tower)        
        
        # chk from bottom the first unequal blk in current tower - let's say it's tower[firstuneuqalidx]
        # from top (in a loop) move out i.e. MoveBlk(startState=startState, srcxz=xz, destxz=('?','?') 
        # out of tower up unitl firstuneuqalidx
        
        firstunequalidx = next( (i for i, currentBlk in enumerate(currentTower[:currentTowerBlkCnt]) \
                                 if not blksEqual(currentBlk, self.tower[i])), None)
        moveoutHlas = []
        if firstunequalidx is not None:
            print(self)
            print("currentTower", currentTower)
            print("first unequal Idx", firstunequalidx)
            [moveoutHlas.append(MoveBlk(startState=self.startState, srcxz=self.xz, destxz=('?','?') )) \
            for i, blk in enumerate(currentTower[:currentTowerBlkCnt][::-1]) if i >= firstunequalidx]
                
        # 2 strategies for plans here on:
        
        # 1: Now go again in a loop from idx=firstuneuqalidx upwards and bring self.tower[idx] 
        #    MoveBlkIn(starstState=startState, toxz=self.towerxz, self.tower[idx]) 
        #    any srcxz which has at least one block that is equal to self.tower[idx]; idx++
        
        # 2: Just get the blocks from any tower with blocks having anyone of the desired blocks in self.tower
        #    if blocks not in order, do recursively buildTower again - hope is moveoouts followed by moveIns successively 
        #    will make it proper at some stage
        
        # for each remaining block, explore all possible srcxz out of a other towers - each possiblity leads to a different plan
        plan = Plan(startState=self.startState)
        for hla in moveoutHlas:
            plan.addAction(hla)
            
        plans.append(plan)
        
        print(plans)
        
        return

class MoveBlkIn:
    def __init__(self, startState, destxz, blk):
        A.__init__(self, name="MoveBlkIn", startState=startState)
        self.destxz = destxz
        self.blkColor = blkColor
        
    def __repr__(self):
        return "MoveBlkIn:" + repr(self.blk) + "->" + repr(self.destxz)
    
    def evalPlans(self):
        # eval plans required to achieve this, cost and endstate, set them on base action.
        # will consist of a bunch of MoveBlk HLAs
        #    identify such srcxz towers with desired block
        #    for each such srcxz:
        #       recurse:
        #           if top block != desired block (self.blk), move out top i.e. MoveBlk(startState, srcxz, destxz=('?','?') )
        #       
        #       move top block to toxz i.e. MoveBlk(startState, srcxz, destxz=toxz) until 
        #    for all such towers
        return
        
class MoveBlk:
    def __init__(self, startState, srcxz, destxz=('?','?')):
        A.__init__(self, name="MoveBlk", startState=startState)
        self.srcxz=srcxz
        self.destxz=destxz   
        
    def __repr__(self):
        return "MoveBlk:" + repr(self.srcxz) + "->" + repr(self.destxz)
    
    def evalPlans(self):
        # eval plans required to achieve this, cost and endstate, set them on base action.
        # drone has to move to top of srcxz, attach, move to top of destxz, release
        plans = []
        plan = Plan(startState=self.startState)
        cost = 0
        # move to top of srcxz
        x = self.srcxz[0]
        z = self.srcxz[1]
        y = self.startState.numBlksAt(self.srcxz)
        moveToSrcTop = MoveDrone(startState=self.startState, droneDest=(x,z,y))
        moveToSrcTop.evalPlans()
        cost = cost + moveToSrcTop.cost
        plan.addAction(moveToSrcTop)
#         print("After {} with cost {} end state is \n {}".format(moveToSrcTop, moveToSrcTop.cost, moveToSrcTop.endState))
        
        attachToTopOfSrc = Attach(startState=moveToSrcTop.endState)
        attachToTopOfSrc.evalPlans()
        cost = cost + attachToTopOfSrc.cost
        plan.addAction(attachToTopOfSrc)
#         print("After {} with cost {} end state is \n {}".format(attachToTopOfSrc, attachToTopOfSrc.cost, attachToTopOfSrc.endState))  
        
        x = self.destxz[0]
        z = self.destxz[1]
        #y = self.startState.numBlksAt(self.destxz) if self.startState.numBlksAt(self.destxz)>0 else self.startState.Yrange[1]
        y = self.startState.Yrange[1]
        moveToDestTop = MoveDrone(startState=attachToTopOfSrc.endState, droneDest=(x,z,y))
        moveToDestTop.evalPlans()
        cost = cost + moveToDestTop.cost
        plan.addAction(moveToDestTop)
#         print("After {} with cost {} end state is \n {}".format(moveToDestTop, moveToDestTop.cost, moveToDestTop.endState))
        
        releaseFromTopOfDest = Release(startState=moveToDestTop.endState)
        releaseFromTopOfDest.evalPlans()
        cost = cost + releaseFromTopOfDest.cost
        plan.addAction(releaseFromTopOfDest)
#         print("After {} with cost {} end state is \n {}".format(releaseFromTopOfDest, releaseFromTopOfDest.cost, releaseFromTopOfDest.endState))
        
        self.endState = releaseFromTopOfDest.endState
        self.cost = cost
#         print("total cost is ", self.cost)
        plans.append(plan)
        
        return

# A* will be required for shorted path for MoveDrone
class MoveDrone:
    def __init__(self, startState, droneDest):
        A.__init__(self, name="MoveDrone", startState=startState)
        
        self.droneDest = droneDest   
        
    def __repr__(self):
        return "MoveDrone" + "->" + repr(self.droneDest)
    
    def evalPlans(self):
        # eval plans required to achieve this, cost and endstate, set them on base action.
        # drone has to move to from current position to top of destxz
        # returns resulting state
        self.endState = self.startState.moveDroneImmutable(self.droneDest)
        
        source = self.startState.dronePos
        dest = self.endState.dronePos        
        self.cost = euclidean(source, dest)
        
        return 

class Attach(A):
    def __init__(self, startState):
        A.__init__(self, name='attach', startState=startState)            
        
    def __repr__(self):
        return self.name
    
    def evalPlans(self):
        (actionStatus, stepCost, resultingState) = self.startState.takeActionImmutable(('attach',))
        self.endState = resultingState
        self.cost = stepCost
        return 

class Release(A):
    def __init__(self, startState):
        A.__init__(self, name='release', startState=startState)            
        
    def __repr__(self):
        return self.name
    
    def evalPlans(self):
        (actionStatus, stepCost, resultingState) = self.startState.takeActionImmutable(('release',))
        self.endState = resultingState
        self.cost = stepCost
        return 
      
    
class PA(A):
    def __init__(self, startState, actionTuple):
        A.__init__(self, name='PA', startState=startState)
        self.actionTuple = actionTuple
        plan = Plan()
        plan.addAction(self)
        self.possiblePlans.append(plan)       
        
    def __repr__(self):
        return repr(self.actionTuple)
    
    def evalPlans(self):
        # eval endState for this action and set it on base high level A.endState
        return
        
    def getBestPlanCost(self):
        #TODO calculate cost of this primitive action and return, overrides high level Action cost
        return 0            
    
def getPossiblePlansFromGoal(startState, goal):
    #TODO: see if need to readjust if more than 1 tower to be built, goal contradiction etc.
    #TODO: At least let's create plans with all permutations of build towers
    plans = []
    for possibletower in goal.getPossibleTowers():
        plan = Plan(startState=startState)
        plan.addAction(BuildTower(startState=startState, xz=possibletower[0], tower=possibletower[1]))
        plans.append(plan)          
    return plans



# print(getPossibleTowers(state3, goal3))
    