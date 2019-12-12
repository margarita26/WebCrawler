from collections import namedtuple
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from urllib.parse import urlencode
import requests
from dateutil.relativedelta import relativedelta
from datetime import datetime
import random
import time

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

Person = namedtuple('Person',('fist', 'midlle','last','dob', 'city', 'state', 'info'))

#class with static methods that queries persons public record information from family tree
class PeopleFinder():
    # this method returns a dictionary of scrapped information 
    # in the form of a list for each key.
    @staticmethod
    def query(first,last,middle,dob,city,state):
        global user_agent_list
        #get age
        year = ''
        if len(dob) == 4: 
            if dob[0] == '1' or dob[0] == '2':
                year = dob
        
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

            #bypass captcha
            user_agent = random.choice(user_agent_list)
            sleep = random.randint(10,40)
            time.sleep(sleep)
            search_result = Request(url_result, headers={'User-Agent':user_agent})
            page2 = urlopen(search_result)
            soup = BeautifulSoup(page2.read(),'lxml')
            return PeopleFinder._get_info(soup)
        print('not found')
        return None

    #parse and return dictionary of required info form beautiful soup
    def _get_info(soup):
        keys = ['addresses','phone_numbers','associated_names','relatives','associates']
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
        keys = PeopleFinder._proccess_info(requested_info, info)
        return keys

    #function that fills out the dictionary with info
    def _proccess_info(keys,info):
        for i in range(0, len(info)-1):
            current = info[i].strip()
            #this list will hold info for each section, eg Phone Numbers
            if current == 'Associated Names':
                keys['associated_names'] = PeopleFinder._proccess_names(info[i+1])
            if current == 'Possible Relatives':
                keys['relatives'] = PeopleFinder._proccess_associates_relatives(info[i+1])
            if current == 'Possible Associates':
                keys['associates'] = PeopleFinder._proccess_associates_relatives(info[i+1])
            if current == 'Current & Past Addresses':
                keys['addresses'] = PeopleFinder._proccess_addresses(info[i+1])
            if current == 'Phone Numbers':
                keys['phone_numbers'] = PeopleFinder._proccess_pnumbers(info[i+1])
        print(keys)        
        return keys
            
    def _proccess_names(s):
        l = s.split('\n')
        #removes empty strings
        names = list(filter(None,l))
        return names


    def _proccess_associates_relatives(s):
        l = s.split('\n')
        names = list(filter(None,l))
        new = []
        for i in names:
            if not i.strip().isdigit() and i != 'NameAgeBirth Year':
                new.append(i.strip())
        return new

    def _proccess_addresses(s):
        l = list(filter(None,s.split('\n')))
        #tuples of addresses and number of years lived
        new = []
        addresses = []
        years = []

        for i in l:
            if i.strip() == 'Current Address':
                years.append('current')
            else:   
                #append the tuple of time period e.g (2001,2012)
                if i[0] == '(':
                    numbers = i.split()
                    if len(numbers) > 2:
                        #removes paran from the string eg 2012)
                        n1 = numbers[len(numbers)-1][:-1]
                        n2 = numbers[1]
                        years.append((n2,n1))
                    else:
                        n = numbers[len(numbers)-1][:-1]
                        years.append((n,n))
                else:
                    addresses.append(i.strip())
        #create a tuple of address - time period and append to a new list
        for i in range(0,len(addresses)):
            if i < len(years):
                new.append((addresses[i], years[i]))
            else:
                new.append((addresses[i], 0))
        return new

    def _proccess_pnumbers(s):
        l = list(filter(None,s.split('\n')))
        new = []

        for i in l:
            if i[0] == '(':
                new.append(i)
        return new         
        

PeopleFinder.query('Vincent', 'Elia', '', '1989', '', '')
