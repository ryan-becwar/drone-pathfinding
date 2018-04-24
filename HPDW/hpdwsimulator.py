
from itertools import product
import numpy as np
import copy as copy

def euclidean(source, dest):
    return (source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2

def blksEqual(blk1, blk2):
    if (blk1 == '*' and blk2 != '') or (blk2 == '*' and blk1 != ''):       
        return True   
    else:
        return blk1 == blk2
    
def readFile(Xrange, Zrange, Yrange, filename):
    stateMap = {}
    with open(filename, 'r') as file_in:
            for line in file_in.readlines():
                data = line.split()
                #x, z, y, item = (int(data[0]), int(data[1]), int(data[2]), data[3])   
                x, z, y, item = (data[0], data[1], data[2], data[3])  
                if x != '?':
                    x=int(x)
                if z != '?':
                    z=int(z)
                if y != '?':
                    y=int(y)
                if (x, z) not in stateMap:
                    stateMap[(x, z)] = ['']*(Yrange[1]+1)                    
                stateMap[(x, z)][y] = item
    return stateMap

class HPDWSimulator: 
    # loglevel can be 'verbose' or 'silent'
    def __init__(self, Xrange, Zrange, Yrange, filename, loglevel='silent'):
        self.Xrange = Xrange
        self.Zrange = Zrange
        self.Yrange = Yrange
        self.loglevel = loglevel
        self.attached = False        
        self.dronePos = None
        self.stateMap = readFile(Xrange, Zrange, Yrange, filename)
        for xz, xzItems in self.stateMap.items():
            for y, item in enumerate(xzItems):
                if item == 'd':
                    self.dronePos = (xz[0], xz[1], y)
        
    def __repr__(self):
        representation = "loglevel=" + repr(self.loglevel) + " Xrange=" + repr(self.Xrange) + " Zrange=" + repr(self.Zrange) + \
                         " Yrange=" + repr(self.Yrange) + " attached=" + repr(self.attached) + \
                         " dronePos=" + repr(self.dronePos) + "\nstateMap:\n"
        for columnXZ, columnItems in self.stateMap.items(): 
            countNonEmptyItems = sum(1 for i in columnItems if i != '')
            if  countNonEmptyItems > 0:
                representation = representation + repr(columnXZ) + ">" + repr(columnItems) + "\n"
            
        return representation
    
    def isBlkAt(self, blk, xz, y):
        if xz in self.stateMap and self.numBlksAt(xz) > y:            
            if blk == '*':
                return True
            else:
                return blk == self.blkAt(xz, y)
        else:
            return False
        
    def towerAt(self, xz):
        if xz in self.stateMap:
            return self.stateMap[xz]
        else:
            return []
        
    def towersWithBlks(self):        
        return [(xz, tower) for xz, tower in self.stateMap.items() if self.numBlksAt(xz)>0]
        
    def blkAt(self, xz, y):
        if xz in self.stateMap and self.numBlksAt(xz) > y:            
            return self.stateMap[xz][y]
        else:
            return ''
        
    def topBlkAt(self, xz):
        if xz in self.stateMap:            
            return self.stateMap[xz][self.numBlksAt(xz)]
        else:
            return ''
        
    def numBlksAt(self, xz):
        if xz in self.stateMap:
            return sum(1 for item in self.stateMap[xz] if item != '' and item !='d')
        else:
            return 0
    
    def numBlksAtIncludeEmpty(self, xz):
        if xz in self.stateMap:
            return sum(1 for item in self.stateMap[xz] if item !='d')
        else:
            return 0
    
    def getPossibleXZs(self):
        Xs = range(self.Xrange[0], self.Xrange[1]+1)
        Zs = range(self.Zrange[0], self.Zrange[1]+1)
        XZs=[]
        for x in Xs:
            for z in Zs:
                XZs.append((x,z))
        return XZs
    
    def fillWC(self):
        filledStateMap = {}
        for xz, xzTower in self.stateMap.items():
            Xs = range(self.Xrange[0], self.Xrange[1]+1) if xz[0] == '?' else range(xz[0], xz[0]+1)
            Zs = range(self.Zrange[0], self.Zrange[1]+1) if xz[1] == '?' else range(xz[1], xz[1]+1)
            ht = len(xzTower) - next(i for i, item in enumerate(xzTower[::-1]) if item != 'd' and item != '')
            xzTower= ['*' if item == '' or item == '?' else item for item in xzTower[:ht]]

            for x in Xs:
                for z in Zs:
                    filledStateMap[(x,z)]=xzTower
                    
        self.stateMap = filledStateMap
        return 
    
    def fillWCWithPossibleTowers(self, possibleTowers):
        result = copy.deepcopy(self)        
        filledStateMap ={}
        for (xz, xzTower) in possibleTowers:            
            filledStateMap[xz]=xzTower
                    
        result.stateMap = filledStateMap
        return result
    
    def fillWCInY(self):
        filledStateMap = {}
        for xz, xzTower in self.stateMap.items():
            ht = len(xzTower) - next(i for i, item in enumerate(xzTower[::-1]) if item != 'd' and item != '')
            xzTower= ['*' if item == '' or item == '?' else item for item in xzTower[:ht]]

            filledStateMap[xz]=xzTower
                    
        self.stateMap = filledStateMap
        return 
    
    def getPossibleTowers(self):
        possibleTowers = []
        for xz, xzTower in self.stateMap.items():
            Xs = range(self.Xrange[0], self.Xrange[1]+1) if xz[0] == '?' else range(xz[0], xz[0]+1)
            Zs = range(self.Zrange[0], self.Zrange[1]+1) if xz[1] == '?' else range(xz[1], xz[1]+1)
            ht = len(xzTower) - next(i for i, item in enumerate(xzTower[::-1]) if item != 'd' and item != '')
            xzTower= ['*' if item == '' or item == '?' else item for item in xzTower[:ht]]

            for x in Xs:
                for z in Zs:
                    possibleTowers.append(((x,z), xzTower))
        return possibleTowers

    def log(self, message):
        if self.loglevel is 'verbose':
            print(message)
    
    # returns True for success, else False
    def attach(self):
        if self.attached:
            self.log("Already attached...not attaching!")
            return False
        else:
            self.attached = True
            return True
       
    # return True if success, else False
    def release(self):
        if not self.attached:
            self.log("Not attached...can't release!")
            return False
        else:
            # find top of column below drone
            # first the column of items below drone and attached block
            droneColumnXZ = (self.dronePos[0], self.dronePos[1])
            droneY = self.dronePos[2]
            #attached block at droneY-1 
            attachedBlock = self.stateMap[droneColumnXZ][droneY-1]
#             print("During release, attached block is\n", attachedBlock)
            # now the drone column items below the attached block at droneY-1
            droneColumnItems = self.stateMap[droneColumnXZ][:droneY - 1] 
#             print("During release, droneColumnItems\n", droneColumnItems)
            if '' in droneColumnItems:
                # find first '' (empty) item bottoms up on the remaining column to take in the attached block to be released
                destY = droneColumnItems.index('')
#                 print("During release, first empty slot in droneColumnItems\n", destY)
                # now place attached block at droneY-1 at destY
                self.stateMap[droneColumnXZ][destY] = attachedBlock
                # mark previously attached block position at droneY-1 as '' (empty)
                self.stateMap[droneColumnXZ][droneY-1] = ''
                self.attached = False
                return True
            else:
#                 self.log('Column {} does not have free slots to take the release... not releasing!'.format(droneColumnXZ) )
                return False
  
    def move(self, dx, dz, dy):
        # alt drone pos by dx, dz, dy
        origDronePos = self.dronePos
        self.dronePos = (origDronePos[0]+dx, origDronePos[1]+dz, origDronePos[2]+dy)
        if (self.dronePos[0], self.dronePos[1]) not in self.stateMap:
            self.stateMap[(self.dronePos[0], self.dronePos[1])] = ['']*(self.Yrange[1]+1)
        self.stateMap[(self.dronePos[0], self.dronePos[1])][self.dronePos[2]] = 'd'
        self.stateMap[(origDronePos[0], origDronePos[1])][origDronePos[2]] = ''
        
        # alt attached block position if attached
        if self.attached:
            origPos = (origDronePos[0], origDronePos[1], origDronePos[2]-1)
            newPos = (origPos[0]+dx, origPos[1]+dz, origPos[2]+dy)
            attachedBlock = self.stateMap[(origPos[0], origPos[1])][origPos[2]]
            if (newPos[0], newPos[1]) not in self.stateMap:
                self.stateMap[(newPos[0], newPos[1])] = ['']*(self.Yrange[1]+1)
            self.stateMap[(newPos[0], newPos[1])][newPos[2]] = attachedBlock
            self.stateMap[(origPos[0], origPos[1])][origPos[2]] = ''
            
        return True
       
    def possibleActions(self):
        actions = [] # # Returns tuples of (attach), (release), (move, dx, dz, dy)
        droneXZ = (self.dronePos[0], self.dronePos[1])
        droneX = self.dronePos[0]
        droneZ = self.dronePos[1]
        droneY = self.dronePos[2]        
        droneColumnItems = self.stateMap[droneXZ]        
        # First find possible attaches
        if droneY >= 1 and droneColumnItems[droneY - 1] != '' and (not self.attached) :
            actions.append(('attach',))
        # Now find possible releases
        if droneY >= 1 and '' in droneColumnItems[:droneY - 1] and self.attached:
            actions.append(('release',))
        
        # Finally find possible moves (in ideal world there are 27 such moves involving cartesian products of {-1}, {0}, {1})
        moves = set(product(set([-1,0,1]), repeat=3))
        # Now append to actions if we are allowed to make these moves
        for move in moves:
            dx, dz, dy = move
            # first check if drone move is within drone world ranges
            if (droneX + dx >= self.Xrange[0] and droneX + dx <= self.Xrange[1]) and \
                (droneZ + dz >= self.Zrange[0] and droneZ + dz <= self.Zrange[1]) and \
                (droneY + dy >= self.Yrange[0] and droneY + dy <= self.Yrange[1]) and \
                ((droneX + dx, droneZ + dz) not in self.stateMap or self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy] == ''):
                # if attached, check whether attached block (1 below drone) can also move to corresponding new position
                if self.attached:
                    if (droneY + dy - 1 < self.Yrange[0]) or \
                        (droneY + dy - 1 > self.Yrange[1]) or \
                         ( ((droneX + dx, droneZ + dz) in self.stateMap) and \
                            (self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy - 1] is not '') ) :
                        continue                    
                
                actions.append(('move', dx, dz, dy))
                    
        self.log("Possible actions {}".format(actions))            
        return actions
    
    def possibleDroneMoves(self):
        actions = [] # # Returns tuples of (attach), (release), (move, dx, dz, dy)
        droneXZ = (self.dronePos[0], self.dronePos[1])
        droneX = self.dronePos[0]
        droneZ = self.dronePos[1]
        droneY = self.dronePos[2]        
        droneColumnItems = self.stateMap[droneXZ]        
