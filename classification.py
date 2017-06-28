
# AnyTree: Powerful and Lightweight Python Tree Data Structure with various plugins.
from anytree import Node, RenderTree, AsciiStyle
from anytree.dotexport import RenderTreeGraph
from anytree.iterators import PostOrderIter

#NLTK: NLTK is a leading platform for building Python programs to work with human language data. It provides easy-to-use interfaces to over 50 corpora and lexical resources such as WordNet, along with a suite of text processing libraries for classification, tokenization, stemming, tagging, parsing, and semantic reasoning, wrappers for industrial-strength NLP libraries, and an active discussion forum.

import nltk
from nltk.stem.porter import *
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords


import random
from collections import defaultdict

from rule import Rule
from antecedent import Antecedent
from consequent import Consequent

#Global Variables--------------------------------------------------------------------------------

#Current word index
word_index = 0

#antecedant and consequent indeces (Used in tree visualization)
antecedant_index=0
consequent_index=0
#------------------------------------------------------------------------------------------------


#List of keywords is the sentence that are described by a word (e.g: weather (sunny, rainy, ...)
keywords_described = defaultdict(list)

#List of keywords is the sentence that are boolean (e.g: starter turning (yes, no)
keywords_boolean = {}




#getToken(sentence): Returns the next word in a sentence, or -1 if End of statement--------------
def getToken(sentence):
	global word_index
	word_index=word_index+1
	sentence = sentence.split()
	if(word_index<=len(sentence)):
		return sentence[word_index-1]
	else:
		return -1
#------------------------------------------------------------------------------------------------


#backToken(): Returns the word index pointer 1 word behind---------------------------------------
def backToken():
	global word_index
	word_index=word_index-1
#------------------------------------------------------------------------------------------------





#Recursive Descent Parser------------------------------------------------------------------------
def S(sentence_index):
	#print ("In S")
	root = Node ("SENTENCE")
	#print ("Calling ANTECEDANT")
	ANTECEDANT(root)
	
	while True:
		CONJUNCTION(root)
		#ANTECEDANT called in CONJ
		tok = getToken(lst[sentence_index])
		#print "WHLE TRUE:" + tok
		if(tok != "AND" and tok != "OR"):
			backToken()
			break
		else:
			backToken()

	CONSEQUENT(root)
	return root


def ANTECEDANT(root):
	global antecedant_index
	antecedant_index = antecedant_index + 1
	#print ("IN ANTECEDANT")
	antecedant = Node(str("ANTECEDANT" + str(antecedant_index)), parent=root)
	#print ("Calling WORDS")
	WORDS(antecedant)


def WORDS(root):
	#print ("IN WORDS")
	token = getToken(lst[sentence_index])
	#print ("asa" + lst[sentence_index])
	#print(token)
	if(token == -1):
		return;
	if(token != "THEN" and token != "OR" and token != "AND"):
		Node(token, parent=root)
		#print ("calling WORDS")
		WORDS(root)
	else:
		backToken()

def CONJUNCTION(root):
	#print ("IN CONJUNCTION")
	token = getToken(lst[sentence_index])
	if(token == "AND" or token == "OR"):
		Node(token, parent=root)
		#print ("CALLING ANTECEDANT")
		ANTECEDANT(root)
	else:
		backToken()

def CONSEQUENT(root):
	#print ("IN CONSEQUENT")
	global consequent_index
	consequent_index = consequent_index + 1
	consequent = Node(str("CONSEQUENT" + str(consequent_index)), parent=root)
	token = getToken(lst[sentence_index])
	#print("CONS: "+token)
	if(token == "THEN"):
		#Node(token, parent=consequent)
		#print ("CALLING WORDS")
		WORDS(consequent)

#END RECURSIVE DESCENT PARSER -----------------------------------------------------------



