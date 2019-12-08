from collections import namedtuple
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime
import random

#~~~~~~~~~~~~~~~~~~~~~~~~ Part 1 ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#list of user agent to bypass captcha going to be chosen randomly
user_agent_list = [
   #Chrome
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    #Firefox
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

Person = namedtuple('Person',('fist', 'midlle','last','dob', 'city', 'state'))

#class with static methods that queries persons public record information from truepeoplesearch
class PeopleFinder():
    # if you dont want to use one of the fields pass in an empty string,
    # site is still going to work if at least one of the params are filled out
    @staticmethod
    def query(first,last,middle,dob,city,state):
        global user_agent_list
        #get age
        year = ''
        if len(dob) > 0: 
            birth_day = datetime.strptime(dob, '%Y-%m-%d')
            year = birth_day.year
        
        #params for search
        person_params = {
            'first' : first,
            'middle': middle,
            'last': last,
            'citystatezip' : city + ' ' + state,
            'dobyyyy': year
            }

        url = "https://www.familytreenow.com/search/genealogy/results?"
        #bypass captcha
        user_agent = random.choice(user_agent_list)
        #create a link for search with personal details
        url_result = url + urlencode(person_params)
        search_result = Request(url_result, headers={'User-Agent':user_agent})
        #open the link  
        page = urlopen(search_result)
        #use beautiful soup for easier html parsing
        soup = BeautifulSoup(page.read(), 'lxml')

        #finds links to all people matched with paramters if found
        #the long class name appears when there is a button with 'View Details'
        anchors = soup.find_all('a', {'class': 'btn btn-success btn-sm detail-link', 'href': True})
        l =  len(anchors)
        if l > 0:
            #view details of the first person in search list
            url_result += '&rid=0s0'
            print(url_result)
            #bypass captcha
            user_agent = random.choice(user_agent_list)
            search_result = Request(url_result, headers={'User-Agent':user_agent})
            page2 = urlopen(search_result)
            soup = BeautifulSoup(page2.read(),'lxml')
            return PeopleFinder.get_info(soup)
        return None

    #parse and return dictionary of required info form beautiful soup
    def get_info(soup):
        keys = ['addreses','phone_numbers','associated_names','relatives','associates']
        requested_info = {key: None for key in keys}
        #find all tables with information
        results = soup.find_all('div', {'class': 'panel panel-primary'})
        info = []  
        #loops through each table e.g.Phone Numbers section
        for result in results:
            try:
                name = result.find('div', {'class': 'panel-heading text-center'}).get_text() 
                val = result.find('table', {'class': 'table table-condensed'}).get_text() 
                info.append(name)
                info.append(val)
            except AttributeError:
                print()
        keys = PeopleFinder.proccess_info(requested_info, info)
        return keys

    #function that filles out the dictionary with info
    def proccess_info(keys,info):
        for i in range(0, len(info)-1):
            current = info[i].strip()
            #this list will hold info for each section, eg Phone Numbers
            if current == 'Associated Names':
                keys['associated_names'] = PeopleFinder.proccess_names(info[i+1])
            if current == 'Possible Relatives':
                keys['relatives'] = PeopleFinder.proccess_associates_relatives(info[i+1])
            if current == 'Possible Associates':
                keys['associates'] = PeopleFinder.proccess_associates_relatives(info[i+1])
            if current == 'Current & Past Addresses':
                keys['addreses'] = PeopleFinder.proccess_addresses(info[i+1])
            if current == 'Phone Numbers':
                keys['phone_numbers'] = PeopleFinder.proccess_pnumbers(info[i+1])

        for key,val in keys.items():
            print(key,val) 

        return keys
            
    def proccess_names(s):
        l = s.split('\n')
        names = list(filter(None,l))
        return names

    def proccess_associates_relatives(s):
        l = s.split('\n')
        names = list(filter(None,l))
        new = []
        for i in names:
            if not i.strip().isdigit() and i != 'NameAgeBirth Year':
                new.append(i.strip())
        return new

    def proccess_addresses(s):
        l = list(filter(None,s.split('\n')))
        #tuples of addresses and number of years lived
        new = []
        addresses = []
        years = []

        for i in l:
            if i.strip() == 'Current Address':
                years.append('current')
            else:   
                if i[0] == '(':
                    n = 0
                    numbers = i.split()
                    if len(numbers) > 2:
                        #removes paran from the string eg 2012)
                        n1 = numbers[len(numbers)-1][:-1]
                        n2 = numbers[1]
                        n = int(n1) - int(n2)
                    #append 1 because the difference can be 2012 - 2012
                    #technically 0 but actually 1 year lived at that location 
                    if n == 0: 
                         years.append(1)
                    else:
                        years.append(n)
                else:
                    addresses.append(i.strip())
        #create tuples
        for i in range(0,len(addresses)):
            if i < len(years):
                new.append((addresses[i], years[i]))
            else:
                new.append((addresses[i], 0))

        return new

    def proccess_pnumbers(s):
        l = list(filter(None,s.split('\n')))
        new = []

        for i in l:
            if i[0] == '(':
                new.append(i)
        return new         
        

PeopleFinder.query('Jason', 'Smith', '', '1978-10-5', '', '')
