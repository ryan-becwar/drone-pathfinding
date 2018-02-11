WIDTH = 11 #x dimension
LENGTH = 11 #z dimension
HEIGHT = 5 #y dimension (vertical)

class Simulator:
    def __init__(self, filename):
        self.initialize(filename)
        self.attached = False
        self.drone_pos = self.find_drone()

    
    #TODO: check if configuration is valid, no floating blocks
    def initialize(self, filename):
        self.map = [[[" " for y in range(HEIGHT)] for z in range(LENGTH)] for x in range(WIDTH)]
        with open(filename, 'r') as file_in:
            for line in file_in.readlines():
                data = line.split()
                x,z,y,item = (int(data[0]), int(data[1]), int(data[2]), data[3])
                self.map[x][z][y] = item

    def writeout(self, filename):
        with open(filename, 'w') as out:
            out.writelines(['{0} {1} {2} {3}\n'.format(item[0], item[1], item[2], item[3]) for item in self.to_list()])

    def state(self):
        return self.map

    def attach(self):
        x, z, y = self.find_drone()#change to drone_pos once move implemented

        if z > 0:
            if self.map[x][z][y-1] != "d" and self.map[x][z][y-1] != " ":
                self.attached = True
            else:
                print("No block below drone")

        return


    def move(self, dx, dy, dz):
        if abs(dx) > 1 or abs (dy) > 1 or abs (dz) > 1:
            print("Invalid move magnitude: %s", (dx, dy, dz))
            return
        
        x,z,y = self.drone_pos
        xn,zn,yn = x+dx, z+dz, y+dy
        if 0 <= xn < WIDTH and 0 <= zn < LENGTH and 0 <= yn < HEIGHT and (not self.attached or 0 <= yn -1): #drone inbounds
            if not (self.map[xn][zn][yn] == " " or ((dx, dy, dz) == (0,-1,0) and self.attached)):
                print("Collision: %s", (xn, yn, zn))
                return
            if self.attached:
                if self.map[xn][zn][yn-1] == " " or (dx, dy, dz) == (0,1,0):
                    self.map[x][z][y-1], self.map[xn][zn][yn-1] = self.map[xn][zn][yn-1], self.map[x][z][y-1] #swap block below
                else:
                    print("Block collision: %s", (xn, yn-1, zn))
                    return

            self.map[x][z][y], self.map[xn][zn][yn] = self.map[xn][zn][yn], self.map[x][z][y] #swap drone position
            self.drone_pos = (xn, zn, yn)
        else:
            print("Move out of bounds: %s", (xn, yn, zn))

        return

    def release(self):
        if self.attached:
            x, z, y = self.find_drone() #change to drone_pos once move implemented
            self.attached = False

            below = self.map[x][z][:y-1] #list of all blocks two below drone
            if " " in below:
                drop = below.index(" ")
                self.map[x][z][y-1], self.map[x][z][drop] = self.map[x][z][drop], self.map[x][z][y-1] 

        return

    def speak(string):
        print(string)
        return

    #internal helper methods
    def find_drone(self):
        for x in range(len(self.map)):
            for z in range(len(self.map[x])):
                if "d" in self.map[x][z]:
                    self.drone_pos = (x,z,self.map[x][z].index("d"))
                    return self.drone_pos

        return (-1,-1,-1)

    #returns the state as a list of objects
    def to_list(self):
        return([(x, z, y, self.map[x][z][y]) for x in range(len(self.map)) for z in range(len(self.map[x])) for y in range(len(self.map[x][z])) if self.map[x][z][y] != " "])

