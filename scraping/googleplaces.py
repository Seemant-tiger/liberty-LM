from scraping.utils import web, scoring, cleaners
from scraping import _static


SEARCH_ENDPOINT = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
PLACE_ENDPOINT = "https://maps.googleapis.com/maps/api/place/details/json?placeid="


api_key = _static.gp_places


def main(name, address):
    acc_address = address['address']['formatted_address']
    acc_name = cleaners.cleaned_name(name)
    name_addr = acc_name + ', ' + acc_address
    results = search_results_api(acc_name, acc_address, name_addr)
    if results:
        # top_result = max(results, key=lambda result: scoring.name_match(acc_name, result["name"]).tough)
        [r.update({'name_score': scoring.name_match(acc_name, r['name']).tough}) for r in results]
        [r.update({'address_score': scoring.name_match(acc_address, r['formatted_address']).tough}) for r in results]
		
        top_result = max(results, key=lambda result: result['name_score'] * result['address_score'])

        data = place_data(top_result)
        #data.update({'name_score': scoring.name_match(acc_name, data['name']).tough})})
        #data.update({'address_score': scoring.name_match(acc_address, data['address']).tough})})
        data = {f'gp_{k}':v for k,v in data.items()}
        data.update({'processed_name': acc_name})
        return data
    else:
        return {'processed_name': ''}


def search_results_api(name, address, name_addr):

    url = SEARCH_ENDPOINT + name_addr + "&inputtype=textquery&fields=formatted_address,name,geometry,place_id,permanently_closed"+'&key=' + api_key
    r = web.response(url)
    result = r.json()
    if not result['candidates']:
        url = SEARCH_ENDPOINT + name + "&inputtype=textquery&fields=formatted_address,name,geometry,place_id,permanently_closed"+'&key=' + api_key
        r = web.response(url)
        result = r.json()
    return result.get("candidates", [])


def place_data(top_result):
    place_id = top_result["place_id"]
    url = f"{PLACE_ENDPOINT}{place_id}&key={api_key}"
    r = web.response(url)
    return r.json()['result']