import pickle
import numpy as np

def readIndex(filename):
	index_file = open(filename, "rb")
	primIndex = pickle.load(index_file)
	index_file.close()
	return primIndex

def update_query_index(word,queryIndex):
	queryIndex[word] = queryIndex.get(word,0) + 1

def polish_word_and_update_index(word,queryIndex):
	word = word.lower()
	if word.isalpha():
		update_query_index(word,queryIndex)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
	if len(pol_word)>1:
		pol_word = ''.join(pol_word)
		update_query_index(pol_word,queryIndex)

def input_and_process_query(queryIndex):
	query = input("Please enter the query.[Keep words space separated for better results]:\n")
	for word in query.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,queryIndex)
			continue
		for w in words:
			polish_word_and_update_index(w,queryIndex)


primIndex = readIndex("index")			
queryIndex = {}
while True:
	input_and_process_query(queryIndex)
	
	#Call ranking methods here and display results.
	
	if input("Input E to exit and any other key to enter another query: ").lower()=='e':
		break
		