#Traverse the tree to extract keywords---------------------------------------------
def extractKeywords(root):
	global keywords_described	
	global keywords_boolean
	rule = Rule()
	rule.reset()
	first = True
	firstName = ""
	antecedent = Antecedent()
	consequent = Consequent()
	for node in PostOrderIter(root):
		if(node.parent != None):
			if node.parent.name.find("ANTECEDANT") != -1:
				if(first):
					if(node.name not in keywords_described):
						keywords_described[node.name] = []
					antecedent.key = node.name
					#print "antecedent key: " + antecedent.key
					firstName = node.name
					first = False
				else:
					antecedent.val = node.name					
					rule.antecedent.append(antecedent)
					antecedent = Antecedent()
					keywords_described[firstName].append(node.name) 
					first = True
			if node.parent.name.find("CONSEQUENT") != -1:
					consequent.val = node.name
					rule.consequent.append(consequent)
					consequent = Consequent()

	#print(keywords_described)
	return rule
#----------------------------------------------------------------------------------

		


	


#Remove duplicates from the dictionary --------------------------------------------
def removeDuplicates(dictionary):
	for key, value in keywords_described.iteritems():
		withoutDuplicates = (set(value))
		del dictionary[key]
		dictionary[key] = withoutDuplicates
		
	return dictionary
#----------------------------------------------------------------------------------


#Pretty print a dictionary--------------------------------------------------------
def pretty(d, indent=0):
	for key, value in d.iteritems():
		print '\t' * indent + str(key)
		if isinstance(value, dict):
         		pretty(value, indent+1)
		else:
			print '\t' * (indent+1) + str(value)
#----------------------------------------------------------------------------------





#Combine negative words with their corresponding word: E.g: not turn => not-turn
def combineNegatives(sentence):
	negated = False

	for n,i in enumerate(sentence):
		#print ("In combineNegatives " + i)
		if(i == "NOT" or i == "NO"):
			negated = True
			continue
		if(negated):
			sentence[n] = "NOT-" + sentence[n]
			sentence.pop(n-1)
			negated = False
#----------------------------------------------------------------------------------





#STEMMING AND LEMMATIZING

stemmer = PorterStemmer()
wordnet_lemmatizer = WordNetLemmatizer()


#Accept input from the user (the paragraph)------------------------------------------------
stmt = raw_input("Enter a sentence: ")
#Remove commas from the sentence
stmt = stmt.replace(",","")

#Split the string into words
s = stmt.split()

#Lemmatize plural nouns
singles = [wordnet_lemmatizer.lemmatize(plural) for plural in s]
singles_str = ' '.join(singles)
#print (singles_str)


#print("\n\n\n")


#Lemmatize plural verbs
singles = [wordnet_lemmatizer.lemmatize(plural,wn.VERB) for plural in s]
singles_str = ' '.join(singles)
#print (singles_str)


operators = set(('and', 'or', 'not', 'then', 'no'))
stop = set(stopwords.words('english')) - operators
sentence = singles_str

a= [i for i in sentence.lower().split() if i not in stop]
a = [x.upper() for x in a]

combineNegatives(a)

a_joined = ' '.join(a)




lst = a_joined.split(".")


#print (a_joined) 
#print(len(lst))


#tagged = nltk.pos_tag(a)

#print(tagged)

tree = []

for sentence_index in range (len(lst)-1):
	tree.append(S(sentence_index))
	word_index = 0
	antecedant_index=0
	consequent_index=0
	#for pre, fill, node in RenderTree(tree[sentence_index]):
		#print("%s%s" % (pre, node.name))
	RenderTreeGraph(tree[sentence_index]).to_picture("tree_" + str(sentence_index) + ".png" )





keywords_described = removeDuplicates(keywords_described)


#pretty(keywords_described)

s = []
r=0



f = open('CLIPS_PROGRAM.clp', 'w')


for t in tree:
	s.append(extractKeywords(t))
	#s[r].display()
	f.write(s[r].generateCLIPSAction(r))
	r = r +1
	#print("\n\n\n\n")



Rule.generateCLIPSRules(s,f)

f.close()


#print(keywords_described)

#Traverse(tree[1])


#RenderTreeGraph(tree).to_dotfile("tree.dot")

#for pre, fill, node in RenderTree(tree):
#	print("%s%s" % (pre, node.name))
