from bs4 import BeautifulSoup
import codecs
import pickle

#Updates the primary index using the temporary index created for document.
def update_primary_index(tempIndex,primIndex,doc_id):
	for word,tf in tempIndex.items():
		wordDict = primIndex.get(word,([],0))
		post = wordDict[0]
		post.append((doc_id,tf))
		primIndex[word] = (post,wordDict[1]+1)
		
#Updates term frequency of a word in a document.
def update_doc_index(word,tempIndex):
	tempIndex[word] = tempIndex.get(word,0) + 1
	
#Makes sure that words are purely made of alphabets before updating index.
def polish_word_and_update_index(word,tempIndex):
	word = word.lower()
	if word.isalpha():
		update_doc_index(word,tempIndex)
		return
	#If word has non-alphabet characters, remove them.
	pol_word = []
	for c in word:
		if c.isalpha():
			pol_word.append(c)
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

#Reads a file and updates the index    
def parseFile(filename,primIndex):
	with codecs.open(filename, encoding='utf-8') as f:
		data = f.read()
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.find_all('doc')	#Separates data among different doc tags.
	global no_docs 
	for t in tags:
    		doc_id = int(t["id"])
    		print("Reading document id: "+str(doc_id))
    		doc_title = t["title"]
    		doc_contents = t.get_text()
    		readDoc(doc_id,doc_contents,primIndex)
    		no_docs+=1
	
no_docs = 0
primIndex = {}				#The data structure for the index.  		
parseFile("wiki_00",primIndex)	#Parsing the first file
parseFile("wiki_01",primIndex)	#Parsing the second file
parseFile("wiki_02",primIndex)	#Parsing the third file

#Dumping the dictionary into binary file 'index' in pickle format (Not readable)
index_file = open('index', 'wb')
pickle.dump(primIndex, index_file) 
index_file.close() 

print("\nNumber of documents read = "+str(no_docs))
print("Index created and saved in 'index' file.")
