
class BlockSpec:
    def __init__(self):
        self.x = '?'
        self.z = '?'
        self.y = '?'
        self.name = '?'
    
    def __repr__(self):
        return repr(self.x) + " " + repr(self.z) + " " + repr(self.y) + " " + repr(self.name)
    
    def equals(self, other):
        return self.x == other.x and self.z == other.z and self.y == other.y and self.name == other.name
    
class RelativeBlockSpec:
    def __init__(self):
        self.blockSpec1 = BlockSpec()
        self.relation = ''
        self.blockSpec2 = BlockSpec()
        
    def __repr__(self):
        return repr(self.blockSpec1) + " " + repr(self.relation) + repr(self.blockSpec2)
        
class TowerSpec:
    def __init__(self):
        self.blockSpecs = []
        self.height = 0
        self.location = ('?','?')
        
    def __repr__(self):
        return repr(self.location) + '=>' + repr(self.blockSpecs)
        
class Spec:
    def __init__(self):
        self.blockSpecs = []
        self.towerSpecs = []
        self.towerHeight = None
        self.relativeBlockSpecs = []
    
    def __repr__(self):
        out =''
        
#         if len(self.blockSpecs) > 0 :
#             out = out + 'Blocks\n'
        for blockSpec in self.blockSpecs:
            out = out + repr(blockSpec) + '\n'
            
#         if len(self.relativeBlockSpecs) > 0 :
#             out = out + 'Relative Blocks\n'
#         for relativeBlockSpec in self.relativeBlockSpecs:
#             out = out + repr(relativeBlockSpec) + '\n'
            
#         if len(self.towerSpecs) > 0 :
#             out = out + 'Towers\n'
#         for towerSpec in self.towerSpecs:
#             out = out + repr(towerSpec) + '\n'
        
#         out = out + 'Tower ht ' + repr(self.towerHeight)
        return out
    
    def blockSpecExists(self, inputBlockSpec):
        for blockSpec in self.blockSpecs:
            if blockSpec.equals(inputBlockSpec):
                return True
        return False
    
    def finalize(self, initialBWState):
        # if no specific block color or position specified
        if len(self.blockSpecs) == 0:
            # process cases of just tower height 
            if self.towerHeight is not None and int(self.towerHeight) > 0:
                for i in range(int(self.towerHeight)):
                    blockSpec = BlockSpec()
                    blockSpec.y = str(i)
                    self.blockSpecs.append(blockSpec)                
            
        for towerSpec in self.towerSpecs:
            xz=towerSpec.location.split(',')
            for blockSpec in self.blockSpecs:
                blockSpec.x = xz[0]
                blockSpec.z = xz[1]
                
        # process non numeric blk positions
        for blockSpec in self.blockSpecs:
            if blockSpec.y in ['top', 'atop', 'last']:
                blockSpec.y = int(self.towerHeight) -1
            if blockSpec.y in ['bottom', 'first']:
                blockSpec.y = '0'
        
        # process relatives
        for relativeBlockSpec in self.relativeBlockSpecs:
            if relativeBlockSpec.relation in ['above', 'over', 'atop', 'higher']:
                if int(self.towerHeight) == 2:
                    relativeBlockSpec.blockSpec1.y = '1'
                    relativeBlockSpec.blockSpec2.y = '0'
                else:
                    relativeBlockSpec.blockSpec1.y = str(int(relativeBlockSpec.blockSpec2.y) + 1)
            if relativeBlockSpec.relation in ['below', 'under', 'beneath', 'lower']:
                if int(self.towerHeight) == 2:
                    relativeBlockSpec.blockSpec1.y = '0'
                    relativeBlockSpec.blockSpec2.y = '1'
                else:
                    relativeBlockSpec.blockSpec1.y = str(int(relativeBlockSpec.blockSpec2.y) -1)
        
        return 

#################################################

