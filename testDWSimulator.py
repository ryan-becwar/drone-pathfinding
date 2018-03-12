from dwsimulator import *
from tools.generator import *

gen_file("foo.txt", numBlocks=100, maxBlocksPerColumn=14)

sim = DWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,50), filename='foo.txt', loglevel='verbose')

print(sim)
print('goalTest(42 -24 0 b)', goalTest(sim, (42, -24, 0, 'b')))
print('goalTest(42 -24 49 b)', goalTest(sim, (42, -24, 49, 'b')))

sim.attach()
print(sim)
sim.release()

gen_file("3x3x1.txt", numBlocks=9, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))
f = open('3x3x1.txt', 'r')
file_contents = f.read()
print(file_contents)
f.close()

sim3x3x1 = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='3x3x1.txt', loglevel='verbose')

print(sim3x3x1)

sim3x3x1.release()

print(sim3x3x1.dronePos)

for action in sim3x3x1.possibleActions():
    sim3x3x1.takeAction(action)
    print(sim3x3x1)
    sim3x3x1.revertAction(action)
    print(sim3x3x1)


