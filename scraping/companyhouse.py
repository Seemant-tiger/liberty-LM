from scraping.utils import web, scoring, cleaners
from scraping import _static


SEARCH_ENDPOINT = "https://api.companieshouse.gov.uk/search/companies"
COMPANY_ENDPOINT = "https://api.companieshouse.gov.uk/company/"
OFFICERS_ENDPOINT = "https://api.companieshouse.gov.uk/company/{}/officers"
FILING_ENDPOINT = "https://api.companieshouse.gov.uk/company/{}/filing-history"
INSOLVANCY_ENDPOINT = "https://api.companieshouse.gov.uk/company/{}/insolvency"
REGISTRIES_ENDPOINT = "https://api.companieshouse.gov.uk/company/{}/registers"
EXCEPTIONS_ENDPOINT = "https://api.companieshouse.gov.uk/company/{}/exemptions"


api_key = _static.company_house_api


def main(name, address):
    name = cleaners.cleaned_name(name)
    results = search_results_api(name, address['address']['formatted_address'])
    top_result = max(
        results, key=lambda result: scoring.name_match(name, result["title"]).tough
    )

    data = additional(top_result)
    data = {f'ch_{k}':v for k,v in data.items()}
    return data


def search_results_api(name, address):

    params = [("q", name + ", " + address)]
    r = web.response(SEARCH_ENDPOINT, params=params, auth=(api_key, ""))
    result = r.json()

    return result.get("items", [])


def additional(top_result):
    
    company_id = top_result["company_number"]
    company_data = company_data_api(company_id)
    officer_data = officer_data_api(company_id)
    filings_data = filings_data_api(company_id)
    insolvency_data = insolvency_data_api(company_id)
    registries_data = registries_data_api(company_id)
    exceptions_data = exceptions_data_api(company_id)

    return {
        **{"meta-data" : top_result },
        **{"company-data" : company_data},
        **{"officer-data":officer_data},
        **{"filings-data":filings_data},
        **{"insolvency-data":insolvency_data},
        **{"registries-data":registries_data},
        **{"exceptions-data":exceptions_data}
    }


def company_data_api(company_id):
    r_c = web.response(COMPANY_ENDPOINT + company_id, auth=(api_key, ""))
    company_result = r_c.json()
    return company_result


def officer_data_api(company_id):
    url = OFFICERS_ENDPOINT.format(company_id)

    r = web.response(url, auth=(api_key, ""))

    return r.json()


def filings_data_api(company_id):
    url = FILING_ENDPOINT.format(company_id)

    r = web.response(url, auth=(api_key, ""))

    return r.json()


def insolvency_data_api(company_id):
    url = INSOLVANCY_ENDPOINT.format(company_id)
    r = web.response(url, auth=(api_key, ""))
    return r.json()


def registries_data_api(company_id):
    url = REGISTRIES_ENDPOINT.format(company_id)
    r = web.response(url, auth=(api_key, ""))
    return r.json()

def exceptions_data_api(company_id):
    url = EXCEPTIONS_ENDPOINT.format(company_id)
    r = web.response(url,auth=(api_key,""))
    return r.json()