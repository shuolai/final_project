import json
import requests
#from requests_oauthlib import OAuth1

#import secrets

#CACHE_FILENAME = "covid_data.json"
#CACHE_FILENAME_2 = "covid_data_2.json"
#CACHE_DICT = {}

URL = "https://covid-19-statistics.p.rapidapi.com/reports"

querystring = {"region_province":"Michigan","iso":"USA","region_name":"US","date":"2022-03-13"}

HEADERS = {
	"X-RapidAPI-Host": "covid-19-statistics.p.rapidapi.com",
	"X-RapidAPI-Key": "0321333511mshad6a68c8c4f94a7p1d29c6jsne0c8aeb123f8"
}

def open_cache(file_name):
    ''' opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary
    Parameters
    ----------
    None
    Returns
    -------
    The opened cache
    '''
    try:
        cache_file = open(file_name, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict,file_name):
    ''' saves the current state of the cache to disk
    Parameters
    ----------
    cache_dict: dict
        The dictionary to save
    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(file_name,"w")
    fw.write(dumped_json_cache)
    fw.close() 

def construct_querystring_key(baseurl, state, date):
    ''' constructs a key that is guaranteed to uniquely and 
    repeatably identify an API request by its baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the unique key as a string
    '''
    querystring = {"region_province":"Michigan","iso":"USA","region_name":"US","date":"2022-03-13"}
    querystring["region_province"]  = state
    querystring["date"] = date
    unique_key = state + "_" + date
    return unique_key,querystring

def make_request(baseurl, querystring):
    '''Make a request to the Web API using the baseurl and params
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    #response = requests.get(endpoint_url, params=params, auth=oauth)
    response = requests.request("GET", baseurl, headers=HEADERS, params=querystring)
    return response.json()

def make_request_with_cache(baseurl, state, date, cache_dict, file_name):
    '''Check the cache for a saved result for this baseurl+params
    combo. If the result is found, return it. Otherwise send a new 
    request, save it, then return it.
    Parameters
    ----------
    baseurl: string
        The URL for the API endpoint
    params: dictionary
        A dictionary of param: param_value pairs
    Returns
    -------
    string
        the results of the query as a Python object loaded from JSON
    '''
    request_key,querystring = construct_querystring_key(baseurl, state, date)
    if request_key in cache_dict.keys():
        print("cache hit!", request_key)
        #return CACHE_DICT[request_key]
    else:
        print("cache miss!", request_key)
        print(querystring)
        cache_dict[request_key] = make_request(baseurl, querystring)
        save_cache(cache_dict,file_name)
        #return CACHE_DICT[request_key]

#CACHE_DICT = open_cache()

#endpoint_url = 'https://api.twitter.com/1.1/search/tweets.json'
#params = {'q': '@umsi'}
#results = make_request_with_cache(endpoint_url, params)
#tweets = results['statuses']
#for t in tweets:
#    print(t['text'])