import math
import random

def read_data(fname):
	temp_data=[]
	try:
		with open(fname) as docs:
			for line in docs:
				line=line.replace(".0000","")
				line=line.replace(" ","")
				line=line.strip()
				#line=line.replace("","")
				#line=map(int,line.split())
				#print line
				temp_data.append(line)

	except Exception,e:
		raise e
		print "File Not Found, program will exit"
		exit()

	return temp_data


def calculate_unique(labels):
	unique={}
	data_entropy=0.0
	for elem in labels:
		if elem in unique:
			unique[elem]=unique[elem]+1
		else:
			unique[elem]=1

	return unique

def calculate_gain(labels,tuples):
	labels=tuples["total"]
	del tuples["total"]
	entropy=calculate_entropy(labels,tuples)
	return entropy
	
def gain(data,single_attribute,column,total_entropy,dict_for_entropy):
	unique=calculate_unique(single_attribute)
	occurences={}
	for elem in data:
		if elem[column] in unique:
			if elem[column] in occurences:				
				if elem[-1] in occurences[elem[column]]:
					occurences[elem[column]][elem[-1]]=occurences[elem[column]][elem[-1]]+1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
				else:
					occurences[elem[column]][elem[-1]]=1
					occurences[elem[column]]["total"]=occurences[elem[column]]["total"]+1
			else:
				occurences[elem[column]]={elem[-1]:1}
				occurences[elem[column]]["total"]=1

	info_gain=0.0
	for keys in occurences:
		Dj=occurences[keys]["total"]
		D=len(data)
		info_gain=info_gain+(float(Dj)/D)*calculate_gain(len(single_attribute),occurences[keys])
	dict_for_entropy[total_entropy-info_gain]=column
	return total_entropy-info_gain,dict_for_entropy

def choose_best_attribute(data,list_of_attributes,class_labels,gain):
	unique=calculate_unique(class_labels)
	total_entropy=calculate_entropy(len(class_labels),unique)
	best_gain=0.0
	entropy_results={}
	
	for i in range(len(list_of_attributes[0])):
		label_by_label=[]
		for j in range(len(list_of_attributes)):
			label_by_label.append(list_of_attributes[j][i])
		
		info_gain,entropy_results=gain(data,label_by_label,i,total_entropy,entropy_results)
		if info_gain>best_gain:
			best_gain=info_gain
		else:
			continue

	return(entropy_results[best_gain])


def calculate_entropy(labels,unique):
	data_entropy=0.0
	for frequency in unique.values():
		data_entropy -= (float(frequency)/labels) * math.log(float(frequency)/labels, 2)


	return data_entropy 

def get_best_attribute(data,best_column):
	best_attribute=[]
	for i in range(len(data)):
		best_attribute.append(data[i][best_column])
	
	return best_attribute	

def get_examples(data,best_attribute,best_column_number,class_labels):
	unique=calculate_unique(best_attribute)
	respective_values=[]
	for val in unique:
		for elem in range(len(data)):
			if val==data[elem][best_column_number]:
				respective_values.append([val,data[elem][-1],elem])

	values_dict={}
	for elem in respective_values:
		if (elem[0]) in values_dict:
			values_dict[elem[0]].append(elem[2])
		else:
			values_dict[elem[0]]=[elem[2]]

	respective_values_list=[]
	for a in values_dict:
		respective_values_list.append([a,values_dict[a]])

	return respective_values_list

def get_values(elem,data,best):
	temp_data=[]
	derived_data=[]
	for i in elem[1]:
		temp_data.append(data[i])

	for i in temp_data:
		derived_data.append(i[:best]+i[best+1:])

	return derived_data	

def get_classification(record,tree,i):
	if type(tree) == type("string"):
		return tree
	else:
		attr = tree.keys()[0]
		if record[attr] in tree[attr]:
			t = tree[attr][record[attr]]
			new_record=record[:attr]+record[attr+1:]
		else:
			return "x"
		return get_classification(new_record, t,i)

def classify(tree,test_data):
	classification=[]
	for record in test_data:
		classification.append(get_classification(record, tree,0))
	return classification	

def find_subset(data):
	subset_feature_data=[]
	random_indexes=[random.randint(0,len(data[0])-2) for i in range(8)]
	random_indexes=sorted(random_indexes)
	for row in data:
		temp=""
		for item in random_indexes:
			temp=temp+row[item]
		subset_feature_data.append(temp)

	subset_data=[]
	for i,row in enumerate(subset_feature_data):
		row=row+data[i][-1]
		subset_data.append(row)
	subset_attributes=[i[0:-1] for i in subset_data]
	subset_labels=[i[-1] for i in subset_data]
	return subset_data, subset_attributes, subset_labels, random_indexes

	
