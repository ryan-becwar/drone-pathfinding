
import taggerchunker as tc

texts=[]
texts.append("A tower of height 5 at position ( 0, 1 ) with a red block in position 0 and black block in position 4.")
texts.append("A tower 5 blocks high at (0,1) with a red block in the bottom and black block in the top.")
texts.append("A tower 5 blocks tall at (0,1) with a red block in the bottom and black block in the top.")
texts.append("A tower of height 2 at coordinate (0,0) with a black block above a red block.")
texts.append("17 blocks in a single column.")
texts.append("All blocks in a single column.")
texts.append("Every block in a single column.")
texts.append("Seventeen blocks in a single column")

for text in texts:    
    taggedText = tc.getTaggedTextForChunking(text)
    chunkParsedTree = tc.chunk_text(taggedText)
    print(chunkParsedTree)
   
    # for subtree in chunkParsedTree.subtrees(): 
    #         print(subtree)
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print()