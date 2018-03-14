from dwsimulator import *
from tools.generator import *

gen_file('simfiles/foo.txt', numBlocks=100, maxBlocksPerColumn=14)

print("sim = DWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,50), filename='simfiles/foo.txt', loglevel='verbose')")
sim = DWSimulator(Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,50), filename='simfiles/foo.txt', loglevel='verbose')

print(sim)
print('goalTest(42 -24 0 b)', goalTest(sim, (42, -24, 0, 'b')))
print('goalTest(42 -24 49 b)', goalTest(sim, (42, -24, 49, 'b')))

sim.attach()
print(sim)
sim.release()

print("gen_file('simfiles/3x3x1Full.txt', numBlocks=9, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))")

#gen_file('simfiles/3x3x1Full.txt', numBlocks=9, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))
f = open('simfiles/3x3x1Full.txt', 'r')
file_contents = f.read()
print(file_contents)
f.close()

print("sim3x3x1Full = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1Full.txt', loglevel='verbose')")
sim3x3x1Full = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1Full.txt', loglevel='verbose')

print(sim3x3x1Full)

sim3x3x1Full.release()

for action in sim3x3x1Full.possibleActions():
    sim3x3x1Full.takeAction(action)
    print(sim3x3x1Full)
    sim3x3x1Full.revertAction(action)
    print(sim3x3x1Full)

sim3x3x1Full.release()

print("Let's attach and verify that we can't move, can't release, basically zero possible actions.")

sim3x3x1Full.attach()

for action in sim3x3x1Full.possibleActions():
    sim3x3x1Full.takeAction(action)
    print(sim3x3x1Full)
    sim3x3x1Full.revertAction(action)
    print(sim3x3x1Full)

print("Good. Now let's try to keep some room for drone move with attached block by initializing a DW sim with 8 blocks in same 3x3x1 world.")

print("gen_file('simfiles/3x3x1SomeRoom.txt', numBlocks=8, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))")

#gen_file("simfiles/3x3x1SomeRoom.txt", numBlocks=8, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))
f = open('simfiles/3x3x1SomeRoom.txt', 'r')
file_contents = f.read()
print(file_contents)
f.close()

print("sim3x3x1SomeRoom = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1SomeRoom.txt', loglevel='verbose')")

sim3x3x1SomeRoom = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1SomeRoom.txt', loglevel='verbose')

print(sim3x3x1SomeRoom)

for action in sim3x3x1SomeRoom.possibleActions():
    sim3x3x1SomeRoom.takeAction(action)
    print(sim3x3x1SomeRoom)
    sim3x3x1SomeRoom.revertAction(action)
    print(sim3x3x1SomeRoom)

print("now attach and try - at least one move should be possible. Right?")

sim3x3x1SomeRoom.attach()

print(sim3x3x1SomeRoom)

for action in sim3x3x1SomeRoom.possibleActions():
    sim3x3x1SomeRoom.takeAction(action)
    print(sim3x3x1SomeRoom)
    sim3x3x1SomeRoom.revertAction(action)
    print(sim3x3x1SomeRoom)

print("Let's reduce the number of blocks further and see if we have some possible moves with drone attached.")

print("gen_file('simfiles/3x3x1MoreRoom.txt', numBlocks=6, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))")

#gen_file('simfiles/3x3x1MoreRoom.txt', numBlocks=6, maxBlocksPerColumn=1, Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1))
f = open('simfiles/3x3x1MoreRoom.txt', 'r')
file_contents = f.read()
print(file_contents)
f.close()

print("sim3x3x1MoreRoom = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1MoreRoom.txt', loglevel='verbose')")


sim3x3x1MoreRoom = DWSimulator(Xrange=(-1,1), Zrange=(-1,1), Yrange=(0,1), filename='simfiles/3x3x1MoreRoom.txt', loglevel='verbose')

print(sim3x3x1MoreRoom)

sim3x3x1MoreRoom.attach()

for action in sim3x3x1MoreRoom.possibleActions():
    sim3x3x1MoreRoom.takeAction(action)
    print(sim3x3x1MoreRoom)
    sim3x3x1MoreRoom.revertAction(action)
    print(sim3x3x1MoreRoom)

