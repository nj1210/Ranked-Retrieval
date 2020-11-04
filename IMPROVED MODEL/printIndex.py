import pickle

#Reading the index from the pickle file.
index_file = open("index", "rb")
primIndex = pickle.load(index_file)
index_file.close()

index_file = open("titleIndex", "rb")
titleIndex = pickle.load(index_file)
index_file.close()

print("Printing Content Index:")
for key,val in primIndex.items():
	print(key+":")
	print("\tDF = "+str(val[1]))
	print("\tPosting List: "+str(val[0]))

print("\nPrinting Title Index:")
for key,val in titleIndex.items():
	print(key+":")
	print("\tDF = "+str(val[1]))
	print("\tPosting List: "+str(val[0]))

print("\n\nSize of vocabulary of content = "+str(len(primIndex))+".")
print("\nSize of vocabulary of title = "+str(len(titleIndex))+".")
