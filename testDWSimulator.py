from dwsimulator import *
from tools.generator import *

gen_file("foo.txt", numBlocks=100, maxBlocksPerColumn=14)

sim = DWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,50), filename='foo.txt', loglevel='verbose')

print(sim)

sim.attach()
print(sim)
sim.release()
