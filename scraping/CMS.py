from sodapy import Socrata
import itertools
from scraping import _static

# Medicare Hospital Cost Report PUF 2017
# Inpatient Prospective Payment System (IPPS) Provider Summary for All Diagnosis-Related Groups (DRG) - FY2018
# Provider Outpatient Hospital Charge Data by APC, CY2018
# Provider of Services File - CLIA - September 2020
datasets = {'4sfm-kqny': 'Medicare_Hospital_2017', 
'yekz-wzdr': 'IPPS_2018', 
'cgdj-v6ht': 'Provider_Outpatient_2018', 
'9p9t-3sdx': 'Provider_of_Services_2020'}

path = 'D:/Liberty Mutual/script_test/CMS'

def main():

    client = Socrata("data.cms.gov", None)
    for data, name in datasets.items():
        df = []
        items = client.get_all(data)	
        i = True
        n = 100000
        while i:
            first_n = list(itertools.islice(items, n))
            df.extend(first_n)
            if len(first_n) != n:
                i = False
        df.to_csv(f'{path}/{name}.csv', index=False)

    return True