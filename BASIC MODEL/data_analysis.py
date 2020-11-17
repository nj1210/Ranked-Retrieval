from bs4 import BeautifulSoup
import codecs
import pickle

#Reads a file and updates the index    
def parseFile(filename,writefile):
	with codecs.open(filename, encoding='utf-8') as f:
		data = f.read()
	soup = BeautifulSoup(data,'html.parser')
	tags = soup.find_all('doc')	#Separates data among different doc tags.
	file1 = open(writefile, "a")  # append mode 
	for t in tags:
    		doc_id = int(t["id"])
    		#print("Working on doc - "+str(doc_id))
    		doc_title = t["title"]
    		file1.write(str(doc_id)+"\t\t"+doc_title+"\n") 
	file1.close()
		
file2 = open("data_description.txt", "w")
file2.close()
parseFile("wiki_00","data_description.txt")
parseFile("wiki_01","data_description.txt")
parseFile("wiki_02","data_description.txt")
