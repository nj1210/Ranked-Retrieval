import pickle
import os.path
#Reading the index from the pickle file.
index_file = open("index", "rb")
primIndex = pickle.load(index_file)
index_file.close()

print(len(primIndex))
#Printing the content index.
for key,val in primIndex.items():
	print("Word:"+key+"\t\tidf: "+str(val[0]))

print("\n\nSize of vocabulary = "+str(len(primIndex))+".")