#         # First find possible attaches
#         if droneY >= 1 and droneColumnItems[droneY - 1] != '' and (not self.attached) :
#             actions.append(('attach',))
#         # Now find possible releases
#         if droneY >= 1 and '' in droneColumnItems[:droneY - 1] and self.attached:
#             actions.append(('release',))
        
        # Finally find possible moves (in ideal world there are 27 such moves involving cartesian products of {-1}, {0}, {1})
        moves = set(product(set([-1,0,1]), repeat=3))
        # Now append to actions if we are allowed to make these moves
        for move in moves:
            dx, dz, dy = move
            # first check if drone move is within drone world ranges
            if (droneX + dx >= self.Xrange[0] and droneX + dx <= self.Xrange[1]) and \
                (droneZ + dz >= self.Zrange[0] and droneZ + dz <= self.Zrange[1]) and \
                (droneY + dy >= self.Yrange[0] and droneY + dy <= self.Yrange[1]) and \
                ((droneX + dx, droneZ + dz) not in self.stateMap or self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy] == ''):
                # if attached, check whether attached block (1 below drone) can also move to corresponding new position
                if self.attached:
                    if (droneY + dy - 1 < self.Yrange[0]) or \
                        (droneY + dy - 1 > self.Yrange[1]) or \
                         ( ((droneX + dx, droneZ + dz) in self.stateMap) and \
                            (self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy - 1] is not '') ) :
                        continue                    
                
                actions.append(('move', dx, dz, dy))
                    
        self.log("Possible actions {}".format(actions))            
        return actions
    
    def takeActionImmutable(self, action):
        resultingDWSim = copy.deepcopy(self)
        (actionStatus, stepCost) = resultingDWSim.takeAction(action)
        return (actionStatus, stepCost, resultingDWSim)
        
    # assumes a valid action returned by possibleActions
    def takeAction(self, action):
        # returns a tuple of True/False depending on success/failure status of action and step cost.
        # step cost is euclidean for move, 1 for release/attach        
        status = False
        stepCost = -1.0
        self.log("Taking action {}".format(action))
        if action[0] == 'attach':
            status = self.attach()
            stepCost = 1.0
        elif action[0] == 'release':
            status = self.release()
            stepCost = 1.0
        elif action[0] == 'move':
            actionStr, dx, dz, dy = action
            status = self.move(dx, dz, dy)
            source = self.dronePos
            dest = (self.dronePos[0]+dx, self.dronePos[1]+dz, self.dronePos[2]+dy)
            stepCost = euclidean(source, dest)
        else:
            self.log('Invalid action requested!')            
        return (status, stepCost)
    
    def isGoal(self, goal):
        diffs = 0
        for goalTowerXZ, goalTowerItems in goal.stateMap.items():
            if (self.numBlksAt(goalTowerXZ) == goal.numBlksAt(goalTowerXZ)):
                towerItems = self.towerAt(goalTowerXZ)
                diffs = diffs + sum(1 for i, item in enumerate(towerItems[:self.numBlksAt(goalTowerXZ)]) \
                                    if (not blksEqual(item, goalTowerItems[i])) )
            else:
                return False        
        return diffs==0
   
    def moveDroneImmutable(self, droneDest):
        resultingState = copy.deepcopy(self)
        origDronePos = resultingState.dronePos
        resultingState.dronePos = droneDest
        if (resultingState.dronePos[0], resultingState.dronePos[1]) not in resultingState.stateMap:
            resultingState.stateMap[(resultingState.dronePos[0], resultingState.dronePos[1])] = \
                                                                   ['']*(resultingState.Yrange[1]+1)
            
        resultingState.stateMap[(resultingState.dronePos[0], resultingState.dronePos[1])][resultingState.dronePos[2]] = 'd'
        resultingState.stateMap[(origDronePos[0], origDronePos[1])][origDronePos[2]] = ''
        
        # alt attached block position if attached
        if resultingState.attached:
            origPos = (origDronePos[0], origDronePos[1], origDronePos[2]-1)
            newPos = (droneDest[0], droneDest[1], droneDest[2]-1)
            attachedBlock = resultingState.stateMap[(origPos[0], origPos[1])][origPos[2]]
            if (newPos[0], newPos[1]) not in resultingState.stateMap:
                resultingState.stateMap[(newPos[0], newPos[1])] = ['']*(resultingState.Yrange[1]+1)
            resultingState.stateMap[(newPos[0], newPos[1])][newPos[2]] = attachedBlock
            resultingState.stateMap[(origPos[0], origPos[1])][origPos[2]] = ''
        
        return resultingState
    
def goalTest(dwsim, goal):
    return dwsim.isGoal(goal)