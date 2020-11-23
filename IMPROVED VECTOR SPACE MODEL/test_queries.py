import pickle
import numpy as np
import math
import operator
import time

#Printing the list of top 30 documents in decreasing order
def print_topK_docs(sorted_scores):
    print()
    if len(sorted_scores)==0:
        print("\nNo documents matching query found.")
        return
    print("\nList of the most relevant documents and their scores: ")
    for i in range(min(10,len(sorted_scores))):
        print(f"{i+1:2}. \tid: {sorted_scores[i][0]:4} \ttitle: {id_title[sorted_scores[i][0]]:60} score:{sorted_scores[i][1]}")

#Calculates final score for each document with respect to current query.
def mergeScores(content_scores,title_scores):
    title_factor = 0.20
    content_factor = 0.80
    scores = {}

    for key,con_score in content_scores.items():
        titleScore = title_scores.get(key,None)
        if titleScore is None:
            scores[key] = content_factor * con_score
        else:
            scores[key] = (content_factor * con_score) + (title_factor * titleScore)
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    sorted_scores.reverse()
    return sorted_scores

#Calculate score of each document with respect to current query.
def calculate_score(index,query_index):
    no_doc=len(id_title)  #Total no of Docs

    scores={}
    q_norm = 0
    for query_word in query_index:
        if index.get(query_word,None) is None:
            continue
        idf= (index[query_word])[1]
        w_tq = idf * (1+math.log(query_index[query_word],10))
        q_norm += w_tq*w_tq
        word_list =(index[query_word])[0]
        for i in range(len(word_list)):
            w_td = word_list[i][1]
            score_d = w_td * w_tq
            scores[word_list[i][0]]= scores.get(word_list[i][0],0) + score_d

    q_norm = math.sqrt(q_norm)
    #Query Normalization. Scores stored in index are already Document normalized.
    for doc_id in scores:
        scores[doc_id] = scores[doc_id]/q_norm

    return scores

#Read index/map from pickle file.
def readIndex(filename):
	index_file = open(filename, "rb")
	index = pickle.load(index_file)
	index_file.close()
	return index

#Updates term frequency of a word in the query index.
def update_query_index(word,query_index):
    word = word.lower()
    query_index[word] = query_index.get(word,0) + 1

#Makes sure that words are purely made of alphabets before updating index.
def polish_word_and_update_index(word,query_index):
	if word.isalpha():
		update_query_index(word,query_index)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
	if len(pol_word)>0:
		pol_word = ''.join(pol_word)
		update_query_index(pol_word,query_index)

#Inputs a query and processes it to populate the query index.
def input_and_process_query(query_index):
	query = input("\nPlease enter the query.[Keep words space separated for better results]:\n")
	if len(query) < 1 :
		print("Invalid query")
		return
	for word in query.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,query_index)
			continue
		for w in words:
			polish_word_and_update_index(w,query_index)

#Reading the content index, title index and id-title map.
content_index = readIndex("index")
id_title = readIndex("map")
title_index = readIndex("titleIndex")

while True:
    query_index = {}
    input_and_process_query(query_index)
    #Ranking documents and display results.
    start = time.time()
    content_scores = calculate_score(content_index,query_index)
    title_scores = calculate_score(title_index,query_index)
    scores = mergeScores(content_scores,title_scores)
    end = time.time()
    print("\nResults obtained in "+str(end-start)+" seconds.")
    print_topK_docs(scores)

    #To break out from the loop/continue.
    if input("\nInput E to exit and any other key to enter another query: ").lower()=='e':
        break
