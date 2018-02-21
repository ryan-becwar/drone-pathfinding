import simulator as s
import algos.recursiveBestFirstAstar as a



sim = s.Simulator("gamestates/simple")
locations = sim.to_list()
dimensions = (s.WIDTH, s.LENGTH, s.HEIGHT)


a.aStarSearch(s.state(), s.possibleActionsF, resultingStateFromActionF, goalTestF, heuristicF)
