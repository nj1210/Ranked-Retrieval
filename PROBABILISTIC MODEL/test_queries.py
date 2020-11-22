import pickle
import numpy as np
import math
import operator
import time

#Printing the list of top 30 documents in decreasing order
def print_topK_docs(sorted_scores):
    print()
    if len(sorted_scores)==0:
        print("No documents matching query found.")
        return
    print("List of relevant documents and their scores: ")
    for i in range(min(30,len(sorted_scores))):
        print(f"{i:2}. \tid: {sorted_scores[i][0]:4} \ttitle: {id_title[sorted_scores[i][0]]:60} score:{sorted_scores[i][1]}")

#Calculate score of each document with respect to current query.
def calculate_score(index,query_index,k3):
    scores={}
    for query_word in query_index:
        if index.get(query_word,None) is None:
            continue
        w_tq = query_index[query_word]*(k3+1)/(query_index[query_word]+k3)
        posting_list = index[query_word]
        for i in range(len(posting_list)):
            w_td = posting_list[i][1]
            score_d = w_td * w_tq
            scores[posting_list[i][0]]= scores.get(posting_list[i][0],0) + score_d
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    sorted_scores.reverse()
    return sorted_scores

#Read index/map from pickle file.
def read_index(filename):
	index_file = open(filename, "rb")
	inv_index = pickle.load(index_file)
	index_file.close()
	return inv_index

#Updates term frequency of a word in the query index.
def update_query_index(word,query_index):
	query_index[word] = query_index.get(word,0) + 1

#Makes sure that words are purely made of alphabets before updating index.
def polish_word_and_update_index(word,query_index):
	word = word.lower()
	if word.isalpha():
		update_query_index(word,query_index)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
	if len(pol_word)>1:
		pol_word = ''.join(pol_word)
		update_query_index(pol_word,query_index)

def input_and_process_query(query_index):
	query = input("\nPlease enter the query.[Keep words space separated for better results]:\n")
	for word in query.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,query_index)
			continue
		for w in words:
			polish_word_and_update_index(w,query_index)


inv_index = read_index("index")
id_title = read_index("map")
k3 = 1.4

while True:
    query_index = {}
    input_and_process_query(query_index)
    start = time.time()
    scores = calculate_score(inv_index,query_index,k3)
    end = time.time()
    print("\nResults obtained in "+str(end-start)+" seconds.")
    print_topK_docs(scores)

    if input("\nInput E to exit and any other key to enter another query: ").lower()=='e':
        break