def create_tree(data,list_of_attributes,class_labels,gain):
	unique=calculate_unique(i[-1] for i in data)
	max=0
	most_frequent=None
	for keys in unique:
		if unique[keys]>max:
			max=unique[keys]
			most_frequent=keys

	if not data or (len(list_of_attributes) - 1) <= 0:
		return	most_frequent

	elif class_labels.count(class_labels[0])==len(class_labels):
		return class_labels[0]

	else:
		subset_data, subset_attributes, subset_labels, random_indexes=find_subset(data)
		best=choose_best_attribute(subset_data,subset_attributes,subset_labels,gain)
		best=random_indexes[best]
		best_attribute=get_best_attribute(data,best)
		tree={best:{}}
		respective_values_list=get_examples(data,best_attribute,best,class_labels)
		
		for elem in respective_values_list:

			derived_list_of_attributes=[]
			derived_data=get_values(elem,data,best)
			#random_indexes=[random.randint(0,len(derived_data)-1) for i in range(int(0.6*len(derived_data)))]
			#for index in random_indexes:
			#	temp_data.append(derived_data[index])
			#derived_data=temp_data
			derived_class_labels=[i[-1] for i in derived_data]
			for i in derived_data:
				derived_list_of_attributes.append(i[:-1])


		
			tree[best][elem[0]]=create_tree(derived_data,derived_list_of_attributes,derived_class_labels,gain)
	return tree

def main(fname1,fname2):
	data=[]
	tree=[]
	file_name="data/handwriting/train.data"
	list_of_attributes=read_data(file_name)
	file_name="data/handwriting/train.labels"
	class_labels=read_data(file_name)
	#print class_labels
	data=[]
	for i in range(len(list_of_attributes)):
		if class_labels[i]=="1":
			data.append(list_of_attributes[i]+class_labels[i])
		else:
			data.append(list_of_attributes[i]+'0')

	#print 
	class_labels=[i[-1] for i in data]
	for i in range(5):
		temp_data=[]
		random_indexes=[random.randint(0,999) for i in range(600)]
		for index in random_indexes:
			temp_data.append(data[index])
		
		tree.append(create_tree(temp_data,list_of_attributes,class_labels,gain))
		#break
	#print tree


	file_name=fname1
	test_attributes=read_data(file_name)
	file_name=fname2
	test_class_labels=read_data(file_name)
	#print class_labels
	test_data=[]
	for i in range(len(test_attributes)):
		if test_class_labels[i]=="1":
			test_data.append(test_attributes[i]+test_class_labels[i])
		else:
			test_data.append(test_attributes[i]+'0')


	test_class_labels=[i[-1] for i in test_data]
	
	svm_temp_data=[]
	for i in range(len(tree)):
		classification=classify(tree[i],test_data)
		positive=0
		negative=0
		for j in range(len(classification)):
			if classification[j]==test_data[j][-1]:
				positive+=1
			else:
				negative+=1

		total=positive+negative
		print "Accuracy of tree",i+1, "on data is",float(positive)/total
		svm_temp_data.append(classification)

	svm_data=[]
	for i in range(len(svm_temp_data[0])):
		temp=[]
		for row in svm_temp_data:
			if row[i]=="0":
				temp.append(float("-1"))
		
			if row[i]=="1":
				temp.append(float(row[i]))
			

		svm_data.append(temp)


	#_____________________________________________________________________________________
	file_name="data/handwriting/test.data"
	test_attributes=read_data(file_name)
	file_name="data/handwriting/train.labels"
	test_class_labels=read_data(file_name)
	#print class_labels
	test_data=[]
	for i in range(len(test_attributes)):
		if test_class_labels[i]=="1":
			test_data.append(test_attributes[i]+test_class_labels[i])
		else:
			test_data.append(test_attributes[i]+'0')


	test_class_labels=[i[-1] for i in test_data]
	
	svm_temp_test_data=[]
	for i in range(len(tree)):
		classification=classify(tree[i],test_data)
		positive=0
		negative=0
		for j in range(len(classification)):
			if classification[j]==test_data[j][-1]:
				positive+=1
			else:
				negative+=1

		total=positive+negative
		print "Accuracy of tree",i+1, "on data is",float(positive)/total
		svm_temp_test_data.append(classification)

	svm_test_data=[]
	for i in range(len(svm_temp_test_data[0])):
		temp=[]
		for row in svm_temp_test_data:
			if row[i]=="0":
				temp.append(float("-1"))
		
			if row[i]=="1":
				temp.append(float(row[i]))
			

		svm_test_data.append(temp)

	
	return svm_data, svm_test_data





