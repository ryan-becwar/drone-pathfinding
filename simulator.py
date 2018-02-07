class Simulator:
    def __init__(self, state):
        self.state = state
        self.attached = False

    
    def initialize(filename):
        return

    def state(self):
        return self.state

    def attach():
        return

    def move(dx, dy, dz):
        return

    def release():
        return

    def speak(string):
        print(string)
        return



WIDTH = 11 #x dimension
LENGTH = 11 #z dimension
HEIGHT = 5 #y dimension (vertical)

startState = [[[" " for y in range(HEIGHT)] for z in range(LENGTH)] for x in range(WIDTH)]

startState[5][5][0] = "d"
print(startState)
sim = Simulator(startState)

print(sim)
