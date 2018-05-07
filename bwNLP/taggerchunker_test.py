
import taggerchunker as tc

texts=[]
texts.append("A tower of height 5 at position ( 0, 1 ) with a red colored block in position 0 and a block of color red in position 4.")
texts.append("A tower 5 blocks high at (0,1) with a red block in the bottom and black block in the top.")
texts.append("A tower 5 blocks tall at (0,1) with a red block in the bottom and black block in the top.")
texts.append("A tower of height 2 at coordinate (0,0) with a block of color black above a red colored block.")
texts.append("2 blocks at coordinate (0,0) with a black colored block on a block of color red.")
texts.append("A tower of height 2 at (0,0) with a block of color red under a black colored block at top.")
texts.append("A tower of height 2 at (0,0) with a red colored block under a block of color black at position 1.")
texts.append("A tower of height 2 at (0,0) with a block of color black on top and a red colored block below it.")
texts.append("A tower of height 2 at (0,0) with a black colored block at position 1 having a block of color red below it.")
texts.append("A tower of height 2 at -50,-49 with a block of color black at position 1 and a block of color red below the black colored block.")
texts.append("17 blocks in a single column.")
texts.append("All blocks in a single column.")
texts.append("Every block in a single column.")
texts.append("Seventeen blocks in a single column")
texts.append("In position 20,-19 stack 17 blocks in a column.")
texts.append("In position 20,-19 stack 17 blocks.")

for text in texts:    
    taggedText = tc.getTaggedTextForChunking(text)
    chunkParsedTree = tc.chunk_text(taggedText)
    print(chunkParsedTree)
   
    # for subtree in chunkParsedTree.subtrees(): 
    #         print(subtree)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()