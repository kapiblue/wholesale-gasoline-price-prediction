import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://www.lotos.pl/145/type,oil_95/dla_biznesu/hurtowe_ceny_paliw/archiwum_cen_paliw"
data = requests.get(url).text

soup = BeautifulSoup(data, 'html.parser')

df = pd.DataFrame(columns= ['Date', 'Price', 'Excise', 'Surcharge'])

table = soup.find('table')
rows = []

for row in table.tbody.find_all('tr'):
    columns = row.find_all('td')

    if (columns != []):
        date = columns[0]
        price = columns[1]
        excise = columns[2]
        surcharge = columns[3]
    
    rows.append({'Date' : date,
        'Price' : price, 
        'Excise' : excise,
        'Surcharge' : surcharge})

df = pd.concat([df, pd.DataFrame(rows)], axis=0, ignore_index=True)

df.to_csv("LOTOS.cvs")