def processBlkColorSpecTree(tree, spec, parent):
    blockSpec = BlockSpec()
    colors = [leaf[0] for leaf in tree.leaves() if leaf[1] == 'BLKCOLOR']
    if len(colors) > 0:
        blockSpec.name = colors[0]    
    ypositions = []
    if parent.label() == 'NUMERICBLKSPEC':
        ypositions = [leaf[0] for leaf in parent.leaves() if leaf[1] == 'CD']        
    elif parent.label() == 'TEXTBLKSPEC':
        ypositions = [leaf[0] for leaf in parent.leaves() if leaf[1] in ['NN', 'JJ', 'JJR', 'VBR']]
    if len(ypositions) > 0 :
            blockSpec.y = ypositions[0]
            
    if not spec.blockSpecExists(blockSpec):
        spec.blockSpecs.append(blockSpec) 
    return blockSpec

def processBlkSpecTree(tree, spec):     
    if tree.label() == 'BLKCOLORSPEC':
        return processBlkColorSpecTree(tree, spec, parent = tree)
    elif tree.label() == 'BLKSPEC':
        return processBlkColorSpecTree(tree[0][0], spec, parent = tree[0])
    return BlockSpec()          

def processRelativeBlkSpecTree(tree, spec):
    # find children trees first to instantiate the blocks first     
    relativeBlockSpec = RelativeBlockSpec()
    relativeBlockSpec.blockSpec1 = processBlkSpecTree(tree[0], spec)
    relativeBlockSpec.blockSpec2 = processBlkSpecTree(tree[2], spec)
    relativeBlockSpec.relation = tree[1][0]    
    spec.relativeBlockSpecs.append(relativeBlockSpec)    
    return

def processRelativeBlkSpecPossesiveTree(tree, spec):
    relativeBlockSpec = RelativeBlockSpec()    
    relativeBlockSpec.blockSpec2 = processBlkSpecTree(tree[0], spec)
    relativeBlockSpec.blockSpec1 = processBlkSpecTree(tree[2], spec)
    relativeBlockSpec.relation = tree[3][0]
    spec.relativeBlockSpecs.append(relativeBlockSpec)
    return
    
def processTowerPosTree(tree, spec):
    xzpositions = [leaf[0] for leaf in tree.leaves() if leaf[1] == 'XZPOS']
    if len(xzpositions) > 0:
        towerSpec = TowerSpec()
        towerSpec.location = xzpositions[0]
        spec.towerSpecs.append(towerSpec)

def processTowerHtTree(tree, spec):
    if tree.label() == 'TOWERHTSPECRAW':
        heights = [leaf[0] for leaf in tree.leaves() if leaf[1] == 'CD'] 
        if len(heights) > 0:
            spec.towerHeight = heights[0]
    elif tree.label() == 'TOWERHTSPECINBLKS':
        for subtree in tree:
            try:
                if subtree.label() == 'BLKSSPEC':
                    blkCnt = processBlksSpecTree(subtree)
                    if  blkCnt is not None:
                        spec.towerHeight = blkCnt 
            except AttributeError:
                continue
    return

def processBlksSpecTree(tree):
    blkCnts = [leaf[0] for leaf in tree.leaves() if leaf[1] in ['CD', 'NN', 'DT']]
    return blkCnts[0] if len(blkCnts)>0 else None
    
def traverse(tree, spec):
    for subtree in tree: 
        try:
            if subtree.label() == 'RELATIVEBLKSPEC':
                processRelativeBlkSpecTree(subtree, spec)
            
            elif subtree.label() == 'RELATIVEBLKSPECPOSSESIVE':
                processRelativeBlkSpecPossesiveTree(subtree, spec)
            
            elif subtree.label() == 'BLKSPEC':
                processBlkSpecTree(subtree, spec)
                
            elif subtree.label() == 'TOWERPOSSPEC':
                processTowerPosTree(subtree, spec)
                
            elif subtree.label() == 'BLKSSPEC':
                processBlksSpecTree(subtree)
                
            elif subtree.label() == 'TOWERHTSPECRAW':
                processTowerHtTree(subtree, spec)
                
            elif subtree.label() == 'TOWERHTSPECINBLKS':
                processTowerHtTree(subtree, spec)               
            
        except AttributeError:
            continue
    spec.finalize(initialBWState=None)
    return