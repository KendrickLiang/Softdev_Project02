import json, base64
import urllib.request as request

from util import db as silo
def access_info(URL_STUB, header, body):
    '''
    Helper to access the info for a URL. Returns the JSON.
    Params: URL_STUB, API_KEY, header for applying headers to requests
    NOTE: API_KEY should only be used if the key can be put in the URL. Otherwise, use **kwargs.
    '''
    request_object = request.Request(URL_STUB, headers=header,data=body)
    response = request.urlopen(request_object)
    response = response.read()
    info = json.loads(response)
    return info

def searchLocation(query):
    with open("keys/accuWeather.json") as json_file:
        keys = json.load(json_file)
    URL = "http://dataservice.accuweather.com/locations/v1/cities/autocomplete?apikey="
    API_KEY = keys['key']
    #print (query)
    URL_STUB = URL + API_KEY + "&q=" + query.replace(" ", "%20").strip()
    return access_info(URL_STUB, {}, None)

def getipLocation():
    URL = "http://dataservice.accuweather.com/locations/v1/cities/ipaddress?apikey="
    with open("keys/accuWeather.json") as json_file:
        keys = json.load(json_file)
    API_KEY = keys['key']
    URL_STUB = URL + API_KEY
    return access_info(URL_STUB, {}, None)

def weatherInfo(user, farm):
    URL = "http://dataservice.accuweather.com/currentconditions/v1/"
    with open("keys/accuWeather.json") as json_file:
        keys = json.load(json_file)
    API_KEY = keys['key']
    URL_STUB = URL + silo.getLocationKey(user, farm) + "?apikey=" + API_KEY + "&details=True"
    return access_info(URL_STUB, {}, None)

def getCropInfo():
    '''
        Returns listing of all crop types provided by awhere.
    '''
    with open("keys/aWhere.json") as json_file:
        keys = json.load(json_file)

    api_key = keys['0']['key']
    api_secret = keys['0']['secret_key']
    api_URL= "https://api.awhere.com/"
    URI = "v2/agronomics/crops"
    URL_STUB = api_URL + URI
    auth_token = get_oauth_token(encode_secret_and_key(api_key, api_secret))
    header = {
        "Authorization": "Bearer %s" % auth_token,
    }
    data = access_info(URL_STUB, header, None)
    return data

def getModels():
    '''
        Get Model listing
    '''
    with open("keys/aWhere.json") as json_file:
        keys = json.load(json_file)

    api_key = keys['0']['key']
    api_secret = keys['0']['secret_key']
    api_URL= "https://api.awhere.com/"
    URI = "v2/agronomics/models"
    URL_STUB = api_URL + URI
    auth_token = get_oauth_token(encode_secret_and_key(api_key, api_secret))
    header = {
        "Authorization": "Bearer %s" % auth_token,
    }
    data = access_info(URL_STUB, header, None)
    return data['models']






def getModelDetails(URI):
    '''
        Get a specific models details
    '''
    with open("keys/aWhere.json") as json_file:
        keys = json.load(json_file)

    api_key = keys['0']['key']
    api_secret = keys['0']['secret_key']
    api_URL= "https://api.awhere.com/"
##    print(URI)
    URL_STUB = api_URL + URI + "/details"
    auth_token = get_oauth_token(encode_secret_and_key(api_key, api_secret))
    header = {
        "Authorization": "Bearer %s" % auth_token,
    }
    data = access_info(URL_STUB, header, None)
    return data

def encode_secret_and_key(key, secret):
    """
    Docs:
        http://developer.awhere.com/api/authentication
    Returns:
        Returns the base64-encoded {key}:{secret} combination, seperated by a colon.
    """
    # Base64 Encode the Secret and Key
    key_secret = '%s:%s' % (key, secret)
    #print('\nKey and Secret before Base64 Encoding: %s' % key_secret)

    encoded_key_secret = base64.b64encode(
        bytes(key_secret, 'utf-8')).decode('ascii')

    #print('Key and Secret after Base64 Encoding: %s' % encoded_key_secret)
    return encoded_key_secret

def get_oauth_token(encoded_key_secret):
    """
    Demonstrates how to make a HTTP POST request to obtain an OAuth Token

    Docs:
        http://developer.awhere.com/api/authentication

    Returns:
        The access token provided by the aWhere API
    """
    auth_url = 'https://api.awhere.com/oauth/token'

    auth_headers = {
        "Authorization": "Basic %s" % encoded_key_secret,
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    body = str.encode("grant_type=client_credentials")

    request_object = request.Request(auth_url, headers=auth_headers,data=body)
    response = request.urlopen(request_object)
    response = response.read()

    # .json method is a requests lib method that decodes the response
    return json.loads(response)['access_token']
