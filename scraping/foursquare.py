from scraping.utils import web, scoring, cleaners
from scraping import _static
import requests
import copy


SEARCH_ENDPOINT = "https://api.foursquare.com/v2/venues/search"
VENUE_ENDPOINT = "https://api.foursquare.com/v2/venues"


client_id = _static.fs_client_id
client_secret = _static.fs_client_secret
version = _static.fs_version

params = {'client_id': client_id, 'client_secret': client_secret, 'v': version}

def main(name, address):
    acc_name = cleaners.cleaned_name(name)
    acc_address = address['address']['formatted_address']
    results = search_results_api(acc_name, acc_address)
    if results:
        # top_result = max(results, key=lambda result: scoring.name_match(acc_name, result["name"]).tough)
        [r.update({'name_score': scoring.name_match(acc_name, r['name']).tough}) for r in results]
        [r.update({'address_score': scoring.name_match(acc_address, r['location'].get('address', '')).tough}) for r in results]
		
        top_result = max(results, key=lambda result: result['name_score'] * result['address_score'])

        data = venue_data(top_result)
        data = {f'fs_{k}':v for k,v in data.items()}
        data.update({'processed_name': acc_name})
        return data
    else:
        return {'processed_name': ''}


def search_results_api(name, address):

    search_params = copy.deepcopy(params)
    search_params.update({'query': name, 'near': address, 'limit': 10})
    r = requests.get(url=SEARCH_ENDPOINT, params=search_params)
    result = r.json()['response']

    return result.get("venues", [])


def venue_data(top_result):
    venue_id = top_result["id"]
    r = requests.get(url=f'{VENUE_ENDPOINT}/{venue_id}', params=params)
    return r.json()['response']['venue']