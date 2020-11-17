from bs4 import BeautifulSoup
import codecs
import pickle
import time
import math

def normalize(index):
    norm = {}
    for word,tup in index.items():
        posting_list = tup[0]
        df = tup[1]
        idf = math.log(no_docs/df,10)
        for i in range(len(posting_list)):
            doc_id = posting_list[i][0]
            tf = posting_list[i][1]
            norm[doc_id] = norm.get(doc_id,0) + (tf**2)
        index[word] = (posting_list,idf)
    
    for doc_id in norm:
    	norm[doc_id] = math.sqrt(norm[doc_id])
    	
    for word,tup in index.items():
        posting_list = tup[0]
        for i in range(len(posting_list)):
            doc_id = posting_list[i][0]
            wt = posting_list[i][1]
            new_wt = wt/norm[doc_id]
            posting_list[i] = (doc_id,new_wt)

#Updates the primary index using the temporary index created for document.
def update_primary_index(tempIndex,primIndex,doc_id):
	for word,tf in tempIndex.items():
		wordTuple = primIndex.get(word,([],0))
		post = wordTuple[0]
		post.append((doc_id, 1+math.log(tf)))
		primIndex[word] = (post,wordTuple[1]+1)

#Updates term frequency of a word in a document.
def update_doc_index(word,tempIndex):
	global stopWords
	if len(word)==1 or word not in stopWords:
		word = word.lower()
		tempIndex[word] = tempIndex.get(word,0) + 1
	else:
		word = word.upper()
		tempIndex[word] = tempIndex.get(word,0) + 1

#Makes sure that words are purely made of alphabets before updating index.
def polish_word_and_update_index(word,tempIndex):
	if word.isalpha():
		update_doc_index(word,tempIndex)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
	if len(pol_word)>0:
		pol_word = ''.join(pol_word)
		update_doc_index(pol_word,tempIndex)

#Reads a document and updates the index.
def readDoc(doc_id,doc_contents,primIndex):
	tempIndex = {}
	for line in doc_contents.splitlines():
		for word in line.strip().split(" "):
			words = word.split("-")		#For '-' separated words.
			if len(words)==1:
				polish_word_and_update_index(word,tempIndex)
				continue
			for w in words:
				polish_word_and_update_index(w,tempIndex)

	#Update the primary index using the temporary index created for document.
	update_primary_index(tempIndex,primIndex,doc_id)

def readDocTitle(doc_id,doc_title,titleIndex):
	tempIndex = {}
	for word in doc_title.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,tempIndex)
			continue
		for w in words:
			polish_word_and_update_index(w,tempIndex)

	#Update the primary index using the temporary index created for document.
	update_primary_index(tempIndex,titleIndex,doc_id)

#Reads a file and updates the index
def parseFile(filename,primIndex,titleIndex):
	global id_title
	with codecs.open(filename, encoding='utf-8') as f:
		data = f.read()
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.find_all('doc')	#Separates data among different doc tags.
	global no_docs
	for t in tags:
    		doc_id = int(t["id"])
    		#print("Reading document id: "+str(doc_id))
    		doc_title = t["title"]
    		id_title[doc_id] = doc_title
    		doc_contents = t.get_text()
    		readDoc(doc_id,doc_contents,primIndex)
    		readDocTitle(doc_id,doc_title,titleIndex)
    		no_docs+=1

print("Starting the indexing process.")
start = time.time()
no_docs = 0

stopWords = ['ourselves', 'hers', 'between', 'yourself', 'but', 'again', 'there', 'about', 'once', 'during', 'out', 'very', 'having', 'with', 'they', 'own', 'an', 'be', 'some', 'for', 'do', 'its', 'yours', 'such', 'into', 'of', 'most', 'itself', 'other', 'off', 'is', 's', 'am', 'or', 'who', 'as', 'from', 'him', 'each', 'the', 'themselves', 'until', 'below', 'are', 'we', 'these', 'your', 'his', 'through', 'don', 'nor', 'me', 'were', 'her', 'more', 'himself', 'this', 'down', 'should', 'our', 'their', 'while', 'above', 'both', 'up', 'to', 'ours', 'had', 'she', 'all', 'no', 'when', 'at', 'any', 'before', 'them', 'same', 'and', 'been', 'have', 'in', 'will', 'on', 'does', 'yourselves', 'then', 'that', 'because', 'what', 'over', 'why', 'so', 'can', 'did', 'not', 'now', 'under', 'he', 'you', 'herself', 'has', 'just', 'where', 'too', 'only', 'myself', 'which', 'those', 'i', 'after', 'few', 'whom', 't', 'being', 'if', 'theirs', 'my', 'against', 'a', 'by', 'doing', 'it', 'how', 'further', 'was', 'here', 'than']

primIndex = {}				#The data structure for the content index.
titleIndex = {}			#The data structure for the title index.
id_title = {}				#Map from doc ids to titles.
parseFile("wiki_00",primIndex,titleIndex)	#Parsing the first file
parseFile("wiki_01",primIndex,titleIndex)	#Parsing the second file
parseFile("wiki_02",primIndex,titleIndex)	#Parsing the third file

normalize(primIndex)
normalize(titleIndex)

end = time.time()

#Dumping the dictionary into binary file 'index' in pickle format (Not readable)
index_file = open('index', 'wb')
pickle.dump(primIndex, index_file)
index_file.close()

id_file = open('map','wb')
pickle.dump(id_title, id_file)
id_file.close()

title_file = open('titleIndex','wb')
pickle.dump(titleIndex, title_file)
title_file.close()

print("\nIndex created and saved in 'index' file.")
print("\nNumber of documents parsed = "+str(no_docs))
print("Size of content vocabulary = "+str(len(primIndex)))
print("Size of title vocabulary = "+str(len(titleIndex)))
print("Time taken for parsing and indexing = "+str(end-start)+" seconds.")

