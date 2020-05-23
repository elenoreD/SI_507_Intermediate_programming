#########################################
##### Name:  Shengnan Duan          #####
##### Uniqname:     elenore         #####
#########################################

from requests_oauthlib import OAuth1
import json
import requests
import secrets # file that contains your OAuth credentials
from collections import Counter 

CACHE_FILENAME = "twitter_cache.json"
CACHE_DICT = {}

client_key = secrets.TWITTER_API_KEY
client_secret = secrets.TWITTER_API_SECRET
access_token = secrets.TWITTER_ACCESS_TOKEN
access_token_secret = secrets.TWITTER_ACCESS_TOKEN_SECRET

oauth = OAuth1(client_key,
            client_secret=client_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret)

def test_oauth():
    ''' Helper function that returns an HTTP 200 OK response code and a 
    representation of the requesting user if authentication was 
    successful; returns a 401 status code and an error message if 
    not. Only use this method to test if supplied user credentials are 
    valid. Not used to achieve the goal of this assignment.'''

    url = "https://api.twitter.com/1.1/account/verify_credentials.json"
    auth = OAuth1(client_key, client_secret, access_token, access_token_secret)
    authentication_state = requests.get(url, auth=auth).json()
    return authentication_state


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
    request_from_tweeter = requests.get(baseurl, auth=oauth, params=params).json()
    return request_from_tweeter

def make_request_with_cache(baseurl, hashtag, count):
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
    params = {"q": hashtag, 'count': count}
    key_to_find = construct_unique_key(baseurl, params)
    if key_to_find in CACHE_DICT:
        return CACHE_DICT[key_to_find]
    else: 
        tweets_return = make_request(baseurl, params)
        
        CACHE_DICT[key_to_find] = tweets_return
        save_cache(CACHE_DICT)
        return CACHE_DICT[key_to_find]
    


def find_most_common_cooccurring_hashtag(tweet_data, hashtag_to_ignore):
    ''' Finds the hashtag that most commonly co-occurs with the hashtag
    queried in make_request_with_cache().

    Parameters
    ----------
    tweet_data: dict
        Twitter data as a dictionary for a specific query
    hashtag_to_ignore: string
        the same hashtag that is queried in make_request_with_cache() 
        (e.g. "#election2020")

    Returns
    -------
    string
        the hashtag that most commonly co-occurs with the hashtag 
        queried in make_request_with_cache()

    '''
    #remember case insensitive

    
    hashtag_dic = {}
    for tweet in tweet_data["statuses"]:
        # list of hashtags
        hashtags = tweet["entities"]["hashtags"]
        for hashtag in hashtags:
            hashtag_title = hashtag["text"].lower()
            if hashtag_title in hashtag_dic:
                hashtag_dic[hashtag_title] += 1
            else:
                hashtag_dic[hashtag_title] = 1
    

 
    count = Counter(hashtag_dic) 
    
    # Finding 3 highest values 
    i = 4
    top_3 = []
    high_values = count.most_common(i) 
    if high_values: 
        for tuples in high_values:
            hashtag_key = "#" + tuples[0]
            if hashtag_key != hashtag_to_ignore:
                top_3.append(hashtag_key)
        if len(top_3) > 3:
            return top_3[:3]
        else:
            return top_3 
    else:
        return top_3
    

    ''' Hint: In case you're confused about the hashtag_to_ignore 
    parameter, we want to ignore the hashtag we queried because it would 
    definitely be the most occurring hashtag, and we're trying to find 
    the most commonly co-occurring hashtag with the one we queried (so 
    we're essentially looking for the second most commonly occurring 
    hashtags).'''


def find_top_10_words(tweet_data):
    stopwords = set(["RT","a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it", "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the"])

    word_dict = {}
    for tweet in tweet_data["statuses"]:
        word_list = tweet["text"].split()
        for topwords in word_list:
            if topwords not in stopwords:
                if topwords in word_dict:
                    word_dict[topwords] += 1
                else:
                    word_dict[topwords] = 1

    count = Counter(word_dict)

    # Finding 10 highest values 
    i = 10
    top_10 = []
    high_values = count.most_common(i) 
    if high_values: 
        for tuples in high_values:
            if not tuples[0].startswith('#'):
                top_10.append(tuples[0])
        if len(top_10) > 10:
            return top_10[:10]
        else:
            return top_10 
    else:
        return top_10
             
            

    

if __name__ == "__main__":
    if not client_key or not client_secret:
        print("You need to fill in CLIENT_KEY and CLIENT_SECRET in secret_data.py.")
        exit()
    if not access_token or not access_token_secret:
        print("You need to fill in ACCESS_TOKEN and ACCESS_TOKEN_SECRET in secret_data.py.")
        exit()

    CACHE_DICT = open_cache()

    while True:
        baseurl = "https://api.twitter.com/1.1/search/tweets.json"
        hashtag = input('please enter the hashtag you want to search for, eg: #2020election ')

        if not hashtag.startswith('#'):
            hashtag = "#" + hashtag
        count = 100
    
        tweet_data = make_request_with_cache(baseurl, hashtag, count)
        most_common_cooccurring_hashtag = find_most_common_cooccurring_hashtag(tweet_data, hashtag)

        if most_common_cooccurring_hashtag:
            print("The top {} most commonly cooccurring hashtag with {} is: ".format(len(most_common_cooccurring_hashtag), hashtag))
            for h in most_common_cooccurring_hashtag:
                print(h)
        top10words = find_top_10_words(tweet_data)
        if top10words:
            print("The top 10 most commonly cooccurring words with {} is {}: ".format(hashtag, top10words))
            break
        else:
            print('change your search')




    


    
