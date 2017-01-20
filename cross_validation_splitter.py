import sys
import random
from random import randint
def read_data(fname):
	temp_data=[]
	try:
		with open(fname) as docs:
			for line in docs:
				line=line.split()
				temp_data.append(line)

	except Exception,e:
		raise e
		print "File Not Found, program will exit"
		exit()

	return temp_data

def read_train_data(i,k,file_name):
	labels=[]
	temp_data=[]
	for j in range(k):
		if j==i:
			continue
		else:
			with open(file_name %j) as docs:
				for line in docs:
					line=map(float,line.split())
					temp_data.append(line)

	return temp_data

def read_test_data(i,file_name):
	labels=[]
	temp_data=[]
	
	with open(file_name % i) as doc:
		for line in doc:
			line=map(float,line.split())
			temp_data.append(line)

	return temp_data

def populate_weights(max_features):
	weights=[randint(-1,1) for i in range(max_features)]
	return weights


def perceptron(data,labels,weights,epoch,rate,C):
	j=0
	x=0
	t=0
	gamma_t=rate
	while j<epoch:
		for i in range(len(data)):
			t=i+1
			gamma_t=float(rate)/(1+((rate*t)/C))
			dot_product=map(lambda x,y:x*y,weights,data[i])
			derived_label=reduce(lambda x,y:x+y,dot_product)
			actual_label=labels[i]
			if derived_label*actual_label<=1:
				update=map(lambda x:x*C*gamma_t*actual_label,data[i])
				weights=map(lambda x,y: x+y,map(lambda x:x*(1-gamma_t),weights),update)
			else:
				gamma_t=1-gamma_t
				weights=map(lambda x:x*gamma_t,weights)
		j+=1
	return weights

def calculate_accuracy(weights,data,labels,hits,miss):
	for i in range(len(data)):
		dot_product=map(lambda x,y:x*y,weights,data[i])
		derived_label=reduce(lambda x,y:x+y,dot_product)
		actual_label=labels[i]
		if derived_label*actual_label>0:
			hits+=1
		else:
			miss+=1
	return float(hits)/(hits+miss)



def split(k):
	file_name="data/madelon/madelon_train.data"
	data=read_data(file_name)
	file_name="data/madelon/madelon_train.labels"
	labels=read_data(file_name)
	split_parts=len(labels)/k

	for i in range(len(labels)):
		if i%split_parts==0:
			if i>0:
				target.close()
			number=i/split_parts
			target=open("data/madelon/train_%d.data"%number,"w")
		target.write(' '.join(labels[i]+data[i]))
		target.write("\n")	


def cross_validate(k,epoch_list, c, learning_rate):
	for rate in learning_rate:
		for C in c:
			for i in xrange(k):
				accuracies_final=[]
				file_name="data/madelon/train_%d.data"
				combined_data=read_train_data(i,k,file_name)
				combined_test_data=read_test_data(i,file_name)
				test_labels=[i[0] for i in combined_test_data]
				test_data=[[1]+i[1:] for i in combined_test_data]
				
				weight_initialize=populate_weights(len(combined_data[0])-1)
				initialized_bias=randint(-1,1)

				for epoch in epoch_list:
					random.shuffle(combined_data)
					labels=[i[0] for i in combined_data]
					data=[[1]+i[1:] for i in combined_data]
					weights=[initialized_bias]+weight_initialize
					final_weight_vector=perceptron(data,labels,weights,epoch,rate,C)
				
					if len(test_data[0])>len(data[0]):
						difference=len(test_data[0])-len(data[0])
						final_weight_vector=final_weight_vector+[0]*difference
					
					accuracy=calculate_accuracy(final_weight_vector,test_data,test_labels,0,0)
					accuracies_final.append([accuracy,rate,epoch])
					print "Accuracy found",accuracy*100,"-> C",C," for rate",rate,"with epoch ",epoch
					weights=[]
			
				result=max(accuracies_final)
				print "\n"
				print result[0],"max accuracy for learning rate",result[1],"C",C,"and epoch",result[2]




		
