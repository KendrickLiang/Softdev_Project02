import json, base64
import urllib.request as request

def access_info(URL_STUB, API_KEY = None, **kwargs):
    '''
    Helper to access the info for a URL. Returns the JSON.
    Params: URL_STUB, API_KEY = None, **kwargs for applying headers to requests
    NOTE: API_KEY should only be used if the key can be put in the URL. Otherwise, use **kwargs.
    '''
    # if there's an API key that is not a header
    if API_KEY:
        URL = URL_STUB + API_KEY
    else:
        URL = URL_STUB
    request_object = request.Request(URL)
    # iterate through, adding headers if needed
    for key, value in kwargs.items():
        request_object.add_header(key, value)

    response = request.urlopen(request_object)
    response = response.read()
    info = json.loads(response)
    return info

def getCropInfo():
    api_key = '0EI5hYgGm8avoh0Wb3FtHv2Zticj2SFP'
    api_secret = '8rMs8Smk6yEj8wAo'
    url = "https://api.awhere.com/v2/agronomics/crops"
    auth_token = get_oauth_token(encode_secret_and_key(api_key, api_secret))
    header = {
        "Authorization": "Bearer %s" % auth_token,
    }
    request_object = request.Request(url, headers=header)
    response = request.urlopen(request_object)
    response = response.read()
    data = json.loads(response)
    print(data)

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
