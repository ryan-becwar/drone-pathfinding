from simulator import *
import algos.recursiveBestFirstAstar as a



sim = Simulator.from_file("gamestates/simple")
print(sim.to_list())
s2 = Simulator(sim.state())
print(s2.to_list())
#locations = sim.to_list()
#dimensions = (s.WIDTH, s.LENGTH, s.HEIGHT)


#a.aStarSearch(s.state(), s.possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF)
