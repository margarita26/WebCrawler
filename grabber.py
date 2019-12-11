import time 
import names
import random
from people_finder import PeopleFinder 
from people_finder import Person
import csv

list_people = []
i = 0 
more_sleep = 0

while i <  50: 
	sleep = random.randint(10,50)
	time.sleep(sleep)
	last = names.get_last_name()
	dob = str(random.randint(1950,2000))
	info = PeopleFinder.query('', last, '',dob,'','')
	if info is not None:
		if info['addreses'] is not None:
			print(info)
			list_people.append(Person('', '',last, dob,'','', info))
			i+=1  


with open('file.csv',mode = 'w') as out:
    csv_out=csv.writer(out, delimiter=',')
    csv_out.writerow(['first name','middle name', 'last name', 'dob','city','state','info'])
    for row in list_people:
        csv_out.writerow(row)


