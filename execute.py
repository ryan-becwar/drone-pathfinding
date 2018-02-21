import simulator as s
import tools.plot as p
import algos.recursiveBestFirstAstar as a
import algos.IDS as ids

sim = s.Simulator("gamestates/simple")
locations = sim.to_list()
dimensions = (s.WIDTH, s.LENGTH, s.HEIGHT)
p.plotBoard(locations, dimensions)


depthLimit = 10
ids.depthLimitedSearch(startState, goalState, possibleActionsF, resultingStateFromActionF, depthLimit)
a.aStarSearch(startState, possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF)