import pickle

#Reading the index from the pickle file.
index_file = open("index", "rb")
primIndex = pickle.load(index_file)
index_file.close()

#Printing it.
for key,val in primIndex.items():
	print(key+":")
	print("\tDF = "+str(val[1]))
	print("\tPosting List: "+str(val[0]))
	
print("\n\nSize of vocabulary = "+str(len(primIndex))+".")
