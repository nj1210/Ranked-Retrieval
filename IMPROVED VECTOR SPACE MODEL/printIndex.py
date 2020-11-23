import pickle

#Reading the content index from the pickle file.
index_file = open("index", "rb")
primIndex = pickle.load(index_file)
index_file.close()

#Reading the title index from the pickle file.
index_file = open("titleIndex", "rb")
titleIndex = pickle.load(index_file)
index_file.close()

output_file = open("readable_content_index.txt","w")
print("\nContent index saved in readable format in 'readable_content_index.txt'.")
for key,val in primIndex.items():
	output_file.write("\n\n"+key+":")
	output_file.write("\n\tIDF = "+str(val[1]))
	output_file.write("\n\tPosting List: "+str(val[0]))
output_file.close()

output_file = open("readable_title_index.txt","w")
print("\nTitle index saved in readable format in 'readable_title_index.txt'.")
for key,val in titleIndex.items():
	output_file.write("\n\n"+key+":")
	output_file.write("\n\tIDF = "+str(val[1]))
	output_file.write("\n\tPosting List: "+str(val[0]))
output_file.close()

#Displaying overall Statistics of the indexes.
print("\n\nSize of vocabulary of content = "+str(len(primIndex))+".")
print("\nSize of vocabulary of title = "+str(len(titleIndex))+".")
