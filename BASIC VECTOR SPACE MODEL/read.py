from bs4 import BeautifulSoup
import codecs
import pickle
import time
import os.path

#Updates the content index using the temporary index created for document.
def update_content_index(temp_index,content_index,doc_id):
	for word,tf in temp_index.items():
		wordDict = content_index.get(word,([],0))
		post = wordDict[0]
		post.append((doc_id,tf))
		content_index[word] = (post,wordDict[1]+1)

#Updates term frequency of a word in a document.
def update_doc_index(word,temp_index):
	temp_index[word] = temp_index.get(word,0) + 1

#Makes sure that words are purely made of lower case alphabets before updating index.
def polish_word_and_update_index(word,temp_index):
	word = word.lower()
	if word.isalpha():
		update_doc_index(word,temp_index)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
	if len(pol_word)>1:
		pol_word = ''.join(pol_word)
		update_doc_index(pol_word,temp_index)

#Reads a document and updates the index.
def index_doc(doc_id,doc_contents,content_index):
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
	update_content_index(temp_index,content_index,doc_id)


#Reads a file and updates the index
def parse_file(filename,content_index):
	global id_title
	#Reading all data from file "filename" stored in parent directory.
	with codecs.open(os.path.join(os.path.dirname(__file__),os.pardir,filename), encoding='utf-8') as f:
		data = f.read()

	#Initializing the BeautifulSoup object to the data read from the file.
	soup = BeautifulSoup(data,'html.parser')
	#Separates data among different doc tags.
	tags = soup.find_all('doc')

	for t in tags:						#For each document identified
		doc_id = int(t["id"])			#Document id
		doc_title = t["title"]			#Document title
		id_title[doc_id] = doc_title	#Mapping the document id and title
		doc_contents = t.get_text()		#Document contents
		#Indexing the contents of the document.
		index_doc(doc_id,doc_contents,content_index)


#Beginning of program.
print("\nStarting the indexing process.")
start = time.time()				#Noting start time for indexing.

content_index = {}				#The data structure for the index.
id_title = {}					#Map from doc ids to titles.

parse_file("wiki_00",content_index)	#Parsing the first file
parse_file("wiki_01",content_index)	#Parsing the second file
parse_file("wiki_02",content_index)	#Parsing the third file

no_docs = len(id_title)
end = time.time()				#Noting end time for indexing.

#Dumping the inverted index into binary file 'index' in pickle format (Not readable)
index_file = open('index', 'wb')
pickle.dump(content_index, index_file)
index_file.close()

#Dumping the id-name map into binary file 'map' in pickle format (Not readable)
id_file = open('map','wb')
pickle.dump(id_title, id_file)
id_file.close()

#Printing Indexing Statistics
print("\nIndex created and saved.")
print("\nNumber of documents parsed = "+str(no_docs))
print("Size of vocabulary = "+str(len(content_index)))
print("Time taken for parsing and indexing = "+str(end-start)+" seconds.")
