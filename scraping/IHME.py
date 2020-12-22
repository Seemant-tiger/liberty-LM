from scraping.utils import web, scoring, cleaners
from scraping import _static
import zipfile, io
import os
import pandas as pd
import shutil

zip_file_url = "https://ihmecovid19storage.blob.core.windows.net/latest/ihme-covid19.zip"
data_extraction_path = "D:/Liberty Mutual/script_test/IHME"

def main():
    
    # Download the zip file and extract it in a folder
    r = web.response(zip_file_url)
    z = zipfile.ZipFile(io.BytesIO(r.content))
    z.extractall(data_extraction_path)
    
    # Load data from the zip-file and process it.
    df = pd.read_csv(f'{data_extraction_path}/{os.listdir(data_extraction_path)[0]}/reference_hospitalization_all_locs.csv')
    df['date'] = pd.to_datetime(df['date'])
#     df['week_start'] = df['date'] - df['date'].dt.weekday * np.timedelta64(1, 'D')
    df['month_start'] = df['date'].values.astype('datetime64[M]')
    
    df.fillna(0).groupby(['location_id', 'location_name', 'month_start']).sum().reset_index().drop('V1', axis=1).to_csv(f'{data_extraction_path}/IHME_data.csv', index=False)
    
    shutil.rmtree(f'{data_extraction_path}/{os.listdir(data_extraction_path)[0]}')
    
    return True