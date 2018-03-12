from itertools import product
import numpy as np

def euclidean(source, dest):
    return np.sqrt((source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2)

class DWSimulator: 
    # loglevel can be 'verbose' or 'silent'
    def __init__(self, Xrange, Zrange, Yrange, filename, loglevel='silent'):
        self.stateMap = {}
        self.attached = False
        self.dronePos = None
        self.Xrange = Xrange
        self.Zrange = Zrange
        self.Yrange = Yrange
        self.loglevel = loglevel
        with open(filename, 'r') as file_in:
            for line in file_in.readlines():
                data = line.split()
                x, z, y, item = (int(data[0]), int(data[1]), int(data[2]), data[3])                
                if (x, z) not in self.stateMap:
                    self.stateMap[(x, z)] = ['']*(self.Yrange[1]+1)
                self.stateMap[(x, z)][y] = item
                if item == 'd':
                    self.dronePos = (x, z, y)        
        
    def __repr__(self):
        representation = "loglevel=" + repr(self.loglevel) + " Xrange=" + repr(self.Xrange) + " Zrange=" + repr(self.Zrange) + \
                         " Yrange= " + repr(self.Yrange) + " attached=" + repr(self.attached) + \
                         " dronePos=" + repr(self.dronePos) + "\nstateMap:\n"
        for columnXZ, columnItems in self.stateMap.items(): 
            representation = representation + repr(columnXZ) + ">" + repr(columnItems) + "\n"
            
        return representation
    
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
    
    def revertAttach(self):
        if self.attached:
            self.attached = False
        return
    
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
            # now the drone column items below the attached block at droneY-1
            droneColumnItems = self.stateMap[droneColumnXZ][:droneY - 1] 
            if '' in droneColumnItems:
                # find first '' (empty) item bottoms up on the remaining column to take in the attached block to be released
                destY = droneColumnItems.index('')
                # now place attached block at droneY-1 at destY
                droneColumnItems[destY] = attachedBlock
                # mark previously attached block position at droneY-1 as '' (empty)
                self.stateMap[droneColumnXZ][droneY-1] = ''
                self.attached = False
                return True
            else:
                self.log('Column {} does not have free slots to take the release... not releasing!'.format(droneColumnXZ) )
                return False
    
    def revertRelease(self):
        if not self.attached:
            self.attached = True
            # un release                      
            droneColumnXZ = (self.dronePos[0], self.dronePos[1])
            droneColumnItems = self.stateMap[droneColumnXZ]
            droneY = self.dronePos[2]
            # find where the block would have been released on column below drone  
            relasedDestY = droneColumnItems.index('') - 1 # must be one below first empty bottoms up
            releasedBlock = droneColumnItems[releasedDestY]
            # now revert
            droneColumnItems[relasedDestY] = ''
            droneColumnItems[droneY-1] = releasedBlock            
        return
    
    def move(self, dx, dz, dy):
        # alt drone pos by dx, dz, dy
        origDronePos = self.dronePos
        self.dronePos = (origDronePos[0]+dx, origDronePos[1]+dz, origDronePos[2]+dy)
        self.stateMap[(self.dronePos[0], self.dronePos[1])][self.dronePos[2]] = 'd'
        self.stateMap[(origDronePos[0], origDronePos[1])][origDronePos[2]] = ''
        
        # alt attached block position if attached
        if self.attached:
            origPos = (origDronePos[0], origDronePos[1], origDronePos-1)
            newPos = (origPos[0]+dx, origPos[1]+dz, origPos[2]+dy)
            attacheBlock = self.stateMap[(origPos[0], origPos[1])][origPos[2]]
            
            self.stateMap[(newPos[0], newPos[1])][newPos[2]] = attachedBlock
            self.stateMap[(origPos[0], origPos[1])][origPos[2]] = ''
            
        return True
    
    def revertMove(self, dx, dz, dy):
         # alt drone pos by subtracting dx, dz, dy
        origDronePos = self.dronePos
        self.dronePos = (origDronePos[0]-dx, origDronePos[1]-dz, origDronePos[2]-dy)
        self.stateMap[(self.dronePos[0], self.dronePos[1])][self.dronePos[2]] = 'd'
        self.stateMap[(origDronePos[0], origDronePos[1])][origDronePos[2]] = ''
        
        # alt attached block position if attached by subtracting dx, dz, dy
        if self.attached:
            origPos = (origDronePos[0], origDronePos[1], origDronePos-1)
            newPos = (origPos[0]-dx, origPos[1]-dz, origPos[2]-dy)
            attacheBlock = self.stateMap[(origPos[0], origPos[1])][origPos[2]]
            
            self.stateMap[(newPos[0], newPos[1])][newPos[2]] = attachedBlock
            self.stateMap[(origPos[0], origPos[1])][origPos[2]] = ''
        return
    
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
        if droneY >= 1 and '' in droneColumnItems[:droneY - 1]:
            actions.append(('release',))
        
        # Finally find possible moves (in ideal world there are 27 such moves involving cartesian products of {-1}, {0}, {1})
        moves = set(product(set([-1,0,1]), repeat=3))
        # Now append to actions if we are allowed to make these moves
        for move in moves:
            dx, dz, dy = move
            # first check if drone move is within drone wolrd ranges
            if (droneX + dx >= self.Xrange[0] and droneX + dx <= self.Xrange[1]) and \
                (droneZ + dz >= self.Zrange[0] and droneZ + dz <= self.Zrange[1]) and \
                (droneY + dy >= self.Yrange[0] and droneY + dy <= self.Yrange[1]) and \
                (self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy] == '') :
                # if attached, check whether attached block (1 below drone) can also move to corresponding new position
                if self.attached and (self.stateMap[(droneX + dx, droneZ + dz)][droneY + dy - 1] is not '') :
                    continue                    
                else:
                    actions.append(('move', dx, dz, dy))
                    
        self.log("Possible actions {}".format(actions))            
        return actions
    
    # assumes a valid action returned by possibleActions
    def takeAction(self, action):
        # returns a tuple of True/False depending on success/failure status of action and step cost.
        # step cost is euclidean for move, 1 for release/attach
       
        status = False
        stepCost = -1.0
        self.log("Taking action {}".format(action[0]))
        if action[0] == 'attach':
            status = self.attach()
            stepCost = 1.0
        elif action[0] == 'release':
            status = self.release()
            stepCost = 1.0
        elif action[0] == 'move':
            actionStr, dx, dz, dy = action
            status = self.move(dx, dz, dy)
            stepCost = euclidean(self.dronePos, (self.dronePos[0]+dx, self.dronePos[1]+dz, self.dronePos[2]+dy))
        else:
            self.log('Invalid action requested!')            
        return (status, stepCost)
    
    # assumes a valid action taken previously - call order is important, either immediately after a corresponding previous
    # takeAction call or called in a reverse ordered sequence of multiple corresponding previous takenAction calls
    # also should be called only if previously called corresponding takeAction had returned status = True (success)
    def revertAction(self, action):
        self.log("Reverting action {}".format(action[0]))
        if action[0] == 'attach':
            self.attached = False
        elif action[0] == 'release':
            self.revertRelease()
        elif action[0] == 'move':
            actionStr, dx, dz, dy = action
            self.revertMove(dx, dz, dy)
        else:
            self.log('Invalid action requested to be reverted!')
        return
    
    def isGoal(self, goal):
        goalXZ = (goal[0], goal[1])
        goalY = goal[2]
        goalItem = goal[3]        
        return goalXZ in self.stateMap and len(self.stateMap[goalXZ])-1 >= goalY and self.stateMap[goalXZ][goalY] is goalItem
    
def goalTest(dwsim, goal):
    return dwsim.isGoal(goal)
