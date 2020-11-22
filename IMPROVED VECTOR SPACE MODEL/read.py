from bs4 import BeautifulSoup
import codecs
import pickle
import time
import math
import operator
import os.path

#Normalizes the index
def normalize(index):
    norm = {}
    for word,tup in index.items():
        posting_list = tup[0]
        df = tup[1]
        idf = math.log(no_docs/df,10)
        #Traversing the posting list.
        for i in range(len(posting_list)):
            doc_id = posting_list[i][0]
            tf = posting_list[i][1]
            #Updating the normalization factor for the document.
            norm[doc_id] = norm.get(doc_id,0) + (tf**2)
        #Storing the idf value in the inverted index instead of df.
        index[word] = (posting_list,idf)

    #Getting the value of normalization factor for each document.
    for doc_id in norm:
    	norm[doc_id] = math.sqrt(norm[doc_id])

    #Normalizing the scores of each term-document pair.
    for word,tup in index.items():
        posting_list = tup[0]
        for i in range(len(posting_list)):
            doc_id = posting_list[i][0]
            wt = posting_list[i][1]
            new_wt = wt/norm[doc_id]
            posting_list[i] = (doc_id,new_wt)
        #Sorting the documents in reverse order of their tf scores.
        posting_list.sort(key=operator.itemgetter(1),reverse=True)
        #Getting the champion list for the term by getting top 150 documents for current term.
        index[word] = (posting_list[0:150],tup[1])

#Updates the content index using the temporary index created for document.
def update_index(temp_index,content_index,doc_id):
	for word,tf in temp_index.items():
		wordTuple = content_index.get(word,([],0))
		post = wordTuple[0]
		post.append((doc_id, 1+math.log(tf)))
		content_index[word] = (post,wordTuple[1]+1)

#Updates term frequency of a word in a document.
def update_temp_index(word,temp_index):
	temp_index[word] = temp_index.get(word,0) + 1

#Makes sure that words are purely made of alphabets before updating index.
def polish_word_and_update_index(word,temp_index):
    word = word.lower()        #Converting word to lower case.
    #If word only has alphabet characters, update index.
    if word.isalpha():
        update_temp_index(word,temp_index)
        return
	#If word has non-alphabet characters, remove them first.
    pol_word = []
    for c in word:
        if c.isalpha():
            pol_word.append(c)
    if len(pol_word)>0:
        pol_word = ''.join(pol_word)
        update_temp_index(pol_word,temp_index)

#Reads a document and updates the index.
def index_content(doc_id,doc_contents,content_index):
	temp_index = {}
	for line in doc_contents.splitlines():
		for word in line.strip().split(" "):
			words = word.split("-")		#For '-' separated words.
			if len(words)==1:
				polish_word_and_update_index(word,temp_index)
				continue
			for w in words:
				polish_word_and_update_index(w,temp_index)

	#Update the content index using the temporary index created for document.
	update_index(temp_index,content_index,doc_id)

#Reads a document title and updates the index.
def index_title(doc_id,doc_title,title_index):
	temp_index = {}
	for word in doc_title.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		if len(words)==1:
			polish_word_and_update_index(word,temp_index)
			continue
		for w in words:
			polish_word_and_update_index(w,temp_index)

	#Update the title index using the temporary index created for document.
	update_index(temp_index,title_index,doc_id)

#Reads a file and updates the index
def parse_file(filename,content_index,title_index):
    global id_title
    #Reading all data from file "filename".
    with codecs.open(os.path.join(os.path.dirname(__file__),os.pardir,filename), encoding='utf-8') as f:
        data = f.read()
    #Initializing the BeautifulSoup object to the data read from the file.
    soup = BeautifulSoup(data,'html.parser')
    #Separating data among different doc tags.
    tags = soup.find_all('doc')
    for t in tags:                     #For each document identified
        doc_id = int(t["id"])          #Document id
        doc_title = t["title"]         #Document title
        id_title[doc_id] = doc_title   #Mapping the document id and title
        doc_contents = t.get_text()    #Document contents
        #Indexing the contents of the document.
        index_content(doc_id,doc_contents,content_index)
        #Indexing the title of the document.
        index_title(doc_id,doc_title,title_index)


#Beginning of program.
print("Starting the indexing process.")
start = time.time()         #Noting start time for indexing.

content_index = {}			#The data structure for the content index.
title_index = {}			#The data structure for the title index.
id_title = {}			    #Map from doc ids to titles.

parse_file("wiki_00",content_index,title_index)	#Parsing the first file
parse_file("wiki_01",content_index,title_index)	#Parsing the second file
parse_file("wiki_02",content_index,title_index)	#Parsing the third file

no_docs = len(id_title)

normalize(content_index)    #Normalizing the content scores
normalize(title_index)      #Normalizing the title scores

end = time.time()           #Noting end time for indexing.

#Dumping the content index into binary file 'index' in pickle format (Not readable)
index_file = open('index', 'wb')
pickle.dump(content_index, index_file)
index_file.close()

#Dumping the id-name map into binary file 'map' in pickle format (Not readable)
id_file = open('map','wb')
pickle.dump(id_title, id_file)
id_file.close()

#Dumping the title index into binary file 'title_index' in pickle format (Not readable)
title_file = open('titleIndex','wb')
pickle.dump(title_index, title_file)
title_file.close()

#Printing Indexing Statistics
print("\nIndex created and saved.")
print("\nNumber of documents parsed = "+str(no_docs))
print("Size of content vocabulary = "+str(len(content_index)))
print("Size of title vocabulary = "+str(len(title_index)))
print("Time taken for parsing and indexing = "+str(end-start)+" seconds.\n")
