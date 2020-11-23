import pickle

#Reading the index from the pickle file.
index_file = open("index", "rb")
primIndex = pickle.load(index_file)
index_file.close()

output_file = open("readable_index.txt","w")

#Storing the content index in readable format.
for key,val in primIndex.items():
	output_file.write("\n\n"+key+":")
	output_file.write("\n\tDF = "+str(val[1]))
	output_file.write("\n\tPosting List: "+str(val[0]))

output_file.close()
print("\nIndex saved in readable format in 'readable_index.txt'")
print("\nSize of vocabulary = "+str(len(primIndex))+".")
