import json
import numpy as np
import pandas as pd

data_to_analyze = []

with open('people.json') as f: 
  data = json.load(f)

#get info from neccessary info from json file
for i in data:
	data_to_analyze.append((data[i]['age'], data[i]['addresses'],data[i]['relatives']))

proccessed = []
proccessed.append(['','age', 'num_of_states', 'num_addresses', 'num_relatives', 'current_state'])

#count the number of states the person lived in
def count_states(person):
	d = dict()

	for i in person[1]:
		state = i['state']
		if state not in d:
			d[state] = 1
		else: 
			d[state] +=1
	return len(d)

#proccess to create numpy array
current = 0
for person in data_to_analyze:
	info = []
	if person[0].isdigit():
		info.append(current) #row number
		info.append(person[0]) #age
		info.append(count_states(person)) #number of state
		info.append(len(person[1])) #number of addresses
		info.append(len(person[2])) #number of relatives
		info.append(person[1][0]['state']) #current or last state
		proccessed.append(info) #append list to proccessed list
		current +=1

#convert 2d array to numpy 
np_array = np.array(proccessed)
#create data frame form numpy
df = pd.DataFrame(data=np_array[1:,1:],index=np_array[1:,0],columns=np_array[0,1:])

pd.set_option('display.max_colwidth', -1)
print(df)






