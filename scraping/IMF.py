from scraping.utils import web, scoring, cleaners
from scraping import _static
from bs4 import BeautifulSoup
import win32com.client as win32
from datetime import datetime
import os

base_url = "https://www.imf.org/en/Publications/WEO/weo-database/{}/{}/download-entire-database"
data_extraction_path = "D:\Liberty Mutual\script_test"

def main():
    year = datetime.now().year
    month = ['April' if datetime.now().month in [5, 6, 7, 8, 9, 10] else 'October'][0]
    r = requests.get(base_url.format(year, month))
    soup = BeautifulSoup(r.text)
    data_url = "https://www.imf.org" + soup.find_all('div', class_='belt-caption')[0].find('a')['href']

    r = requests.get(data_url)
    with open(f'{data_extraction_path}\IMF.xls', 'wb') as f:
        f.write(r.content)

    fname = f'{data_extraction_path}\IMF.xls'
#     excel = win32.gencache.EnsureDispatch('Excel.Application')
    excel = win32.DispatchEx('Excel.Application')
    wb = excel.Workbooks.Open(fname)
    wb.SaveAs(f'{data_extraction_path}\IMF_data.xlsx', FileFormat = 51)    #FileFormat = 51 is for .xlsx extension
    wb.Close()                               #FileFormat = 56 is for .xls extension
    excel.Application.Quit()
    
    os.remove(f"{data_extraction_path}\IMF.xls")

    return True