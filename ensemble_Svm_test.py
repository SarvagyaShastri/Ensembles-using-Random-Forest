import sys
import random
from random import randint
import cross_validation_splitter
import random_forest
def read_data(fname):
	temp_data=[]
	try:
		with open(fname) as docs:
			for line in docs:
				line=map(float,line.split())
				temp_data.append(line)

	except Exception,e:
		raise e
		print "File Not Found, program will exit"
		exit()

	return temp_data

def populate_weights(max_features):
	weights=[randint(-1,1) for i in range(max_features)]
	return weights

def perceptron(data,labels,weights,epoch,rate,C):
	j=0
	x=0
	t=0
	gamma_t=rate
	train=0
	while j<epoch:
		for i in range(len(data)):
			t=i+1
			gamma_t=float(rate)/(1+((rate*t)/C))
			try:
				dot_product=map(lambda x,y:x*y,weights,data[i])
				derived_label=reduce(lambda x,y:x+y,dot_product)
				actual_label=labels[i]
				
				if derived_label*actual_label<=1:	
					train+=1
					update=map(lambda x:x*C*gamma_t*actual_label,data[i])
					weights=map(lambda x,y: x+y,map(lambda x:x*(1-gamma_t),weights),update)
				else:
					gamma_t=1-gamma_t
					weights=map(lambda x:x*gamma_t,weights)
			except Exception:
				pass
		j+=1
	#print train
	return weights

def calculate_accuracy(weights,data,labels,hits,miss):
	TP=FP=FN=0
	for i in range(len(data)):
		try:
			dot_product=map(lambda x,y:x*y,weights,data[i])
			derived_label=reduce(lambda x,y:x+y,dot_product)
			actual_label=labels[i]

			if derived_label>0 and actual_label<0:
				FP+=1
			if derived_label<0 and actual_label>0:
				FN+=1
			if derived_label>0 and actual_label>0:
				TP+=1
				

			if derived_label*actual_label>0:
				hits+=1
			else:
				miss+=1
		except Exception:
			pass

	return float(hits)/(hits+miss),TP,FP,FN

def main():
	epoch_list=[3,5,8]
	C=1
	learning_rate=[0.1,0.01]
	accuracies_final=[]
	temp_data, test_data =random_forest.main("data/handwriting/train.data","data/handwriting/train.labels")
	file_name="data/handwriting/train.labels"
	labels=read_data(file_name)
	combined_data=[]
	for i in range(len(temp_data)):
		combined_data.append(labels[i]+temp_data[i])
	
	try:
		file_name=sys.argv[2]
	except Exception:
		
		file_name="data/handwriting/train.data"

	temp_test_data = test_data 
	file_name="data/handwriting/test.labels"
	test_labels =read_data(file_name)
	combined_test_data=[]

	for i in range(len(temp_test_data)):
		combined_test_data.append(test_labels[i]+temp_test_data[i])

	test_labels=[i[0] for i in combined_test_data]
	test_data=[[1]+i[1:] for i in combined_test_data]
	weight_initialize=populate_weights(len(combined_data[0])-1)
	initialized_bias=randint(-1,1)
	for epoch in epoch_list:
		random.shuffle(combined_data)
		labels=[i[0] for i in combined_data]
		data=[[1]+i[1:] for i in combined_data]
		
		for rate in learning_rate:
			weights=[initialized_bias]+weight_initialize
			final_weight_vector=perceptron(data,labels,weights,epoch,rate,C)
			if len(test_data[0])>len(data[0]):
				difference=len(test_data[0])-len(data[0])
				final_weight_vector=final_weight_vector+[0]*difference

			accuracy,TP,FP,FN=calculate_accuracy(final_weight_vector,test_data,test_labels,0,0)
			p=float(TP)/(TP+FP)
			r=float(TP)/(TP+FN)
			F1=float(2*p*r)/(p+r)
			accuracies_final.append([accuracy,rate,epoch,p,r,F1])
			#print "Accuracy found:",accuracy*100,"for rate:",rate,"with epoch:",epoch,"p:",p,"r:",r,"F1:",F1

			weights=[]
	
	result=max(accuracies_final)
	#print "\n"
	print result[0],"max accuracy"
	
main()
