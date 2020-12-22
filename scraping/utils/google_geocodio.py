import json

from scraping import _static as static
from scraping.utils import web


geocoding_key = static.gp_geocoding
GEO_ENDPOINT = "https://maps.googleapis.com/maps/api/geocode/json?"


def google_geocode(acc_address):
    address = {}
    
    params = {
        "address" :acc_address,
        "key" : geocoding_key
    }

    r = web.response(GEO_ENDPOINT, params=params)
    
    result = r.json()['results'][0]
    
    country = [i['short_name'] for i in result['address_components'] if 'country' in i['types']]
    country_full = [i['long_name'] for i in result['address_components'] if 'country' in i['types']]
    zipcode = [i['short_name'] for i in result['address_components'] if 'postal_code' in i['types']]
    state = [i['short_name'] for i in result['address_components'] if 'administrative_area_level_1' in i['types']]
    state_full = [i['long_name'] for i in result['address_components'] if 'administrative_area_level_1' in i['types']]
    county = [i['short_name'] for i in result['address_components'] if 'administrative_area_level_2' in i['types']]
    locality = [i['short_name'] for i in result['address_components'] if 'locality' in i['types']]
    street_name = [i['short_name'] for i in result['address_components'] if 'route' in i['types']]
    street_number = [i['short_name'] for i in result['address_components'] if 'street_number' in i['types']]
    
    address.update({'formatted_address': result.get('formatted_address', '')})
    address.update({'location': result.get('geometry', {}).get('location', {})})
    address.update({'location_type': result.get('geometry', {}).get('location_type', '')})
    address.update({'place_id': result.get('place_id', '')})
    address.update({'street_number': street_number[0] if street_number else ''})
    address.update({'street_name': street_name[0] if street_name else ''})
    address.update({'locality': locality[0] if locality else ''})
    address.update({'county': county[0] if county else ''})
    address.update({'state': state[0] if state else ''})
    address.update({'state_full': state_full[0] if state_full else ''})
    address.update({'zipcode': zipcode[0] if zipcode else ''})
    address.update({'country': country[0] if country else ''})
    address.update({'country_full': country_full[0] if country_full else ''})
    address.update({'geocodio_raw': json.dumps(result, separators=(',', ':'))})
    
    return address