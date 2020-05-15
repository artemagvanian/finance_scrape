# pip3 install requests bs4

import requests 
from bs4 import BeautifulSoup
from pprint import pprint
import csv

url = 'https://finance.yahoo.com/quote/GOGL.OL/financials?p=GOGL.OL'
page = requests.get(url)

soup = BeautifulSoup(page.text, 'html.parser')
company_json = {}
search_clauses = ['EBITDA', 'Operating Income or Loss']

for clause in search_clauses:
	for div in soup.find_all("div", string=clause):
		div = div.parent
		company_json[clause] = []
		for i in range(4):
			company_json[clause].append(div.next_sibling.text)
			div = div.next_sibling

pprint(company_json)

csv_file = "data.csv"
with open(csv_file, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=search_clauses)
    writer.writeheader()
    for data in [dict(zip(company_json,t)) for t in zip(*company_json.values())]:
        writer.writerow(data)
