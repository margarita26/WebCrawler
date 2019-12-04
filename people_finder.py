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
class PeopleFider():
    # if you dont want to use one of the fields pass in an empty string,
    # site is still going to work if at least one of the params are filled out
    @staticmethod
    def query(first,last,middle,dob,city,state):
        global user_agent_list
        #get age
        birth_day = datetime.strptime(dob, '%Y-%m-%d')
        age = relativedelta(datetime.today(),birth_day).years
        #params for search
        person_params = {
            'name' : first + ' ' + middle + ' ' + last,
            'citystatezip' : city + ' ' + state,
            'agerange': str(age) + '-' + str(age)
            }
        url = "https://www.truepeoplesearch.com/results?"
        #bypass captcha
        user_agent = random.choice(user_agent_list)
        #create a link for search with personal details
        url_result = url + urlencode(person_params)
        search_result = Request(url_result, headers={'User-Agent':user_agent})
        #open the link with header and read teh result
        page = urlopen(search_result)
        #use beautiful soup for easier html parsing
        soup = BeautifulSoup(page.read(), 'lxml')
        #finds links to all people matched with paramters if found
        #the long class name appears when there is a button with 'View Details'
        anchors = soup.find_all('a', {'class': 'btn btn-success btn-lg detail-link shadow-form', 'href': True})
        l =  len(anchors)
        if l > 0:
            #person is found, view details of the first person in search list
            url_result += '&rid=0x0'
            #bypass captcha
            user_agent = random.choice(user_agent_list)
            search_result = Request(url_result, headers={'User-Agent':user_agent})
            page2 = urlopen(search_result)
            soup = BeautifulSoup(page2.read(), 'lxml')
            print(soup.prettify())
            #return get_info(soup)
        return None

    #parse and return dictionary of required info form beautiful soup
    @staticmethod
    def get_info(soup):
        keys = ['current_adr','past_adr','phone_numbers','email','associated_names','relatives','associates','businesses']
        requested_info = {key: None for key in keys}

        return requested_info

PeopleFider.query('Lu', 'Zang', '', '1964-10-26', 'San Diego', 'CA')
