from scraping.utils.geocodio_parse import geocodio_data
from scraping._static import scraping_columns, op_path
from scraping.utils import status, logs
from scraping.utils._general import parallel_results_mapped
from collections import namedtuple
import concurrent.futures
import itertools
import functools
import copy
import time
import json
import datetime
import scraping.source_execution_config as SEC
import re

logs.init()

def input_record(business):
    address_cols = ['Address1', 'Address2', 'City', 'State', 'Zip', 'Country']
    address = ', '.join(str(business[i]) for i in address_cols)
    address = re.sub('\s,', '', address)
    business['acc_address'] = geocodio_data(address)
    
    Record = namedtuple('Record', [
        'entity', 'name', 'address', 'base_columns'
    ])
    
    return Record(
    business['Unique_ID'],
        {
            'name': business['Business Name'],
        },
        {
            'Address1': business['Address1'],
            'Address2': business['Address2'],
            'City': business['City'],
            'State': business['State'],
            'Country': business['Country'],
            'Zip': business['Zip'],
            'address': business['acc_address'],
        },
        base_columns={k: business[k] for k in (
            'Unique_ID',
            'Business Name',
            'Address1',
            'Address2',
            'City',
            'State',
            'Zip',
            'Country',
            'acc_address',
        )},
    )

# @status.time_this('scraping')
def scrape_sources(sources, record):

    data = {}
    for source, column in scraping_columns.items():
        if source in sources:
            data[source] = dict(zip(column, itertools.repeat('')))
            data[source]['Unique_ID'] = record.entity

    results = parallel_results_mapped(
        source_main,
        sources,
        name=record.name,
        address=record.address,
        uid=record.entity,
    )
    data.update(results)
    
    return data


def source_main(source, name, address, uid):

    try:
        time_start = time.time()
        SEC.init({source})
        func = SEC.config['search_dict'].get(source)

        result = func(name['name'], copy.deepcopy(address))
#         status.status['scraping']['particular'][source] = {
#             'success': True,
#             'hit': bool(result['processed_name']),
#             'name-source': source,
#         }
    except Exception as exc:
        logs.log_event(
            msg='source_scraping.__init__.main',
            err=logs.error_info(exc),
            source=source,
        )
#         status.status['scraping']['particular'][source] = {
#             'success': False,
#             'hit': False,
#             'name-source': source,
#         }
        result = {}

    time_end = time.time()
    result['Unique_ID'] = uid
    result['time-start'] = time_start
    result['time-end'] = time_end
    
    return result
            
def add_extra_columns(dictionary, extra_items, ts=True, single=False):
    FMT_TS = '%m-%d-%Y %H:%M:%S'
    if ts:
        extra_items = {
            **extra_items,
            'updated_timestamp': datetime.datetime.now().strftime(FMT_TS),
        }
    
    if single:
        dictionary.update(extra_items)
    else:
        for v in dictionary.values():
            v.update(extra_items)
            
            
def process_single_record(business, sources):

    business['created-timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    business_data = {
        'uid': business['Unique_ID'],
        'input': {},
        'scraped-data': {},
    }
    
    record = input_record(business)
    
    business_data['input'] = {
        **record.base_columns,
    }

#     status.update_inputs(business['Unique_ID'], record)

    business_data['scraped-data'] = scrape_sources(sources, record)

#     status.update_scraping(business_data['scraped-data'], sources)

    add_extra_columns(business_data['scraped-data'], record.base_columns)
    
    business_data['created-timestamp'] = business['created-timestamp']
    business_data['updated-timestamp'] = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    with open(f"{op_path}/data/{business_data['uid']}.json", 'w', encoding='utf-8') as f:
        json.dump(business_data, f)
    
    return True