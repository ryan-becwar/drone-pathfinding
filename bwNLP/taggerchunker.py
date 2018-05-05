
import nltk

knownBlockColorJJs = ['violet', 'indigo', 'blue', 'green', 'yellow', 'red', 'white', 'black']
knownTowerJJs = ['tall', 'high', 'height']

blkRegexPattern = nltk.re.compile(r'block(\.|,)?$')

blksRegexPattern = nltk.re.compile(r'blocks(\.|,)?$')

xzPosRegex = r'((\(\s*)?)((\-)?[0-9]+,\s*(\-)?[0-9]+)((\s*\))?)'
xzPosRegexPattern = nltk.re.compile(xzPosRegex)

xzyPosRegex = r'(\(\s*)?(\-)?[0-9]+,\s*(\-)?[0-9]+,\s*[0-9]+(\s*\))?'
xzyPosRegexPattern = nltk.re.compile(xzyPosRegex)

def preprocess_text(text):    
    def clean_coordinates(matchobj):
        cleaned = matchobj.group(0).replace(' ', '')
        return cleaned 
    
    lowerText = text.lower()    
    cleanedText = nltk.re.sub(xzyPosRegex, clean_coordinates, nltk.re.sub(xzPosRegex, clean_coordinates, lowerText))
    if cleanedText.endswith('.'):        
        cleanedText = cleanedText[:len(cleanedText)-1]
    
    return cleanedText

def tokenize_text(cleanedText):
#     tokenizedText = nltk.word_tokenize(cleanedText)
    tokenizedText = cleanedText.split()
    return tokenizedText

def pos_tag_text(tokenizedText):
    posTaggedText=nltk.pos_tag(tokenizedText)
    return posTaggedText

def custom_tag(posTaggedText):
    customTaggedText = []
    for posTaggedTuple in posTaggedText: 
        token = posTaggedTuple[0]
        if xzyPosRegexPattern.match(token):
            tag ='XZYPOS'
        elif xzPosRegexPattern.match(token):
            tag = 'XZPOS'
        elif posTaggedTuple[0] in knownBlockColorJJs:
            tag = 'BLKCOLOR'
        elif blkRegexPattern.match(posTaggedTuple[0]):
            matched = blkRegexPattern.match(posTaggedTuple[0])
#             print(matched.group(0))            
            tag = 'BLK'
        elif blksRegexPattern.match(posTaggedTuple[0]):
            matched = blksRegexPattern.match(posTaggedTuple[0])
#             print(matched.group(0))   
            tag = 'BLKS'
        else:
            tag = posTaggedTuple[1]
            
        customTaggedText.append((token, tag))
    return customTaggedText

def getTaggedTextForChunking(text):
    print(text)

    preprocessedText = preprocess_text(text)
    print("Preprocessed\n", preprocessedText)

    tokenizedText = tokenize_text(preprocessedText)

    posTaggedText = pos_tag_text(tokenizedText)
    print("POS tagged\n", posTaggedText)

    taggedText = custom_tag(posTaggedText)
    print("Custom tagged\n", taggedText)
    
    return taggedText

#TOWERSPEC: {<DT|IN>?<JJ.*|NN.*|IN|DT>*<CD>*<JJ.*|NN.*|IN|DT>*<XZPOS>}
grammar = r"""
              
              BLKCOLORSPEC: {<DT|IN>?<BLKCOLOR><BLK>}
              RELATIVEBLKSPEC: {<BLKCOLORSPEC><IN|JJR|RBR><BLKCOLORSPEC>} 
              NUMERICBLKSPEC: {<BLKCOLORSPEC><IN|DT>*<NN.*|JJ.*>*<CD|XZYPOS>}
              TEXTBLKSPEC: {<BLKCOLORSPEC><IN|DT>*<NN>}
              BLKSPEC: {<NUMERICBLKSPEC|TEXTBLKSPEC>}
              BLKSSPEC: {<DT|NN|CD><BLKS>+}
              TOWERPOSSPEC: {<DT|IN|NN|CC>*<XZPOS>}
              TOWERHTSPECINBLKS: {<BLKSSPEC><JJ|VBP|IN|JJR|RBR>}
              TOWERHTSPECRAW: {<DT|IN>?<NN><IN>*<JJ|JJR|RBR><CD>}            
              
           """
cp = nltk.RegexpParser(grammar) 

def chunk_text(taggedText):
    chunkParsedTree = cp.parse(taggedText)
    return chunkParsedTree