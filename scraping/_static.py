__all__ = [
    'geocodio',
    'proxy',
    'USER_AGENT',
    'REQUESTS_TIMEOUT',
]

inp_cols = ['Unique_ID', 'Address1', 'Address2', 'City', 'State', 'Zip', 'Country', 'acc_address', 'processed_name']

op_path = "D:/Liberty Mutual/outputs/individual/json"

scraping_columns = {
    "GP": inp_cols,
    "CH": inp_cols,
    "ZI": inp_cols,
    "FS": inp_cols,
}


from collections import namedtuple
import os

import yaml

with open('config.yml', 'r') as fr:
    config = yaml.safe_load(fr)

yelp = namedtuple('Yelp', 'api_key')(
    os.environ.get('YELP_API_KEY') or config['yelp']['api-key'],
)

geocodio = namedtuple('Geocodio', 'api_key version')(
    os.environ.get('GEOCODIO_API_KEY') or config['geocodio']['api-key'],
    os.environ.get('GEOCODIO_API_VERSION') or config['geocodio']['version'],
)

# GEOCODIO_API_KEY = os.environ.get('GEOCODIO_API_KEY')
# GEOCODIO_API_KEY = "88085ebce8e5021cb11885dfc20ecbfb0b2bf00"
GEOCODIO_API_KEY = "e5dedd0a44ffe2dc6e40cca6fc5ee5220ea2262"
GEOCODIO_VERSION = '1.6'

ZOMATO_API = os.environ.get("ZOMOTO_API") or config["zomato"]["api-keys"][0]

proxy = namedtuple('Proxy', 'endpoint username password')(
    os.environ.get('PROXY_ENDPOINT'),
    os.environ.get('PROXY_USERNAME'),
    os.environ.get('PROXY_PASSWORD'),
)

USER_AGENT = (
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/84.0.4147.135 Safari/537.36'
)

REQUESTS_TIMEOUT = 30


config_gp = {
    "google_places": {
        'test': {
            "0": {
                "api_key": os.environ.get('GP_API_KEY') or "AIzaSyAQ8ZIZkOAY85A1uSFXzEW4I0RCKgmtHrw",
                "place_seach_query": 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=',
                "place_id_query": 'https://maps.googleapis.com/maps/api/place/details/json?placeid='
            },
           
    },
    },
    "headers": {
        'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36"
   
}
    }


fb_token = config["facebook"]["api-key"]
company_house_api = config["companyhouse"]["api-key"]
gp_places = config["googleplaces"]["places-key"]
gp_geocoding = config["googleplaces"]["geocodio-key"]
zm_user = config["zoominfo"]["username"]
zm_pass = config["zoominfo"]["password"]
fs_client_id = config["foursquare"]["client_id"]
fs_client_secret = config["foursquare"]['client_secret']
fs_version = config["foursquare"]['version']