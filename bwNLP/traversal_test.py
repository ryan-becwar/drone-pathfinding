import taggerchunker as tc
import treetraversal as tt
texts=[]
texts.append("A tower of height 16 at position ( 0, 1 ) with a red block in position 0 and black block in position 15.")
texts.append("A tower of height 16 at position ( 0, 1 ) with a black block at top and red block in bottom.")
texts.append("2 blocks at coordinate (0,0) with a black block on top and a red block in bottom.")
texts.append("A tower of height 2 at (0,0) with a black block above a red block.")
texts.append("A tower of height 3 at (0,0) with a red colored block below a block of color black at position 1.")
texts.append("A tower of height 3 at (0,0) with a black colored block above a block of color red at position 0.")
texts.append("A tower of height 3 at (0,0) with a black colored block at position 1 having a block of color red below it.")
texts.append("A tower of height 3 at (0,0) with a red colored block at position 0 having a block of color black above it.")
texts.append("A tower of height 3 at (0,0) with a block of color black at position 1 and a block of color red below the black colored block.")
texts.append("A tower of height 3 at (0,0) with a block of color red at position 0 and a block of color black above the black colored block.")
texts.append("17 blocks in a single column.")
texts.append("In position 19, -20 stack 17 blocks.")

for text in texts:
    taggedText = tc.getTaggedTextForChunking(text)
    chunkParsedTree = tc.chunk_text(taggedText)
    print(chunkParsedTree)

    # for subtree in chunkParsedTree.subtrees(): 
    #          print(subtree.label())
    # print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    # print()
    # chunkParsedTree.draw()
    spec = tt.Spec()
    tt.traverse(chunkParsedTree, spec)

    print(spec)