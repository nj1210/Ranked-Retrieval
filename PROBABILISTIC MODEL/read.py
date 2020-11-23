from bs4 import BeautifulSoup
import codecs
import pickle
import time
import math
import operator
import os.path

def get_av_len(lengths):
	sum = 0
	for doc,len in lengths.items():
		sum+=len
	return sum/no_docs

#Store the scores in the merged inverted index.
def calculate_score(content_index,title_index,content_factor,title_factor,Lav_content,Lav_title,doc_content_len,doc_title_len,k1,b):
	final_index = {}
	for word,tup in content_index.items():
		posting_list = tup[0]
		df = tup[1]
		idf = math.log( 1+((no_docs-df+0.5)/(df+0.5)) , 10)
		#Traversing the posting list.
		post = []
		for doc_id,tf_c in posting_list.items():
			tf_t = title_index.get(word,({},0))[0].get(doc_id,0)
			B_c = (1-b) + b*(doc_content_len[doc_id]/Lav_content)
			B_t = (1-b) + b*(doc_title_len[doc_id]/Lav_title)
			tf = (tf_t*title_factor/B_t)+(tf_c*content_factor/B_c)
			score = idf * (k1+1)*tf/(k1+tf)
			post.append((doc_id,score))
        #Storing the scores in the inverted index.
		final_index[word] = post

	for word,posting_list in final_index.items():
		#Sorting the documents in reverse order of their tf scores.
		posting_list.sort(key=operator.itemgetter(1),reverse=True)
		#Getting the champion list for the term by getting top 150 documents for current term.
		final_index[word] = posting_list[0:100]

	return final_index

#Updates the content index using the temporary index created for document.
def update_index(temp_index,content_index,doc_id,doc_len):
	doc_len[doc_id] = 0
	for word,tf in temp_index.items():
		doc_len[doc_id] += tf
		wordTuple = content_index.get(word,({},0))
		post = wordTuple[0]
		post[doc_id] = tf
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
def index_content(doc_id,doc_contents,content_index,doc_content_len):
	temp_index = {}
	for line in doc_contents.splitlines():
		for word in line.strip().split(" "):
			words = word.split("-")		#For '-' separated words.
			for w in words:
				polish_word_and_update_index(w,temp_index)

	#Update the content index using the temporary index created for document.
	update_index(temp_index,content_index,doc_id,doc_content_len)

#Reads a document title and updates the index.
def index_title(doc_id,doc_title,title_index,doc_title_len):
	temp_index = {}
	for word in doc_title.strip().split(" "):
		words = word.split("-")		#For '-' separated words.
		for w in words:
			polish_word_and_update_index(w,temp_index)

	#Update the title index using the temporary index created for document.
	update_index(temp_index,title_index,doc_id,doc_title_len)

#Reads a file and updates the index
def parse_file(filename,content_index,title_index,doc_content_len,doc_title_len):
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
        index_content(doc_id,doc_contents,content_index,doc_content_len)
        #Indexing the title of the document.
        index_title(doc_id,doc_title,title_index,doc_title_len)


#Beginning of program.
print("\nStarting the indexing process.")
start = time.time()         #Noting start time for indexing.

k1 = 1.2
b = 0.75

doc_content_len = {}		#Holds the lengths of contents of each document.
doc_title_len = {}			#Holds the lengths of titles of each document.
content_index = {}			#The data structure for the content index.
title_index = {}			#The data structure for the title index.
id_title = {}			    #Map from doc ids to titles.

parse_file("wiki_00",content_index,title_index,doc_content_len,doc_title_len)	#Parsing the first file
parse_file("wiki_01",content_index,title_index,doc_content_len,doc_title_len)	#Parsing the second file
parse_file("wiki_02",content_index,title_index,doc_content_len,doc_title_len)	#Parsing the third file

no_docs = len(id_title)
Lave_content = get_av_len(doc_content_len)
Lave_title = get_av_len(doc_title_len)

final_index = calculate_score(content_index,title_index,0.8,0.2,Lave_content,Lave_title,doc_content_len,doc_title_len,k1,b)

end = time.time()           #Noting end time for indexing.

#Dumping the content index into binary file 'index' in pickle format (Not readable)
index_file = open('index', 'wb')
pickle.dump(final_index, index_file)
index_file.close()

#Dumping the id-name map into binary file 'map' in pickle format (Not readable)
id_file = open('map','wb')
pickle.dump(id_title, id_file)
id_file.close()

#Printing Indexing Statistics
print("\nIndex created and saved.")
print("\nNumber of documents parsed = "+str(no_docs))
print("Size of content vocabulary = "+str(len(content_index)))
print("Size of title vocabulary = "+str(len(title_index)))
print("Time taken for parsing and indexing = "+str(end-start)+" seconds.\n")
