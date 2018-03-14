
import random as random

def gen_file(filename, numBlocks=500000, maxBlocksPerColumn=50, 
             Xrange=(-50,50), Zrange=(-50,50), Yrange=(0,50), blockColors=['r', 'g', 'b', 'y']):
    if maxBlocksPerColumn <=0 and maxBlocksPerColumn > Yrange[1]:
        print('Invalid max # of blocks requested for chosen Y range!')
        return
    if numBlocks > (abs(Xrange[0])+abs(Xrange[1]) + 1)*(abs(Zrange[0])+abs(Zrange[1]) + 1)*maxBlocksPerColumn:        
        print("Invalid # blocks {} requested for chosen (X,Z) ranges.. only {} blocks at max can be fitted!".format(
             numBlocks, (abs(Xrange[0])+abs(Xrange[1]) + 1)*(abs(Zrange[0])+abs(Zrange[1]) + 1)*maxBlocksPerColumn))
        return
    stateMap = {}
    # it has <= 101x101 and >= minColumns(=numBlocks//maxBlocksPerColumn) columns of blocks - columns identified by (x, z) coordinates. 
    # every column has <= maxBlocksPerColumn blocks along the y axis 
    # has a drone at some randomly free (x, z, y) coordinate
    
    cntBlocksOnTable = 0
    while True:
        #print("Blocks on table", cntBlocksOnTable)
        if cntBlocksOnTable == numBlocks:
            break
        randomColumnX = random.randint(Xrange[0],Xrange[1])
        randomColumnZ = random.randint(Zrange[0],Zrange[1])        
        randomNumBlocksOnThisColumn = random.randint(0,maxBlocksPerColumn)
        if randomNumBlocksOnThisColumn > 0 :
            if (randomColumnX, randomColumnZ) not in stateMap:
                stateMap[(randomColumnX, randomColumnZ)] = []
            randomColumnOfBlocks = stateMap[(randomColumnX, randomColumnZ)]
            if (len(randomColumnOfBlocks) + randomNumBlocksOnThisColumn <= maxBlocksPerColumn) :
                for i in range(randomNumBlocksOnThisColumn):
                    ## choose color randomly and place on this column
                    randomColumnOfBlocks.append(random.choice(blockColors))            
                    cntBlocksOnTable = cntBlocksOnTable + 1
                    if cntBlocksOnTable == numBlocks:
                        #print("Got to {} blocks on table breaking from inner for loop".format(cntBlocksOnTable))
                        break
        
    ## now place drone on any free slot
    foundDroneSlot = False
    while not foundDroneSlot:
        for column, columnBlocks in stateMap.items():
            if len(columnBlocks) < maxBlocksPerColumn + 1:
                if (column[0], column[1]) not in stateMap:
                    stateMap[(column[0], column[1])] = []
                stateMap[(column[0], column[1])].append('d')
                foundDroneSlot = True
                break                
        
    with open(filename, 'w') as out:
        out.writelines(['{0} {1} {2} {3}\n'.format(pillar[0], pillar[1], blkIdx, blk) 
                        for pillar, blkList in stateMap.items() for blkIdx, blk in enumerate(blkList)])