import random as random

def gen_file(filename, numBlocks=500000, maxBlocksPerColumn=50, blockColors=['red', 'green', 'blue', 'yellow']):
    stateMap = {}
    # it has <= 101x101 and >= minColumns(=numBlocks//maxBlocksPerColumn) columns of blocks - columns identified by (x, z) coordinates. 
    # every column has <= maxBlocksPerColumn blocks along the y axis 
    # has a drone at some randomly free (x, z, y) coordinate
    
    cntBlocksOnTable = 0
    while True:
        if cntBlocksOnTable == numBlocks:
            break
        randomColumnX = random.randint(-50,50)
        randomColumnZ = random.randint(-50,50)
        randomNumBlocksOnThisColumn = random.randint(0,maxBlocksPerColumn)
        if randomNumBlocksOnThisColumn > 0:
            if (randomColumnX, randomColumnZ) not in stateMap:
                stateMap[(randomColumnX, randomColumnZ)] = []
            for i in range(randomNumBlocksOnThisColumn):
                ## choose color randomly and place on this column
                stateMap[(randomColumnX, randomColumnZ)].append(random.choice(blockColors))            
                cntBlocksOnTable = cntBlocksOnTable + 1
                if cntBlocksOnTable == numBlocks:
                    break
        
    ## now place drone on any free slot
    foundDroneSlot = False
    while not foundDroneSlot:
        for column, columnBlocks in stateMap.items():
            if len(columnBlocks) < maxBlocksPerColumn:
                if (column[0], column[1]) not in stateMap:
                    stateMap[(column[0], column[1])] = []
                stateMap[(column[0], column[1])].append('d')
                foundDroneSlot = True
                break
                
        
    with open(filename, 'w') as out:
        out.writelines(['{0} {1} {2} {3}\n'.format(pillar[0], pillar[1], blkIdx, blk) 
                        for pillar, blkList in stateMap.items() for blkIdx, blk in enumerate(blkList)])

        
# test
gen_file("foo.txt", numBlocks=100, maxBlocksPerColumn=14)

