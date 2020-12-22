import pandas as pd
import concurrent.futures

from main_code import process_single_record

sources = ['FS']

df = pd.read_csv('LM_input.csv')
business = df.fillna('').to_dict('records')

results = []
threads = 1

with concurrent.futures.ThreadPoolExecutor(threads) as executor:
    futures = {
        executor.submit(process_single_record, b, sources): b for b in business[:threads]
    }
for future in concurrent.futures.as_completed(futures):
    results.append(future.result())