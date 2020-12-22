import functools
import random

import requests
from bs4 import BeautifulSoup

from scraping import _static


def response(url, max_hits=1, **kwargs):
    '''Perform a GET request using requests library and return the response.
    
    Parameters
    ----------
        url      -- URL to fetch
        max_hits -- Number of attempts before a successful response is fetched
                    (default: 1)
    
    Keyword Arguments
    -----------------
        Arguments to pass to `requests.get` function
        E.g.: headers, params, etc.
    
    Response
    --------
        requests.Response object
    
    Exceptions
    ----------
        If the final response is None, the encountered error is raised again,
        so that the caller can handle it.
    '''
    
    r = None
    err = None
    
    for __ in range(max_hits):
        try:
            r = _response(url, **kwargs)
            if r.status_code == 200:
                return r
        except Exception as e:
            err = e
    
    if r is not None:
        return r
    raise err


def _response(url, **kwargs):
    '''Perform a GET request for a URL and return the response object.'''
    if 'headers' not in kwargs:
        kwargs = {**kwargs, 'headers': {'User-Agent': _static.USER_AGENT}}
    r = requests.get(
        url,
        **kwargs,
        # try using proxies(1, 100_000) if the default doesn't work
        proxies=proxies(),
        timeout=_static.REQUESTS_TIMEOUT,
    )
    return r


def proxies(rand_min=100_000, rand_max=1_000_000):
    '''Return a proxies dictionary with a random number after username.
    
    Parameters
    ----------
        rand_min -- Minimum value for the random number (default: 100_000)
        rand_max -- Maximum value for the random number (default: 1_000_000)
    
    Response
    --------
        Dictionary like this:
        {
            'http': 'http://username-random:password@proxy_name:port',
            'https': 'https://username-random:password@proxy_name:port',
        }
    '''
    
    if not all(_static.proxy):
        return {}
    
    endpoint, username, password = _static.proxy
    rand = random.randint(rand_min, rand_max)
    return {
        'http': f'http://{username}-{rand}:{password}@{endpoint}',
        'https': f'https://{username}-{rand}:{password}@{endpoint}',
    }

def make_soup(url,**kwargs):
    r = response(url,**kwargs)
    soup = BeautifulSoup(r.text,"lxml")
    return soup


def get_curl_response(url, user_agent, request='GET',data=None):
    '''
    Function to make an HTTP request using CURL
    Input:
        url:str
        user_agent:str
        request:str
    Output:
        return:str

    '''
    # Get a random number
    rand_var = random.randint(1, 100000)

    # Create curl command
    cmd = f'curl -L -x {static.PROXY_ENDPOINT} -U {static.PROXY_USERNAME}-{rand_var}'
    if not data:
        cmd = cmd + f':{static.PROXY_PASSWORD} -H "User-Agent: ' + user_agent + \
            '" -H "Cache-Control: no-cache" --connect-timeout 20 -X '
    else:
        cmd = cmd + f':{static.PROXY_PASSWORD} -H "User-Agent: ' + user_agent + \
            '" -H "Cache-Control: no-cache" -H "Content-Type: application/json" -d \''\
            + data +'\' --connect-timeout 20 -X '
    cmd = cmd + request + " \"" + url + "\""
    process = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    # res = stdout.decode("utf-8")
    res = to_unicode(stdout)

    return res

