# https://gist.github.com/pbexe/7262a1082c6f13d230fd

from BlockSpec import *
from TowerSpec import *  

import nltk


def prepare(text):
	sentences = nltk.sent_tokenize(text)
	sentences = [nltk.word_tokenize(sent) for sent in sentences]
	sentences = [nltk.pos_tag(sent) for sent in sentences]
	return sentences

def clean(sentences):
	knownJJ = ['Red', 'Orange', 'Yellow', 'Green', 'Blue', 'Purple', 'Brown', 
		'Magenta', 'Tan', 'Cyan', 'Olive', 'Maroon', 'Navy', 'Aquamarine', 
		'Turquoise', 'Silver', 'Lime', 'Teal', 'Indigo', 'Violet', 'Pink', 
		'Black', 'White', 'Gray', 'Grey', 'height']

	knownNN = ['block', 'drone', 'tower'] 

	knownRB = ['coordinate', 'x-coordinate', 'y-coordinate', 'z-coordinate', 'top', 'bottom'] 

	c_sentences = []

	for sentence in sentences:
		c_sentence = []

		for tag in sentence:
			if tag[0] in knownJJ:
				c_sentence.append((tag[0], 'JJ'))
			elif tag[0] in knownNN:
				c_sentence.append((tag[0], 'NN'))
			elif tag[0] in knownRB:
				c_sentence.append((tag[0], 'RB'))
			else:
				c_sentence.append(tag)

		c_sentences.append(c_sentence)

	return c_sentences

def chunkTower(sentence):
	chunksToExtract = """
		CDCE: {<\(><CD><\)>}
		NCE: {<NN><IN>?<JJ><CD>}
			{<RB><CDCE>}
			{<JJ><NN><IN>?<RB>}"""

	parser = nltk.RegexpParser(chunksToExtract)
	result = parser.parse(sentence)
	
	for subtree in result.subtrees():
		if subtree.label() == 'NCE':
			t = subtree
			print(' '.join(word for word, pos in t.leaves()))
			print(' '.join(pos for word, pos in t.leaves()))
	
sentences = prepare("Build a tower of height 15 at coordinate (0,1) with a red block on top and a black block on bottom")
sentences = clean(sentences)

print(sentences)

for sentence in sentences:
	if len([tag for tag in sentence if tag[0] == 'tower']) > 0:
		chunkTower(sentence)