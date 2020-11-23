import pickle
import numpy as np
import math
import operator
import time

#Printing the list of top 10 documents in decreasing order
def print_topK_docs(sorted_scores):
    print()
    if len(sorted_scores)==0:
        print("No documents matching query found.")
        return
    print("List of relevant documents and their scores: ")
    for i in range(min(10,len(sorted_scores))):
        print(f"id: {sorted_scores[i][0]:4} \ttitle: {id_title[sorted_scores[i][0]]:60} score:{sorted_scores[i][1]}")

#Calculating the normalization factor for each document.
def calculate_doc_norm_factor(index):
    norm={}

    for word in index:
        posting_list = index[word][0]
        for i in range(len(posting_list)):
            norm[posting_list[i][0]] = norm.get(posting_list[i][0],0) + (1 + math.log(posting_list[i][1],10) )**2

    for id,val in norm.items():
        norm[id] = math.sqrt(val)
    return norm

#Calculate score of each document with respect to current query.
def calculate_score(index,query_index,doc_norm):
    no_doc=len(id_title)  #Total no of Docs

    scores={}
    q_norm = 0
    for query_word in query_index:
        if index.get(query_word,None) is None:
            continue
        df= (index[query_word])[1]
        idf = math.log(no_doc/df,10)
        w_tq = idf * (1+math.log(query_index[query_word],10))
        q_norm += w_tq*w_tq
        word_list =(index[query_word])[0]
        for i in range(len(word_list)):
            w_td = 1+ math.log (word_list[i][1],10)
            score_d = w_td * w_tq
            scores[word_list[i][0]]= scores.get(word_list[i][0],0) + score_d

    q_norm = math.sqrt(q_norm)

    #Query and Document Normalization
    for doc_id in scores:
        scores[doc_id] = scores[doc_id]/(q_norm*doc_norm[doc_id])

    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    sorted_scores.reverse()
    return sorted_scores

#Read index/map from pickle file.
def readIndex(filename):
	index_file = open(filename, "rb")
	primIndex = pickle.load(index_file)
	index_file.close()
	return primIndex

#Updates term frequency of a word in the query index.
def update_query_index(word,query_index):
	query_index[word] = query_index.get(word,0) + 1

#Makes sure that words are purely made of lower case alphabets before updating index.
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

#Takes a query input and processes the query to populate the query_index
def input_and_process_query(query_index):
	query = input("\nPlease enter the query.[Keep words space separated for better results]:\n")
	for word in query.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,query_index)
			continue
		for w in words:
			polish_word_and_update_index(w,query_index)

#Beginning of program.
primIndex = readIndex("index")      #Reading the index file.
id_title = readIndex("map")         #Reading the id-title map file.

#Calculating the document normalization factors.
norm = calculate_doc_norm_factor(primIndex)

while True:
    query_index = {}
    #Input and process query.
    input_and_process_query(query_index)
    #Rank documents and display results.
    start = time.time()
    scores = calculate_score(primIndex,query_index,norm)
    end = time.time()
    print("\nResults obtained in "+str(end-start)+" seconds.")
    print_topK_docs(scores)

    #To break out from the loop/continue.
    if input("\nInput E to exit and any other key to enter another query: ").lower()=='e':
        break
