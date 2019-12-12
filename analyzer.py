import json

data_to_analyze = []

with open('people.json') as json_file:
    data = json.load(json_file)
   
    for i in data:
    	data_to_analyze.append((data[i]['age'],data[i]['full_name'], data[i]['addresses'], data[i]['relatives']))


print(len(data_to_analyze[0][2]))
print(len(data_to_analyze[0][3]))