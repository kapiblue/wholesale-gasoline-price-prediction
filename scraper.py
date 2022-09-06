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
        date = columns[0].text
        price = float(columns[1].text.replace(',', '.').replace(" ", ""))
        excise = float(columns[2].text.replace(',', '.').replace(" ", ""))
        surcharge = float(columns[3].text.replace(',', '.').replace(" ", ""))
    
    rows.append({'Date' : date,
        'Price' : price, 
        'Excise' : excise,
        'Surcharge' : surcharge})

df = pd.concat([df, pd.DataFrame(rows)], axis=0, ignore_index=True)

df["Date"] = pd.to_datetime(df["Date"])
df["Price"] = df["Price"].astype(float)
df["Excise"] = df["Excise"].astype(float)
df["Surcharge"] = df["Surcharge"].astype(float)

df = df.reset_index(drop=True)
df = df.iloc[::-1]

df.to_csv("LOTOS.csv", index=False)