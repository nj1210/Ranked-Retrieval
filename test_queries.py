import pickle
import numpy as np
import math
import operator


def print_topK_docs(sorted_scores):
    print()
    if len(sorted_scores)==0:
        print("No documents matching query found.")
    for i in range(min(50,len(sorted_scores))):
        print(f"id: {sorted_scores[i][0]:4} \ttitle: {id_title[sorted_scores[i][0]]:60} score:{sorted_scores[i][1]}")

def ranking(primIndex,queryIndex):

    no_doc=1614  #Total no of Docs


    scores={}
    normalize={}
    q_norm = 0
    for query_word in queryIndex:
        if primIndex.get(query_word,None) is None:
            continue
        df= (primIndex[query_word])[1]
        idf = math.log(no_doc/df,10)
        w_tq = idf * (1+math.log(queryIndex[query_word],10))
        q_norm += w_tq*w_tq
        word_list =(primIndex[query_word])[0]
        for i in range(len(word_list)):
            w_td = 1+ math.log (word_list[i][1],10)
            score_d = w_td * w_tq
            if word_list[i][0] in scores:
                scores[word_list[i][0]]= scores[word_list[i][0]] + score_d
            else:
                scores[word_list[i][0]]= score_d

    for doc_id in scores:
        normalize[doc_id]=0

    for word in primIndex:
        posting_list = primIndex[word][0]

        for i in range(len(posting_list)):
            if posting_list[i][0] in normalize:
                normalize[posting_list[i][0]]= normalize[posting_list[i][0]] + (1 + math.log(posting_list[i][1],10) )**2


#from collections import OrderedDict

    for doc_id in scores:
        scores[doc_id] = scores[doc_id]/(math.sqrt(q_norm)*math.sqrt(normalize[doc_id]))


    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    sorted_scores.reverse()
    return sorted_scores


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
	query = input("\n\nPlease enter the query.[Keep words space separated for better results]:\n")
	for word in query.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,queryIndex)
			continue
		for w in words:
			polish_word_and_update_index(w,queryIndex)


primIndex = readIndex("index")
id_title = readIndex("map")
queryIndex = {}
while True:
    input_and_process_query(queryIndex)
    #Call ranking methods here and display results.
    scores = ranking(primIndex,queryIndex)
    print_topK_docs(scores)

    if input("\nInput E to exit and any other key to enter another query: ").lower()=='e':
        break
