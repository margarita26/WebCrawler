import json
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier 
from sklearn.model_selection import train_test_split 
from sklearn import metrics
from pandas import ExcelWriter

data_to_analyze = []

with open('people.json') as f: 
  data = json.load(f)

#get info from neccessary info from json file
for i in data:
	data_to_analyze.append((data[i]['age'], data[i]['addresses'],data[i]['relatives']))

proccessed = []
proccessed.append(['','age', 'num_of_states','current_state'])

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
		info.append(int(current)) #row number
		info.append(int(person[0])) #age
		info.append(int(count_states(person))) #number of state
		info.append(person[1][0]['state']) #current or last state
		proccessed.append(info) #append list to proccessed list
		current +=1

#convert 2d array to numpy 
np_array = np.array(proccessed)
#create data frame form numpy
df = pd.DataFrame(data=np_array[1:,1:],index=np_array[1:,0],columns=np_array[0,1:])
df['age'] = df['age'].astype(str).astype(int)
df['num_of_states'] = df['num_of_states'].astype(str).astype(int)
df['current_state'] = df['current_state'].astype(str)

print(df.info())
# writer = ExcelWriter('PythonExport.xlsx')
# df.to_excel(writer,'Sheet1')
# writer.save()

features = ['age', 'num_of_states']

x = df[features]
y = df.current_state

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=1)

#decision tree classifier 
clf = DecisionTreeClassifier(criterion = 'entropy', max_depth = 3)
clf = clf.fit(x_train,y_train)
y_pred = clf.predict(x_test)

print('accuracy',metrics.accuracy_score(y_test,y_pred))





