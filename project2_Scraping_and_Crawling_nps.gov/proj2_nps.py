#################################
##### Name:  Shengnan Duan
##### Uniqname:  elenore
#################################

from bs4 import BeautifulSoup
import requests
import json
import secrets # file that contains your API key

CACHE_FILENAME = "project2_cache.json"
CACHE_DICT = {} 

class NationalSite:
    '''a national site

    Instance Attributes
    -------------------
    category: string
        the category of a national site (e.g. 'National Park', '')
        some sites have blank category.
    
    name: string
        the name of a national site (e.g. 'Isle Royale')

    address: string
        the city and state of a national site (e.g. 'Houghton, MI')

    zipcode: string
        the zip-code of a national site (e.g. '49931', '82190-0168')

    phone: string
        the phone of a national site (e.g. '(616) 319-7906', '307-344-7381')
    '''
    def __init__(self, category, name, address, zipcode, phone):
        self.category = category
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.phone = phone
    
    def info(self):
        return f"{self.name} ({self.category}): {self.address} {self.zipcode}"


def build_state_url_dict():
    ''' Make a dictionary that maps state name to state page url from "https://www.nps.gov"

    Parameters
    ----------
    None

    Returns
    -------
    dict
        key is a state name and value is the url
        e.g. {'michigan':'https://www.nps.gov/state/mi/index.htm', ...}
    '''

    state_dict ={}
    url = 'https://www.nps.gov/index.htm'

    response = make_request_with_cache(url)
    soup = BeautifulSoup(response, 'html.parser')
    drop_down_div = soup.find_all('ul', class_='dropdown-menu SearchBar-keywordSearch')

    for li in drop_down_div[0].find_all('li'):
        state_name = li.text.strip().lower()
        state_url = li.find('a').get('href')
        state_dict [state_name] = 'https://www.nps.gov' + state_url
    
    return state_dict


def get_site_instance(site_url):
    '''Make an instances from a national site URL.
    
    Parameters
    ----------
    site_url: string
        The URL for a national site page in nps.gov
    
    Returns
    -------
    instance
        a national site instance
    '''

    response = make_request_with_cache(site_url)
    soup = BeautifulSoup(response, 'html.parser')

    vcard = soup.find('div', class_="vcard")
    address1 = vcard.find(itemprop="addressLocality").text.strip()
    
    address2 = vcard.find(itemprop="addressRegion").text.strip()
    
    zipcode = vcard.find(itemprop="postalCode").text.strip()
    phone = vcard.find(itemprop="telephone").text.strip()
    category = soup.find('div', class_="Hero-designationContainer").find(class_="Hero-designation").text.strip()
    name = soup.find('div', class_="Hero-titleContainer clearfix").find('a').text.strip()
    
    national_site = NationalSite(category=category, name=name, address= address1+ ', ' + address2, zipcode=zipcode, phone=phone)  

    return national_site
    

def get_sites_for_state(state_url):
    '''Make a list of national site instances from a state URL.
    
    Parameters
    ----------
    state_url: string
        The URL for a state page in nps.gov
    
    Returns
    -------
    list
        a list of national site instances
    '''

    national_site_list = []

    response = make_request_with_cache(state_url)
    soup = BeautifulSoup(response, 'html.parser')
    site_div = soup.find(id='list_parks').find_all('li',recursive=False)

    for li in site_div:
        site_link = li.find('h3').find('a')['href']
        site_link = 'https://www.nps.gov'+site_link
        national_site_instance = get_site_instance(site_link)
        national_site_list.append(national_site_instance)
            

    return national_site_list

def print_site_formatly(alist):
    '''Format the output for get_sites_for_state.
    
    Parameters
    ----------
    alist: list
        a list sites of a state
    
    Returns
    -------
    None
    '''

    count = 0
    for sites in alist:
        count += 1
        info = f"[{count}] {sites.name} ({sites.category}): {sites.address}, {sites.zipcode} "
        print(info)

def get_nearby_places(site_object):
    '''Obtain API data from MapQuest API.
    
    Parameters
    ----------
    site_object: object
        an instance of a national site
    
    Returns
    -------
    dict
        a converted API return from MapQuest API
    '''
    baseurl = 'http://www.mapquestapi.com/search/v2/radius'
    params_dict = {'key': secrets.API_KEY, 'origin': site_object.zipcode, 'radius': 10, 'maxMatches': 10, 'ambiguities': 'ignore', 'outFormat': 'json'}
    response = make_request_with_cache(baseurl,params_dict)
    api_file = json.loads(response)
    
    return api_file


def print_near_by_places(api_file):
    '''Extract info of nearby places from an API file.
    
    Parameters
    ----------
    api_file: dict
        a converted API return from MapQuest API 
    
    Returns
    -------
    None
    '''

    for near_by_place in api_file ['searchResults']:
        try:
            name = near_by_place['fields']['name']
            if len(name) == 0:
                name = 'no name'
            category = near_by_place['fields']['group_sic_code_name']
            if len(category) == 0:
                category = 'no category'
            address = near_by_place['fields']['address']
            if len(address) == 0:
                address = 'no address'
            city = near_by_place['fields']['city']
            if len(city) == 0:
                city ='no city'

        except:
            name = 'no name'
            category = 'no category'
            address = 'no address'
            city ='no city'

    
        print(f"{name} ({category}): {address}, {city}")

def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    
    Parameters
    ----------
    None
    
    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
#    print(type(cache_dict),'aaaa')
    return cache_dict


def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk
    
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_unique_key(baseurl, params):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dict
        A dictionary of param:value pairs
    
    Returns
    -------
    string
        the unique key as a string
    '''


    param_strings = []
    connector = '_'
    for k in params.keys():
        param_strings.append(f'{k}_{params[k]}')
    param_strings.sort()
    unique_key = baseurl + connector +  connector.join(param_strings)
    return unique_key


def make_request(baseurl, params):
    '''Make a request to the Web API using the baseurl and params
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param:value pairs
    
    Returns
    -------
    dict
        the data returned from making the request in the form of 
        a dictionary
    '''
    response = requests.get(baseurl, params=params)
    return response.text


def make_request_with_cache(baseurl, param={}):
    '''Check the cache for a saved result for this baseurl+params:values
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    hashtag: string
        The hashtag to search (i.e. “#2020election”)
    count: int
        The number of tweets to retrieve
    
    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''
    

    key_to_find = construct_unique_key(baseurl, param)
    
    if key_to_find in CACHE_DICT:
        print('using cache')
        return CACHE_DICT[key_to_find]
    else: 
        print('feching')
        tweets_return = make_request(baseurl, param)
        CACHE_DICT[key_to_find] = tweets_return
        save_cache(CACHE_DICT)
        return CACHE_DICT[key_to_find]


if __name__ == "__main__":

    CACHE_DICT = open_cache()
    while True:
        user_input = input('enter a state name or exit: ').lower()
        check_dict = build_state_url_dict()
        if user_input in check_dict: 
            #first search
            sites = get_sites_for_state(check_dict[user_input])
            print_site_formatly(sites)
            # detail search
            while True:
                user_input2 = input('choose a number for detail search or exit or back: ')
                if user_input2.isnumeric() and int(user_input2) < len(sites):
                    sites10 = get_nearby_places(sites[int(user_input2)-1])
                    print(f"Places near {sites[int(user_input2)-1].name}")
                    print_near_by_places(sites10) 

                elif user_input2 == 'back':
                    break

                elif user_input2 == 'exit':
                    exit()

                else: 
                    print('please correct input')
            
        elif user_input == 'exit':
            break
        else: 
            print('please correct your input')