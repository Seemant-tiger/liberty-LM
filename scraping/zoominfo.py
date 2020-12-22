from scraping.utils import web, scoring, cleaners
from scraping import _static
import zi_api_auth_client
import requests


SEARCH_ENDPOINT = "https://api.zoominfo.com/search/company"
ENRICH_ENDPOINT = "https://api.zoominfo.com/enrich/company"


user_name = _static.zm_user
password = _static.zm_pass

jwt_token = zi_api_auth_client.user_name_pwd_authentication(user_name, password)

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {jwt_token}"
}

enrich_op_fields = ['id',
 'ticker',
 'name',
 'website',
 'domainList',
 'logo',
 'socialMediaUrls',
 'revenue',
 'employeeCount',
 'numberOfContactsInZoomInfo',
 'phone',
 'fax',
 'street',
 'city',
 'state',
 'zipCode',
 'country',
 'companyStatus',
 'companyStatusDate',
 'descriptionList',
 'sicCodes',
 'naicsCodes',
 'competitors',
 'ultimateParentId',
 'ultimateParentName',
 'ultimateParentRevenue',
 'ultimateParentEmployees',
 'subUnitCodes',
 'subUnitType',
 'subUnitIndustries',
 'primaryIndustry',
 'industries',
 'locationMatch',
 'parentId',
 'parentName',
 'locationCount',
 'alexaRank',
 'metroArea',
 'lastUpdatedDate',
 'createdDate',
 'certificationDate',
 'certified',
 'products',
 'revenueRange',
 'employeeRange',
 'companyFunding',
 'recentFundingAmount',
 'recentFundingDate',
 'totalFundingAmount',
 'employeeGrowth',
 'continent',
 'type']

def main(name, address):
    acc_name = cleaners.cleaned_name(name)
    results = search_results_api(acc_name, address)
    if results:
        top_result = max(results, key=lambda result: scoring.name_match(acc_name, result["name"]).tough)

        data = company_data(top_result)
        data = {f'zi_{k}':v for k,v in data.items()}
        data.update({'processed_name': acc_name})
        return data
    else:
        return {'processed_name': ''}


def search_results_api(name, address):

    params = {'companyName': name, "rpp": 10}
    if address['address'].get('country', ''): params.update({'country': address['address']['country']})
    if address['address'].get('zipcode', ''): params.update({'zipcode': address['address']['zipcode']})

    r = requests.post(SEARCH_ENDPOINT, headers=headers, json=params)
    result = r.json()

    return result.get("data", [])


def company_data(top_result):
    company_id = top_result["id"]
    params = {"matchCompanyInput": [
    {
        "companyId": 62637459,
    }
    ],
    "outputFields": enrich_op_fields
    }

    r = requests.post(ENRICH_ENDPOINT, headers=headers, json=params)

    return r.json()['data']['result'][0]['data'][0]