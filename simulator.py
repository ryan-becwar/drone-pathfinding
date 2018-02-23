from copy import deepcopy
import numpy as np
WIDTH = 11 #x dimension
LENGTH = 11 #z dimension
HEIGHT = 5 #y dimension (vertical)

def euclidean(source, dest):
    return np.sqrt((source[0]-dest[0])**2 + (source[1]-dest[1])**2 + (source[2]-dest[2])**2)

class Simulator:
    def __init__(self, state):
        self.map = state[0]
        self.attached = state[1]
        self.currentStateMap = state[2]
        self.drone_pos = self.find_drone()

    @classmethod
    def from_file(cls, filename):
        map, stateMap = cls.initialize(filename)
        obj = cls((map, False, stateMap))
        return obj

    def __hash__(self):
        return hash((str(self.map), self.attached))

    def __eq__(self, other):
        return (str(self.map), self.attached) == (str(other.map), other.attached)

    def __ne__(self,other):
        return not(self == other)

    
    #TODO: check if configuration is valid, no floating blocks
    def initialize(filename):
        map = [[[" " for y in range(HEIGHT)] for z in range(LENGTH)] for x in range(WIDTH)]
        currentStateMap = {}
        
        with open(filename, 'r') as file_in:
            for line in file_in.readlines():
                data = line.split()
                x, z, y, item = (int(data[0]), int(data[1]), int(data[2]), data[3])
                map[x][z][y] = item
                if (int(data[0]), int(data[1])) not in currentStateMap:
                    currentStateMap[(int(data[0]), int(data[1]))] = [' ' for i in range(HEIGHT)]
                currentStateMap[(int(data[0]), int(data[1]))][int(data[2])] = data[3]
        return (map, currentStateMap)


    def writeout(self, filename):
        with open(filename, 'w') as out:
            out.writelines(['{0} {1} {2} {3}\n'.format(item[0], item[1], item[2], item[3]) for item in self.to_list()])

    def state(self):
         return (self.map, self.attached, self.currentStateMap)

    def attach(self):
        if self.attached:
            print("Drone already attached")
            return

        x, z, y = self.drone_pos
        
        if y > 0:
            if self.map[x][z][y-1] != " ":
                self.attached = True
            else:
                print("No block below drone")
        else:
            print("Drone is on floor")

        return (self.to_list(), self.attached)

    def move_block(self, startpos, endpos):
        x0, z0, y0 = startpos
        x1, z1, y1 = endpos
        if self.map[x0][z0][y0] == ' ' or self.map[x0][z0][y0] == 'd':
            print("No block at starting position", startpos)
            return self.to_list()
        if self.map[x1][z1][y1] != ' ' and self.map[x1][z1][y1] != 'd':
            print("Ending position not empty", endpos)
            return self.to_list()
        below = self.map[x1][z1][:y1] #list of all blocks below destination
        if 'd' in below or ' ' in below:
            print("Destination not supported by blocks", endpos, "src: ", startpos,  "column: ", below, self.currentStateMap)
            return self.to_list()

        #update blocks in statemap
        self.currentStateMap[(x0,z0)][y0] = ' '
        if (x1,z1) not in self.currentStateMap:
            self.currentStateMap[(x1,z1)]=[' ' for i in range(HEIGHT)]
        self.currentStateMap[(x1,z1)][y1] = self.map[x0][z0][y0]

        #update in map
        self.map[x1][z1][y1] = self.map[x0][z0][y0]
        self.map[x0][z0][y0] = ' '
        return self.to_list()


    def move(self, dx, dy, dz):
        if abs(dx) > 1 or abs(dy) > 1 or abs(dz) > 1:
            print("Invalid move magnitude: %s", (dx, dy, dz))
            return (self.to_list(), self.attached)
        
        x, z, y = self.drone_pos
        xn, zn, yn = x+dx, z+dz, y+dy
        
        if 0 <= xn < WIDTH and 0 <= zn < LENGTH and 0 <= yn < HEIGHT and (not self.attached or 0 <= (yn-1)): #drone inbounds
            if not (self.map[xn][zn][yn] == " " or ((dx, dy, dz) == (0,-1,0) and self.attached)):
                print("Collision: %s", (xn, yn, zn))
                return (self.to_list(), self.attached)
            if not (not self.attached or self.map[xn][zn][yn-1] == " " or (dx, dy, dz) == (0,1,0)):
                print("Block collision: %s", (xn, yn-1, zn))
                return (self.to_list(), self.attached)

            #swap drone first if moving up
            if(dy >= 0):
                #drone swap
                self.currentStateMap[(x,z)][y] = ' '
                if (xn,zn) not in self.currentStateMap:
                    self.currentStateMap[(xn,zn)]=[' ' for i in range(HEIGHT)]
                self.currentStateMap[(xn,zn)][yn] = self.map[x][z][y]

                #swap drone position
                self.map[x][z][y], self.map[xn][zn][yn] = self.map[xn][zn][yn], self.map[x][z][y]

                self.drone_pos = (xn, zn, yn)

                if(self.attached):
                    #block swap
                    # update currentStateMap first before block swap
                    self.currentStateMap[(x,z)][y-1] = ' '
                    if (xn,zn) not in self.currentStateMap:
                        self.currentStateMap[(xn,zn)]=[' ' for i in range(HEIGHT)]
                    self.currentStateMap[(xn,zn)][yn-1] = self.map[x][z][y-1]
                    
                    #swap block below                    
                    self.map[x][z][y-1], self.map[xn][zn][yn-1] = self.map[xn][zn][yn-1], self.map[x][z][y-1] 
            else:
                if(self.attached):
                    #block swap
                    # update currentStateMap first before block swap
                    self.currentStateMap[(x,z)][y-1] = ' '
                    if (xn,zn) not in self.currentStateMap:
                        self.currentStateMap[(xn,zn)]=[' ' for i in range(HEIGHT)]
                    self.currentStateMap[(xn,zn)][yn-1] = self.map[x][z][y-1]
                    
                    #swap block below                    
                    self.map[x][z][y-1], self.map[xn][zn][yn-1] = self.map[xn][zn][yn-1], self.map[x][z][y-1] 

                #drone swap
                self.currentStateMap[(x,z)][y] = ' '
                if (xn,zn) not in self.currentStateMap:
                    self.currentStateMap[(xn,zn)]=[' ' for i in range(HEIGHT)]
                self.currentStateMap[(xn,zn)][yn] = self.map[x][z][y]

                #swap drone position
                self.map[x][z][y], self.map[xn][zn][yn] = self.map[xn][zn][yn], self.map[x][z][y]

                self.drone_pos = (xn, zn, yn)

        else:
            print("Move out of bounds: ", (xn, zn, yn), " Position: ", self.drone_pos, " Attached: ", self.attached)

        return (self.to_list(), self.attached)

    def release(self):
        if not self.attached:
            print("No block attached")
            return

        x, z, y = self.drone_pos
        self.attached = False

        below = self.map[x][z][:y-1] #list of all blocks two below drone
            
        if " " in below:
            drop = below.index(" ")
            # update currentStateMap first before swap due to release
            self.currentStateMap[(x,z)][drop] = self.map[x][z][y-1]
            self.currentStateMap[(x,z)][y-1] = ' '

            self.map[x][z][y-1], self.map[x][z][drop] = self.map[x][z][drop], self.map[x][z][y-1] 
        
        return

    def speak(self, string):
        print(string)
       
        return

    def take_action(self, action):
        dx, dy, dz, type = action

        if type == "move":
            return self.move(dx, dy, dz)
        elif type == "attach":
            return self.attach()
        elif type == "release":
            return self.release()
        else:
            print("Invalid move: ", action)
            return

    def take_block_action(self, action):
        return self.move_block((action[0][0], action[0][1], action[0][2]), action[1])

    #Algorithm interaction methods
    def goalTest(self, goal):
        x, z, y, color = goal
        if self.map[x][z][y] == color:
            return True
        else:
            return False

    def resultingStateFromAction(self, action):
        temp_sim = Simulator(deepcopy(self.state()))
        temp_sim.take_action(action)
        #x0, z0, y0, _ = action[0]
        #x1, z1, y1 = action[1]
        #dist = max(abs(x0 - x1), abs(z0 - z1), abs(y0 -y1))
        #return (temp_sim, dist)
        return (temp_sim, 0)

    def possibleActions(self):
        return self.possible_commands()

    #internal helper methods
    def find_drone(self):
        for x in range(len(self.map)):
            for z in range(len(self.map[x])):
                if "d" in self.map[x][z]:
                    self.drone_pos = (x,z,self.map[x][z].index("d"))
                    return self.drone_pos

        return (-1,-1,-1)

    def space_empty(self, x, z, y):
        return self.map[x][z][y] == " " or self.map[x][z][y] == "d"
    def space_taken(self, x, z, y):
        return y == -1 or (self.map[x][z][y] != " " and self.map[x][z][y] != "d")
    def pillar_height(self, x, z):
        for x in range(len(self.map)):
            for z in range(len(self.map[x])):
                for y in range(len(self.map[x][z])):
                    if space_empty(x, z, y):
                        return y

    #returns the state as a list of objects
    def to_list(self):
        return([(x, z, y, self.map[x][z][y]) for x in range(len(self.map)) for z in range(len(self.map[x])) for y in range(len(self.map[x][z])) if self.map[x][z][y] != " "])

    #returns the list of top-level blocks on the map
    def top_level_blocks(self):
        return [(x, z, y, self.map[x][z][y]) for x in range(len(self.map)) for z in range(len(self.map[x])) for y in range(len(self.map[x][z])) if self.space_taken(x, z, y) and self.space_empty(x, z, y + 1)]

    #return a list of positions on the map that a block could be placed, ignoring the position that block is already
    def top_level_positions(self, ignore):
        return [(x, z, y) for x in range(len(self.map)) for z in range(len(self.map[x])) for y in range(len(self.map[x][z])) if (x, z) != ignore and self.space_empty(x, z, y) and self.space_taken(x, z, y - 1)]

    def possible_block_moves(self):
        actions = []
        for top_level in self.top_level_blocks():
            for position in self.top_level_positions((top_level[0], top_level[1])):
                actions.append((top_level, position))
        return actions

    def resultingStateFromBlockAction(self, action):
        temp_sim = Simulator(deepcopy(self.state()))
        temp_sim.take_block_action(action)
        return (temp_sim, 1.0) #TODO: Update cost to vary with action

    #returns the list of possible commands in tuple format based on current state (dx, dy, dz, "action")
    def possible_commands(self):
        x, z, y = self.drone_pos
        actions = []
        
        # consider all drone move combinations
        for dx in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dy in [-1, 0, 1]:                                        
                    if (dx, dy, dz) == (0, 0, 0): # if no movement in drone, consider possible actions
                        #actions.append((dx, dy, dz, "")) # do nothing

                        if self.attached:
                            actions.append((dx, dy, dz, "release"))
                        
                        elif self.map[x][z][y-1] != " ":
                            actions.append((dx, dy, dz, "attach"))
                    
                    else: # drone is moving, check for collisions
                        xn, zn, yn = x+dx, z+dz, y+dy

                        if 0 <= xn < WIDTH and 0 <= zn < LENGTH and 0 <= yn < HEIGHT and (not self.attached or 0 <= (yn-1)): #drone inbounds
                            if self.attached: # Check for block and drone collisions 
                                if (dx, dy, dz) == (0, -1, 0): # drone is going vertically down and will take the attached block position
                                    if self.map[xn][zn][yn-1] == " ": # no collisions with block
                                        actions.append((dx, dy, dz, "move"))
                                else:
                                    if self.map[xn][zn][yn] == " " and (self.map[xn][zn][yn-1] == " " or self.map[xn][zn][yn-1] == "d"): # no collisions with drone or block
                                        actions.append((dx, dy, dz, "move"))
                                                                        
                            else: # Check for drone collisions
                                if self.map[xn][zn][yn] == " ": # no collisions with drone
                                    actions.append((dx, dy, dz, "move"))
                        
        return actions
