import simulator as s
import tools.plot as p

sim = s.Simulator("gamestates/simple")
locations = sim.to_list()
dimensions = (s.WIDTH, s.LENGTH, s.HEIGHT)
p.plotBoard(locations, dimensions)