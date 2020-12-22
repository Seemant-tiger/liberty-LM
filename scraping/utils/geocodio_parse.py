import functools
import json

import geocodio

from scraping import _static as static


__all__ = ['geocodio_data']

_geocodio_client = None


@functools.singledispatch
def geocodio_data(address):
    if not address:
        return {}
    raise TypeError(f'Invalid address: {address}')


@geocodio_data.register(str)
def _(address):
    _geocodio_init()
    response = _geocodio_client.geocode(address)
    return _custom_formatted(
        response['results'][0],
        address,
    )


@geocodio_data.register(list)
def _(address):
    _geocodio_init()
    response = _geocodio_client.geocode(address)
    results = []
    for k, i in enumerate(response):
        try:
            results.append(
                _custom_formatted(i['results'][0], address[k])
            )
        except IndexError:
            results.append({})
    
    return results


def _custom_formatted(results, fallback_address):
    components = results.get('address_components',  {})
    return {
        'formatted_address': results.get('formatted_address', fallback_address),
        'location': results.get('location', {}),
        'street_number': components.get('number', ''),
        'street_name': components.get('formatted_street', ''),
        'state': components.get('state', ''),
        'city': components.get('city', ''),
        'zipcode': components.get('zip', ''),
        'county': components.get('county', ''),
        'country': components.get('country', ''),
        'geocodio_raw': json.dumps(results, separators=(',', ':')),
    }


def _geocodio_init():
    global _geocodio_client
    global geocodio_raw
    import os;print(os.getcwd())
    with open("geocodio_raw.json","r") as f:
        geocodio_raw = json.load(f)

    if _geocodio_client is None:
        _geocodio_client = geocodio.GeocodioClient(
            key=static.GEOCODIO_API_KEY,
            version=static.GEOCODIO_VERSION,
        )


def geocodio_response(address):
    _geocodio_init()
    if address in geocodio_raw:
        print("geocodio - comes from raw file")
        return geocodio_raw[address]
    
    result = geocodio_data(address)
    print("geocodio- new request")
    geocodio_raw[address] = result

    with open("geocodio_raw.json","w") as f:
        json.dump(geocodio_raw,f)

    
    return result
    