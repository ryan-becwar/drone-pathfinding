import simulator as s
import tools.generator as g
import tools.plot as p
import algos.recursiveBestFirstAstar as a
import algos.IDS as ids

#g.gen_file("gamestates/world100", 100)
sim = s.Simulator.from_file("gamestates/world100")
locations = sim.to_list()
dimensions = (s.WIDTH, s.LENGTH, s.HEIGHT)
p.plotBoard(locations, dimensions)


depthLimit = 10
ids.depthLimitedSearch(startState, goalState, possibleActionsF, resultingStateFromActionF, depthLimit)
a.aStarSearch(startState, possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF)
